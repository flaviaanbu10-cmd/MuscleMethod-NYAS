"""Demo safety checks. No physical glove is connected."""


def check_safety(payload, agreement, pattern):
    reasons = []

    for key in ('sensors_connected', 'force_within_limit', 'movement_within_limit', 'emergency_stop'):
        if key in payload and type(payload[key]) is not bool:
            raise ValueError(key + ' must be true or false')

    quality = payload.get('signal_quality', 1.0)
    if type(quality) not in (int, float) or not 0 <= quality <= 1:
        raise ValueError('signal_quality must be between 0 and 1')

    if payload.get('emergency_stop', False):
        reasons.append('Emergency stop is enabled')
    if not payload.get('sensors_connected', True):
        reasons.append('Sensor connection is missing')
    if not payload.get('force_within_limit', True):
        reasons.append('Simulated force limit warning')
    if not payload.get('movement_within_limit', True):
        reasons.append('Simulated movement limit warning')
    if quality < 0.55:
        reasons.append('Signal quality is too low')
    if agreement < 0.62:
        reasons.append('Model vote agreement is low')
    if pattern['status'] == 'review_recommended':
        reasons.append('Unusual pattern needs therapist review')

    return {
        'status': 'BLOCKED' if reasons else 'PERMITTED_FOR_SIMULATION',
        'reasons': reasons,
        'allows_assistance_increase': not reasons,
        'note': 'These are demonstration rules, not validated medical safety limits.'
    }
