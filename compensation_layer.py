
"""MuscleMethod compensation analysis.
Educational simulation only. Not a clinical diagnosis.
"""

import math
from model import predict as classifier_predict


def check_value(signals, name):
    value = signals.get(name, 0.0)

    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or not 0 <= value <= 1
    ):
        raise ValueError(
            f"{name} must be a number from 0 to 1"
        )

    return float(value)


def predict(payload):

    if not isinstance(payload, dict):
        raise ValueError("Request must be an object")

    signals = payload.get("signals", {})

    if not isinstance(signals, dict):
        raise ValueError("signals must be an object")

    # New simulated movement indicators
    trunk_lean = check_value(signals, "trunk_lean")
    shoulder_hike = check_value(signals, "shoulder_hike")

    # Run the existing EEG/EMG/IMU AI model
    result = classifier_predict(payload)

    intent = check_value(signals, "eeg_intent")
    hand_motion = check_value(signals, "imu_motion")

    # Check for possible upper-body substitution
    trunk_flag = trunk_lean >= 0.70
    shoulder_flag = shoulder_hike >= 0.70

    substitution_review = (
        intent >= 0.50
        and hand_motion >= 0.40
        and (trunk_flag or shoulder_flag)
    )

    patterns = []

    if trunk_flag:
        patterns.append("trunk leaning")

    if shoulder_flag:
        patterns.append("shoulder hiking")

    # Include the new evidence in the API result
    result["upper_body_substitution_flag"] = substitution_review

    result["upper_body_evidence"] = {
        "trunk_lean": trunk_lean,
        "shoulder_hike": shoulder_hike,
        "hand_motion": hand_motion,
        "patterns_above_demo_threshold": patterns
    }

    if substitution_review:

        result["review_flag"] = True

        result["safety_reasons"].append(
            "Possible upper-body movement substitution ("
            + ", ".join(patterns)
            + "); therapist review suggested"
        )

        # Preserve emergency-stop and poor-signal decisions
        if result["decision"] not in (
            "Stop / No Automatic Assistance",
            "Unclear — Review Signals"
        ):
            result["decision"] = "Pattern Review Recommended"

        # Block simulated automatic assistance increase
        result["assistance_increase_allowed"] = False
        result["safety_state"] = "BLOCKED"

        if result["assistance_increase_requested"]:
            result["assistance_status"] = "BLOCKED"
        else:
            result["assistance_status"] = (
                "NO INCREASE REQUESTED; REVIEW ACTIVE"
            )

        result["movement_explanation"] = (
            "Hand movement is present, but simulated "
            "trunk/shoulder movement suggests an "
            "alternative movement strategy. "
            "This is a review flag, not a diagnosis."
        )

    elif not result["review_flag"]:

        result["movement_explanation"] += (
            " No upper-body substitution threshold "
            "was triggered."
        )

    return result
