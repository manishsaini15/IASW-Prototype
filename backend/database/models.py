from database.db import get_db_connection

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Pending Requests Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pending_requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT NOT NULL,
        change_type TEXT NOT NULL,
        old_value TEXT,
        new_value TEXT,
        extracted_old_value TEXT,
        extracted_new_value TEXT,
        confidence_old REAL,
        confidence_new REAL,
        forgery_flag TEXT,
        overall_confidence REAL,
        status TEXT DEFAULT 'AI_VERIFIED_PENDING_HUMAN',
        filenet_ref_id TEXT,
        ai_summary TEXT,
        checker_decision TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Mock RPS Customer Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS rps_customer_master (
        customer_id TEXT PRIMARY KEY,
        full_name TEXT
    )
    """)

    # Insert sample customer record (for demo)
    cur.execute("""
    INSERT OR IGNORE INTO rps_customer_master (customer_id, full_name)
    VALUES ('C001', 'Priya Sharma')
    """)

    conn.commit()
    conn.close()