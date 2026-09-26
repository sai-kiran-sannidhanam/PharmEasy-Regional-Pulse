"""review_gate.py -- Review-gate engine with validation and append-only audit logging."""
import json
import uuid
from datetime import datetime, timezone

AUDIT_LOG_PATH = "audit_log.jsonl"
VALID_DECISIONS = {"approve", "edit", "reject"}

def review_gate_v1(report: dict, decision: str, reviewer_note: str = "") -> dict:
    """
    Validates reviewer decision, sets downstream usage authorization,
    and appends a verifiable entry to the audit log.
    """
    if decision not in VALID_DECISIONS:
        raise ValueError(f"Invalid decision '{decision}'. Must be one of {VALID_DECISIONS}")

    run_id = f"run_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    downstream_allowed = (decision == "approve")
    region = report.get("region", "MULTIPLE_REGIONS")

    audit_entry = {
        "timestamp": now_iso,
        "run_id": run_id,
        "region": region,
        "decision": decision,
        "reviewer_note": reviewer_note
    }

    # Append to audit log
    with open(AUDIT_LOG_PATH, "a") as f:
        f.write(json.dumps(audit_entry) + "\n")

    updated_report = dict(report)
    updated_report["review_metadata"] = {
        "run_id": run_id,
        "reviewed_at": now_iso,
        "decision": decision,
        "reviewer_note": reviewer_note,
        "downstream_allowed": downstream_allowed
    }

    return updated_report

def run_test_harness():
    print("Executing Review Gate Test Harness...")

    sample_report_guntur = {
        "region": "Guntur",
        "metric_flag": "MoM Sales Surge (+122.19%)",
        "draft_summary": "Guntur order volumes surged to 75 orders in May 2026."
    }

    sample_report_vizag = {
        "region": "Visakhapatnam",
        "metric_flag": "MoM Sales Contraction (-50.62%)",
        "draft_summary": "Vizag order volumes dropped sharply in May 2026."
    }

    sample_report_bengaluru = {
        "region": "Bengaluru",
        "metric_flag": "MoM Sales Contraction (-17.91%)",
        "draft_summary": "Bengaluru orders fell from 116 to 97."
    }

    # 1. Exercise 'approve'
    approved = review_gate_v1(sample_report_guntur, "approve", "Numbers verified against SQLite engine. Recommendation sound.")
    print(f"\n[Path 1: APPROVE] Downstream Allowed: {approved['review_metadata']['downstream_allowed']}")

    # 2. Exercise 'edit'
    edited = review_gate_v1(sample_report_vizag, "edit", "Requesting breakdown of distributor vs retail order drops.")
    print(f"[Path 2: EDIT]    Downstream Allowed: {edited['review_metadata']['downstream_allowed']}")

    # 3. Exercise 'reject'
    rejected = review_gate_v1(sample_report_bengaluru, "reject", "Unverified assumption on rider strike. Re-draft with fulfillment logs.")
    print(f"[Path 3: REJECT]  Downstream Allowed: {rejected['review_metadata']['downstream_allowed']}")

    # 4. Test invalid decision check
    try:
        review_gate_v1(sample_report_guntur, "publish_now", "Bypassing gate")
    except ValueError as e:
        print(f"[Validation Check] Successfully caught invalid decision: '{e}'")

    print(f"\nTest harness completed. All entries appended to {AUDIT_LOG_PATH}.")

if __name__ == "__main__":
    run_test_harness()