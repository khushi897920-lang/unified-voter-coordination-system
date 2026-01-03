# Unified Voter Coordination System (PoC)

## Overview
India’s electoral system operates at massive scale and faces challenges such as
interstate migration, duplicate voter registrations, fragmented state databases,
and risks of electoral misuse.

This repository presents a **Proof of Concept (PoC)** for a **Unified Voter
Coordination System** that enables nationwide coordination **without
centralizing raw voter data**.

The system is designed with **state data sovereignty, privacy, and human
accountability** at its core.

---

## Core Design Principles
- **State Ownership:** Raw voter data remains with individual states.
- **No Centralized Voter Database:** Only encrypted coordination references are shared.
- **One Voter, One Active State:** A voter can be active in only one state at a time.
- **Lifecycle-Based Management:** Records are never deleted, only transitioned.
- **Human-in-the-Loop:** AI assists; final decisions remain with officers.

---

## System Architecture (Mapped to Code)

| Architectural Layer (Proposal) | Code Module |
|--------------------------------|-------------|
| State Voter Registration Layer | `state_layer` (via models & DB) |
| Cryptographic Transformation  | `crypto_layer` (simulated) |
| National Reference Layer      | `reference_layer.py` |
| Lifecycle & Deduplication     | `lifecycle_engine` (logic) |
| Migration Workflow            | `migration_workflow.py` |
| Voting Validation             | `voting_layer.py` |
| AI Advisory & Security        | `ai_advisory.py` |

---

## Voter Lifecycle States
- **ACTIVE** – Eligible to vote in current state
- **IN-TRANSFER** – Migration in progress
- **INACTIVE** – Migrated out / not eligible
- **BLOCKED** – Deceased or legally disqualified

**Rule:** At any time, a voter can have only **one ACTIVE state**.

---

## Key Flows Demonstrated in This PoC

### 1. Voter Registration
- Voter registers in a state
- A cryptographic reference ID is generated
- State record becomes ACTIVE

### 2. Interstate Migration
- New state requests migration
- Reference layer checks existing ACTIVE status
- Old state releases voter
- New state activates voter
- Status transitions are audited

### 3. Voting Validation
- Voter allowed to vote only if:
  - Status = ACTIVE
  - Has not voted in the current election cycle

---

## Role of AI (Advisory Only)
AI is used strictly as a **support layer**, not a decision-maker.

AI assists with:
- Flagging possible duplicate registrations
- Detecting suspicious registration patterns
- Prioritizing migration requests
- Data quality suggestions

**AI has no access to raw voter data and cannot modify records.**

---

## Security & Privacy
- Raw voter data never leaves the state
- Only encrypted reference IDs are shared
- No biometric or demographic data is centralized
- All critical actions are auditable
- System remains safe even if AI is compromised

---

## What This PoC Intentionally Does NOT Implement
- Aadhaar or real biometric integration
- Real Zero-Knowledge Proof cryptography
- Production-grade AI models
- Blockchain or national-scale infrastructure

These are considered **future extensions** beyond the scope of a hackathon PoC.

---

## Tech Stack
- **Backend:** Python (FastAPI)
- **Database:** SQLite
- **Architecture Style:** Modular, API-driven
- **AI:** Rule-based simulation

---

## How to Run (Local)
```bash
pip install -r requirements.txt
uvicorn main:app --reload

> This repository focuses on explainability and system design clarity rather than production-scale implementation.
