# Intelligent Account Servicing Workflow (IASW) - Prototype

## Overview
This project is a prototype implementation of an Intelligent Account Servicing Workflow (IASW) for banks.
It automates document verification and data validation for customer account change requests using an AI Maker Agent,
while strictly enforcing Human-in-the-Loop (HITL) approval before updating the core system.

## Supported Flow
✅ Legal Name Change Workflow (End-to-End)

## Workflow Steps
1. Staff submits name change request + uploads supporting document.
2. AI Maker Agents perform:
   - Customer validation (mock RPS check)
   - OCR extraction (Tesseract)
   - Forgery/quality check
   - Confidence scoring
   - Summary generation
3. Request stored in Pending Table (`AI_VERIFIED_PENDING_HUMAN`)
4. Checker reviews request and manually approves/rejects.
5. If approved, mock RPS system is updated.

## Tech Stack
- Backend: Flask (Python)
- OCR: Tesseract OCR + pdf2image
- Database: SQLite
- Document Archival: Local filesystem mock (FileNet mock)
- Observability: Audit logs (`logs/audit.log`)

---

## Setup Instructions

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate