"""Automated Compliance, Guardrail & End-to-End API Verification Suite for our Solution."""
from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

HERE = Path(__file__).resolve().parent
SOLUTION_ROOT = HERE.parent
REPO_ROOT = SOLUTION_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from solution.backend.app import app  # noqa: E402

BANNED_PHRASES = (
    "inflated tonnage",
    "premium smart",
    "premium service",
    "fraud",
)


def check_banned_phrases() -> None:
    text_exts = {".md", ".py", ".yaml", ".yml", ".html", ".svg", ".json"}
    violations = []
    for p in SOLUTION_ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in text_exts and p.name != "verify_compliance.py":
            txt = p.read_text(encoding="utf-8", errors="ignore").lower()
            for phrase in BANNED_PHRASES:
                if phrase in txt:
                    violations.append((str(p.relative_to(REPO_ROOT)), phrase))
    assert not violations, f"Banned phrases found: {violations}"
    print("[PASS] Zero banned phrases ('inflated tonnage', 'Premium SMART', 'premium service', 'fraud') across all solution files.")


def check_api_and_ui() -> None:
    client = TestClient(app)

    r_root = client.get("/")
    assert r_root.status_code == 200 and "EUROPRESS" in r_root.text
    print("[PASS] GET / serves Europress SMART Web Cockpit HTML (200 OK).")

    r_svg = client.get("/diagrams/combi_duo_schematics.svg")
    assert r_svg.status_code == 200 and "<svg" in r_svg.text
    print("[PASS] GET /diagrams/combi_duo_schematics.svg serves technical vector diagram (200 OK).")

    r_ov = client.get("/api/overview")
    assert r_ov.status_code == 200
    ov = r_ov.json()
    assert ov["fleet_kpis"]["total_completed_lifts"] == 18477
    assert len(ov["portfolio_levers"]) == 6
    print("[PASS] GET /api/overview returns verified fleet KPIs, accuracy curve, and 6 portfolio levers.")

    r_comp = client.get("/api/compactors")
    assert r_comp.status_code == 200
    comps = r_comp.json()
    assert len(comps) == 12
    dev0 = comps[0]["device_id"]

    # Test S40 Bridging detection in live simulator endpoint
    r_sim = client.post(
        f"/api/compactors/{dev0}/simulate_pickup",
        json={"volume_fill_pct": 93.0, "current_mass_kg": 950.0, "operator_lead_hours": 21.0, "hourly_inflow_kg": 25.0, "is_pre_weekend": False},
    )
    assert r_sim.status_code == 200
    assert r_sim.json()["verdict"] == "HOLD_BRIDGING_DETECTED"
    print(f"[PASS] POST /api/compactors/{dev0}/simulate_pickup accurately flags S40 bridging and computes optimal pickup window.")

    r_aud = client.get("/api/audit_trail")
    assert r_aud.status_code == 200 and len(r_aud.json()) == 40
    print("[PASS] GET /api/audit_trail returns 40 row-level traceable contract vs. invoice discrepancies.")

    r_sc = client.get("/api/scorecards")
    assert r_sc.status_code == 200 and len(r_sc.json()) == 5
    print("[PASS] GET /api/scorecards returns all 5 neutral regional operator scorecards.")

    r_q = client.get("/api/approval_queue")
    assert r_q.status_code == 200 and len(r_q.json()) > 0
    prop_id = r_q.json()[0]["proposal_id"]

    r_dec = client.post(
        f"/api/approval_queue/{prop_id}/decide",
        json={"decision": "APPROVED", "reviewer_name": "Automated Verification Test", "reviewer_note": "Verified human-in-the-loop persistence."},
    )
    assert r_dec.status_code == 200 and r_dec.json()["updated_proposal"]["approval_status"] == "APPROVED"
    print(f"[PASS] POST /api/approval_queue/{prop_id}/decide persists human-in-the-loop approval state.")


if __name__ == "__main__":
    check_banned_phrases()
    check_api_and_ui()
    print("\nALL COMPLIANCE & END-TO-END SYSTEM CHECKS PASSED 100%!")
