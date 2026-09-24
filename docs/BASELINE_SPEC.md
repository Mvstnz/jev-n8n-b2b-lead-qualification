# Rules-only baseline specification

Build this baseline during development, freeze it before final evaluation and run it on the same input records as JEV. It is a comparator, not a deliberately weak straw man.

Use explicit, reviewed phrase/negation rules to infer transaction direction, current-phase scope, funding status and buying intent. Handle phrases such as "not approved", "not requesting a quotation", "existing contract", "separate paid scope", "only this pilot", "not the current purchase" and "frozen". Unknown or conflicting meanings must yield review, not an optimistic default.

Use the same current-phase budget floors, timing gates and scoring formula as the JEV workflow. Add no case-ID exceptions and do not tune against the final evaluation labels. Do not give the baseline label/rationale/title data or contact prestige as input.

If an internal adapter requires probability-shaped fields, fixed certainty values may represent matched deterministic rules only. Label them RULES ONLY and do not present them as model probabilities or calibrated confidence. Document this interface choice.

Report the two systems side by side on the same first-run inputs, including every failure and review. If the baseline matches or exceeds JEV on this small synthetic set, state that. One self-authored portfolio dataset is not proof of general superiority or real-world conversion performance.

The packet does not include a completed baseline implementation. Implementing and testing it is part of the handoff.
