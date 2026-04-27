
---

# ✅ STEP 5C: Create Solution Design Report (Mandatory)

📌 `docs/Solution_Design_Report.md`

```md
# IASW - Solution Design and Implementation Report

## 1. Executive Summary
This project implements a prototype Intelligent Account Servicing Workflow (IASW) for banking account change requests.
The AI system automates the Maker role (document OCR, validation, scoring) while enforcing a strict Human-in-the-Loop (HITL)
Checker approval before updating the core banking system.

This prototype demonstrates a complete Legal Name Change workflow.

---

## 2. Problem Understanding & Scope
Banks process thousands of account change requests daily. Manual processing is slow, error-prone, and expensive.
IASW automates document verification and data validation while maintaining regulatory compliance.

### Scope Implemented
- Legal Name Change request flow
- OCR-based extraction of document text
- Confidence scoring
- Pending request staging in relational database
- Checker UI for approval/rejection
- Mock RPS update only after checker approval
- Mock FileNet archival
- Audit logging

---

## 3. Solution Architecture

### Architecture Components
- Staff Intake UI (Frontend HTML form)
- Flask Backend API
- Validation Agent (RPS lookup)
- Document Processor Agent (OCR extraction)
- Forensics Agent (basic forgery/quality check)
- Confidence Scorer Agent
- Summary Agent
- SQLite Pending Table
- Checker UI Dashboard + Review Screen
- FileNet Mock Storage (local archived docs)
- Mock RPS System (SQLite table)
- Observability Layer (audit.log)

---

## 4. Architecture Diagram (Mermaid)

```mermaid
flowchart TD

A[Staff Intake UI] --> B[Flask Backend]
B --> C[Validation Agent]
B --> D[Document Processor OCR Agent]
D --> E[Forensics Agent]
E --> F[Confidence Scorer]
F --> G[Summary Agent]

G --> H[(Pending Table SQLite)]
D --> I[FileNet Mock Archive]

H --> J[Checker Dashboard UI]
J --> K[Review Request Screen]

K -->|Approve| L[Mock RPS Update Service]
K -->|Reject| M[Update Status Rejected]

L --> N[(RPS Customer Master Table)]