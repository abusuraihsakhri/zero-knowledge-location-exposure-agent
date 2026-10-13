/**
 * Browser-only analogue of agents/workers.py threshold rules.
 * This is deterministic triage logic, not a zero-knowledge proof or contact trace.
 */
const STATUS_FLAGS = ["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"];

export function evaluateTask(input) {
  const taskId = String(input.task_id ?? "").trim();
  const target = String(input.target_identifier ?? "").trim();
  const descriptor = String(input.status_descriptor ?? "NOMINAL").trim();
  for (const [name, value] of [["Task ID", taskId], ["Target identifier", target], ["Status descriptor", descriptor]]) {
    if (!value || value.length > 128) throw new Error(name + " must contain 1–128 characters.");
  }
  const primary = Number(input.primary_metric);
  const secondary = Number(input.secondary_metric);
  if (!Number.isFinite(primary) || !Number.isFinite(secondary) ||
      input.primary_metric === "" || input.secondary_metric === "") {
    throw new Error("Both metrics must be finite numbers.");
  }
  const critical = input.is_critical_flag === true;
  const alerts = [];
  if (primary > 25) {
    alerts.push({
      origin_worker: "InvariantQCWorker",
      urgency: "ELEVATED_RISK",
      summary: "Primary Metric Threshold Exceeded",
      technical_details: "Primary measurement (" + primary.toFixed(2) + ") exceeds configured limit (25.00).",
      actionable_remediation: "Review the measurement and secondary parameters."
    });
  }
  if (critical || secondary > 12) {
    alerts.push({
      origin_worker: "SafetyEscalationWorker",
      urgency: critical ? "CRITICAL_STAT_PANIC" : "ELEVATED_RISK",
      summary: "Safety Interlock Triggered",
      technical_details: "CriticalFlag=" + critical + "; secondary index=" + secondary.toFixed(2) + ".",
      actionable_remediation: "Review and escalate per local procedures."
    });
  }
  if (STATUS_FLAGS.some(flag => descriptor.toUpperCase().includes(flag))) {
    alerts.push({
      origin_worker: "ProtocolConformanceWorker",
      urgency: "ELEVATED_RISK",
      summary: "Descriptor Discordance Detected",
      technical_details: "Descriptor flagged for review: " + descriptor,
      actionable_remediation: "Review the descriptor and verify input data."
    });
  }
  const criticalCount = alerts.filter(a => a.urgency === "CRITICAL_STAT_PANIC").length;
  const urgency = criticalCount ? "CRITICAL_STAT_PANIC" : alerts.length ? "ELEVATED_RISK" : "ROUTINE";
  return {
    mode: "local_demo",
    task_id: taskId,
    target_identifier: target,
    overall_urgency: urgency,
    integrity_status: criticalCount ? "RECALIBRATION_REQUIRED" : alerts.length ? "DISCORDANT_ANOMALY" : "VALIDATED_OPTIMAL",
    total_alerts: alerts.length,
    critical_alerts_count: criticalCount,
    alerts,
    consensus_summary: "Local rule-based evaluation completed. No location matching or cryptographic proof was performed."
  };
}
