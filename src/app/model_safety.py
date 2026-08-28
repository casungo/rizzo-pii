"""Guardie leggere per gli output del modello che non hanno una forma PII."""

import re


_CURRENCY = re.compile(r"(?i)(?:€|\b(?:eur|euro|usd|dollar[io]?|gbp|sterlin[ae]|chf)\b)")


def keep(label, text, start, end):
    """Un AMOUNT nudo e' un numero ambiguo, non un importo affidabile."""
    if label != "AMOUNT":
        return True
    return bool(_CURRENCY.search(text[max(0, start - 8):min(len(text), end + 8)]))
