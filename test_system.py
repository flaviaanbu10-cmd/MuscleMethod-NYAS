
"""Quick software tests for MuscleMethod."""

from model import predict


def run(signals, **changes):

    payload = {
        "signals": signals,
        "signal_quality": 0.92,
        "sensors_connected": True,
        "force_within_limit": True,
        "movement_within_limit": True,
        "emergency_stop": False
    }

    payload.update(changes)

    return predict(payload)


normal = {
    "eeg_intent": 0.83,
    "emg_target": 0.27,
    "coactivation": 0.22,
    "fatigue": 0.25,
    "imu_motion": 0.28,
    "imu_smoothness": 0.47
}

conflict = {
    "eeg_intent": 0.88,
    "emg_target": 0.20,
    "coactivation": 0.80,
    "fatigue": 0.15,
    "imu_motion": 0.18,
    "imu_smoothness": 0.18
}

weakness = dict(conflict, coactivation=0.18)


# Normal assistance
assert run(normal)["decision"] == "Assist More"
assert run(normal)["assistance_increase_allowed"] is True

# Conflicting signals
assert run(conflict)["decision"] == "Pattern Review Recommended"
assert run(conflict)["assistance_increase_allowed"] is False

# Weakness should not automatically flag compensation
assert run(weakness)["review_flag"] is False

# Poor signal quality
assert run(normal, signal_quality=0.20)[
    "decision"
] == "Unclear — Review Signals"

assert run(normal, signal_quality=0.20)[
    "assistance_increase_allowed"
] is False

# Emergency stop
assert run(normal, emergency_stop=True)[
    "decision"
] == "Stop / No Automatic Assistance"

assert run(normal, emergency_stop=True)[
    "assistance_increase_allowed"
] is False


print("PASS: 9 software regression checks")
