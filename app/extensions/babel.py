from flask_babel import Babel
from flask import request
from config.translate import get_lang, DEFAULT, LANGS

babel = None

def init_babel(app):
    global babel

    def locale_selector():
        # 1. Ambil dari URL prefix (request.view_args)
        lang = request.view_args.get("lang") if request.view_args else None

        # 2. Ambil dari query string
        if not lang:
            lang = request.args.get("lang")

        # 3. Ambil dari Accept-Language browser
        if not lang:
            lang = request.accept_languages.best_match(LANGS)

        # 4. Fallback ke default
        if not lang or lang not in LANGS:
            lang = DEFAULT

        lang = get_lang(lang)

        print(f"[BABEL] Active lang: {lang}")
        return lang

    babel = Babel()
    babel.init_app(app, locale_selector=locale_selector)

    return babel
