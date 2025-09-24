from flask_babel import Babel
from flask import request
from config.translate import get_lang, DEFAULT

babel = None

def init_babel(app):
    global babel

    def locale_selector():
        """
        Tentukan bahasa aktif.
        - Ambil dari URL prefix (/<lang>)
        - Kalau tidak ada, fallback ke query string ?lang=xx
        - Kalau tetap tidak ada, fallback ke DEFAULT
        """
        lang = None

        # Dari URL prefix (/<lang>/...)
        if request.view_args:
            lang = request.view_args.get("lang")

        # Dari query string ?lang=xx
        if not lang:
            lang = request.args.get("lang", DEFAULT)

        return get_lang(lang)

    babel = Babel()
    babel.init_app(app, locale_selector=locale_selector)

    return babel
