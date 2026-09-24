"""Build a protected n8n intake draft; private bindings are CLI inputs only.

The default output uses inert placeholders. A bound source containing actual
workflow/sheet IDs belongs outside the public repository.
"""
from argparse import ArgumentParser
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def code_node(var,name,body):
    return f"const {var} = node({{ type: 'n8n-nodes-base.code', version: 2, config: {{ name: {json.dumps(name)}, parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {json.dumps(body)} }} }} }});"

def build(core_id: str, sheet_id: str) -> str:
    fields = [
        ("company_name","Company name","text",True),
        ("contact_name","Contact name","text",True),
        ("contact_email","Contact email","email",True),
        ("contact_role","Contact role (display only)","text",False),
        ("company_size","Company size (display only)","number",False),
        ("message","Describe the current request","textarea",True),
        ("budget_eur","Total EUR budget for the current paid phase","number",False),
        ("target_delivery_date","Requested completion date of the current phase","date",False),
    ]
    form_params = {
        "authentication":"n8nUserAuth", "requireExecuteAccess":True,
        "formTitle":"Business Automation Enquiry - JEV Demo",
        "formDescription":"Fictional business. Synthetic data only. This form does not create a contract or confirm delivery. The date is requested completion, not a meeting or start date.",
        "formFields":{"values":[{"fieldName":n,"fieldLabel":label,"fieldType":kind,"requiredField":required} for n,label,kind,required in fields]},
        "responseMode":"lastNode", "options":{"path":"jev-b2b-demo-intake-gated"},
    }
    normalizer = (ROOT / "workflows/intake_normalize.js").read_text(encoding="utf-8")
    invalid = "return $input.all().map(item=>({json:{status:'INVALID_INPUT',errors:item.json.errors,next_action:'Correct the submitted information. No evaluation or storage occurred.'}}));"
    preview = "const x=$('Evaluate Current Paid Phase').first().json; const esc=s=>String(s??'Not stated').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/@/g,'＠').slice(0,500);const l=x.lead;const message=['B2B ENQUIRY | DEMO | LIVE JEV','Company: '+esc(l.company_name),'Current phase: '+esc(x.answers?.engagement_scope?.choice),'Budget EUR: '+esc(l.budget_eur),'Requested completion: '+esc(l.target_delivery_date),'Category: '+esc(x.route),'Priority: '+(x.priority_score===null?'Not scored':x.priority_score),'Reason: '+esc(x.reason_code),'Next action: '+esc(x.next_action),'Owner: '+esc(x.owner_queue)].join('\\n');return [{json:{status:'SAVED',run_source:x.provider_error?'LIVE JEV ERROR':'LIVE JEV',route:x.route,slack_status:'PREVIEW_ONLY',slack_preview:message,note:'No Slack message was sent.'}}];"
    finish = "return $input.all().map(item=>({json:{status:item.json.status,route:item.json.route,message:'Synthetic demo enquiry recorded for human review. No quote or delivery promise.',slack_status:'PREVIEW_ONLY'}}));"
    mapped = {
        "Received at":"{{ $now.toISO() }}",
        "Company":"{{ $json.lead.company_name }}",
        "Current-phase budget EUR":"{{ $json.lead.budget_eur }}",
        "Requested completion":"{{ $json.lead.target_delivery_date }}",
        "Scope assessed":"{{ $json.answers?.engagement_scope?.choice ?? '' }}",
        "Reported funding status":"{{ $json.answers?.buying_readiness?.choice ?? '' }}",
        "Category":"{{ $json.route }}",
        "Priority score":"{{ $json.priority_score ?? '' }}",
        "Main reason":"{{ $json.reason_code }}",
        "Next action":"{{ $json.next_action }}",
        "Owner queue":"{{ $json.owner_queue }}",
        "Review required":"{{ $json.review_required }}",
        "Data source":"{{ $json.provider_error ? 'LIVE JEV ERROR' : 'LIVE JEV' }}",
        "contact_email":"{{ $json.lead.contact_email }}",
        "original_message":"{{ $json.lead.message }}",
        "reason_code":"{{ $json.reason_code }}",
        "policy_version":"{{ $json.policy_version }}",
        "model_id":"{{ $json.jev_metadata?.model ?? '' }}",
        "provider_generation_id":"{{ $json.jev_metadata?.id ?? '' }}",
        "slack_status":"PREVIEW_ONLY",
        "execution_id":"{{ $execution.id }}",
    }
    value = "{" + ",".join(json.dumps(k)+":expr("+json.dumps(v)+")" for k,v in mapped.items()) + "}"
    schema = [{"id":k,"displayName":k,"required":False,"defaultMatch":False,"display":True,"type":"string","canBeUsedToMatch":False} for k in mapped]
    sheets = (
        "const save = node({ type: 'n8n-nodes-base.googleSheets', version: 4.7, config: { name: 'Save Lead to Private Google Sheet', parameters: { resource: 'sheet', operation: 'append', authentication: 'oAuth2', documentId: { __rl: true, mode: 'id', value: " + json.dumps(sheet_id) + " }, sheetName: { __rl: true, mode: 'name', value: 'Leads' }, columns: { mappingMode: 'defineBelow', value: " + value + ", schema: " + json.dumps(schema) + " }, options: { cellFormat: 'RAW' } }, credentials: { googleSheetsOAuth2Api: newCredential('Google Sheets account') } } });"
    )
    inputs = "{ mappingMode: 'defineBelow', value: { lead: expr('{{ $json.lead }}'), run_source: 'LIVE JEV' }, matchingColumns: [], schema: [{ id: 'lead', displayName: 'lead', required: false, defaultMatch: false, display: true, canBeUsedToMatch: false, type: 'object' }, { id: 'run_source', displayName: 'run_source', required: false, defaultMatch: false, display: true, canBeUsedToMatch: false, type: 'string' }] }"
    lines = [
        "const form = trigger({ type: 'n8n-nodes-base.formTrigger', version: 2.6, config: { name: 'Receive Protected Demo Enquiry', parameters: " + json.dumps(form_params) + " } });",
        code_node("normalize","Normalize and Validate",normalizer),
        "const valid = ifElse({ version: 2.2, config: { name: 'Valid Enquiry?', parameters: { conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'strict' }, conditions: [{ leftValue: expr('{{ $json.status }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'VALIDATED' }], combinator: 'and' } } } });",
        code_node("invalid","Return Input Error Without Side Effects",invalid),
        "const evaluate = node({ type: 'n8n-nodes-base.executeWorkflow', version: 1.3, config: { name: 'Evaluate Current Paid Phase', parameters: { mode: 'each', source: 'database', workflowId: { __rl: true, mode: 'id', value: " + json.dumps(core_id) + " }, workflowInputs: " + inputs + ", options: { waitForSubWorkflow: true } } } });",
        sheets,
        code_node("preview","Build Internal Slack Preview Only",preview),
        code_node("finish","Return Demo Receipt",finish),
        "export default workflow('jev-b2b-demo-intake-gated','JEV B2B Demo | Intake').add(form).to(normalize).to(valid.onTrue(evaluate.to(save.to(preview.to(finish)))).onFalse(invalid));",
    ]
    return "\n".join(lines)

def main():
    parser = ArgumentParser()
    parser.add_argument("--core-id",default="REPLACE_WITH_PRIVATE_CORE_ID")
    parser.add_argument("--sheet-id",default="REPLACE_WITH_PRIVATE_SHEET_ID")
    parser.add_argument("--output",type=Path,default=ROOT / "workflows/intake-pipeline.template.sdk.js")
    args=parser.parse_args()
    args.output.write_text(build(args.core_id,args.sheet_id),encoding="utf-8")
    print("Built protected intake pipeline draft; no external requests")

if __name__ == "__main__":
    main()
