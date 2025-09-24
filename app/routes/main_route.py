from flask import Blueprint, render_template, request, redirect, url_for
from flask_babel import gettext
from config.translate import get_lang, static_translate, DEFAULT, LANGS

# ======================================================
# Blueprint dengan prefix bahasa di URL
# ======================================================
main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/<lang>",
)


# ======================================================
# Validasi bahasa dari URL prefix
# ======================================================
@main_bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    if values:
        values["lang"] = get_lang(values.get("lang", DEFAULT))


# ======================================================
# Inject helper ke template (Jinja bisa langsung akses)
# ======================================================
@main_bp.app_context_processor
def inject_translations():
    # Ambil bahasa aktif dari Babel agar konsisten
    from flask_babel import get_locale
    
    lang = str(get_locale())
    t_static = static_translate.get(lang, static_translate[DEFAULT])

    return {
        "t_static": t_static,
        "gettext": gettext(),
        "current_lang": lang,
        "LANGS": LANGS,
    }



# ======================================================
# Middleware: validasi prefix bahasa
# ======================================================
@main_bp.before_app_request
def validate_lang_prefix():
    # 🚨 Abaikan request ke static dan favicon.ico
    if request.endpoint and (
        request.endpoint.startswith("static")
        or request.path.startswith("/favicon.ico")
    ):
        return None

    # validasi prefix bahasa
    parts = request.path.strip("/").split("/")
    if parts and parts[0] not in LANGS:
        return redirect(url_for("main.index", lang=get_lang(DEFAULT)))


# ======================================================
# Routes
# ======================================================
@main_bp.route("")
def index(lang):
    return render_template("layouts/index.html")


@main_bp.route("/about")
def about(lang):
    return render_template("layouts/about.html")
