import unittest
from src.risk_engine import analyze_message
from src.analytics import load_incidents, load_messages, load_documented_cases, dataset_quality

class RiskEngineTests(unittest.TestCase):
    def test_otp_request_triggers_credential_signal(self):
        result = analyze_message("Please share your OTP immediately to keep your account active.")
        self.assertGreater(result["score"], 0)
        self.assertTrue(any("Credential" in item["signal"] for item in result["signals"]))

    def test_benign_reminder_has_no_configured_signal(self):
        result = analyze_message("The class meeting starts at 10 AM tomorrow.")
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["level"], "No rule triggered")

    def test_score_is_capped(self):
        result = analyze_message("URGENT police digital arrest OTP password CVV pay now don't tell anyone click here")
        self.assertLessEqual(result["score"], 20)

    def test_url_is_extracted_but_not_visited(self):
        result = analyze_message("Please click https://example.invalid/login")
        self.assertEqual(result["urls_found"], ["https://example.invalid/login"])
        self.assertIn("not a probability", result["disclaimer"].lower())

class DataLoadingTests(unittest.TestCase):
    def test_synthetic_data_loads(self):
        incidents = load_incidents()
        messages = load_messages()
        self.assertGreater(len(incidents), 0)
        self.assertGreater(len(messages), 0)
        self.assertTrue(incidents["synthetic_record"].astype(str).str.lower().isin(["true", "1"]).all())

    def test_historical_cases_cover_2010_to_2025(self):
        cases = load_documented_cases()
        self.assertGreaterEqual(int(cases["year"].min()), 2010)
        self.assertLessEqual(int(cases["year"].max()), 2025)
        self.assertTrue({"case_name", "defensive_lesson", "source_url"}.issubset(cases.columns))
        self.assertGreater(len(cases), 0)

if __name__ == "__main__":
    unittest.main()
