"""Local FastAPI interface for the rule-based evaluation demo.

Every operational endpoint requires API_ACCESS_TOKEN in the X-API-Key header.
Deploy behind TLS and avoid exposing the service directly to the public internet.
"""
import hmac
import os
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from .base import AuditLogger, SecurityException
from .models import SystemTaskPayload
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Location Exposure Agent — Rule Evaluation API",
    description="Deterministic threshold demonstration; no geohashing or zero-knowledge proof generation.",
    version="3.0.1",
)


def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    configured = os.getenv("API_ACCESS_TOKEN", "")
    if len(configured) < 16:
        raise HTTPException(status_code=503, detail="API_ACCESS_TOKEN must be configured with at least 16 characters.")
    if x_api_key is None or not hmac.compare_digest(x_api_key, configured):
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "zero-knowledge-location-exposure-agent", "version": "3.0.1"}


@app.get("/metrics", dependencies=[Depends(require_api_key)])
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
    }


@app.post("/api/audit", dependencies=[Depends(require_api_key)])
def api_audit(payload: SystemTaskPayload):
    try:
        return supervisor.process_task(payload).to_dict()
    except SecurityException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/chat", dependencies=[Depends(require_api_key)])
def api_chat(req: ChatRequest):
    try:
        return {"response": supervisor.query_supervisory_chat(req.query)}
    except SecurityException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/audit/logs", dependencies=[Depends(require_api_key)])
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
