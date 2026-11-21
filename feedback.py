"""Save therapist review actions locally for the demo."""
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name('review_log.jsonl')


def save_feedback(data):
    if not isinstance(data, dict):
        raise ValueError('Feedback must be an object')
    action = data.get('action')
    if action not in ('accept', 'override', 'flag'):
        raise ValueError('action must be accept, override or flag')
    session = data.get('session_id')
    attempt = data.get('attempt_id')
    if not isinstance(session, str) or not 1 <= len(session) <= 80:
        raise ValueError('session_id is required')
    if not isinstance(attempt, str) or not 1 <= len(attempt) <= 80:
        raise ValueError('attempt_id is required')
    note = data.get('notes', '')
    if not isinstance(note, str) or len(note) > 500:
        raise ValueError('notes must be text under 500 characters')

    saved = {'session_id': session, 'attempt_id': attempt,
             'action': action, 'notes': note, 'data_source': 'demo'}
    with DATA_FILE.open('a', encoding='utf-8') as file:
        file.write(json.dumps(saved) + '\n')
    return {'saved': True, 'feedback': saved,
            'note': 'Review recorded. It does not retrain the AI or control a glove.'}


def get_feedback(session_id):
    if not DATA_FILE.exists():
        return []
    results = []
    for line in DATA_FILE.read_text(encoding='utf-8').splitlines():
        item = json.loads(line)
        if item['session_id'] == session_id:
            results.append(item)
    return results
