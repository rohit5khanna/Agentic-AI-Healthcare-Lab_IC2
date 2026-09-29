import unittest

from lab_core import CATALOG_BY_ID, parse_action, run_demo


class LabCoreTests(unittest.TestCase):
    def test_catalog_has_ten_unique_demos(self):
        self.assertEqual(len(CATALOG_BY_ID), 10)
        self.assertEqual(set(CATALOG_BY_ID), {f"{number:02d}" for number in range(1, 11)})
        self.assertTrue(all(demo.implemented for demo in CATALOG_BY_ID.values()))

    def test_minimal_loop_explore_is_a_real_tool_trajectory(self):
        result = run_demo("02", "Explore")
        self.assertEqual(result.status, "completed")
        self.assertEqual(
            [step.action for step in result.trace],
            ["get_latest_inr", "get_medications", "draft_followup", "final"],
        )
        self.assertFalse(result.final_state["Medication order changed"])

    def test_human_gate_denies_by_default(self):
        result = run_demo(
            "03",
            "Explore",
            gate_decision="Request more information",
            evidence=["Latest INR", "Current medication"],
        )
        self.assertEqual(result.final_state["Current medications"], ["warfarin 5 mg daily"])
        self.assertFalse(result.final_state["Audit"][0]["executed"])

    def test_human_gate_approval_still_requires_complete_evidence(self):
        result = run_demo(
            "03",
            "Explore",
            gate_decision="Approve",
            evidence=["Latest INR", "Current medication"],
        )
        self.assertFalse(result.final_state["Audit"][0]["executed"])

    def test_human_gate_executes_only_with_approval_and_complete_evidence(self):
        result = run_demo(
            "03",
            "Explore",
            gate_decision="Approve",
            evidence=["Latest INR", "Current medication", "Bleeding assessment", "Prescriber identity"],
        )
        self.assertTrue(result.final_state["Audit"][0]["executed"])

    def test_fhir_write_back_is_denied(self):
        result = run_demo("09", "Explore", gate_decision="Reject")
        self.assertEqual(result.final_state["Communications"], [])
        self.assertFalse(result.final_state["Medication changed"])

    def test_memory_demo_exposes_stale_and_current_recall(self):
        result = run_demo("04", "Explore")
        recommendations = result.final_state["Recommendations"]
        self.assertEqual(set(recommendations), {"Naive", "Current"})
        self.assertNotEqual(recommendations["Naive"], recommendations["Current"])
        self.assertFalse(result.final_state["Order changed"])

    def test_tool_retrieval_is_deterministic_and_reduces_exposure(self):
        result = run_demo("05", "Live")
        self.assertEqual(result.telemetry, [])
        self.assertLess(len(result.final_state["Tools exposed"]), 15)
        self.assertEqual(result.final_state["Unsafe exposure"], [])

    def test_uncertainty_experiment_retains_all_76_interactions(self):
        result = run_demo("06", "Explore")
        self.assertEqual(result.final_state["Model interactions represented"], 76)
        self.assertEqual(len(result.telemetry), 76)
        self.assertFalse(result.final_state["Agreement is calibrated probability"])

    def test_compounding_reliability_scores_the_whole_trajectory(self):
        result = run_demo("07", "Explore")
        self.assertAlmostEqual(
            result.final_state["End-to-end analytic reliability"], 0.95**5, places=4
        )
        self.assertLess(
            result.final_state["End-to-end analytic reliability"],
            result.final_state["Per-step reliability"],
        )

    def test_orchestrator_compares_four_calls_and_verifies(self):
        result = run_demo("08", "Explore")
        self.assertEqual(len(result.telemetry), 4)
        self.assertTrue(result.final_state["Aggregation verified"])
        self.assertIsNotNone(result.final_state["Single-agent baseline"])

    def test_prompt_injection_is_blocked_by_policy(self):
        result = run_demo("10", "Explore", gate_decision="Approve")
        self.assertFalse(result.final_state["Proposal executed"])
        self.assertFalse(result.final_state["Dose policy passed"])
        self.assertEqual(result.final_state["Current medications"], ["warfarin 5 mg daily"])

    def test_every_demo_has_an_explore_trajectory(self):
        for demo_id in CATALOG_BY_ID:
            with self.subTest(demo_id=demo_id):
                result = run_demo(demo_id, "Explore")
                self.assertNotEqual(result.status, "not yet translated")
                self.assertGreater(len(result.trace), 0)

    def test_parser_rejects_unknown_action(self):
        with self.assertRaises(ValueError):
            parse_action('{"thought":"x","action":"delete_record","action_input":{}}', {"read", "final"})


if __name__ == "__main__":
    unittest.main()
