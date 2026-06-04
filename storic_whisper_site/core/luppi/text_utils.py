"""Text matching helpers — avoid false positives (e.g. 'ai' inside 'pain')."""
import re


def term_in_text(term: str, text: str) -> bool:
    """Substring match with word boundaries for short terms (≤3 chars)."""
    term = term.lower().strip()
    text = text.lower()
    if len(term) <= 3:
        return bool(re.search(r'(?<!\w)' + re.escape(term) + r'(?!\w)', text))
    return term in text
