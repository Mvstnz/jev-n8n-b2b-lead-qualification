"""Build a side-effect-free n8n mock regression runner for all evaluation cases."""
from datetime import date, timedelta
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

policy = read("config/policy.json")
fixtures = read("fixtures/evaluation_inputs.json")
mocks = read("fixtures/mock_answers.json")
labels = {row["case_id"]:row["expected_route"] for row in read("fixtures/labels/evaluation_expected.json")}
assert len(fixtures) == len(labels) == 30
cases = []
for case in fixtures:
    lead = dict(case["input"])
    days = lead.pop("target_delivery_days_from_reference")
    lead["target_delivery_date"] = None if days is None else (
        date.fromisoformat(policy["defaults"]["test_reference_date"]) + timedelta(days=days)
    ).isoformat()
    lead["reference_date"] = policy["defaults"]["test_reference_date"]
    cases.append({"case_id":case["case_id"], "lead":lead,
                  "answers":mocks[case["case_id"]]["answers"]})

prepare = (
    "const policy=" + json.dumps(policy,separators=(",",":")) + ";"
    "const cases=" + json.dumps(cases,separators=(",",":")) + ";"
    "const rows=[]; for (const x of cases) for(let repetition=1;repetition<=3;repetition++) "
    "rows.push({json:{...x,policy,repetition,run_source:'MOCK_REPEAT'}}); return rows;"
)
state = "return $input.all().map(item=>{const x=item.json,l=x.lead; const days=l.target_delivery_date===null?null:Math.round((Date.parse(l.target_delivery_date+'T00:00:00Z')-Date.parse(l.reference_date+'T00:00:00Z'))/86400000);return {json:{...x,jev_state:{business:x.policy.business,lead:{message:l.message,budget_eur:l.budget_eur,currency:l.currency,target_delivery_date:l.target_delivery_date,days_until_delivery:days}}}};});"
decide = (ROOT / "workflows/mock_decide.js").read_text(encoding="utf-8")
aggregate = (
    "const expected=" + json.dumps(labels,separators=(",",":")) + ";"
    "const rows=$input.all().map(i=>i.json);"
    "const matches=rows.filter(x=>x.route===expected[x.case_id]).length;"
    "const falseHot=rows.filter(x=>x.route==='HOT'&&expected[x.case_id]!=='HOT').length;"
    "const distribution={};for(const x of rows)distribution[x.route]=(distribution[x.route]||0)+1;"
    "const mismatches=rows.filter(x=>x.route!==expected[x.case_id]).map(x=>({case_id:x.case_id,repetition:x.repetition,expected:expected[x.case_id],observed:x.route}));"
    "return [{json:{run_source:'MOCK_REPEAT',case_count:Object.keys(expected).length,repetitions_per_case:3,item_count:rows.length,route_agreement_count:matches,false_hot_count:falseHot,route_distribution:distribution,mismatches,live_jev_attempts:0,google_sheet_writes:0,slack_sends:0,note:'Hand-authored mock answer policy regression only; not JEV stability or model quality.'}}];"
)
def code_node(var,name,body):
    return f"const {var} = node({{ type: 'n8n-nodes-base.code', version: 2, config: {{ name: {json.dumps(name)}, parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {json.dumps(body)} }} }} }});"

source = "\n".join([
    "const start = trigger({ type: 'n8n-nodes-base.manualTrigger', version: 1, config: { name: 'Start Mock Regression' } });",
    code_node("prepare","Prepare Thirty Synthetic Cases Times Three",prepare),
    code_node("state","Build Allowlisted JEV States",state),
    code_node("route","Validate Typed Mocks and Apply Gates",decide),
    code_node("summary","Join Authored Labels After Routing",aggregate),
    "export default workflow('jev-b2b-demo-test-runner','JEV B2B Demo | Test Runner').add(start).to(prepare).to(state).to(route).to(summary);",
])
(ROOT / "workflows/test-runner.sdk.js").write_text(source,encoding="utf-8")
print("Built 30-case, three-repeat MOCK regression runner; no external requests")
