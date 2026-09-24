// n8n Code node body. All input records here are synthetic and admin supplied.
const policy = $input.first().json.policy;
const choices = ['inquiry_type','engagement_scope','buying_readiness','delivery_risk'];
const scores = ['service_fit','buying_intent'];
const flags = ['contradiction','instruction_attack','semantic_ambiguity'];
const number = x => typeof x === 'number' && Number.isFinite(x);
function validAnswers(a) {
  if (!a || typeof a !== 'object') return false;
  for (const k of choices) {
    const x=a[k], opts=policy.choice_options[k];
    if (!x || x.type!=='choice' || !opts.includes(x.choice) || !x.probabilities ||
        Object.keys(x.probabilities).sort().join('|')!==[...opts].sort().join('|') ||
        Object.values(x.probabilities).some(v=>!number(v)||v<0||v>1) ||
        Math.abs(Object.values(x.probabilities).reduce((s,v)=>s+v,0)-1)>.02 ||
        x.probabilities[x.choice]<Math.max(...Object.values(x.probabilities))-1e-9) return false;
  }
  for (const k of scores) {
    const x=a[k];
    if (!x || x.type!=='score' || !number(x.score) || x.score<0 || x.score>3 ||
        !x.probabilities || Object.keys(x.probabilities).sort().join('|')!=='0|1|2|3' ||
        Object.values(x.probabilities).some(v=>!number(v)||v<0||v>1) ||
        Math.abs(Object.values(x.probabilities).reduce((s,v)=>s+v,0)-1)>.02) return false;
  }
  return flags.every(k=>a[k] && a[k].type==='boolean' && number(a[k].probability) && a[k].probability>=0 && a[k].probability<=1);
}
function decision(lead,a) {
  const out=(route,reason,next_action,owner_queue='sales',priority_score=null,breakdown=null)=>({route,reason_code:reason,next_action,owner_queue,priority_score,breakdown,review_required:route==='NEEDS_REVIEW',policy_version:policy.policy_version});
  const review=(reason,next_action='A person must clarify this point before sales prioritisation.',owner='sales_review')=>out('NEEDS_REVIEW',reason,next_action,owner);
  if (!validAnswers(a)) return review('malformed_model_response','Inspect the typed model answer.','technical_review');
  const t=policy.review_thresholds;
  if (a.instruction_attack.probability>=t.instruction_attack_probability) return review('instruction_attack','Keep configuration unchanged.','technical_review');
  if (a.contradiction.probability>=t.contradiction_probability) return review('conflicting_information','Clarify current-phase facts.');
  const uncertain=k=>{const p=Object.values(a[k].probabilities).sort((x,y)=>y-x);return a[k].probabilities[a[k].choice]<t.minimum_choice_probability || p[0]-p[1]<t.minimum_choice_margin;};
  const kind=a.inquiry_type.choice;
  if (uncertain('inquiry_type')||kind==='unclear') return review('unclear_inquiry_type','Clarify who is buying what.');
  if (kind==='existing_customer_support') return out('NOT_A_SALES_LEAD','existing_customer_support','Route for support triage; do not discard or sales-score.','support');
  if (kind==='supplier_pitch') return out('NOT_A_SALES_LEAD','supplier_pitch','Route to vendor review.','vendor_review');
  if (kind==='careers') return out('NOT_A_SALES_LEAD','careers','Route to the people inbox.','people');
  if (kind==='mixed_support_and_sales') return review('mixed_support_and_sales','Preserve both support and sales work.','support_and_sales');
  if (a.semantic_ambiguity.probability>=t.semantic_ambiguity_probability) return review('ambiguous_request','Clarify the current deliverable.');
  if (uncertain('engagement_scope')) return review('uncertain_scope');
  const scope=a.engagement_scope.choice,fit=a.service_fit.score,intent=a.buying_intent.score;
  if (scope==='unsupported'||fit<=policy.routing.clear_mismatch_max_fit) return out('COLD','outside_service_offer','Record the mismatch; no automatic rejection.');
  if (scope==='unclear'||scope==='not_applicable'||fit<policy.routing.minimum_clear_fit) return review('scope_needs_clarification');
  if (scope==='enterprise_rollout') return review('enterprise_feasibility','Assign solution review.','solution_review');
  if (uncertain('delivery_risk')||a.delivery_risk.choice!=='none_stated') return review('delivery_dependency','Check access, integration or hosting.','solution_review');
  if (lead.budget_eur===null||lead.target_delivery_date===null) return review('missing_commercial_fields','Ask for current-phase budget and completion date.');
  const phase=policy.business.phases[scope];
  const days=Math.round((Date.parse(lead.target_delivery_date+'T00:00:00Z')-Date.parse(lead.reference_date+'T00:00:00Z'))/86400000);
  if (days<phase.minimum_notice_days) return review('delivery_too_soon','Discuss the date with a delivery owner.','solution_review');
  if (lead.budget_eur<phase.minimum_budget_eur) return out('COLD','budget_below_current_scope','Record the budget-to-scope gap.');
  if (uncertain('buying_readiness')) return review('uncertain_approval');
  const ready=a.buying_readiness.choice;
  if (ready==='unknown'||ready==='not_applicable') return review('approval_not_stated','Ask whether current-phase funding is approved.');
  if (ready==='on_hold') return out('WARM','project_on_hold','Resume only after explicit restart.');
  if (ready==='approval_pending') return out('WARM','approval_pending','Support the approval process.');
  if (ready==='exploration_only') return out('WARM','research_stage','Keep visible without automatic outreach.');
  if (days>policy.routing.long_horizon_days) return out('WARM','future_delivery_horizon','Recommend later follow-up, no automatic campaign.');
  const ratio=lead.budget_eur/phase.minimum_budget_eur;
  const parts={service_fit:fit/3*policy.weights.service_fit,buying_intent:intent/3*policy.weights.buying_intent,budget_fit:ratio>=1.5?20:15,timing:days<=90?15:10};
  const total=Object.values(parts).reduce((s,v)=>s+v,0),display=Math.round(total*100)/100;
  if (total>=policy.routing.hot_min_score&&fit>=policy.routing.hot_min_service_fit&&intent>=policy.routing.hot_min_buying_intent) return out('HOT','qualified_current_phase','Recommend personal sales follow-up.', 'sales',display,parts);
  if (total>=policy.routing.warm_min_score) return out('WARM','not_yet_concrete_buying_step','Clarify the next buying step.','sales',display,parts);
  return out('COLD','low_policy_priority','Keep the record; no automatic rejection.','sales',display,parts);
}
return $input.all().map(item=>({json:{...item.json,...decision(item.json.lead,item.json.answers)}}));
