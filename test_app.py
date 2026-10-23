"""
Automated Unit and Integration Test Suite for Multimodal Construction Intelligence Platform.
Validates calculation metrics, JSON schema adherence, fallback inference, and preset generation.
"""

import sys
import unittest
import json

class TestConstructionPlatform(unittest.TestCase):

    def test_presets_generation(self):
        """Verify synthetic sample image generators produce valid PIL images."""
        from sample_data.presets import get_all_sample_presets
        presets = get_all_sample_presets()
        self.assertGreaterEqual(len(presets), 3)
        for name, img in presets.items():
            self.assertEqual(img.size, (800, 550))
            self.assertEqual(img.mode, "RGB")
        print("[PASSED] Presets generation test passed.")

    def test_ai_mock_ppe_contract(self):
        """Verify safety audit JSON contract conforms strictly to schema."""
        from modules.ai_engine import generate_mock_analysis
        result = generate_mock_analysis("ppe")
        
        self.assertIn("safety_score", result)
        self.assertIn("overall_status", result)
        self.assertIn("ppe_detection", result)
        self.assertIn("identified_site_hazards", result)
        self.assertIsInstance(result["safety_score"], int)
        self.assertGreaterEqual(result["safety_score"], 0)
        self.assertLessEqual(result["safety_score"], 100)
        self.assertGreater(len(result["ppe_detection"]), 0)
        self.assertGreater(len(result["identified_site_hazards"]), 0)
        print("[PASSED] PPE JSON contract schema test passed.")

    def test_ai_mock_crack_contract(self):
        """Verify crack diagnostics JSON contract conforms strictly to schema."""
        from modules.ai_engine import generate_mock_analysis
        result = generate_mock_analysis("crack")
        
        self.assertIn("defect_type", result)
        self.assertIn("estimated_width_mm", result)
        self.assertIn("severity_score", result)
        self.assertIn("structural_urgency", result)
        self.assertIn("recommended_repairs", result)
        self.assertGreater(result["estimated_width_mm"], 0.0)
        self.assertGreater(len(result["recommended_repairs"]), 0)
        print("[PASSED] Crack Diagnostics JSON contract schema test passed.")

    def test_valuation_calculations(self):
        """Verify parametric costing, INR valuation, and BOQ material takeoffs."""
        from modules.valuation_planner import calculate_project_metrics, format_inr
        
        metrics = calculate_project_metrics(
            structure_type="Residential High-Rise (G+25)",
            built_up_sqft=100000,
            location_key="Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Hyderabad, Chennai)",
            quality_grade="Premium (High-End Finishes / Home Automation)",
            completion_pct=50.0
        )
        
        self.assertGreater(metrics["total_budget_inr"], 0)
        self.assertEqual(metrics["capex_incurred_inr"], metrics["total_budget_inr"] * 0.5)
        self.assertEqual(metrics["cost_to_complete_inr"], metrics["total_budget_inr"] * 0.5)
        self.assertGreater(metrics["steel_mt"], 0)
        self.assertGreater(metrics["cement_bags"], 0)
        self.assertGreater(metrics["rmc_cum"], 0)
        
        # Test INR formatting
        self.assertTrue(format_inr(50_000_000).startswith("₹ 5.00 Cr"))
        self.assertTrue(format_inr(2_500_000).startswith("₹ 25.00 L"))
        print("[PASSED] Valuation and BOQ metrics calculations test passed.")

    def test_pollinations_url_format(self):
        """Verify Pollinations AI / Flux URL generation."""
        from modules.valuation_planner import generate_pollinations_url
        url = generate_pollinations_url("modern high rise building", seed=100)
        self.assertTrue(url.startswith("https://image.pollinations.ai/prompt/"))
        self.assertIn("width=1024", url)
        self.assertIn("model=flux", url)
        self.assertIn("seed=100", url)
        print("[PASSED] Pollinations URL generation test passed.")

    def test_weather_chat_fallback(self):
        """Verify domain engineering chatbot responds accurately."""
        from modules.ai_engine import generate_mock_chat_response
        resp = generate_mock_chat_response("What is the nominal cover under IS 456?")
        self.assertIn("IS 456", resp)
        self.assertIn("Footings", resp)
        print("[PASSED] Engineering chatbot domain knowledge test passed.")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConstructionPlatform)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
