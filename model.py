
"""MuscleMethod educational AI prototype.
Uses synthetic examples, not real patient recordings.
Not a medical device or physical glove controller.
"""

import csv
import math
import random
from collections import Counter
from pathlib import Path


LABELS = [
    "Assist More",
    "Assist Less",
    "Rest",
    "Pattern Review Recommended",
    "No Action"
]

FIELDS = [
    "eeg_intent",
    "emg_target",
    "coactivation",
    "fatigue",
    "imu_motion",
    "imu_smoothness"
]

# Simulated rehabilitation scenarios
CENTERS = {
    "Assist More": [0.83, 0.27, 0.22, 0.25, 0.28, 0.47],
    "Assist Less": [0.85, 0.79, 0.18, 0.18, 0.80, 0.82],
    "Rest": [0.61, 0.32, 0.34, 0.88, 0.35, 0.39],
    "Pattern Review Recommended": [0.83, 0.72, 0.83, 0.24, 0.45, 0.28],
    "No Action": [0.14, 0.15, 0.16, 0.14, 0.12, 0.50]
}

SEED = 20261115


def clip(value):
    return round(max(0.0, min(1.0, value)), 4)


# Create simulated differences between patients
def make_patient(rng, name):
    return {
        "id": name,
        "baseline": {
            "emg_target": round(rng.uniform(0.07, 0.25), 4),
            "imu_motion": round(rng.uniform(0.04, 0.17), 4)
        },
        "gain": {
            "emg_target": round(rng.uniform(0.58, 1.13), 4),
            "imu_motion": round(rng.uniform(0.65, 1.12), 4)
        },
        "coactivation_bias": round(rng.uniform(-0.13, 0.15), 4),
        "intent_bias": round(rng.uniform(-0.08, 0.08), 4)
    }


# Generate synthetic sensor data
def sample(rng, label, patient, noise=0.095):
    base = CENTERS[label]

    values = {}

    for key, center in zip(FIELDS, base):
        values[key] = clip(center + rng.gauss(0, noise))

    values["emg_target"] = clip(
        patient["baseline"]["emg_target"]
        + patient["gain"]["emg_target"] * values["emg_target"]
    )

    values["imu_motion"] = clip(
        patient["baseline"]["imu_motion"]
        + patient["gain"]["imu_motion"] * values["imu_motion"]
    )

    values["coactivation"] = clip(
        values["coactivation"] + patient["coactivation_bias"]
    )

    values["eeg_intent"] = clip(
        values["eeg_intent"] + patient["intent_bias"]
    )

    return values


# Normalize values using a simulated patient baseline
def normalize(values, patient):
    normalized = dict(values)

    for key in ["emg_target", "imu_motion"]:
        normalized[key] = clip(
            (values[key] - patient["baseline"][key])
            / patient["gain"][key]
        )

    normalized["coactivation"] = clip(
        values["coactivation"] - patient["coactivation_bias"]
    )

    normalized["eeg_intent"] = clip(
        values["eeg_intent"] - patient["intent_bias"]
    )

    # Experimental intent-execution mismatch
    normalized["intent_execution_gap"] = clip(
        max(
            0,
            normalized["eeg_intent"]
            - (
                normalized["emg_target"]
                + normalized["imu_motion"]
            ) / 2
        )
    )

    return normalized


# K-nearest neighbors classification model
class KNN:

    def __init__(self, feature_names):
        self.feature_names = feature_names
        self.examples = []

    def fit(self, rows):
        self.examples = [
            (
                [row["values"][key] for key in self.feature_names],
                row["label"]
            )
            for row in rows
        ]

        return self

    def predict(self, values, k=9):
        vector = [
            values[key] for key in self.feature_names
        ]

        neighbors = sorted(
            (
                (math.dist(vector, x), label)
                for x, label in self.examples
            ),
            key=lambda pair: pair[0]
        )[:k]

        weights = {
            name: 0.0 for name in LABELS
        }

        for distance, label in neighbors:
            weights[label] += 1 / (distance + 0.06)

        best = max(
            LABELS,
            key=lambda label: weights[label]
        )

        confidence = weights[best] / sum(weights.values())

        return best, round(confidence, 3)


# Create training and test datasets
def build_dataset(
    train_patients=35,
    test_patients=12,
    examples_per_label=12,
    noise=0.18
):
    rng = random.Random(SEED)

    training = []
    testing = []

    patients = [
        make_patient(rng, f"SIM-{i:03d}")
        for i in range(train_patients + test_patients)
    ]

    for index, patient in enumerate(patients):

        if index < train_patients:
            destination = training
        else:
            destination = testing

        for label in LABELS:
            for j in range(examples_per_label):
                raw = sample(rng, label, patient, noise)

                destination.append({
                    "patient": patient,
                    "values": normalize(raw, patient),
                    "raw": raw,
                    "label": label
                })

    rng.shuffle(training)
    rng.shuffle(testing)

    return training, testing


FEATURES_BASIC = ["eeg_intent"]

FEATURES_FUSED = [
    "eeg_intent",
    "emg_target",
    "coactivation",
    "fatigue",
    "imu_motion",
    "imu_smoothness"
]

FEATURES_PERSONAL = FEATURES_FUSED + [
    "intent_execution_gap"
]


# Train the classifier
def create_model():
    training, testing = build_dataset()

    model = KNN(FEATURES_PERSONAL)
    model.fit(training)

    return model, training, testing


MODEL, TRAIN, TEST = create_model()


# AI prediction and separate safety checks
def predict(payload):

    inputs = payload.get("signals", {})

    if not isinstance(inputs, dict):
        raise ValueError("signals must be an object")

    raw = {}

    for key in FIELDS:
        value = inputs.get(key)

        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or not 0 <= value <= 1
        ):
            raise ValueError(
                f"{key} must be a number from 0 to 1"
            )

        raw[key] = float(value)

    calibration = payload.get("calibration")

    if calibration is None:
        calibration = {
            "id": "DEMO_DEFAULT",
            "baseline": {
                "emg_target": 0.15,
                "imu_motion": 0.10
            },
            "gain": {
                "emg_target": 0.85,
                "imu_motion": 0.90
            },
            "coactivation_bias": 0,
            "intent_bias": 0
        }

    normalized = normalize(raw, calibration)

    label, confidence = MODEL.predict(normalized)

    quality = float(payload.get("signal_quality", 1.0))

    if not math.isfinite(quality) or not 0 <= quality <= 1:
        raise ValueError("signal_quality must be 0 to 1")

    connected = payload.get("sensors_connected", True)
    stop = payload.get("emergency_stop", False)
    force_ok = payload.get("force_within_limit", True)
    movement_ok = payload.get("movement_within_limit", True)

    if not all(
        isinstance(value, bool)
        for value in [connected, stop, force_ok, movement_ok]
    ):
        raise ValueError("Safety flags must be booleans")

    reasons = []

    if stop:
        reasons.append("Emergency stop enabled")

    if not connected:
        reasons.append("Sensor disconnected")

    if not force_ok:
        reasons.append("Force limit exceeded")

    if not movement_ok:
        reasons.append("Movement limit reached")

    if quality < 0.55:
        reasons.append("Poor signal quality")

    if confidence < 0.62:
        reasons.append("Uncertain model prediction")

    # Compensation-related pattern review
    # Weak movement alone does not prove compensation.
    mismatch = round(
        normalized["intent_execution_gap"], 3
    )

    possible_atypical_pattern = (
        mismatch >= 0.75
        and normalized["coactivation"] >= 0.70
        and normalized["imu_smoothness"] <= 0.35
    )

    if possible_atypical_pattern:
        reasons.append(
            "Possible atypical activation/movement pattern; "
            "therapist review suggested"
        )

    # Safety gate
    hard_stop = (
        stop
        or not connected
        or not force_ok
        or not movement_ok
    )

    low_quality = quality < 0.55
    low_agreement = confidence < 0.62

    if hard_stop:
        display = "Stop / No Automatic Assistance"

    elif low_quality or low_agreement:
        display = "Unclear — Review Signals"

    elif possible_atypical_pattern:
        display = "Pattern Review Recommended"

    else:
        display = label

    increase_requested = label == "Assist More"

    review_or_safety_block = (
        hard_stop
        or low_quality
        or low_agreement
        or possible_atypical_pattern
    )

    allow_increase = (
        increase_requested
        and not review_or_safety_block
    )

    if review_or_safety_block:
        safety_state = "BLOCKED"

        if increase_requested:
            assistance_status = "BLOCKED"
        else:
            assistance_status = (
                "NO INCREASE REQUESTED; RESTRICTION ACTIVE"
            )

    elif increase_requested:
        safety_state = "PERMITTED FOR SIMULATION ONLY"
        assistance_status = "PERMITTED IN SIMULATION ONLY"

    else:
        safety_state = "NO INCREASE REQUESTED"
        assistance_status = "NOT APPLICABLE"

    # Explain the movement pattern
    if possible_atypical_pattern:
        movement_explanation = (
            "Strong mismatch, co-activation and reduced "
            "smoothness together warrant review in "
            "this demonstration."
        )

    elif (
        mismatch >= 0.75
        and normalized["coactivation"] < 0.70
    ):
        movement_explanation = (
            "Weak execution relative to intent; "
            "without additional movement evidence "
            "this is not a compensation flag."
        )

    elif (
        normalized["coactivation"] >= 0.70
        and mismatch < 0.75
    ):
        movement_explanation = (
            "Co-activation alone is insufficient "
            "for a compensation flag."
        )

    else:
        movement_explanation = (
            "No combined atypical-pattern threshold "
            "triggered; this does not establish "
            "normal movement."
        )

    return {
        "decision": display,
        "model_prediction": label,
        "vote_confidence": confidence,
        "confidence_note": (
            "Weighted neighbor-vote agreement, "
            "not calibrated probability"
        ),
        "intent_execution_gap": mismatch,
        "assistance_increase_allowed": allow_increase,
        "assistance_increase_requested": increase_requested,
        "assistance_status": assistance_status,
        "safety_state": safety_state,
        "safety_reasons": reasons,
        "review_flag": possible_atypical_pattern,
        "movement_explanation": movement_explanation,
        "evidence": {
            "normalized_intent": normalized["eeg_intent"],
            "normalized_target_muscle": normalized["emg_target"],
            "normalized_movement": normalized["imu_motion"],
            "fatigue": normalized["fatigue"],
            "coactivation": normalized["coactivation"],
            "smoothness": normalized["imu_smoothness"]
        },
        "disclaimer": (
            "Synthetic educational demonstration; "
            "no diagnosis, real sensors, "
            "or physical glove control."
        )
    }


# Compare AI model performance
def evaluate():

    variants = {
        "EEG only (normalized)": FEATURES_BASIC,
        "Combined features (normalized)": FEATURES_FUSED,
        "Combined + mismatch (normalized)": FEATURES_PERSONAL
    }

    results = []

    for name, features in variants.items():

        model = KNN(features).fit(TRAIN)
        correct = 0

        for row in TEST:
            label, confidence = model.predict(row["values"])

            if label == row["label"]:
                correct += 1

        results.append({
            "experiment": name,
            "correct": correct,
            "total": len(TEST),
            "accuracy": round(correct / len(TEST), 4)
        })

    # Additional synthetic noise testing
    for noise in [0.24, 0.30]:

        _, difficult = build_dataset(noise=noise)

        for name, features in variants.items():

            model = KNN(features).fit(TRAIN)

            correct = sum(
                model.predict(row["values"])[0] == row["label"]
                for row in difficult
            )

            results.append({
                "experiment": f"{name} / noisy stress {noise}",
                "correct": correct,
                "total": len(difficult),
                "accuracy": round(correct / len(difficult), 4)
            })

    return results


# Generate CSV files when executed
if __name__ == "__main__":

    folder = Path(__file__).resolve().parent

    results = evaluate()

    print("MuscleMethod V4 — Synthetic AI Experiment")
    print("Training:", len(TRAIN))
    print("Testing:", len(TEST))

    for result in results:
        print(
            f"{result['experiment']}: "
            f"{result['correct']}/{result['total']} = "
            f"{result['accuracy']:.1%}"
        )

    with (folder / "evaluation.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "experiment",
                "correct",
                "total",
                "accuracy"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    with (folder / "test_predictions.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "simulated_patient_id",
            "reference_scenario",
            "predicted_scenario",
            "vote_confidence",
            *FIELDS
        ])

        for row in TEST:
            label, confidence = MODEL.predict(row["values"])

            writer.writerow([
                row["patient"]["id"],
                row["label"],
                label,
                confidence,
                *[row["raw"][key] for key in FIELDS]
            ])

    print("Created evaluation.csv and test_predictions.csv")
