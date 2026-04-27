from database.db import get_db_connection

def insert_pending_request(customer_id, old_name, new_name,
                           extracted_old, extracted_new,
                           confidence_old, confidence_new,
                           forgery_flag, overall_confidence,
                           filenet_ref_id, ai_summary):
    
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO pending_requests (
        customer_id, change_type, old_value, new_value,
        extracted_old_value, extracted_new_value,
        confidence_old, confidence_new,
        forgery_flag, overall_confidence,
        status, filenet_ref_id, ai_summary
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        customer_id, "LEGAL_NAME",
        old_name, new_name,
        extracted_old, extracted_new,
        confidence_old, confidence_new,
        forgery_flag, overall_confidence,
        "AI_VERIFIED_PENDING_HUMAN",
        filenet_ref_id, ai_summary
    ))

    conn.commit()
    conn.close()