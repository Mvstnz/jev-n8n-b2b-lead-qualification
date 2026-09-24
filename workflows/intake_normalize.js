// n8n Code node body: customer values remain untrusted.
const allowed = new Set(['company_name','contact_name','contact_email','contact_role','company_size','message','budget_eur','currency','target_delivery_date','submittedAt','formMode']);
const raw = $input.first().json;
const keys = Object.keys(raw);
const extra = keys.filter(k=>!allowed.has(k));
const errors = [];
if (JSON.stringify(raw).length > 32768) errors.push('payload_too_large');
if (extra.length) errors.push('unauthorized_fields');
const text=(name,max,required=false)=>{
  const value=raw[name];
  if (value===undefined||value===null||value==='') {if(required) errors.push('missing_'+name);return null;}
  if(typeof value!=='string') {errors.push('invalid_'+name);return null;}
  const clean=value.trim().replace(/\s+/g,' ');
  if ((required&&!clean)||clean.length>max) errors.push('invalid_'+name);
  return clean;
};
const company_name=text('company_name',200,true);
const contact_name=text('contact_name',200,true);
const contact_email=text('contact_email',254,true);
if (contact_email&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact_email)) errors.push('invalid_contact_email');
const contact_role=text('contact_role',200);
let company_size=raw.company_size;
if (company_size===''||company_size===undefined) company_size=null;
if (company_size!==null) {
  if (typeof company_size==='string'&&/^\d+$/.test(company_size)) company_size=Number(company_size);
  if (!Number.isSafeInteger(company_size)||company_size<1) errors.push('invalid_company_size');
}
const message=typeof raw.message==='string'?raw.message.trim():null;
if (!message||message.length>5000) errors.push('invalid_message');
let budget_eur=raw.budget_eur;
if (budget_eur===''||budget_eur===undefined) budget_eur=null;
if (budget_eur!==null) {
  if(typeof budget_eur==='string'&&/^(?:0|[1-9]\d*)(?:\.\d{1,2})?$/.test(budget_eur)) budget_eur=Number(budget_eur);
  if(typeof budget_eur!=='number'||!Number.isFinite(budget_eur)||budget_eur<0) errors.push('invalid_budget');
}
const currency=raw.currency??'EUR';
if(currency!=='EUR') errors.push('unsupported_currency');
let target_delivery_date=raw.target_delivery_date??null;
if(target_delivery_date==='') target_delivery_date=null;
if(target_delivery_date!==null) {
  const match=typeof target_delivery_date==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(target_delivery_date);
  const parsed=match?new Date(target_delivery_date+'T00:00:00Z'):null;
  if(!match||Number.isNaN(parsed.getTime())||parsed.toISOString().slice(0,10)!==target_delivery_date) errors.push('invalid_delivery_date');
}
const lead={company_name,contact_name,contact_email,contact_role,company_size,message,budget_eur,currency,target_delivery_date};
return [{json:{status:errors.length?'INVALID_INPUT':'VALIDATED',errors,lead,source:'n8n_form',run_mode:'MOCK',slack_status:'PREVIEW_ONLY',next_action:errors.length?'Correct submitted information.':'Await authorised JEV execution and Sheets credential binding.'}}];
