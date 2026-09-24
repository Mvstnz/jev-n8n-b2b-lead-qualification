"""Reproducible offline mock and rules-only runs; never contacts a service."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

from policy_reference import decide, materialize_fixture
from rules_baseline import baseline_decide

ROOT = Path(__file__).resolve().parents[1]
def read(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

def run():
    policy = read("config/policy.json")
    day = policy["defaults"]["test_reference_date"]
    development = read("fixtures/development_inputs.json")
    evaluation = read("fixtures/evaluation_inputs.json")
    mocks = read("fixtures/mock_answers.json")
    labels_dev = read("fixtures/labels/development_expected.json")
    labels_eval = read("fixtures/labels/evaluation_expected.json")
    records = []
    for source, fixtures in (("development", development), ("evaluation", evaluation)):
        for case in fixtures:
            lead = materialize_fixture(case, day)
            base = baseline_decide(lead, policy, day)
            record = {"case_id":case["case_id"], "source":source,
                      "rules_only_route":base["route"], "rules_only_reason":base["reason_code"]}
            if case["case_id"] in mocks:
                mock = decide(lead, mocks[case["case_id"]]["answers"], policy, day)
                record.update(mock_route=mock["route"],mock_reason=mock["reason_code"])
            records.append(record)
    # Labels are joined only after the routes have been computed.
    def expected(labels, case_id):
        return next(row["expected_route"] for row in labels if row["case_id"] == case_id)
    for record in records:
        record["expected_route"] = expected(labels_dev if record["source"] == "development" else labels_eval,record["case_id"])
    for source in ("development","evaluation"):
        subset = [r for r in records if r["source"] == source]
        for mode in ("rules_only","mock"):
            present = [r for r in subset if mode+"_route" in r]
            correct = sum(r[mode+"_route"] == r["expected_route"] for r in present)
            print(f"{source} {mode}: {correct}/{len(present)} authored-policy route agreement")
        print(f"{source} labels:",dict(Counter(r["expected_route"] for r in subset)))
    return records

if __name__ == "__main__":
    run()
