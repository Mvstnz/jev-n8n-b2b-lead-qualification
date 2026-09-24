"""Build an authenticated, inactive n8n form draft with strict input checks."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
normalizer = (ROOT / "workflows/intake_normalize.js").read_text(encoding="utf-8")
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
field_data = [{"fieldName":name,"fieldLabel":label,"fieldType":kind,"requiredField":required} for name,label,kind,required in fields]
form_params = {"authentication":"n8nUserAuth","requireExecuteAccess":True,
               "formTitle":"Business Automation Enquiry - JEV Demo",
               "formDescription":"Fictional business. Synthetic data only. This form does not create a contract or confirm delivery. The date is requested completion, not a meeting or start date.",
               "formFields":{"values":field_data},"responseMode":"lastNode",
               "options":{"path":"jev-b2b-demo-intake-private"}}
code = "\n".join([
    "const form = trigger({ type: 'n8n-nodes-base.formTrigger', version: 2.6, config: { name: 'Receive Enquiry', parameters: " + json.dumps(form_params) + " } });",
    "const normalize = node({ type: 'n8n-nodes-base.code', version: 2, config: { name: 'Normalize and Validate', parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: " + json.dumps(normalizer) + " } } });",
    "export default workflow('jev-b2b-demo-intake-preview','JEV B2B Demo | Intake Preview').add(form).to(normalize);"
])
target = ROOT / "workflows/intake-preview.sdk.js"
target.write_text(code,encoding="utf-8")
print("Built authenticated intake draft; no external calls")
