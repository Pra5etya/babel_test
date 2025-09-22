from flask import Blueprint, render_template, request, redirect, url_for
from flask_babel import gettext
from config.translate import get_lang, static_translate, DEFAULT, LANGS

# Semua route otomatis prefix bahasa
main_bp = Blueprint("main", __name__, url_prefix="/<lang>")

# 🔹 Validasi bahasa dari URL
@main_bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    if values:
        lang = values.get("lang", DEFAULT)
        values["lang"] = get_lang(lang)


# 🔹 Inject helper ke template
@main_bp.app_context_processor
def inject_translations():
    lang = request.view_args.get("lang", DEFAULT)
    lang = get_lang(lang)

    return {
        "t_static": static_translate.get(
            lang, 
            static_translate[DEFAULT]
            ),   # static translate di HTML
        
        "gettext" : gettext,

        "current_lang": lang                        # ambil list language dari endpoint
    }


# 🔹 Middleware untuk redirect root `/` → default/lang
@main_bp.before_app_request
def redirect_root():
    if request.path == "/":
        # Gunakan header Accept-Language untuk default
        accept_lang = request.headers.get("Accept-Language", "")
        preferred = accept_lang.split(",")[0].split("-")[0] if accept_lang else DEFAULT
        lang = get_lang(preferred)

        return redirect(url_for("main.index", lang=lang))

    # Kalau prefix salah, redirect ke default
    parts = request.path.strip("/").split("/")
    if parts and parts[0] not in LANGS:
        return redirect(url_for("main.index", lang=get_lang(DEFAULT)))


# 🔹 Routes
@main_bp.route("/")
def index(lang):
    print(gettext("Hello from Python code!"))  # contoh dynamic translation
    return render_template("layouts/index.html")

@main_bp.route("/about")
def about(lang):
    return render_template("layouts/about.html")
