from difflib import SequenceMatcher

def similarity_score(a, b):
    """
    Returns similarity percentage between two strings.
    """
    return round(SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100, 2)

def calculate_confidence(old_name, new_name, extracted_text):
    """
    Checks if old/new name exist in extracted OCR text and generates confidence.
    """
    old_score = similarity_score(old_name, extracted_text)
    new_score = similarity_score(new_name, extracted_text)

    overall = round((old_score + new_score) / 2, 2)

    return old_score, new_score, overall