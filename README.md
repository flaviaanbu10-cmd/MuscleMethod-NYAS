# MuscleMethod final demo

This is a **synthetic educational prototype**. It does not process actual patient signals, diagnose compensation, or control a robotic glove.

## Files

- `model.py`: existing V4 KNN synthetic classifier, plus new combined prediction response
- `movement_review.py`: separate experimental pattern checks
- `safety.py`: demo-only blocking rules
- `feedback.py`: local therapist feedback log
- `server.py`: local web server and API
- `index.html`: small working example website (Aisha can replace the design)
- `test_model.py`: basic tests

## Run

Open PowerShell inside this folder:

```powershell
py test_model.py
py model.py
py server.py
```

Open `http://127.0.0.1:8000` in your browser. To stop the server, press Ctrl+C.

## Connect Aisha's website

Use `POST /predict` with a JSON object containing `signals` (six original normalized synthetic features), optional `history`, and optional safety fields. The response contains `model_prediction`, `movement_review`, `safety`, `evidence`, and legacy-compatible fields such as `decision` and `safety_state`.

Use `POST /feedback` to record `session_id`, `attempt_id`, `action` (`accept`, `override`, or `flag`) and optional `notes`.

Use `GET /session/demo-001` to see feedback recorded for that session.

Keep the Python API and website on the same local server for the easiest setup. For an external website, CORS/hosting must be configured separately. The server binds only to 127.0.0.1 and is not meant to host real patient data.

## Important model limitation

The original V4 training labels include `Pattern Review Recommended` as a classifier class. The final interface maps that class to `Unclear` for its assistance recommendation and adds a separate pattern-review result. This is a **compatibility bridge**, not a retrained five-assistance-class model. The original V4 uses simulated EEG, EMG, fatigue, and IMU-derived features. It cannot establish real compensation detection or clinical performance.

Thresholds in `movement_review.py` and `safety.py` are hand-set demonstration thresholds, not medical limits. Therapist feedback is saved locally only and never retrains the model.
