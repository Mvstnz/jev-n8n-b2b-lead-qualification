"""Build an inactive n8n native-JEV core draft with no embedded credential."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

policy = read("config/policy.json")
questions = read("config/jev-questions.json")
prepare = "\n".join([
    "const LIVE_ENABLED=false; if(!LIVE_ENABLED) throw new Error('Vercel account verification and runtime credential binding required');",
    "const x=$input.first().json;",
    "if(x.run_source!=='LIVE JEV'||!x.lead||typeof x.lead!=='object') throw new Error('Trusted LIVE JEV input required');",
    "const l=x.lead;",
    "if(typeof l.message!=='string'||!l.message.trim()||l.message.length>5000||l.currency!=='EUR'||(l.budget_eur!==null&&(typeof l.budget_eur!=='number'||!Number.isFinite(l.budget_eur)||l.budget_eur<0))) throw new Error('Invalid normalized lead');",
    "if(l.target_delivery_date!==null&&!/^\\d{4}-\\d{2}-\\d{2}$/.test(l.target_delivery_date)) throw new Error('Invalid delivery date');",
    "const policy=" + json.dumps(policy,separators=(",",":")) + ";",
    "const questions=" + json.dumps(questions,separators=(",",":")) + ";",
    "const today=new Date().toISOString().slice(0,10);",
    "const days=l.target_delivery_date===null?null:Math.round((Date.parse(l.target_delivery_date+'T00:00:00Z')-Date.parse(today+'T00:00:00Z'))/86400000);",
    "if(l.target_delivery_date!==null&&!Number.isFinite(days)) throw new Error('Invalid delivery date');",
    "const state={business:policy.business,lead:{message:l.message,budget_eur:l.budget_eur,currency:l.currency,target_delivery_date:l.target_delivery_date,days_until_delivery:days}};",
    "const jev_request={model:'typesafe-ai/jev',state,questions};",
    "const price=0.000000042,allowedUsd=0,estimatedMax=JSON.stringify(jev_request).length*price;",
    "if(estimatedMax>allowedUsd) throw new Error('Per-request allowance exceeded');",
    "return [{json:{lead:{...l,reference_date:today},policy,jev_request,run_source:'LIVE JEV',estimated_request_usd:estimatedMax}}];",
])
adapt = "\n".join([
    "const source=$('Build Native JEV Request').first().json; const reply=$input.first().json;",
    "const body=reply.body??reply; const status=reply.statusCode??200;",
    "if(status!==200||!body||body.model!=='typesafe-ai/jev') return [{json:{...source,answers:null,provider_error:'http_or_model_error',http_status:status}}];",
    "return [{json:{...source,answers:body.answers??null,jev_metadata:{model:body.model,id:body.id??null,created:body.created??null,usage:body.usage??null,providerMetadata:body.providerMetadata??null},http_status:status}}];",
])
route = (ROOT / "workflows/mock_decide.js").read_text(encoding="utf-8")
failure = "return $input.all().map(item=>{const x=item.json;if(!x.provider_error)return item;return {json:{...x,route:'NEEDS_REVIEW',priority_score:null,breakdown:null,reason_code:'provider_error',next_action:'Review the JEV technical failure; do not substitute mock answers.',owner_queue:'technical_review',review_required:true}};});"
def code_node(var,name,body):
    return f"const {var} = node({{ type: 'n8n-nodes-base.code', version: 2, config: {{ name: {json.dumps(name)}, parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {json.dumps(body)} }} }} }});"

source = "\n".join([
    "const incoming = trigger({ type: 'n8n-nodes-base.executeWorkflowTrigger', version: 1.1, config: { name: 'Trusted Internal Evaluation Input', parameters: { inputSource: 'workflowInputs', workflowInputs: { values: [{ name: 'lead', type: 'object' }, { name: 'run_source', type: 'string' }] } } } });",
    code_node("prepare","Build Native JEV Request",prepare),
    "const evaluate = node({ type: 'n8n-nodes-base.httpRequest', version: 4.5, config: { name: 'Evaluate with JEV via Vercel AI Gateway', parameters: { method: 'POST', url: 'https://ai-gateway.vercel.sh/v1/evaluate', authentication: 'genericCredentialType', genericAuthType: 'httpTemplatedCustomAuth', sendBody: true, contentType: 'json', specifyBody: 'json', jsonBody: expr('{{ JSON.stringify($json.jev_request) }}'), options: { response: { response: { fullResponse: true, neverError: true, responseFormat: 'json' } } } }, credentials: { httpTemplatedCustomAuth: newCredential('JEV B2B Demo Vercel Gateway') } } });",
    code_node("adapt","Validate Native Response Envelope",adapt),
    code_node("route","Validate Typed Answers and Apply Policy",route),
    code_node("failure","Route Provider Failures for Review",failure),
    "export default workflow('jev-b2b-demo-evaluation-core','JEV B2B Demo | Evaluation Core').add(incoming).to(prepare).to(evaluate).to(adapt).to(route).to(failure);",
])
(ROOT / "workflows/evaluation-core.sdk.js").write_text(source,encoding="utf-8")
print("Built inactive native JEV core draft; no credential value or request")
