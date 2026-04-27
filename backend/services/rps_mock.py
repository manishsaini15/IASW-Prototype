from database.db import get_db_connection

def update_customer_name(customer_id, new_name):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE rps_customer_master
        SET full_name=?
        WHERE customer_id=?
    """, (new_name, customer_id))

    conn.commit()
    conn.close()