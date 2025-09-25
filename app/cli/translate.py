from flask import Flask
from config.translate import LANGS
from googletrans import Translator  # pip install googletrans==4.0.0-rc1 (versi stabil)

import subprocess, click, os


def register_translate_cli(app: Flask):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    def extract():
        """Extract messages and generate messages.pot"""
        subprocess.run(
            ["pybabel", "extract", "-F", "babel.cfg", "-o", "messages.pot", "app"],
            check=True
        )
        click.echo("\n✅ Extraction complete: messages.pot generated")

    @translate.command()
    def init():
        """Initialize translations for all LANGS"""
        for lang in LANGS:
            subprocess.run(
                ["pybabel", "init", "-i", "messages.pot", "-d", "translations", "-l", lang],
                check=True
            )
            click.echo(f"\✅ Initialized translation for {lang}\n")

    @translate.command()
    def run():
        """Compile translations to .mo files"""
        subprocess.run(
            ["pybabel", "compile", "-d", "translations"],
            check=True
        )
        click.echo("\n✅ Translations compiled")

    @translate.command()
    def auto():
        """
        Automatically translate msgid -> msgstr in all LANGS
        Handles multi-line msgid and only fills empty msgstr.
        Shows progress in realtime.
        """
        po_dir = "translations"
        translator = Translator()
        total_files = 0

        if not os.path.exists(po_dir):
            click.echo(f"❌ Directory '{po_dir}' does not exist. Please check path.")
            return

        for lang in LANGS:
            lang_path = os.path.join(po_dir, lang, "LC_MESSAGES")
            if not os.path.exists(lang_path):
                click.echo(f"⚠️  No folder found for language '{lang}' at '{lang_path}'")
                continue

            po_files = [f for f in os.listdir(lang_path) if f.endswith(".po")]
            if not po_files:
                click.echo(f"⚠️  No .po files found for language '{lang}' in '{lang_path}'")
                continue

            for file in po_files:
                po_path = os.path.join(lang_path, file)
                click.echo(f"\nTranslating {po_path} → {lang}...")

                with open(po_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                new_lines = []
                inside_msgid = False
                msgid_text = ""
                msgid_lines = []
                translated_count = 0

                for line in lines:
                    stripped = line.strip()

                    if stripped.startswith("msgid"):
                        inside_msgid = True
                        msgid_lines = [line]
                        msgid_text = stripped[6:].strip('"')

                    elif inside_msgid and stripped.startswith('"'):
                        # Tambahkan baris multi-line msgid
                        msgid_text += stripped.strip('"')
                        msgid_lines.append(line)

                    elif inside_msgid and stripped.startswith("msgstr"):
                        current_msgstr = stripped[7:].strip('"')
                        new_lines.extend(msgid_lines)  # tulis kembali semua baris msgid
                        if not current_msgstr and msgid_text:
                            try:
                                translation = translator.translate(msgid_text, dest=lang).text

                            except Exception:
                                translation = msgid_text

                            new_lines.append(f'msgstr "{translation}"\n')
                            translated_count += 1

                            click.echo(f"  → Translated: {msgid_text[:50]}...")

                        else:
                            new_lines.append(line)
                            
                        inside_msgid = False
                        msgid_text = ""
                        msgid_lines = []

                    else:
                        new_lines.append(line)

                with open(po_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

                total_files += 1
                click.echo(f"✅ Finished {po_path} → {translated_count} strings translated")

        click.echo(f"\n🎉 Auto-translation completed for all LANGS in {total_files} file(s)")

    @translate.command()
    def update():
        """Update translations for all LANGS"""
        subprocess.run(
            ["pybabel", "update", "-i", "messages.pot", "-d", "translations"],
            check=True
        )
        click.echo("\n✅ Translations updated")

    @translate.command()
    def duplicate():
        """Remove all #, fuzzy in .po files"""
        po_dir = "translations"
        count = 0

        for root, dirs, files in os.walk(po_dir):
            for file in files:
                if file.endswith(".po"):
                    po_path = os.path.join(root, file)
                    with open(po_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    with open(po_path, "w", encoding="utf-8") as f:
                        for line in lines:
                            if not line.strip().startswith("#, fuzzy"):
                                f.write(line)
                    count += 1

        click.echo(f"\n✅ Removed all #, fuzzy in {count} .po file(s)")