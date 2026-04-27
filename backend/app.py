from flask import Flask, render_template, request
import os
from config import UPLOAD_FOLDER
from database.models import init_db
from services.logger import log_event

from agents.validation_agent import validate_customer
from agents.document_processor_agent import extract_text_from_document
from agents.forensics_agent import simple_forgery_check
from agents.confidence_scorer import calculate_confidence
from agents.summary_agent import generate_summary

from services.filenet_mock import archive_document
from services.pending_service import insert_pending_request

from database.db import get_db_connection
from services.rps_mock import update_customer_name

app = Flask(__name__)

# Initialize DB
init_db()

@app.route("/")
def intake():
    return render_template("intake.html")

@app.route("/submit_request", methods=["POST"])
def submit_request():
    customer_id = request.form.get("customer_id")
    old_name = request.form.get("old_name")
    new_name = request.form.get("new_name")

    uploaded_file = request.files["document"]

    if not uploaded_file:
        return "No file uploaded"

    # Save file to uploads folder
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)

    log_event(f"[INTAKE] Request submitted | CustomerID={customer_id} | OldName={old_name} | NewName={new_name}")

    # Agent 1: Validate customer
    valid, existing_name = validate_customer(customer_id)
    if not valid:
        log_event(f"[VALIDATION FAILED] Customer not found: {customer_id}")
        return "Customer ID not found in RPS database!"

    log_event(f"[VALIDATION PASSED] Customer exists | CustomerID={customer_id} | RPS_Name={existing_name}")

    # Agent 2: OCR Extract text
    extracted_text = extract_text_from_document(file_path)
    log_event(f"[OCR] Extracted Text: {extracted_text}")

    # Agent 3: Forgery check
    forgery_flag = simple_forgery_check(extracted_text)
    log_event(f"[FORENSICS] ForgeryFlag={forgery_flag}")

    # Agent 4: Confidence scoring
    old_score, new_score, overall_conf = calculate_confidence(old_name, new_name, extracted_text)
    log_event(f"[CONFIDENCE] Old={old_score}% | New={new_score}% | Overall={overall_conf}%")

    # Agent 5: Summary generation
    summary, recommendation = generate_summary(customer_id, old_name, new_name, old_score, new_score, forgery_flag)
    log_event(f"[SUMMARY] Recommendation={recommendation}")

    # Archive document (Mock FileNet)
    filenet_ref_id, archived_path = archive_document(file_path)
    log_event(f"[FILENET MOCK] Archived Doc={archived_path} | RefID={filenet_ref_id}")

    # Insert into Pending Table
    insert_pending_request(
        customer_id, old_name, new_name,
        old_name, new_name,
        old_score, new_score,
        forgery_flag, overall_conf,
        filenet_ref_id, summary
    )

    log_event(f"[DB] Inserted into pending_requests table | Status=AI_VERIFIED_PENDING_HUMAN")

    return f"""
    Request successfully processed by AI Maker Agent! <br><br>
    <b>FileNet Reference:</b> {filenet_ref_id} <br>
    <b>Overall Confidence:</b> {overall_conf}% <br><br>
    <pre>{summary}</pre>
    """

@app.route("/checker")
def checker_dashboard():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM pending_requests WHERE status='AI_VERIFIED_PENDING_HUMAN'")
    rows = cur.fetchall()
    conn.close()

    return render_template("checker_dashboard.html", requests=rows)


@app.route("/review/<int:request_id>")
def review_request(request_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM pending_requests WHERE request_id=?", (request_id,))
    req = cur.fetchone()
    conn.close()

    return render_template("review_request.html", req=req)


@app.route("/approve/<int:request_id>", methods=["POST"])
def approve_request(request_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM pending_requests WHERE request_id=?", (request_id,))
    req = cur.fetchone()

    if req:
        customer_id = req["customer_id"]
        new_name = req["new_value"]

        # HITL: Only Checker triggers this update
        update_customer_name(customer_id, new_name)

        cur.execute("""
            UPDATE pending_requests
            SET status='APPROVED', checker_decision='APPROVED'
            WHERE request_id=?
        """, (request_id,))

        conn.commit()
        log_event(f"[CHECKER APPROVED] RequestID={request_id} | CustomerID={customer_id} | Updated RPS Name={new_name}")

    conn.close()
    return "Request Approved and RPS Updated! <br><a href='/checker'>Go Back</a>"


@app.route("/reject/<int:request_id>", methods=["POST"])
def reject_request(request_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE pending_requests
        SET status='REJECTED', checker_decision='REJECTED'
        WHERE request_id=?
    """, (request_id,))

    conn.commit()
    conn.close()

    log_event(f"[CHECKER REJECTED] RequestID={request_id}")

    return "Request Rejected! <br><a href='/checker'>Go Back</a>"

if __name__ == "__main__":
    app.run(debug=True)