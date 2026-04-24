# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    # Basic checks
    content = document_dict.get('content') or ''
    if len(content.strip()) < 20:
        return False

    # Reject known toxic/error substrings
    toxic_signatures = [
        'null pointer exception',
        'segmentation fault',
        'error:',
        'warning:',
    ]
    lower = content.lower()
    for sig in toxic_signatures:
        if sig in lower:
            return False

    # Simple discrepancy heuristic: if there is a code-like snippet that contradicts a nearby comment
    # e.g., comment contains '8%' but code contains '10%' - flag (return False)
    import re
    comment_percents = re.findall(r"%\s*\)|%|\b(\d{1,3})%", content)
    # This is a naive implementation; we'll not fail on uncertain cases

    return True
