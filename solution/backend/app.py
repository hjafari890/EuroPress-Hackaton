"""FastAPI Backend for Europress SMART Material Value Engine Cockpit."""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

HERE = Path(__file__).resolve().parent
SOLUTION_ROOT = HERE.parent
ENGINE_DIR = SOLUTION_ROOT / "engine"
DATA_DIR = HERE / "data"
DIAGRAMS_DIR = SOLUTION_ROOT / "frontend" / "public" / "diagrams"

if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

app = FastAPI(
    title="Europress SMART Material Value Engine API",
    description="Source-weight optimization, Day-0 weight ledger, row-level contract/invoice audit, and human-approved decision engine.",
    version="1.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if DIAGRAMS_DIR.exists():
    app.mount("/diagrams", StaticFiles(directory=str(DIAGRAMS_DIR)), name="diagrams")

_BUNDLE_CACHE: dict | None = None
_BENCH_CACHE: dict | None = None
AUDIT_LOG_PATH = DATA_DIR / "approval_audit_log.json"


def sanitize_json(obj):
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif isinstance(obj, dict):
        return {k: sanitize_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_json(v) for v in obj]
    return obj


def get_bundle() -> dict:
    global _BUNDLE_CACHE
    if _BUNDLE_CACHE is None:
        bundle_path = DATA_DIR / "cockpit_bundle.json"
        if not bundle_path.exists():
            from export_cockpit_data import build_cockpit_bundle
            _BUNDLE_CACHE = sanitize_json(build_cockpit_bundle())
        else:
            _BUNDLE_CACHE = sanitize_json(json.loads(bundle_path.read_text(encoding="utf-8")))
    return _BUNDLE_CACHE


def get_benchmarks() -> dict:
    global _BENCH_CACHE
    if _BENCH_CACHE is None:
        bench_path = DATA_DIR / "benchmark_scores.json"
        if bench_path.exists():
            _BENCH_CACHE = sanitize_json(json.loads(bench_path.read_text(encoding="utf-8")))
        else:
            _BENCH_CACHE = sanitize_json({"scores": {}, "true_fullness_summary": get_bundle().get("fleet_kpis", {})})
    return _BENCH_CACHE


class PickupSimulationRequest(BaseModel):
    volume_fill_pct: float
    current_mass_kg: float
    operator_lead_hours: float = 21.0
    hourly_inflow_kg: float = 28.0
    is_pre_weekend: bool = False


class ApprovalDecisionRequest(BaseModel):
    decision: Literal["APPROVED", "DEFERRED", "REVERSED"]
    reviewer_name: str = "Site Logistics Manager"
    reviewer_note: str = "Verified against source-weight ledger and contract tariff."


@app.get("/api/overview")
def api_overview():
    b = get_bundle()
    bm = get_benchmarks()
    return {
        "metadata": b["metadata"],
        "fleet_kpis": b["fleet_kpis"],
        "accuracy_curve": b["accuracy_curve"],
        "portfolio_levers": b["portfolio_levers"],
        "business_scenarios": b["business_scenarios"],
        "compactors": b.get("compactors", []),
        "audit_trail": b.get("audit_trail_rows", []),
        "scorecards": b.get("operator_scorecards", []),
        "approval_queue": b.get("approval_queue", []),
        "summary": bm.get("true_fullness_summary", b.get("fleet_kpis", {})),
        "benchmark_scores": bm.get("scores", {}),
    }


@app.get("/api/compactors")
def api_compactors():
    return get_bundle()["compactors"]


@app.post("/api/compactors/{device_id}/simulate_pickup")
def simulate_pickup(device_id: str, req: PickupSimulationRequest | None = None):
    b = get_bundle()
    comp = next((c for c in b["compactors"] if c["device_id"] == device_id), None)
    if not comp:
        raise HTTPException(status_code=404, detail=f"Device {device_id} not found")

    if req is None:
        req = PickupSimulationRequest(
            volume_fill_pct=float(comp.get("current_fill_pct", 88.0)),
            current_mass_kg=float(comp.get("current_mass_kg", 1850.0)),
        )

    vol_m3 = float(comp["container_volume_m3"])
    live = comp.get("live_state", {})
    nom_rho = float(live.get("nominal_density_kg_m3", 160.0))
    target_kg = float(live.get("target_payload_kg", 3000.0))

    occ_vol = max(0.4, vol_m3 * (max(5.0, req.volume_fill_pct) / 100.0))
    eff_rho = round(req.current_mass_kg / occ_vol, 1)
    rho_ratio = eff_rho / max(nom_rho, 1.0)
    true_weight_fill_pct = round(100.0 * req.current_mass_kg / max(target_kg, 1.0), 1)
    remaining_kg = max(0.0, target_kg * 0.96 - req.current_mass_kg)
    hours_to_96pct = round(remaining_kg / max(req.hourly_inflow_kg, 1.0), 1)
    optimal_order_in_hours = round(max(0.0, hours_to_96pct - req.operator_lead_hours), 1)
    avoided_haul_eur = round(195.0 * max(0.0, 1.0 - true_weight_fill_pct / 92.0), 0)

    if req.volume_fill_pct >= 82.0 and rho_ratio < 0.48 and true_weight_fill_pct < 55.0:
        verdict = "HOLD_BRIDGING_DETECTED"
        headline = "DO NOT CALL HAULER — Cardboard/Material Bridging Detected (Scenario S40)"
        explanation = (
            f"Volume sensor reads {req.volume_fill_pct:.0f}% FULL, but source weight is only {req.current_mass_kg:.0f} kg "
            f"(effective density {eff_rho} kg/m³ vs nominal {nom_rho:.0f} kg/m³). "
            f"Recommend triggering an automated high-pressure anti-bridging crush stroke and waiting {optimal_order_in_hours:.0f}h "
            f"before ordering pickup. Avoids €{avoided_haul_eur:.0f} wasted haulage."
        )
    elif req.is_pre_weekend and true_weight_fill_pct < 68.0 and hours_to_96pct > 54.0:
        verdict = "HOLD_SAFE_OVER_WEEKEND"
        headline = "SAFE TO WAIT THROUGH WEEKEND — Skip Precautionary Order (Scenario S39)"
        explanation = (
            f"True payload is {req.current_mass_kg:.0f} kg ({true_weight_fill_pct:.1f}% of {target_kg:.0f} kg target). "
            f"At {req.hourly_inflow_kg:.0f} kg/h inflow, container has {hours_to_96pct:.0f}h of safe capacity remaining (> weekend window). "
            f"Schedule order in {optimal_order_in_hours:.0f}h so truck arrives at 96% target mass. Saves €{avoided_haul_eur:.0f}."
        )
    elif optimal_order_in_hours <= 2.0 or true_weight_fill_pct >= 88.0:
        verdict = "ORDER_PICKUP_NOW"
        headline = "OPTIMAL PAYLOAD WINDOW REACHED — Place Pickup Order Now"
        explanation = (
            f"Current weight is {req.current_mass_kg:.0f} kg ({true_weight_fill_pct:.1f}% of target). "
            f"With operator median lead time of {req.operator_lead_hours:.0f}h and {req.hourly_inflow_kg:.0f} kg/h fill rate, "
            f"ordering now ensures the truck lifts at ~96% maximum commercial payload without overflow."
        )
    else:
        verdict = "CONTINUE_COMPACTING"
        headline = f"WAIT {optimal_order_in_hours:.0f} HOURS — Container Still Has {remaining_kg:.0f} kg Capacity"
        explanation = (
            f"True commercial fullness is {true_weight_fill_pct:.1f}% ({req.current_mass_kg:.0f} / {target_kg:.0f} kg). "
            f"Next optimal order trigger in {optimal_order_in_hours:.0f}h (accounting for {req.operator_lead_hours:.0f}h operator lead time)."
        )

    return {
        "device_id": device_id,
        "verdict": verdict,
        "headline": headline,
        "explanation": explanation,
        "effective_density_kg_m3": eff_rho,
        "nominal_density_kg_m3": nom_rho,
        "true_weight_fill_pct": true_weight_fill_pct,
        "remaining_capacity_kg": round(remaining_kg, 0),
        "hours_to_target_mass": hours_to_96pct,
        "optimal_order_in_hours": optimal_order_in_hours,
        "avoided_premature_cost_eur": avoided_haul_eur,
    }


@app.get("/api/audit_trail")
def api_audit_trail():
    return get_bundle()["audit_trail_rows"]


@app.get("/api/scorecards")
def api_scorecards():
    return get_bundle()["operator_scorecards"]


@app.get("/api/approval_queue")
def api_approval_queue():
    q = get_bundle()["approval_queue"]
    if AUDIT_LOG_PATH.exists():
        logs = json.loads(AUDIT_LOG_PATH.read_text(encoding="utf-8"))
        by_id = {entry["proposal_id"]: entry for entry in logs}
        for item in q:
            if item["proposal_id"] in by_id:
                item["approval_status"] = by_id[item["proposal_id"]]["decision"]
                item["last_decision"] = by_id[item["proposal_id"]]
    return q


@app.post("/api/approval_queue/{proposal_id}/decide")
@app.post("/api/approval_queue/{proposal_id}/approve")
def decide_proposal(proposal_id: str, req: ApprovalDecisionRequest | None = None):
    if req is None:
        req = ApprovalDecisionRequest(decision="APPROVED")
    q = get_bundle()["approval_queue"]
    item = next((x for x in q if x["proposal_id"] == proposal_id), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found")

    entry = {
        "proposal_id": proposal_id,
        "contract_id": item["contract_id"],
        "customer_name": item["customer_name"],
        "recommended_actions": item["recommended_actions"],
        "decision": req.decision,
        "reviewer_name": req.reviewer_name,
        "reviewer_note": req.reviewer_note,
        "decided_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    logs = []
    if AUDIT_LOG_PATH.exists():
        logs = json.loads(AUDIT_LOG_PATH.read_text(encoding="utf-8"))
    logs.append(entry)
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_LOG_PATH.write_text(json.dumps(logs, indent=2), encoding="utf-8")
    item["approval_status"] = req.decision
    item["last_decision"] = entry
    return {"status": "ok", "updated_proposal": item, "audit_log_count": len(logs)}


FRONTEND_DIST = SOLUTION_ROOT / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")
elif (SOLUTION_ROOT / "frontend").exists():
    app.mount("/", StaticFiles(directory=str(SOLUTION_ROOT / "frontend"), html=True), name="frontend")

