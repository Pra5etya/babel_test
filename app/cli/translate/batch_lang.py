import re
from googletrans import Translator
from config.translate import (
    protect_tokens,
    restore_tokens,
    fix_punctuation_spacing,
    normalize_output,
)

# ==============================
# Init Google Translator
# ==============================
translator = Translator()


# ==============================
# Fungsi dasar translate
# ==============================
def base_translate(msgid_text: str, lang_code: str) -> str:
    """Fungsi dasar translasi yang aman. Dipakai oleh semua bahasa (bisa dioverride)."""
    if not msgid_text:
        return ""

    try:
        # Lindungi token & HTML
        safe_text, mapping = protect_tokens(msgid_text)

        # Translate
        translated = translator.translate(safe_text, dest=lang_code).text
        if translated.strip() == safe_text.strip():
            return ""

        # Restore token & rapikan hasil
        translation = restore_tokens(translated, mapping)
        translation = fix_punctuation_spacing(translation)
        translation = normalize_output(translation)
        return translation

    except Exception:
        return ""


# ==============================
# Utility sanitizer umum
# ==============================
def clean_tokens(text: str) -> str:
    """Hilangkan placeholder seperti [[t0]], [T0]], dsb."""
    # hapus pola [[t0]], [[t1]], dst
    text = re.sub(r"\[\[\s*t\d+\s*\]\]", "", text, flags=re.IGNORECASE)
    # hapus pola [T0]], [T1]], dst
    text = re.sub(r"\[\s*[Tt]\d+\s*\]\]", "", text)
    # hapus bracket nyasar
    text = re.sub(r"[［\[\]］]+", "", text)  # semua [] atau ［］ jadi hilang
    # rapikan spasi
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def normalize_po(text: str) -> str:
    """Normalisasi .PO / .Po → .po"""
    text = re.sub(r"\.\s*PO", ".po", text)
    text = re.sub(r"\.\s*Po", ".po", text)
    return text


# ==============================
# Bahasa spesifik
# ==============================
def translate_en(msgid_text: str) -> str:
    """Dummy translation untuk English (source language)."""
    return msgid_text


def translate_id(msgid_text: str) -> str:
    """Terjemahan ke Bahasa Indonesia"""
    text = base_translate(msgid_text, "id")
    if not text:
        return text

    # Override kata tertentu
    """ overrides = {
        "Website": "Situs Web",
        "website": "situs web",
        "Blog": "Blog",  # jangan diterjemahkan ke "Catatan Harian"
    }
    for src, target in overrides.items():
        text = text.replace(src, target) """

    text = normalize_po(text)
    text = clean_tokens(text)
    return text


def translate_fr(msgid_text: str) -> str:
    """Terjemahan ke Bahasa Prancis"""
    text = base_translate(msgid_text, "fr")
    if not text:
        return text

    text = normalize_po(text)
    text = clean_tokens(text)
    return text


def translate_ko(msgid_text: str) -> str:
    """Terjemahan ke Bahasa Korea"""
    text = base_translate(msgid_text, "ko")
    if not text:
        return text

    text = normalize_po(text)
    text = clean_tokens(text)
    return text


def translate_ja(msgid_text: str) -> str:
    """Terjemahan ke Bahasa Jepang"""
    text = base_translate(msgid_text, "ja")
    if not text:
        return text
    # Normalisasi 「...」。PO → .po
    text = re.sub(r"」?\s*。?\s*PO", ".po", text, flags=re.IGNORECASE)
    # Bersihkan bracket sisa 「] → 「
    text = text.replace("「]", "「").replace("]」", "」").replace("]。", "。")
    text = clean_tokens(text)
    return text


# ==============================
# Mapping agar mudah dipanggil
# ==============================
LANG_FUNCTIONS = {
    "en": translate_en,
    "id": translate_id,
    "fr": translate_fr,
    "ko": translate_ko,
    "ja": translate_ja,
}
