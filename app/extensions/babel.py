from flask_babel import Babel
from flask import request
from config.translate import get_lang, DEFAULT, LANGS
import os

# Variabel global untuk menyimpan instance Babel
babel = None

def init_babel(app):
    global babel  

    def locale_selector():
        # 1. Cek apakah ada parameter "lang" di route (misalnya: /<lang>/page)
        lang = request.view_args.get("lang") if request.view_args else None

        # 2. Jika tidak ada, cek query string (?lang=id)
        if not lang:
            lang = request.args.get("lang")

        # 3. Jika masih kosong, coba cocokkan dengan header "Accept-Language"
        if not lang:
            lang = request.accept_languages.best_match(LANGS)

        # 4. Validasi: jika lang tidak ada atau tidak termasuk dalam daftar LANGS, pakai DEFAULT
        if not lang or lang not in LANGS:
            lang = DEFAULT

        # 5. Normalisasi/konversi kode bahasa (misalnya "id" → "id_ID")
        lang = get_lang(lang)

        # Log bahasa yang aktif
        print(f"\n[BABEL] Active lang: {lang}\n")

        return lang  # inilah yang akan dipakai Babel

    # Membuat instance Babel dan mengikatnya ke Flask app
    babel = Babel()
    babel.init_app(app, locale_selector = locale_selector)

    return babel  # kembalikan instance agar bisa dipakai di tempat lain
