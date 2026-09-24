"""Build a portable n8n Workflow SDK source from synthetic development fixtures."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

policy = read("config/policy.json")
fixtures = read("fixtures/development_inputs.json")
mocks = read("fixtures/mock_answers.json")
selected = set(read("fixtures/showcase_case_ids.json")["case_ids"])
showcase = [f for f in fixtures if f["case_id"] in selected]
payload = []
for case in showcase:
    lead = dict(case["input"])
    days = lead.pop("target_delivery_days_from_reference")
    if days is not None:
        from datetime import date, timedelta
        lead["target_delivery_date"] = (date.fromisoformat(policy["defaults"]["test_reference_date"]) + timedelta(days=days)).isoformat()
    else:
        lead["target_delivery_date"] = None
    lead["reference_date"] = policy["defaults"]["test_reference_date"]
    payload.append({"case_id":case["case_id"],"lead":lead,"answers":mocks[case["case_id"]]["answers"],"policy":policy,"run_source":"MOCK"})

prepare = "const records = " + json.dumps(payload,separators=(",",":")) + "; return records.map(json=>({json}));"
state = "return $input.all().map(item=>{const x=item.json,l=x.lead; const days=l.target_delivery_date===null?null:Math.round((Date.parse(l.target_delivery_date+'T00:00:00Z')-Date.parse(l.reference_date+'T00:00:00Z'))/86400000); return {json:{...x,jev_state:{business:x.policy.business,lead:{message:l.message,budget_eur:l.budget_eur,currency:l.currency,target_delivery_date:l.target_delivery_date,days_until_delivery:days}}}};});"
decide = (ROOT / "workflows/mock_decide.js").read_text(encoding="utf-8")
preview = "const esc=s=>String(s??'Not stated').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/@/g,'＠').slice(0,500); return $input.all().map(item=>{const x=item.json,l=x.lead; return {json:{case_id:x.case_id,run_source:'MOCK',route:x.route,priority_score:x.priority_score,reason_code:x.reason_code,owner_queue:x.owner_queue,review_required:x.review_required,slack_status:'PREVIEW_ONLY',slack_preview:['B2B ENQUIRY | DEMO | MOCK','Company: '+esc(l.company_name),'Current phase: '+esc(x.answers.engagement_scope.choice),'Budget EUR: '+esc(l.budget_eur),'Requested completion: '+esc(l.target_delivery_date),'Category: '+x.route,'Priority: '+(x.priority_score===null?'Not scored':x.priority_score),'Reason: '+esc(x.reason_code),'Next action: '+esc(x.next_action),'Owner: '+esc(x.owner_queue)].join('\\n')}};});"

def code_node(var,name,body):
    return f"const {var} = node({{ type: 'n8n-nodes-base.code', version: 2, config: {{ name: {json.dumps(name)}, parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {json.dumps(body)} }} }} }});"

source = "\n".join([
    "const start = trigger({ type: 'n8n-nodes-base.manualTrigger', version: 1, config: { name: 'Start Mock Showcase' } });",
    code_node("prepare","Prepare Five Synthetic Cases",prepare),
    code_node("build","Build JEV State Allowlist",state),
    code_node("route","Validate Typed Answers and Apply Policy",decide),
    code_node("slack","Build Slack Previews Only",preview),
    "export default workflow('jev-b2b-demo-mock-showcase', 'JEV B2B Demo | Mock Showcase').add(start).to(prepare).to(build).to(route).to(slack);"
])
target = ROOT / "workflows/mock-showcase.sdk.js"
target.write_text(source,encoding="utf-8")
print(f"Built {target.name} with {len(showcase)} cases; no network calls")
