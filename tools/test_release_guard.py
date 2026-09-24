"""Offline tests for release guard; temporary synthetic tokens only, never network."""
from __future__ import annotations
import base64
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from release_guard import Guard, load_private_values

checks=[]
def expect(name, value):
    checks.append((name,bool(value)))

with tempfile.TemporaryDirectory(prefix='jev-release-test-') as tmp:
    root=Path(tmp)/'project';root.mkdir()
    (root/'README.md').write_text('Synthetic demo. No live results claimed.\n')
    g=Guard(root);g.worktree();expect('clean_text',not g.findings)
    secret='example-private-value-'+('Q'*24)
    values={'VERCEL_AI_GATEWAY_KEY':secret}
    for kind,payload in [('plain',secret.encode()),('base64',base64.b64encode(secret.encode()))]:
        (root/'bad.txt').write_bytes(payload)
        g=Guard(root,values);g.worktree()
        expect('known_'+kind,any(f['kind'].startswith('supplied_value:') for f in g.findings))
        expect('no_value_in_report_'+kind,secret not in json.dumps(g.findings))
        (root/'bad.txt').unlink()
    token='vck_'+('A'*48)
    (root/'bad.txt').write_text(token)
    g=Guard(root);g.worktree();expect('token_pattern',any(f['kind']=='vercel_gateway_token' for f in g.findings))
    (root/'bad.txt').unlink()
    (root/'PRIVATE_CREDENTIALS.txt').write_text('SECRET=anything\n')
    g=Guard(root);g.worktree();expect('private_filename',bool(g.findings))
    (root/'PRIVATE_CREDENTIALS.txt').unlink()
    (root/'.env.example').write_text('KEY=\n')
    g=Guard(root);g.worktree();expect('empty_env_example',not g.findings)
    (root/'.env').write_text('KEY=placeholder\n')
    g=Guard(root);g.worktree();expect('real_env_rejected',bool(g.findings))
    (root/'.env').unlink()
    (root/'bundle.zip').write_bytes(b'not an actual archive')
    g=Guard(root);g.worktree();expect('archive_rejected',bool(g.findings));(root/'bundle.zip').unlink()
    image=root/'sample.png';image.write_bytes(b'synthetic bytes for manifest-control test, not a screenshot')
    g=Guard(root);g.worktree();expect('media_needs_review',any(f['kind'].startswith('media_') for f in g.findings))
    (root/'checks').mkdir()
    manifest={'files':{'sample.png':{'sha256':hashlib.sha256(image.read_bytes()).hexdigest(),
                                  'reviewed_for_secrets':True,'reviewer':'synthetic unit test only'}}}
    (root/'checks/media_review.json').write_text(json.dumps(manifest))
    g=Guard(root);g.worktree();expect('matching_review_hash',not g.findings)
    image.write_bytes(b'changed synthetic bytes')
    g=Guard(root);g.worktree();expect('changed_media_hash_rejected',bool(g.findings));image.unlink()
    creds=Path(tmp)/'private.txt'
    creds.write_text('# comment\nVERCEL_AI_GATEWAY_KEY='+secret+'\nIGNORED=value\n')
    expect('private_parser',load_private_values(creds)==values)
    if shutil.which('git'):
        def git(*args):
            result=subprocess.run(['git','-C',str(root),*args],capture_output=True)
            if result.returncode:raise RuntimeError('synthetic Git test setup failed')
        git('init','--quiet');git('config','user.name','Synthetic Test');git('config','user.email','test@example.test')
        (root/'history.txt').write_text(secret)
        git('add','history.txt');git('commit','-qm','Synthetic fixture')
        git('rm','-q','history.txt');git('commit','-qm','Remove synthetic fixture')
        g=Guard(root,values);g.history()
        expect('deleted_secret_still_in_history',any(f['path'].startswith('history:') and f['kind'].startswith('supplied_value:') for f in g.findings))
        (root/'staged.txt').write_text(token);git('add','staged.txt');(root/'staged.txt').write_text('clean working tree')
        g=Guard(root);g.history()
        expect('staged_secret_not_hidden_by_worktree',any(f['path'].startswith('staged:') and f['kind']=='vercel_gateway_token' for f in g.findings))
    else:
        print('Git-specific tests not run: Git is unavailable.')
failed=[name for name,ok in checks if not ok]
print(f'Release guard offline self-tests: {len(checks)-len(failed)}/{len(checks)} passed. No network calls.')
for name in failed:print('FAIL:',name)
raise SystemExit(1 if failed else 0)
