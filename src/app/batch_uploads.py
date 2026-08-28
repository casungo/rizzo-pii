"""Testo di piu' allegati, senza esporre i loro nomi nel risultato."""


def join_texts(texts):
    """Separa i documenti senza spezzare il dizionario dell'anonimizzazione."""
    return "\n\n".join(f"--- DOCUMENTO {i} ---\n\n{text}"
                       for i, text in enumerate(texts, 1))
