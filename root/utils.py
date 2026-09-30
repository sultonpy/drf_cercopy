def pick_lang(obj, base, request=None):
    """title_uz / title_ru maydonlaridan so'ralgan tilni tanlaydi (?lang=ru)."""
    lang = request.query_params.get("lang", "uz") if request is not None else "uz"
    if lang not in ("uz", "ru"):
        lang = "uz"
    return getattr(obj, f"{base}_{lang}", "") or getattr(obj, f"{base}_uz", "")