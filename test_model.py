"""Simple tests for the simulated prediction and feedback flow."""
import unittest
from model import predict
from feedback import save_feedback

SIGNALS = {
    'eeg_intent': .85, 'emg_target': .72, 'coactivation': .90,
    'fatigue': .20, 'imu_motion': .45, 'imu_smoothness': .20
}


class MuscleMethodTests(unittest.TestCase):
    def test_pattern_flag(self):
        result = predict({'signals': SIGNALS, 'data_source': 'synthetic'})
        self.assertEqual(result['movement_review']['status'], 'review_recommended')
        self.assertEqual(result['safety_state'], 'BLOCKED')

    def test_missing_signal(self):
        with self.assertRaises(ValueError):
            predict({'signals': {'eeg_intent': .5}})

    def test_bad_quality(self):
        result = predict({'signals': SIGNALS, 'signal_quality': .20})
        self.assertEqual(result['safety_state'], 'BLOCKED')

    def test_therapist_action(self):
        with self.assertRaises(ValueError):
            save_feedback({'session_id': 'demo', 'attempt_id': '1', 'action': 'unlock_glove'})


if __name__ == '__main__':
    unittest.main()
