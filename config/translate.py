static_translate = {
    "id": {
        "site_name": "WebsiteKu",
        "menu_home": "Beranda",
        "menu_services": "Layanan",
        "menu_blog": "Blog",
        "menu_about": "Tentang",
        "footer_text": "Hak Cipta © 2025 WebsiteKu"
    },

    # "en": {
    #     "site_name": "MyWebsite",
    #     "menu_home": "Home",
    #     "menu_services": "Services",
    #     "menu_blog": "Blog",
    #     "menu_about": "About",
    #     "footer_text": "Copyright © 2025 MyWebsite"
    # },
    
    "fr": {
        "site_name": "MonSite",
        "menu_home": "Accueil",
        "menu_services": "Services",
        "menu_blog": "Blog",
        "menu_about": "À propos",
        "footer_text": "Droits d'auteur © 2025 MonSite"
    },

    "ko": {
        "site_name": "내웹사이트",
        "menu_home": "홈",
        "menu_services": "서비스",
        "menu_blog": "블로그",
        "menu_about": "소개",
        "footer_text": "저작권 © 2025 내웹사이트"
    },

    "ja": {
        "site_name": "マイウェブサイト",
        "menu_home": "ホーム",
        "menu_services": "サービス",
        "menu_blog": "ブログ",
        "menu_about": "紹介",
        "footer_text": "著作権 © 2025 マイウェブサイト"
    }
}


LANGS = ["id", "fr", "ko", "ja"]
DEFAULT = "en"

def get_lang(lang: str) -> str:
    return lang if lang in LANGS else DEFAULT
