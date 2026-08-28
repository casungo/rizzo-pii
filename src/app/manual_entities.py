"""Entita' scelte esplicitamente dall'utente, validate senza il modello."""


def candidates(text, entities, valid_labels):
    """Converte le selezioni manuali in candidati sicuri per ``_merge``."""
    if entities is None:
        return []
    if not isinstance(entities, list):
        raise ValueError("Le selezioni manuali devono essere una lista.")

    out = []
    for entity in entities:
        if not isinstance(entity, dict):
            raise ValueError("Ogni selezione manuale deve essere un oggetto.")
        start, end = entity.get("start"), entity.get("end")
        label = str(entity.get("label", "")).strip().upper()
        if (isinstance(start, bool) or isinstance(end, bool)
                or not isinstance(start, int) or not isinstance(end, int)
                or not 0 <= start < end <= len(text)):
            raise ValueError("Intervallo di selezione manuale non valido.")
        if label not in valid_labels:
            raise ValueError(f"Tag manuale sconosciuto: {label or '(vuoto)'}.")
        if not text[start:end].strip():
            raise ValueError("La selezione manuale non puo' contenere solo spazi.")
        out.append({"label": label, "start": start, "end": end, "score": 1.0,
                    "validated": True, "source": "manuale"})
    return out
