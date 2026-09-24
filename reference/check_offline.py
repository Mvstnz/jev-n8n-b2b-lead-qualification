"""Check policy arithmetic and package fixtures without any external requests.

Run with Python 3.10+ from any working directory. Results written to checks/.
These are offline policy/fixture assertions, not provider or n8n tests.
"""
from __future__ import annotations
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import sys
from policy_reference import decide, materialize_fixture, build_state, validate_answers, validate_input

ROOT = Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
P = load('config/policy.json'); Q=load('config/jev-questions.json')
M = load('fixtures/mock_answers.json'); DATE=P['defaults']['test_reference_date']
checks=[]
def check(name, observed, expected):
    checks.append({'name':name,'passed':observed==expected,'observed':observed,'expected':expected})

all_inputs=[]
for split in ['development','evaluation']:
    inputs=load(f'fixtures/{split}_inputs.json')
    labels={x['case_id']:x for x in load(f'fixtures/labels/{split}_expected.json')}
    all_inputs+=inputs
    check(split+'_ids_match',sorted(x['case_id'] for x in inputs),sorted(labels))
    for item in inputs:
        cid=item['case_id']; lead=materialize_fixture(item,DATE); ans=M[cid]['answers']
        check(cid+'_input_valid',validate_input(lead,P),None)
        check(cid+'_mock_schema_valid',validate_answers(ans,P),None)
        result=decide(lead,ans,P,DATE)
        check(cid+'_expected_route_from_mock',result['route'],labels[cid]['expected_route'])
        if result['route'] in ['NEEDS_REVIEW','COLD','NOT_A_SALES_LEAD']:
            check(cid+'_gated_score',result['priority_score'],None)
        state=build_state(lead,P,DATE)
        check(cid+'_model_state_fields',sorted(state['lead']),sorted(['message','budget_eur','currency','target_delivery_date','days_until_delivery']))
        check(cid+'_label_is_not_in_state','expected_route' in json.dumps(state),False)

lead=materialize_fixture(all_inputs[0],DATE); answers=deepcopy(M['DEV-01']['answers'])
check('weights_total',sum(P['weights'].values()),100)
check('question_count',len(Q),9)
check('total_case_count',len(all_inputs),40)
check('unique_case_ids',len(set(x['case_id'] for x in all_inputs)),40)
check('DEV_01_score',decide(lead,answers,P,DATE)['priority_score'],100.0)
check('provider_error_routes_review',decide(lead,None,P,DATE,'timeout')['route'],'NEEDS_REVIEW')
check('provider_error_not_scored',decide(lead,None,P,DATE,'timeout')['priority_score'],None)

for label,mutator in [
    ('missing_answer',lambda a:a.pop('inquiry_type')),
    ('wrong_score_scale',lambda a:a['service_fit'].update(score=90)),
    ('nan_score',lambda a:a['service_fit'].update(score=float('nan'))),
    ('boolean_instead_of_score',lambda a:a['service_fit'].update(score=True)),
    ('missing_probability',lambda a:a['inquiry_type'].pop('probabilities')),
    ('bad_boolean',lambda a:a['contradiction'].update(probability='false')),
    ('unknown_choice',lambda a:a['engagement_scope'].update(choice='custom')),
    ('invalid_probability_sum',lambda a:a['inquiry_type']['probabilities'].update(new_project=0.1)),
]:
    a=deepcopy(answers);mutator(a)
    check(label,decide(lead,a,P,DATE)['reason_code'],'malformed_model_response')

for field,value,expected_reason in [('budget_eur',-1,'invalid_budget'),('budget_eur',True,'invalid_budget'),('contact_email','not-an-email','invalid_contact_email'),('message','  ','invalid_message'),('currency','USD','unsupported_currency'),('company_size',-3,'invalid_company_size'),('target_delivery_date','2026-02-30','invalid_delivery_date')]:
    l=deepcopy(lead);l[field]=value
    check('invalid_'+field+'_'+str(value),decide(l,answers,P,DATE)['reason_code'],expected_reason)

for name,value in [('budget_eur',None),('target_delivery_date',None)]:
    l=deepcopy(lead);l[name]=value
    check('missing_'+name,decide(l,answers,P,DATE)['reason_code'],'missing_commercial_fields')
l=deepcopy(lead);l['budget_eur']=0
check('zero_is_not_missing',decide(l,answers,P,DATE)['reason_code'],'budget_below_current_scope')

for scope,minimum,days in [('paid_discovery',3000,14),('focused_pilot',5000,21),('standard_rollout',15000,42)]:
    a=deepcopy(answers);opts=P['choice_options']['engagement_scope']
    a['engagement_scope']={'type':'choice','choice':scope,'probabilities':{o:(1.0 if o==scope else 0.0) for o in opts}}
    from datetime import date,timedelta
    for amount,expected in [(minimum-0.01,'COLD'),(minimum,'HOT'),(minimum*1.5,'HOT')]:
        l=deepcopy(lead);l['budget_eur']=amount;l['target_delivery_date']=(date.fromisoformat(DATE)+timedelta(days=days)).isoformat()
        check(scope+'_budget_'+str(amount),decide(l,a,P,DATE)['route'],expected)
    for offset,expected in [(days-1,'NEEDS_REVIEW'),(days,'HOT'),(180,'HOT'),(181,'WARM')]:
        l=deepcopy(lead);l['budget_eur']=minimum*1.5;l['target_delivery_date']=(date.fromisoformat(DATE)+timedelta(days=offset)).isoformat()
        check(scope+'_date_'+str(offset),decide(l,a,P,DATE)['route'],expected)

for field in ['instruction_attack','contradiction','semantic_ambiguity']:
    a=deepcopy(answers);a[field]['probability']=0.5
    check(field+'_inclusive_threshold',decide(lead,a,P,DATE)['route'],'NEEDS_REVIEW')
for key in ['inquiry_type','engagement_scope','buying_readiness','delivery_risk']:
    a=deepcopy(answers);opts=P['choice_options'][key];chosen=a[key]['choice'];others=[x for x in opts if x!=chosen]
    a[key]['probabilities']={x:0.0 for x in opts};a[key]['probabilities'][chosen]=0.74;a[key]['probabilities'][others[0]]=0.26
    check(key+'_low_probability',decide(lead,a,P,DATE)['route'],'NEEDS_REVIEW')

# Invariance checks prove only deterministic-policy invariance, not model invariance.
for changed in [{'company_size':1},{'company_size':100000},{'contact_role':'Managing director'},{'contact_role':'Intern'},{'company_name':'Another fictional company'}]:
    l=deepcopy(lead);l.update(changed)
    check('deterministic_invariance_'+str(changed),decide(l,answers,P,DATE),decide(lead,answers,P,DATE))

for path in sorted(ROOT.rglob('*.json')):
    if path.parent.name=='checks': continue
    try:
        json.loads(path.read_text(encoding='utf-8')); ok=True
    except (ValueError,UnicodeError): ok=False
    check('json_valid_'+str(path.relative_to(ROOT)),ok,True)

failed=[c for c in checks if not c['passed']]
report={'test_kind':'OFFLINE_POLICY_AND_FIXTURE_ASSERTIONS_ONLY','live_jev_calls':0,'external_integrations_tested':False,'assertions':len(checks),'passed':len(checks)-len(failed),'failed':len(failed),'checks':checks}
(ROOT/'checks/offline_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['fixtures','config'] for p in sorted((ROOT/folder).rglob('*.json'))}
(ROOT/'checks/fixture_hashes.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
print(f"Offline assertions: {len(checks)-len(failed)}/{len(checks)} passed. Live JEV calls: 0.")
for f in failed: print('FAIL:',f)
sys.exit(1 if failed else 0)
