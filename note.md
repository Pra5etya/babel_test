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
2. pastikan pakai " bukan ' karena extractor jinja2 lebih konsisten nangkep double-quoted strings.


# Step babel
1. pybabel extract -F babel.cfg -o messages.pot app --ignore-dir=win_env --verbose

    ```bash
    pybabel extract -F babel.cfg -o messages.pot . \
  --ignore-dir=win_env \
  --ignore-dir=config

    ```

2. pybabel init -i messages.pot -d app/translations -l (kode translate yang di inginkan) -> penyesuaian di babel

3. pybabel compile -d app/translations



# Jika terdapat dua kata misal:
Kamu mau kasus seperti ini: "saham merupakan IPO"

* dimana sebagian kata (IPO) tidak ikut diterjemahkan, tapi sisanya ikut sistem translasi.

1. Gunakan placeholder variabel di gettext
    ```bash
    gettext("Saham merupakan %(ipo)s", ipo="IPO")
    ```

    .po file translator akan melihat string:
    ```bash
    msgid "Saham merupakan %(ipo)s"
    msgstr "Stock is %(ipo)s"
    ```

