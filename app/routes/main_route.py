from flask import Blueprint, render_template, request, redirect, url_for
from config.translate import get_lang, DEFAULT, LANGS
from app.extensions.babel import get_static_translation, get_dynamic_translation

main_bp = Blueprint("main", __name__, url_prefix="/<lang>")

# Middleware: validasi bahasa dari URL
@main_bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    if values:
        lang = values.get("lang", DEFAULT)
        values["lang"] = get_lang(lang)

# Context Processor: inject t_static, gettext, dan current_lang
@main_bp.app_context_processor
def inject_translations():
    from app.extensions.babel import gettext  # impor supaya selalu sync

    lang = request.view_args.get("lang", DEFAULT)
    lang = get_lang(lang)

    return {
        "t_static": get_static_translation(lang),       # statis → dict
        "t_dynamic": get_dynamic_translation(lang),     # dinamis → gettext()
        "current_lang": lang
    }

# Middleware root redirect
@main_bp.before_app_request
def redirect_root():
    if request.path == "/":
        accept_lang = request.headers.get("Accept-Language", "")
        preferred = accept_lang.split(",")[0].split("-")[0] if accept_lang else DEFAULT
        lang = get_lang(preferred)

        return redirect(url_for("main.index", lang=lang))

    parts = request.path.strip("/").split("/")
    
    if parts and parts[0] not in LANGS:
        return redirect(url_for("main.index", lang=get_lang(DEFAULT)))

# Routes
@main_bp.route("/")
def index(lang):
    return render_template("layouts/index.html")

@main_bp.route("/about")
def about(lang):
    return render_template("layouts/about.html")
