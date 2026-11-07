"""Run the upgraded Europress SMART Material Value Engine on the competition dataset,
score every task with the official `europress_data.evaluate` harness, compare against
Baselines B1-B6, and export rich cockpit JSON artifacts for the FastAPI + React UI.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
STARTER_ROOT = (
    REPO_ROOT
    / "provided data from company"
    / "Europress_SMART_Material_Value_Engine_v1.0.1_PARTICIPANTS (3)"
    / "Europress_SMART_Material_Value_Engine_v1.0.1"
)
for p in (HERE, STARTER_ROOT / "src", STARTER_ROOT / "baselines"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from b1_economic_calculator import compute as b1_compute  # noqa: E402
from b2_rules_anomaly import run as b2_run  # noqa: E402
from b3_next_best_action import case_features as b3_features, decide as b3_decide  # noqa: E402
from b5_operator_scorecard import scorecard as b5_scorecard  # noqa: E402
from b6_operator_actions import decide as b6_decide  # noqa: E402
from europress_data.evaluate import score_a, score_b, score_b2, score_c, score_c2  # noqa: E402
from smart_value_engine import (  # noqa: E402
    compute_true_fullness_and_pickup_forecast,
    detect_invoice_anomalies,
    solve_task_a,
    solve_task_b,
    solve_task_b2,
    solve_task_c,
    solve_task_c2,
)


def main():
    t0 = time.time()
    pub = STARTER_ROOT / "data" / "competition" / "public"
    lab_dir = pub / "labels_dev"

    print("1. Running Official Baselines vs. Upgraded SMART Value Engine on [competition]...")
    b1_base, _ = b1_compute(pub)
    b2_base, _, _ = b2_run(pub)
    cases_c = pd.read_parquet(pub / "benchmark" / "decision_cases.parquet")
    b3_base = b3_decide(b3_features(pub, cases_c, None))
    b5_base = b5_scorecard(pub)
    b6_base = b6_decide(pub)

    our_a, our_a_lines = solve_task_a(pub)
    our_b, f_enriched, _ = solve_task_b(pub, our_a, our_a_lines)
    our_b2 = solve_task_b2(pub, our_a, our_a_lines)
    our_c = solve_task_c(pub, our_a, our_a_lines)
    inv_flags = detect_invoice_anomalies(pub, our_a, our_a_lines)
    our_c2 = solve_task_c2(pub, our_a, our_a_lines, inv_flags)

    scores = {
        "task_a": {
            "baseline_b1": score_a(b1_base, lab_dir, "validation"),
            "smart_value_engine": score_a(our_a, lab_dir, "validation"),
        },
        "task_b": {
            "baseline_b2": score_b(b2_base, lab_dir, "validation"),
            "smart_value_engine": score_b(our_b, lab_dir, "validation"),
        },
        "task_b2": {
            "baseline_b5": score_b2(b5_base, lab_dir, "all"),
            "smart_value_engine": score_b2(our_b2, lab_dir, "all"),
        },
        "task_c": {
            "baseline_b3": score_c(b3_base, lab_dir, "validation"),
            "smart_value_engine": score_c(our_c, lab_dir, "validation"),
        },
        "task_c2": {
            "baseline_b6": score_c2(b6_base, lab_dir, "dev"),
            "smart_value_engine": score_c2(our_c2, lab_dir, "dev"),
        },
    }

    print("\n=== BENCHMARK SCORES (COMPETITION VALIDATION / DEV SPLIT) ===")
    print(f"Task A  | Net Exact-to-Cent: B1={scores['task_a']['baseline_b1']['net_material_contribution_eur:exact_to_cent_share']:.4f} -> Ours={scores['task_a']['smart_value_engine']['net_material_contribution_eur:exact_to_cent_share']:.4f} | Fabricated €/t: B1={scores['task_a']['baseline_b1']['per_t:fabricated_where_reference_null']} -> Ours={scores['task_a']['smart_value_engine']['per_t:fabricated_where_reference_null']}")
    sb_base = scores["task_b"]["baseline_b2"]
    sb_ours = scores["task_b"]["smart_value_engine"]
    fp_base = sum(v["explained_flagged_as_anomaly"] for k, v in sb_base.items() if isinstance(v, dict))
    fp_ours = sum(v["explained_flagged_as_anomaly"] for k, v in sb_ours.items() if isinstance(v, dict))
    print(f"Task B  | Macro-F1: B2={sb_base['macro_f1']:.4f} -> Ours={sb_ours['macro_f1']:.4f} | False-Positive Traps Flagged: B2={fp_base} -> Ours={fp_ours}")
    print(f"        | PREMATURE_UNJUSTIFIED F1: B2={sb_base['PREMATURE_UNJUSTIFIED']['f1']:.4f} -> Ours={sb_ours['PREMATURE_UNJUSTIFIED']['f1']:.4f}")
    print(f"        | COST_PER_T_HIGH F1:       B2={sb_base['COST_PER_T_HIGH']['f1']:.4f} (FP={sb_base['COST_PER_T_HIGH']['explained_flagged_as_anomaly']}) -> Ours={sb_ours['COST_PER_T_HIGH']['f1']:.4f} (FP={sb_ours['COST_PER_T_HIGH']['explained_flagged_as_anomaly']})")
    print(f"        | CONTAMINATION_LOSS F1:    B2={sb_base['CONTAMINATION_VALUE_LOSS']['f1']:.4f} -> Ours={sb_ours['CONTAMINATION_VALUE_LOSS']['f1']:.4f}")
    print(f"        | WEIGHT_DISCREPANCY F1:    B2={sb_base['WEIGHT_DISCREPANCY']['f1']:.4f} (FP={sb_base['WEIGHT_DISCREPANCY']['explained_flagged_as_anomaly']}) -> Ours={sb_ours['WEIGHT_DISCREPANCY']['f1']:.4f} (FP={sb_ours['WEIGHT_DISCREPANCY']['explained_flagged_as_anomaly']})")
    print(f"Task B2 | Scorecard (0-100): B5={scores['task_b2']['baseline_b5']['scorecard_score_0_100']:.2f} -> Ours={scores['task_b2']['smart_value_engine']['scorecard_score_0_100']:.2f}")
    print(f"        | Weight Bias Score: B5={scores['task_b2']['baseline_b5']['weight_bias_pct:score']:.4f} -> Ours={scores['task_b2']['smart_value_engine']['weight_bias_pct:score']:.4f}")
    print(f"        | Billing Over/Under/Disc: B5=({scores['task_b2']['baseline_b5']['billing_overcharge_pct:score']:.3f}, {scores['task_b2']['baseline_b5']['billing_undercharge_pct:score']:.3f}, {scores['task_b2']['baseline_b5']['discrepant_line_rate:score']:.3f}) -> Ours=({scores['task_b2']['smart_value_engine']['billing_overcharge_pct:score']:.3f}, {scores['task_b2']['smart_value_engine']['billing_undercharge_pct:score']:.3f}, {scores['task_b2']['smart_value_engine']['discrepant_line_rate:score']:.3f})")
    print(f"Task C  | Acceptable Share: B3={scores['task_c']['baseline_b3']['acceptable_share']:.4f} -> Ours={scores['task_c']['smart_value_engine']['acceptable_share']:.4f} | Mean Regret: B3={scores['task_c']['baseline_b3']['mean_regret_eur']:.2f} -> Ours={scores['task_c']['smart_value_engine']['mean_regret_eur']:.2f} EUR | Impermissible: B3={scores['task_c']['baseline_b3']['impermissible_share']:.4f} -> Ours={scores['task_c']['smart_value_engine']['impermissible_share']:.4f}")
    print(f"Task C2 | Mean Regret EUR: B6={scores['task_c2']['baseline_b6']['mean_regret_eur']:.2f} -> Ours={scores['task_c2']['smart_value_engine']['mean_regret_eur']:.2f} | Value Capture Share: B6={scores['task_c2']['baseline_b6']['value_capture_share']:.4f} -> Ours={scores['task_c2']['smart_value_engine']['value_capture_share']:.4f}")

    tf = compute_true_fullness_and_pickup_forecast(pub, f_enriched, our_a)
    print("\n=== TRUE-FULLNESS & 30-DAY OPERATOR LAG SUMMARY ===")
    print(json.dumps(tf["summary"], indent=2))

    out_dir = REPO_ROOT / "solution" / "backend" / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "benchmark_scores.json", "w", encoding="utf-8") as fp:
        json.dump({"scores": scores, "true_fullness_summary": tf["summary"]}, fp, indent=2)

    # Save predictions CSVs for reproducibility
    pred_dir = REPO_ROOT / "solution" / "predictions"
    pred_dir.mkdir(parents=True, exist_ok=True)
    our_a.to_csv(pred_dir / "task_a_predictions.csv", index=False)
    our_b.to_csv(pred_dir / "task_b_predictions.csv", index=False)
    our_b2.to_csv(pred_dir / "task_b2_scorecard.csv", index=False)
    our_c.to_csv(pred_dir / "task_c_decisions.csv", index=False)
    our_c2.to_csv(pred_dir / "task_c2_actions.csv", index=False)
    print(f"\nCompleted in {time.time() - t0:.1f}s. Predictions written to {pred_dir}")


if __name__ == "__main__":
    main()
