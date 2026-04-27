def simple_forgery_check(extracted_text):
    """
    Simple quality check: if extracted text is too short, flag as suspicious.
    """
    if len(extracted_text) < 20:
        return "FLAG"
    return "PASS"