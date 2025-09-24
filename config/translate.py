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
