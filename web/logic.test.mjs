import test from "node:test";
import assert from "node:assert/strict";
import { evaluateTask } from "./logic.mjs";

const base = {task_id:"TASK-1",target_identifier:"KEY-1",primary_metric:12,secondary_metric:4,status_descriptor:"NOMINAL",is_critical_flag:false};
test("nominal evaluation", () => {
  const result = evaluateTask(base);
  assert.equal(result.overall_urgency,"ROUTINE");
  assert.equal(result.total_alerts,0);
  assert.equal(result.mode,"local_demo");
  assert.ok(!("audit_hash" in result));
});
test("threshold boundaries are strict and consistent with Python", () => {
  assert.equal(evaluateTask({...base,primary_metric:25,secondary_metric:12}).total_alerts,0);
  assert.equal(evaluateTask({...base,primary_metric:25.01,secondary_metric:12.01}).total_alerts,2);
});
test("critical flag takes precedence and descriptor produces additional alert", () => {
  const result = evaluateTask({...base,is_critical_flag:true,status_descriptor:"DISCORDANT"});
  assert.equal(result.overall_urgency,"CRITICAL_STAT_PANIC");
  assert.equal(result.critical_alerts_count,1);
  assert.equal(result.total_alerts,2);
});
test("invalid inputs do not produce dossiers", () => {
  assert.throws(()=>evaluateTask({...base,primary_metric:""}),/finite/);
  assert.throws(()=>evaluateTask({...base,primary_metric:"Infinity"}),/finite/);
  assert.throws(()=>evaluateTask({...base,task_id:"  "}),/Task ID/);
  assert.throws(()=>evaluateTask({...base,secondary_metric:NaN}),/finite/);
});
