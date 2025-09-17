# Flask-Babel = alat untuk membuat aplikasi Flask multi-bahasa.

Menangani:
* Terjemahan teks (i18n)
* Pemilihan bahasa otomatis
* Format tanggal/waktu/angka sesuai lokal (l10n)

# Context processor untuk static translate (t tersedia di semua template)
    @app.context_processor -> untuk di bawah langsung core
    @bp.app_context_processor -> untuk di dalam blueprint

# penggunaan babel
1. ditandai di halaman (gettext atau _)


# Step babel
1. pybabel extract -F babel.cfg -o messages.pot .
2. pybabel init -i messages.pot -d app/translations -l de
3. pybabel compile -d app/translations
