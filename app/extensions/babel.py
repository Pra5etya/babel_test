from flask_babel import Babel, gettext
from flask import request
from config.translate import static_translate, get_lang, DEFAULT

babel = None

def init_babel(app):
    global babel

    def locale_selector():
        # Ambil bahasa dari URL prefix (/id, /fr)
        lang = request.view_args.get("lang") if request.view_args else None

        # Jika tidak ada di URL, fallback ke query string ?lang=xx
        if not lang:
            lang = request.args.get("lang", DEFAULT)

        return get_lang(lang)

    babel = Babel(app, locale_selector=locale_selector)
    
    return babel
