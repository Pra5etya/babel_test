from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_babel import gettext, get_locale
from config.translate import get_lang, static_translate, DEFAULT, LANGS

# ======================================================
# Blueprint
# ======================================================
main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/<lang>",  # setiap route di blueprint ini akan diawali /<lang>
)


# ======================================================
# Preprocessor: validasi & normalisasi kode bahasa
# Dipanggil sebelum request diproses
# ======================================================
@main_bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    if values:
        # Ambil lang dari URL, jika tidak ada fallback ke DEFAULT
        # lalu normalisasi dengan get_lang (misalnya 'id' → 'id_ID')
        values["lang"] = get_lang(values.get("lang", DEFAULT))


# ======================================================
# Inject helper ke template
# ======================================================
@main_bp.app_context_processor
def inject_translations():
    # Bahasa aktif berdasarkan Babel
    lang = str(get_locale())

    # Ambil static translations sesuai locale
    t_static = static_translate.get(lang, static_translate[DEFAULT])

    return {
        "t_static": t_static,      # dictionary translasi statis
        "current_lang": lang,      # bahasa aktif
        "LANGS": LANGS,            # daftar bahasa yang tersedia
    }


# ======================================================
# Middleware: validasi prefix bahasa di setiap request
# ======================================================
@main_bp.before_app_request
def validate_lang_prefix():
    # 🚨 Abaikan request ke static dan favicon.ico agar tidak dipaksa redirect
    if request.endpoint and (
        request.endpoint.startswith("static")
        or request.path.startswith("/favicon.ico")
    ):
        return None

    # Pisahkan URL → ambil segmen pertama (prefix bahasa)
    parts = request.path.strip("/").split("/")

    # Jika prefix tidak valid (tidak ada di LANGS), redirect ke default
    if parts and parts[0] not in LANGS:
        return redirect(url_for("main.index", lang=get_lang(DEFAULT)))


# ======================================================
# Routes
# ======================================================
@main_bp.route("")
def index(lang):
    # halaman utama
    return render_template("layouts/index.html")


@main_bp.route("/about")
def about(lang):
    # halaman about
    return render_template("layouts/about.html")


# ======================================================
# Debug
# ======================================================
@main_bp.route("/debug")
def debug_babel(lang = None):
    import os, re, polib

    # Lokasi direktori templates
    templates_dir = os.path.join(current_app.root_path, "templates")
    msgids = {}

    # Regex untuk mencari gettext("...") atau gettext('...')
    pattern = re.compile(r'gettext\(\s*[\"\'](.+?)[\"\']\s*\)')

    # Walk seluruh file .html dalam templates
    for root, _, files in os.walk(templates_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    found = pattern.findall(content)  # cari msgid
                    if found:
                        msgids[file_path] = found

    # Lokasi file .mo aktif berdasarkan locale
    locale = str(get_locale())

    trans_dirs = current_app.config.get("BABEL_TRANSLATION_DIRECTORIES", "translations")
    abs_dirs = [os.path.abspath(d) for d in trans_dirs.split(";")]
    mo_file = os.path.join(abs_dirs[0], locale, "LC_MESSAGES", "messages.mo")

    # Parse isi .mo untuk ambil msgid → msgstr
    mo_entries = {}
    if os.path.exists(mo_file):
        po = polib.mofile(mo_file)
        
        for entry in po:
            mo_entries[entry.msgid] = entry.msgstr

    # Hasil perbandingan runtime gettext vs isi .mo
    results = {}
    for file, msgids_list in msgids.items():
        results[file] = {}
        for msgid in msgids_list:
            results[file][msgid] = {
                "gettext_result": gettext(msgid),          # hasil translasi runtime
                "msgstr_in_mo": mo_entries.get(msgid, None),  # isi msgstr di file .mo
            }

    # Buat info debugging lengkap
    debug_info = {
        "requested_path": request.path,
        "active_locale": locale,
        "LANGS_available": LANGS,
        "msgids_found": msgids,
        "translations": results,
        "mo_file_used": mo_file if os.path.exists(mo_file) else None,
    }

    # Simpan ke log Flask
    current_app.logger.info(f"[DEBUG] {debug_info}")

    # Tampilkan hasil debugging sebagai JSON/dict
    return debug_info
