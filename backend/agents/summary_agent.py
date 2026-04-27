def generate_summary(customer_id, old_name, new_name, old_score, new_score, forgery_flag):
    recommendation = "APPROVE" if old_score > 60 and new_score > 60 and forgery_flag == "PASS" else "REJECT"

    summary = f"""
    Customer ID: {customer_id}
    Requested Name Change: {old_name} -> {new_name}

    OCR Verification Results:
    - Old Name Confidence: {old_score}%
    - New Name Confidence: {new_score}%
    - Forgery Check: {forgery_flag}

    Recommended Action: {recommendation}
    """

    return summary.strip(), recommendation