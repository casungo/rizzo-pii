"""Riusa un dizionario di una serie senza cambiare i placeholder esistenti."""

import re


_PLACEHOLDER = re.compile(r"^\[([A-Z_]+)_(\d+)\]$")


def seed(mapping, valid_labels):
    if mapping is None:
        return {}, {}, {}
    if not isinstance(mapping, dict):
        raise ValueError("Il dizionario della serie deve essere un oggetto JSON.")
    counters, seen, out = {}, {}, {}
    for placeholder, value in mapping.items():
        match = _PLACEHOLDER.fullmatch(str(placeholder))
        if not match or match.group(1) not in valid_labels or not isinstance(value, str):
            raise ValueError("Il dizionario della serie contiene un placeholder non valido.")
        label, number = match.group(1), int(match.group(2))
        key = (label, re.sub(r"\s+", " ", value.strip()).casefold())
        if key in seen and seen[key] != placeholder:
            raise ValueError("Il dizionario della serie assegna due ID allo stesso valore.")
        counters[label] = max(counters.get(label, 0), number)
        seen[key], out[placeholder] = placeholder, value
    return counters, seen, out
