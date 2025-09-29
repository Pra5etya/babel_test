import re
from typing import Tuple, Dict

# ==============================
# Static Translations (untuk UI statis)
# ==============================
static_translate = {
    "en": {
        "site_name": "MyWebsite",
        "menu_home": "Home",
        "menu_services": "Services",
        "menu_blog": "Blog",
        "menu_about": "About",
        "footer_text": "Copyright © 2025 MyWebsite",
    },
    "id": {
        "site_name": "WebsiteKu",
        "menu_home": "Beranda",
        "menu_services": "Layanan",
        "menu_blog": "Blog",
        "menu_about": "Tentang",
        "footer_text": "Hak Cipta © 2025 WebsiteKu",
    },
    "fr": {
        "site_name": "MonSite",
        "menu_home": "Accueil",
        "menu_services": "Services",
        "menu_blog": "Blog",
        "menu_about": "À propos",
        "footer_text": "Droits d'auteur © 2025 MonSite",
    },
    "ko": {
        "site_name": "내웹사이트",
        "menu_home": "홈",
        "menu_services": "서비스",
        "menu_blog": "블로그",
        "menu_about": "소개",
        "footer_text": "저작권 © 2025 내웹사이트",
    },
    "ja": {
        "site_name": "マイウェブサイト",
        "menu_home": "ホーム",
        "menu_services": "サービス",
        "menu_blog": "ブログ",
        "menu_about": "紹介",
        "footer_text": "著作権 © 2025 マイウェブサイト",
    },
}

# Auto sync LANGS → tidak perlu hardcode
LANGS = list(static_translate.keys())

# Default language
DEFAULT = "en"


# ==============================
# Safe language resolver
# ==============================
def get_lang(lang: str) -> str:
    """
    Pastikan lang valid.
    - Jika ada di LANGS → return apa adanya.
    - Jika tidak → pakai DEFAULT.
    - Jika DEFAULT hilang → fallback ke bahasa pertama dari LANGS.
    - Jika LANGS kosong (misconfig) → pakai 'en'.
    """
    if lang in LANGS:
        return lang

    if DEFAULT in LANGS:
        return DEFAULT

    return LANGS[0] if LANGS else "en"


# ==============================
# Mapping ke Google Translate
# ==============================
GOOGLE_TRANS_LANGS = {
    "en": "en",
    "id": "id",
    "fr": "fr",
    "de": "de",
    "ar": "ar",
    "ja": "ja",
    "ko": "ko",
    # tambahkan sesuai kebutuhan
}


def normalize_lang(lang: str) -> str:
    """Convert LANGS entry into googletrans compatible code"""
    return GOOGLE_TRANS_LANGS.get(lang, lang.split("_")[0])


# ==============================
# Tokenizer → melindungi placeholder & HTML
# ==============================
def protect_tokens(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Freeze placeholders {var} dan HTML <...>
    Return (teks aman, mapping token->asli)
    """
    mapping = {}
    idx = 0

    def repl(m):
        nonlocal idx
        token = f"[[T{idx}]]"
        mapping[token] = m.group(0)
        idx += 1
        return token

    safe_text = re.sub(r"\{.*?\}|<.*?>", repl, text)
    return safe_text, mapping


def restore_tokens(text: str, mapping: Dict[str, str]) -> str:
    """Kembalikan token menjadi placeholder/HTML asli"""
    for token, original in mapping.items():
        text = text.replace(token, original)
    return text


# ==============================
# Output formatting
# ==============================
def fix_punctuation_spacing(text: str) -> str:
    """
    Pastikan ada spasi setelah titik.
    Contoh: "Halo.Dunia." -> "Halo. Dunia."
    """
    return re.sub(r"\.(\S)", r". \1", text)


def normalize_output(text: str) -> str:
    """Rapikan escape dan spasi"""
    return (
        text.replace('\\"', '"')
        .replace("  ", " ")
        .replace(" ]]", "]]")  # jaga bracket biar gak rusak
        .strip()
    )


def format_po_multiline(text: str, indent: str = "", width: int = 80) -> list[str]:
    """
    Format string ke format multi-line untuk .po file.
    Contoh:
    msgstr ""
    "Kalimat pertama "
    "lanjutan kalimat."
    """
    if not text:
        return ['msgstr ""\n']

    # Pisahkan ke beberapa baris agar tidak melebihi lebar
    chunks, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            chunks.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        chunks.append(line)

    result = ['msgstr ""\n']
    for chunk in chunks:
        result.append(f'"{chunk} "\n')

    return result
