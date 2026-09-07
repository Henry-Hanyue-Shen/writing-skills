import copy
import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "validate_gate_report.py"
SPEC = importlib.util.spec_from_file_location("validate_gate_report", MODULE_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


def pass_report():
    return {
        "schema_version": "1.0",
        "gate_id": "test-gate",
        "artifact": {
            "input": "input.md",
            "output": "output.md",
            "scope": "full",
            "language": "en",
        },
        "verdict": "PASS",
        "checks": {
            name: {"status": "pass", "detail": f"{name} passed."}
            for name in VALIDATOR.CHECK_NAMES
        },
        "edits": [],
        "return_to_caller": [],
        "unresolved": [],
        "notes": [],
    }


def packet(packet_type="experiment", blocking=True, packet_id="R1"):
    return {
        "id": packet_id,
        "type": packet_type,
        "blocking": blocking,
        "affected_location": "Results, paragraph 2",
        "need": "A missing result artifact.",
        "reason": "The numerical claim cannot be checked without it.",
        "acceptance_test": "Return the frozen result file and its generating command.",
    }


class GateReportValidationTests(unittest.TestCase):
    def test_valid_pass(self):
        self.assertEqual(VALIDATOR.validate(pass_report()), [])

    def test_pass_rejects_blocking_packet(self):
        report = pass_report()
        report["return_to_caller"] = [packet()]
        errors = VALIDATOR.validate(report)
        self.assertTrue(any("PASS cannot contain blocking" in error for error in errors))

    def test_return_for_research_requires_research_packet(self):
        report = pass_report()
        report["verdict"] = "RETURN_FOR_RESEARCH"
        report["return_to_caller"] = [packet(packet_type="author-decision")]
        errors = VALIDATOR.validate(report)
        self.assertTrue(any("requires a blocking research" in error for error in errors))

    def test_integrity_packet_requires_hold(self):
        report = pass_report()
        report["verdict"] = "RETURN_FOR_RESEARCH"
        report["return_to_caller"] = [packet(packet_type="integrity")]
        errors = VALIDATOR.validate(report)
        self.assertTrue(any("HOLD_FOR_INTEGRITY" in error for error in errors))

    def test_valid_integrity_hold(self):
        report = pass_report()
        report["verdict"] = "HOLD_FOR_INTEGRITY"
        report["checks"]["numbers"] = {
            "status": "fail",
            "detail": "The source table and manuscript report different sample sizes.",
        }
        report["return_to_caller"] = [packet(packet_type="integrity")]
        self.assertEqual(VALIDATOR.validate(report), [])

    def test_duplicate_packet_ids_are_rejected(self):
        report = pass_report()
        report["verdict"] = "RETURN_FOR_RESEARCH"
        report["return_to_caller"] = [packet(), copy.deepcopy(packet())]
        errors = VALIDATOR.validate(report)
        self.assertTrue(any("duplicate return packet id" in error for error in errors))

    def test_unknown_check_is_rejected(self):
        report = pass_report()
        report["checks"]["novelty_search"] = {
            "status": "pass",
            "detail": "This full-research check does not belong to the editor gate.",
        }
        errors = VALIDATOR.validate(report)
        self.assertTrue(any("unknown fields" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
