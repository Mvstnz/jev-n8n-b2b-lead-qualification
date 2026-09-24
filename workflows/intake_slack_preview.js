// Internal n8n preview. A separate, approval-gated workflow handles Slack delivery.
const x = $('Ask JEV via Vercel AI Gateway').first().json;
const lead = x.lead || {};
const clean = value => String(value ?? 'Not stated')
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/@/g, '\uFF20').slice(0, 500);
const phase = {
  paid_discovery: 'paid process discovery',
  focused_pilot: 'a focused pilot',
  standard_rollout: 'a rollout for one department',
  enterprise_rollout: 'a large enterprise rollout',
  unsupported: 'work outside this demo service',
  unclear: 'scope that needs clarification',
  not_applicable: 'no new project scope'
}[x.answers?.engagement_scope?.choice] || 'scope that needs clarification';
const decision = {
  HOT: 'Sales follow-up',
  WARM: 'Keep in view and clarify the buying step',
  COLD: 'Record the fit or budget gap',
  NEEDS_REVIEW: 'Human review needed',
  NOT_A_SALES_LEAD: 'Route outside the sales queue'
}[x.route] || 'Human review needed';
const reason = {
  qualified_current_phase: 'The described work, customer-stated funding and timing passed the fixed rules for this requested phase.',
  approval_pending: 'Funding approval for the requested work is still pending.',
  enterprise_feasibility: 'A large rollout needs a specialist feasibility check before a sales score.',
  existing_customer_support: 'This is an issue with an existing service, so it belongs with support.',
  delivery_dependency: 'Access, integration or hosting dependencies need a specialist check.',
  delivery_too_soon: 'The requested completion date needs a delivery check.',
  missing_commercial_fields: 'Budget or requested completion is missing for the current work.',
  approval_not_stated: 'Approval of funding for this specific work was not stated.',
  uncertain_approval: 'Funding approval needs clarification.',
  conflicting_information: 'The request contains conflicting facts.',
  unclear_inquiry_type: 'It is unclear whether this is a new paid request.',
  mixed_support_and_sales: 'The support issue and possible new project need separate owners.',
  ambiguous_request: 'The requested deliverable is ambiguous.',
  uncertain_scope: 'The project scope is uncertain.',
  scope_needs_clarification: 'The scope needs clarification before scoring.',
  budget_below_current_scope: 'The customer-stated budget is below the fixed floor for this scope.',
  project_on_hold: 'The customer described the project as on hold.',
  research_stage: 'The request is still exploratory.',
  future_delivery_horizon: 'The requested completion is too far away for immediate follow-up.',
  outside_service_offer: 'The requested work does not fit the fictional service offer.',
  supplier_pitch: 'This is a supplier approach rather than a sales enquiry.',
  careers: 'This is a careers enquiry rather than a sales enquiry.',
  not_yet_concrete_buying_step: 'Interest is visible, but the next buying step needs clarification.',
  low_policy_priority: 'The fixed priority factors did not reach the sales threshold.',
  instruction_attack: 'The message included instructions that need technical review.'
}[x.reason_code] || 'A person should check the request and the recorded assessment.';
const score = Number.isFinite(x.priority_score)
  ? `${x.priority_score}/100 (business priority, not purchase probability)`
  : 'Not scored; a human decision or a different queue is needed.';
const message = [
  '*JEV lead qualification | synthetic demo | preview only*',
  '*Company:* ' + clean(lead.company_name),
  '*JEV understood the request as:* ' + clean(phase),
  '*Recommended route:* ' + clean(decision),
  '*Why:* ' + clean(reason),
  '*Customer-stated budget for this work:* ' + clean(lead.budget_eur == null ? 'Not stated' : `EUR ${lead.budget_eur}`),
  '*Business priority:* ' + clean(score),
  '*Next step:* ' + clean(x.next_action),
  '_Internal preview only. No Slack message or customer contact happened automatically._'
].join('\n');
return [{ json: {
  status: 'SAVED',
  run_source: x.provider_error ? 'LIVE JEV ERROR' : 'LIVE JEV',
  route: x.route,
  slack_status: 'PREVIEW_ONLY',
  slack_preview: message,
  note: 'No Slack message was sent.'
}}];
