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


# String Extracted

1. Penggunaan string yang ada di html untuk di translasi jangan dipisahkan perbaris (gunakan gettext atau _), misal
    ```html
    <p>
      {{ _("In addition, this system will also be tested across different devices, 
            "from desktops with large screens to mobile phones with smaller displays. "
            "Longer text like this is useful to test how responsive design behaves. "
            "Will the text remain neatly formatted when wrapped, or will it cause layout issues instead?"
      ) }}
    </p>

    tapi seperti berikut:

    <p>
      {{ _("In addition, this system will also be tested across different devices, 
           from desktops with large screens to mobile phones with smaller displays. 
           Longer text like this is useful to test how responsive design behaves. 
           Will the text remain neatly formatted when wrapped, or will it cause layout issues instead?") }}
    </p>
    ```


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

# Step babel
1. pybabel extract -F babel.cfg -o messages.pot app
2. pybabel init -i messages.pot -d translations -l (berdasarkan kode di babel) -> dilakukan sekali saja
3. pybabel compile -d translations
4. pybabel update -i messages.pot -d translations   (Gunakan jika ada terjemahan baru baru)


## ⚡ Ringkasnya:
* Kalau source code berubah → extract + init(sekali saja) + edit .po + update + compile
* Kalau hanya isi terjemahan berubah → cukup compile saja


# 📊 Perbandingan Tools Translasi .po

| Tool / Platform                    | Open Source?                           | Mode Kerja                       | Kelebihan                                                                 | Kekurangan                                                |
| ---------------------------------- | -------------------------------------- | -------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------- |
| **Poedit**                         | ❌ (proprietary, tapi ada versi gratis) | Aplikasi desktop (Win/Mac/Linux) | Mudah dipakai, ada memory, bisa auto-suggest, ada QA check                | Closed-source, fitur MT penuh butuh Pro                   |
| **Weblate**                        | ✅ (GPLv3)                              | Web-based, bisa self-host        | Full control (server sendiri), collaborative, integrasi Git, ada QA check | Setup agak berat (butuh server), lebih cocok untuk tim    |
| **Pootle**                         | ✅ (GPLv3)                              | Web-based, self-host             | Open source, fokus ke `.po`, cocok untuk komunitas                        | Development sudah tidak aktif, UI agak ketinggalan zaman  |
| **POEditor**                       | ❌ (SaaS)                               | Web-based (cloud)                | Mudah dipakai, banyak integrasi                                           | Data di server pihak ketiga, berbayar untuk fitur lengkap |
| **Crowdin / Transifex**            | ❌ (SaaS)                               | Web-based (cloud)                | Banyak fitur enterprise, integrasi CI/CD                                  | Tidak open source, data ada di server mereka              |
| **Manual (VS Code, Vim, Sublime)** | ✅ (editor-nya open source/free)        | Text editor                      | Kendali penuh, ringan, bisa pakai plugin gettext                          | Tidak ada fitur bantu (TM, QA check, glossary)            |