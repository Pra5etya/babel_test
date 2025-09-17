# app/babel.py
from flask_babel import Babel, gettext
from flask import request
from config.translate import static_translate, get_lang, DEFAULT

babel = None  # pegang instance global

def init_babel(app):
    """
    Inisialisasi Flask-Babel untuk dynamic translation
    """
    global babel

    def locale_selector():
        # view_args hanya ada kalau pakai <lang> di URL
        lang = None
        if request.view_args:
            lang = request.view_args.get("lang")
        if not lang:
            lang = request.args.get("lang", DEFAULT)
        return get_lang(lang)

    babel = Babel(app, locale_selector=locale_selector)
    return babel

def get_dynamic_translation():
    """
    Alias untuk gettext → dipakai di template
    """
    return gettext

def get_static_translation(lang):
    """
    Ambil dictionary static translation sesuai bahasa
    """
    return static_translate.get(lang, static_translate[DEFAULT])
