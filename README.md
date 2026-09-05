# Zero Knowledge Location Exposure Agent

> **Domain:** Clinical Decision Support & Biomedical Computing  
> **Reference Guidelines & Standards:** `Standard Clinical Formulations & ISO/IEC Quality Frameworks`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Zero Knowledge Location Exposure Agent** is an advanced analytical and computational platform implementing Geohash trajectory blinded Bloom filter zero-knowledge contact tracing agent.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization with automated clinical/operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection.

---

## 💻 CLI Quickstart & Usage

### Prerequisites
```bash
# Set the required audit secret key (minimum 32 characters)
export AUDIT_SECRET_KEY="your-cryptographic-audit-secret-key-here-min-32-chars"
```

### 1. Run Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target TARGET-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Query the Supervisory Chat
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Process CSV Records
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch FastAPI REST Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### CLI Commands Reference

| Command | Description | Key Arguments |
|:--------|:------------|:--------------|
| `audit` | Run single task evaluation | `--task-id`, `--target`, `--primary`, `--secondary`, `--critical`, `--status` |
| `chat` | System configuration query | `query` (positional, multiple words accepted) |
| `batch` | Batch process CSV records | `-i/--input` (required), `-o/--output` (default: results.csv) |
| `verify-audit` | Verify HMAC audit trail integrity | None |
| `serve` | Launch FastAPI REST server | `--host` (default: 127.0.0.1), `--port` (default: 8000) |

### Input Data Schema

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Unique task / case identifier | Required |
| `target_identifier` | Entity, patient key, or target | Required |
| `primary_metric` | Primary domain measurement or score | Required |
| `secondary_metric` | Secondary kinetic or confidence score | Optional (default: 0.0) |
| `is_critical_flag` | Emergency escalation trigger | Optional (default: false) |
| `status_descriptor` | Status code or phenotype descriptor | Optional (default: NOMINAL) |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active AST and regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
# Set audit key for tests (or rely on conftest.py auto-configuration)
export AUDIT_SECRET_KEY="test-audit-secret-key-for-testing-only-32chars"
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

### Test Coverage

- **PHI Guard Enforcement**: Validates zero-PHI outbound interceptor blocks sensitive identifiers
- **Specialized Workers**: Tests InvariantQCWorker, SafetyEscalationWorker, ProtocolConformanceWorker
- **Supervisor Consensus**: Verifies multi-agent consensus and HMAC-SHA256 audit trail integrity
- **ZK Contact Trace**: Tests GeohashBloomFilterAgent, BlindedContactMatcherAgent, ExposureRiskScorerAgent
- **Enrichment Suite**: Validates threshold-based evaluation engines

---

## 🐳 Container Deployment

```bash
docker build -t zero-knowledge-location-exposure-agent .
docker run -p 8000:8000 zero-knowledge-location-exposure-agent
```
