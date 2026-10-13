"""Regression coverage for input handling and API security."""
import csv
from pathlib import Path

import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient

from agents.api import app
from agents.base import AuditTrail, SecurityException
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor
from cli import main as primary_main
from zk_contact_trace.cli import main as legacy_main


@pytest.mark.parametrize("runner", [primary_main, legacy_main])
def test_csv_booleans_are_not_python_truthiness(runner, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with open("input.csv", "w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=[
            "task_id", "target_identifier", "primary_metric", "secondary_metric",
            "is_critical_flag", "status_descriptor"
        ])
        writer.writeheader()
        writer.writerows([
            dict(task_id="FALSE-CASE", target_identifier="SYNTHETIC", primary_metric=2,
                 secondary_metric=2, is_critical_flag="False", status_descriptor="NOMINAL"),
            dict(task_id="TRUE-CASE", target_identifier="SYNTHETIC", primary_metric=2,
                 secondary_metric=2, is_critical_flag="True", status_descriptor="NOMINAL")
        ])
    assert runner(["batch", "-i", "input.csv", "-o", "output.csv"]) == 0
    with open("output.csv", newline="", encoding="utf-8") as output:
        result = list(csv.DictReader(output))
    key = "overall_urgency" if runner is primary_main else "overall_status"
    assert result[0][key] in ("ROUTINE", "NOMINAL_OPTIMAL")
    assert "CRITICAL" in result[1][key]


@pytest.mark.parametrize("runner", [primary_main, legacy_main])
def test_invalid_csv_bool_is_rejected(runner, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("input.csv").write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "BAD,SYNTHETIC,2,2,maybe,NOMINAL\n", encoding="utf-8"
    )
    assert runner(["batch", "-i", "input.csv", "-o", "output.csv"]) == 1
    assert not Path("output.csv").exists()


def test_phis_in_attributes_are_blocked():
    payload = SystemTaskPayload(
        task_id="T-1", target_identifier="SYNTHETIC", primary_metric=2,
        attributes={"unstructured_note": "Patient MRN-123456"}
    )
    with pytest.raises(SecurityException):
        SystemSupervisor().process_task(payload)


@pytest.mark.parametrize("bad_value", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_metrics_are_rejected(bad_value):
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="T-1", target_identifier="SYNTHETIC", primary_metric=bad_value)


def test_audit_trail_snapshot_cannot_mutate_internal_entries():
    trail = AuditTrail(secret_key="a" * 48)
    trail.log("test", "test", "RUN", {"ok": True})
    trail.get_trail()[0]["current_hash"] = "changed"
    assert trail.verify_integrity() is True


def test_api_requires_access_token(monkeypatch):
    client = TestClient(app)
    monkeypatch.delenv("API_ACCESS_TOKEN", raising=False)
    assert client.get("/health").status_code == 200
    assert client.get("/metrics").status_code == 503
    monkeypatch.setenv("API_ACCESS_TOKEN", "ci-token-should-be-long-enough")
    assert client.get("/metrics").status_code == 401
    assert client.get("/metrics", headers={"X-API-Key": "wrong"}).status_code == 401
    assert client.get("/metrics", headers={"X-API-Key": "ci-token-should-be-long-enough"}).status_code == 200


def test_api_validates_payload_and_guard(monkeypatch):
    monkeypatch.setenv("API_ACCESS_TOKEN", "ci-token-should-be-long-enough")
    client = TestClient(app)
    headers = {"X-API-Key": "ci-token-should-be-long-enough"}
    payload = {"task_id": "TEST", "target_identifier": "SYNTHETIC", "primary_metric": 4}
    assert client.post("/api/audit", json=payload, headers=headers).status_code == 200
    assert client.post("/api/audit", json={**payload, "primary_metric": "NaN"}, headers=headers).status_code == 422
    blocked = {**payload, "attributes": {"text": "MRN-123456"}}
    assert client.post("/api/audit", json=blocked, headers=headers).status_code == 400
