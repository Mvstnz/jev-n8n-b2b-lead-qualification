"""Supplementary public-release check. No network calls and no secret snippets.

Scan exact supplied values (optionally loaded from a PRIVATE file outside the repo),
selected encodings, common token patterns, forbidden files and reviewed media hashes.
--git-history additionally checks staged blobs and all reachable commits/objects.
This does not detect all possible secret forms or inspect text inside image pixels.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote, urlsplit

PATTERNS = {
    'vercel_gateway_token': re.compile(rb'\bvck_[A-Za-z0-9_-]{20,}\b'),
    'jwt': re.compile(rb'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b'),
    'slack_webhook': re.compile(rb'https?://hooks[.]slack[.]com/services/[A-Za-z0-9]+/[A-Za-z0-9]+/[A-Za-z0-9_-]{10,}'),
    'slack_token': re.compile(rb'\bxox[baprs]-[A-Za-z0-9-]{15,}'),
    'github_token': re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})'),
    'private_key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
    'google_api_key': re.compile(rb'\bAIza[A-Za-z0-9_-]{30,}'),
    'credential_in_url': re.compile(rb'https?://[^\s/<>"\']+:[^\s/<>"\']+@'),
}
SKIP_DIRS = {'.git','__pycache__','.pytest_cache','.venv','venv','node_modules'}
MEDIA = {'.png','.jpg','.jpeg','.webp'}
TEXT = {'.md','.txt','.py','.js','.mjs','.cjs','.ts','.tsx','.jsx','.json','.jsonl',
        '.yaml','.yml','.toml','.html','.css','.csv','.sh','.ps1','.bat','.cfg','.ini'}
FORBIDDEN_EXT = {'.zip','.7z','.tar','.gz','.tgz','.pem','.key','.p12','.pfx','.bak','.log','.ipynb'}
MAX_FILE_BYTES = 12 * 1024 * 1024
PRIVATE_KEYS = {'N8N_BASE_URL','N8N_MCP_URL','N8N_MCP_TOKEN','VERCEL_AI_GATEWAY_KEY','SLACK_WEBHOOK_URL'}


def load_private_values(path: Path | None) -> dict[str,str]:
    if path is None:
        return {}
    result = {}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip() or line.lstrip().startswith('#') or '=' not in line:
            continue
        key,value = line.split('=',1)
        key,value = key.strip(),value.strip()
        if key in PRIVATE_KEYS and len(value) >= 12:
            result[key] = value
    return result


def variants(values: dict[str,str]) -> dict[str,set[bytes]]:
    out = {}
    for key,value in values.items():
        strings = {value}
        if key in {'N8N_BASE_URL','N8N_MCP_URL'}:
            if urlsplit(value).hostname:
                strings.add(urlsplit(value).hostname or '')
        if key == 'SLACK_WEBHOOK_URL':
            strings.add(urlsplit(value).path)
            strings.add(value.rsplit('/',1)[-1])
        encoded: set[bytes] = set()
        for text in strings:
            if len(text) < 12:
                continue
            b = text.encode()
            encoded.update({b,quote(text,safe='').encode(),
                            json.dumps(text)[1:-1].encode(),
                            text.replace('/','\\/').encode(),
                            base64.b64encode(b),base64.urlsafe_b64encode(b).rstrip(b'=')})
        out[key] = encoded
    return out


class Guard:
    def __init__(self, root: Path, values: dict[str,str] | None = None):
        self.root = root.resolve()
        self.known = variants(values or {})
        self.findings: list[dict[str,str]] = []
        self.media_reviews: dict = {}
        review = self.root/'checks/media_review.json'
        if review.exists():
            try:
                data=json.loads(review.read_text(encoding='utf-8'))
                entries=data.get('files',{})
                if not isinstance(entries,dict):
                    raise ValueError('invalid media review')
                self.media_reviews=entries
            except (ValueError,UnicodeError,OSError):
                self.add('invalid_media_manifest','checks/media_review.json')

    def safe(self, value: str) -> str:
        b=value.encode(errors='replace')
        for items in self.known.values():
            for item in sorted(items,key=len,reverse=True):
                b=b.replace(item,b'[REDACTED]')
        for pattern in PATTERNS.values():
            b=pattern.sub(b'[REDACTED]',b)
        return b.decode(errors='replace')

    def add(self, kind: str, path: str) -> None:
        finding={'kind':kind,'path':self.safe(path)}
        if finding not in self.findings:
            self.findings.append(finding)

    def bytes(self, data: bytes, label: str) -> None:
        for key,items in self.known.items():
            if any(item in data for item in items):
                self.add('supplied_value:'+key,label)
        for key,pattern in PATTERNS.items():
            if pattern.search(data):
                self.add(key,label)

    def filename(self, rel: str, label: str) -> None:
        parts=Path(rel).parts
        lower=Path(rel).name.lower()
        suffix=Path(rel).suffix.lower()
        private=(lower.startswith('private_credentials') or
                 (lower.startswith('.env') and lower!='.env.example') or
                 any(p.lower() in {'.private','raw_exports','raw_reports','private_reports'} for p in parts) or
                 ('.codex' in parts and lower in {'config.toml','auth.json'}))
        if private or suffix in FORBIDDEN_EXT:
            self.add('forbidden_private_or_archive_file',label)
        self.bytes(rel.encode(),label)

    def blob(self, rel: str, data: bytes, label: str | None=None) -> None:
        label=label or rel
        self.filename(rel,label)
        self.bytes(data,label)
        if len(data)>MAX_FILE_BYTES:
            self.add('oversized_file_manual_review',label)
            return
        suffix=Path(rel).suffix.lower()
        if suffix in MEDIA:
            rec=self.media_reviews.get(rel,{})
            digest=hashlib.sha256(data).hexdigest()
            if (not isinstance(rec,dict) or rec.get('reviewed_for_secrets') is not True
                    or rec.get('sha256')!=digest or not rec.get('reviewer')):
                self.add('media_not_visually_reviewed_at_this_hash',label)
            return
        if suffix not in TEXT and Path(rel).name not in {'.gitignore','.gitattributes','.env.example','LICENSE','NOTICE','Makefile','Dockerfile'}:
            self.add('unsupported_file_type_manual_review',label)
            return
        try:
            data.decode('utf-8-sig')
        except UnicodeError:
            self.add('non_utf8_or_binary_file_manual_review',label)
        if b'\x00' in data:
            self.add('embedded_binary_or_utf16_manual_review',label)

    def worktree(self) -> None:
        if not self.root.is_dir():
            self.add('missing_project_directory',str(self.root))
            return
        for file in sorted(self.root.rglob('*')):
            rel=file.relative_to(self.root)
            if any(part in SKIP_DIRS for part in rel.parts):
                continue
            if file.is_symlink():
                self.add('symlink_not_allowed',rel.as_posix());continue
            if file.is_file():
                try:
                    self.blob(rel.as_posix(),file.read_bytes())
                except OSError:
                    self.add('unreadable_file',rel.as_posix())

    def git(self, *args: str) -> bytes:
        result=subprocess.run(['git','-C',str(self.root),*args],capture_output=True,check=False)
        if result.returncode:
            raise RuntimeError('git operation failed')
        return result.stdout

    def history(self) -> None:
        try:
            top=Path(self.git('rev-parse','--show-toplevel').decode().strip()).resolve()
            if top != self.root:
                self.add('git_root_is_not_project_directory','[git]');return
            # Check staged file contents, including files excluded by .gitignore.
            for row in self.git('ls-files','--stage','-z').split(b'\0'):
                if not row:continue
                metadata,rawpath=row.split(b'\t',1)
                mode,oid,stage=metadata.split()
                path=rawpath.decode('utf-8',errors='strict')
                if mode==b'120000':self.add('staged_symlink',path)
                if stage!=b'0':self.add('unresolved_merge_stage',path)
                self.blob(path,self.git('cat-file','blob',oid.decode()),'staged:'+path)
            # Fresh repos with no commits are valid; there is no history yet.
            for row in self.git('rev-list','--objects','--all').splitlines():
                oid,_,rawpath=row.partition(b' ')
                kind=self.git('cat-file','-t',oid.decode()).strip()
                if kind==b'blob':
                    path=rawpath.decode('utf-8',errors='strict') or '[unlabelled-blob]'
                    self.blob(path,self.git('cat-file','blob',oid.decode()),'history:'+path)
                elif kind in {b'commit',b'tag'}:
                    self.bytes(self.git('cat-file',kind.decode(),oid.decode()),'history:'+kind.decode())
            self.bytes(self.git('remote','-v'),'git-remote-configuration')
        except (RuntimeError,OSError,UnicodeError,ValueError):
            self.add('git_history_scan_incomplete','[git]')


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path('.'))
    parser.add_argument('--credentials',type=Path)
    parser.add_argument('--require-credentials',action='store_true')
    parser.add_argument('--git-history',action='store_true')
    args=parser.parse_args()
    try:
        values=load_private_values(args.credentials)
    except (OSError,UnicodeError):
        print('BLOCKED: cannot read private comparison values; no secret contents displayed.')
        return 2
    if args.require_credentials and not {'N8N_MCP_TOKEN','VERCEL_AI_GATEWAY_KEY','SLACK_WEBHOOK_URL'}.issubset(values):
        print('BLOCKED: required private comparison values are missing.')
        return 2
    guard=Guard(args.root,values)
    guard.worktree()
    if args.git_history:guard.history()
    if guard.findings:
        print(f'BLOCKED: {len(guard.findings)} release findings. No secret snippets are printed.')
        for finding in guard.findings:
            print(f"- {finding['kind']}: {finding['path']}")
        return 1
    print('PASS: no findings from configured exact-value, pattern, file and media checks.')
    print('Known supplied-value comparison: '+('enabled' if values else 'not supplied (pattern checks only)'))
    print('Git staged/history check: '+('requested and completed' if args.git_history else 'not requested'))
    print('This is not a complete security guarantee; visual/media and publication review remain required.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
