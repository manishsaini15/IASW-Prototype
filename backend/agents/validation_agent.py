from database.db import get_db_connection

def validate_customer(customer_id):
    """
    Validates whether customer exists in mock RPS database.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM rps_customer_master WHERE customer_id=?", (customer_id,))
    customer = cur.fetchone()
    conn.close()

    if customer:
        return True, customer["full_name"]
    else:
        return False, None