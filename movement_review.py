"""Extra pattern checks for our simulated movement attempts."""


def assess_pattern(values, signals, history=None):
    # These cutoffs are our demo choices, not clinical limits.
    history = history or []
    evidence = []
    gap = values['intent_execution_gap']
    coactivation = values['coactivation']

    if gap >= 0.45:
        evidence.append('Large difference between simulated intention and execution features')
    if coactivation >= 0.65:
        evidence.append('High simulated coactivation feature')
    if values['imu_smoothness'] <= 0.35:
        evidence.append('Low simulated movement smoothness')

    # This is an OPTIONAL extra simulated EMG feature, not in the V4 training data.
    other = signals.get('emg_non_target')
    if other is not None:
        if type(other) not in (int, float) or not 0 <= other <= 1:
            raise ValueError('emg_non_target must be between 0 and 1')
        if other >= 0.7:
            evidence.append('High simulated non-target muscle activity')

    # See whether earlier attempts had similar flags.
    recent = history[-4:]
    earlier_flags = sum(bool(item.get('pattern_flag')) for item in recent)
    repeated = len(recent) >= 2 and earlier_flags >= 2 and bool(evidence)
    if repeated:
        evidence.append('Similar review flags appeared in earlier attempts')

    if not evidence:
        status = 'no_flag'
    elif len(evidence) >= 2 or repeated:
        status = 'review_recommended'
    else:
        status = 'watch'

    return {
        'status': status,
        'pattern_flag': status == 'review_recommended',
        'evidence': evidence,
        'recent_prior_flags': earlier_flags,
        'validated_compensation': False,
        'note': 'Experimental pattern review only. This is not a compensation diagnosis.'
    }
