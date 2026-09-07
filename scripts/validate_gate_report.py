#!/usr/bin/env python3
"""Validate a Research Editor Gate handoff report without third-party packages."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


VERDICTS = {"PASS", "PASS_WITH_NOTES", "RETURN_FOR_RESEARCH", "HOLD_FOR_INTEGRITY"}
CHECK_STATUSES = {"pass", "warn", "fail", "not_checked"}
CHECK_NAMES = {
    "semantic_fidelity",
    "methodology",
    "terminology",
    "citations",
    "numbers",
    "prose",
}
CLAIM_CHANGES = {"none", "narrowed", "author_confirmation_required"}
RETURN_TYPES = {
    "literature",
    "experiment",
    "analysis",
    "source-recovery",
    "integrity",
    "author-decision",
}
RESEARCH_TYPES = {"literature", "experiment", "analysis", "source-recovery"}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["root must be a JSON object"]

    if report.get("schema_version") != "1.0":
        errors.append("schema_version must equal '1.0'")
    if not nonempty(report.get("gate_id")):
        errors.append("gate_id must be a non-empty string")

    artifact = report.get("artifact")
    if not isinstance(artifact, dict):
        errors.append("artifact must be an object")
    else:
        for key in ("input", "output", "language"):
            if not nonempty(artifact.get(key)):
                errors.append(f"artifact.{key} must be a non-empty string")
        if artifact.get("scope") not in {"full", "partial"}:
            errors.append("artifact.scope must be 'full' or 'partial'")

    verdict = report.get("verdict")
    if verdict not in VERDICTS:
        errors.append(f"verdict must be one of {sorted(VERDICTS)}")

    checks = report.get("checks")
    if not isinstance(checks, dict):
        errors.append("checks must be an object")
        checks = {}
    unknown_checks = set(checks) - CHECK_NAMES
    if unknown_checks:
        errors.append(f"checks contains unknown fields: {sorted(unknown_checks)}")
    for name in sorted(CHECK_NAMES):
        item = checks.get(name)
        if not isinstance(item, dict):
            errors.append(f"checks.{name} must be an object")
            continue
        if item.get("status") not in CHECK_STATUSES:
            errors.append(f"checks.{name}.status must be one of {sorted(CHECK_STATUSES)}")
        if not nonempty(item.get("detail")):
            errors.append(f"checks.{name}.detail must be a non-empty string")

    edits = report.get("edits")
    if not isinstance(edits, list):
        errors.append("edits must be an array")
        edits = []
    for index, edit in enumerate(edits):
        if not isinstance(edit, dict):
            errors.append(f"edits[{index}] must be an object")
            continue
        for key in ("location", "kind", "summary"):
            if not nonempty(edit.get(key)):
                errors.append(f"edits[{index}].{key} must be a non-empty string")
        if edit.get("claim_change") not in CLAIM_CHANGES:
            errors.append(f"edits[{index}].claim_change must be one of {sorted(CLAIM_CHANGES)}")

    packets = report.get("return_to_caller")
    if not isinstance(packets, list):
        errors.append("return_to_caller must be an array")
        packets = []
    packet_ids: set[str] = set()
    for index, packet in enumerate(packets):
        if not isinstance(packet, dict):
            errors.append(f"return_to_caller[{index}] must be an object")
            continue
        packet_id = packet.get("id")
        if not nonempty(packet_id):
            errors.append(f"return_to_caller[{index}].id must be a non-empty string")
        elif packet_id in packet_ids:
            errors.append(f"duplicate return packet id: {packet_id}")
        else:
            packet_ids.add(packet_id)
        if packet.get("type") not in RETURN_TYPES:
            errors.append(f"return_to_caller[{index}].type must be one of {sorted(RETURN_TYPES)}")
        if not isinstance(packet.get("blocking"), bool):
            errors.append(f"return_to_caller[{index}].blocking must be boolean")
        for key in ("affected_location", "need", "reason", "acceptance_test"):
            if not nonempty(packet.get(key)):
                errors.append(f"return_to_caller[{index}].{key} must be a non-empty string")

    for field in ("unresolved", "notes"):
        if not isinstance(report.get(field), list):
            errors.append(f"{field} must be an array")

    blocking_packets = [p for p in packets if isinstance(p, dict) and p.get("blocking") is True]
    check_statuses = [item.get("status") for item in checks.values() if isinstance(item, dict)]
    unresolved = report.get("unresolved") if isinstance(report.get("unresolved"), list) else []
    notes = report.get("notes") if isinstance(report.get("notes"), list) else []

    if verdict == "PASS":
        if blocking_packets:
            errors.append("PASS cannot contain blocking return packets")
        if unresolved:
            errors.append("PASS requires unresolved to be empty")
        if any(status != "pass" for status in check_statuses) or len(check_statuses) != len(CHECK_NAMES):
            errors.append("PASS requires all six checks to be pass")
    elif verdict == "PASS_WITH_NOTES":
        if blocking_packets:
            errors.append("PASS_WITH_NOTES cannot contain blocking return packets")
        if "fail" in check_statuses:
            errors.append("PASS_WITH_NOTES cannot contain a failed check")
        if not (notes or unresolved or "warn" in check_statuses or "not_checked" in check_statuses):
            errors.append("PASS_WITH_NOTES requires a note, unresolved item, warning, or coverage limitation")
    elif verdict == "RETURN_FOR_RESEARCH":
        if not any(p.get("type") in RESEARCH_TYPES for p in blocking_packets):
            errors.append("RETURN_FOR_RESEARCH requires a blocking research/source-recovery packet")
        if any(p.get("type") == "integrity" for p in blocking_packets):
            errors.append("blocking integrity packets require HOLD_FOR_INTEGRITY")
    elif verdict == "HOLD_FOR_INTEGRITY":
        if not any(p.get("type") == "integrity" for p in blocking_packets):
            errors.append("HOLD_FOR_INTEGRITY requires a blocking integrity packet")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Path to EDITOR_GATE.json")
    args = parser.parse_args()

    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: report not found: {args.report}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate(report)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"INVALID: {len(errors)} error(s)", file=sys.stderr)
        return 1

    print(f"VALID: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
