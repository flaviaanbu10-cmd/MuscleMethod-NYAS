
"""MuscleMethod compensation challenge.
All scenarios are simulated.
Expected answers are design assumptions, not clinical labels.
"""

import csv
from pathlib import Path
from model import predict


BASE = {
    "eeg_intent": 0.83,
    "emg_target": 0.27,
    "coactivation": 0.22,
    "fatigue": 0.25,
    "imu_motion": 0.28,
    "imu_smoothness": 0.47
}


def case(
    name,
    changes=None,
    decision="Assist More",
    quality=0.92,
    stop=False
):
    signals = BASE.copy()
    signals.update(changes or {})

    return {
        "name": name,
        "signals": signals,
        "quality": quality,
        "stop": stop,
        "expected_decision": decision
    }


# Simulated testing scenarios
TESTS = [
    case("Standard assisted attempt"),

    case(
        "High intent weak execution high coactivation",
        {
            "eeg_intent": 0.88,
            "emg_target": 0.20,
            "coactivation": 0.80,
            "fatigue": 0.15,
            "imu_motion": 0.18,
            "imu_smoothness": 0.18
        },
        "Pattern Review Recommended",
        0.90
    ),

    case(
        "Weak execution low coactivation",
        {
            "eeg_intent": 0.88,
            "emg_target": 0.20,
            "coactivation": 0.18,
            "fatigue": 0.15,
            "imu_motion": 0.18,
            "imu_smoothness": 0.18
        }
    ),

    case(
        "High coactivation good execution",
        {
            "eeg_intent": 0.85,
            "emg_target": 0.78,
            "coactivation": 0.80,
            "fatigue": 0.18,
            "imu_motion": 0.76,
            "imu_smoothness": 0.80
        },
        "Assist Less",
        0.90
    ),

    case(
        "Borderline coactivation",
        {
            "eeg_intent": 0.88,
            "emg_target": 0.20,
            "coactivation": 0.63,
            "fatigue": 0.15,
            "imu_motion": 0.18,
            "imu_smoothness": 0.18
        }
    ),

    case(
        "Borderline mismatch",
        {
            "eeg_intent": 0.78,
            "emg_target": 0.30,
            "coactivation": 0.78,
            "fatigue": 0.20,
            "imu_motion": 0.29,
            "imu_smoothness": 0.30
        }
    ),

    case(
        "Poor signal quality",
        quality=0.20,
        decision="Unclear — Review Signals"
    ),

    case(
        "Emergency stop",
        stop=True,
        decision="Stop / No Automatic Assistance"
    ),

    case(
        "Fatigue dominant",
        {
            "eeg_intent": 0.61,
            "emg_target": 0.32,
            "coactivation": 0.30,
            "fatigue": 0.90,
            "imu_motion": 0.35,
            "imu_smoothness": 0.39
        },
        decision="Rest",
        quality=0.90
    ),

    case(
        "Near zero execution high coactivation",
        {
            "eeg_intent": 0.98,
            "emg_target": 0.15,
            "coactivation": 0.92,
            "fatigue": 0.18,
            "imu_motion": 0.10,
            "imu_smoothness": 0.10
        },
        decision="Pattern Review Recommended",
        quality=0.90
    )
]


# Run experiments
rows = []

for test in TESTS:

    payload = {
        "signals": test["signals"],
        "signal_quality": test["quality"],
        "emergency_stop": test["stop"],
        "sensors_connected": True,
        "force_within_limit": True,
        "movement_within_limit": True
    }

    result = predict(payload)

    matches = (
        result["decision"] == test["expected_decision"]
    )

    rows.append({
        "scenario": test["name"],
        "expected_decision": test["expected_decision"],
        "actual_decision": result["decision"],
        "matches_expected_decision": int(matches),
        "model_prediction": result["model_prediction"],
        "vote_agreement": result["vote_confidence"],
        "mismatch": result["intent_execution_gap"],
        "review_flag": int(result["review_flag"]),
        "increase_requested": int(
            result["assistance_increase_requested"]
        ),
        "increase_allowed": int(
            result["assistance_increase_allowed"]
        ),
        "safety_state": result["safety_state"],
        "warnings": "; ".join(result["safety_reasons"]),
        "explanation": result["movement_explanation"]
    })

    status = "MATCH" if matches else "REVIEW"

    print(
        f"{status}: {test['name']}: "
        f"{result['decision']} "
        f"(expected: {test['expected_decision']})"
    )


# Automatically save CSV
output = (
    Path(__file__).resolve().parent
    / "compensation_challenge_results.csv"
)

with output.open(
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=list(rows[0].keys())
    )

    writer.writeheader()
    writer.writerows(rows)


correct = sum(
    row["matches_expected_decision"]
    for row in rows
)

print()
print("COMPENSATION CHALLENGE COMPLETE")
print("Matched scenario expectations:", correct, "/", len(rows))
print("Cases requiring review:", len(rows) - correct)
print("Not a clinical accuracy measurement.")
print("CSV saved:", output)
