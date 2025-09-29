import os, click
from config.translate import LANGS, normalize_lang, format_po_multiline
from .batch_lang import LANG_FUNCTIONS

def auto_translate():
    """
    Automatically translate msgid -> msgstr in all LANGS.
    - Uses per-language functions from batch_lang.py
    """
    po_dir = "translations"
    total_files = 0

    if not os.path.exists(po_dir):
        click.echo(f"❌ Directory '{po_dir}' does not exist. Please check path.")
        return

    for lang in LANGS:
        lang_code = normalize_lang(lang)
        lang_path = os.path.join(po_dir, lang, "LC_MESSAGES")

        if not os.path.exists(lang_path):
            click.echo(f"⚠️  No folder found for language '{lang}' at '{lang_path}'")
            continue

        po_files = [f for f in os.listdir(lang_path) if f.endswith(".po")]
        if not po_files:
            click.echo(f"⚠️  No .po files found for language '{lang}' in '{lang_path}'")
            continue

        if lang not in LANG_FUNCTIONS:
            click.echo(f"⚠️  No translation function defined for '{lang}' → skipped")
            continue

        translate_func = LANG_FUNCTIONS[lang]

        for file in po_files:
            po_path = os.path.join(lang_path, file)
            click.echo(f"\n🌍 Translating {po_path} → {lang}...")

            with open(po_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            new_lines, msgid_text, msgid_lines = [], "", []
            inside_msgid, translated_count = False, 0

            for line in lines:
                stripped = line.strip()

                if stripped.startswith("msgid"):
                    inside_msgid, msgid_lines = True, [line]
                    msgid_text = stripped[6:].strip('"')

                elif inside_msgid and stripped.startswith('"'):
                    msgid_text += stripped.strip('"')
                    msgid_lines.append(line)

                elif inside_msgid and stripped.startswith("msgstr"):
                    current_msgstr = stripped[7:].strip('"')
                    new_lines.extend(msgid_lines)

                    if not current_msgstr and msgid_text:
                        translation = translate_func(msgid_text)
                        new_lines.extend(format_po_multiline(translation, indent="", width=80))

                        if translation:
                            translated_count += 1
                            click.echo(f"  ✔ {msgid_text[:50]}...")
                    else:
                        new_lines.append(line)

                    inside_msgid, msgid_text, msgid_lines = False, "", []

                else:
                    new_lines.append(line)

            with open(po_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            total_files += 1
            click.echo(f"✅ Finished {po_path} → {translated_count} strings translated")

    click.echo(f"\n🎉 Auto-translation completed for all LANGS in {total_files} file(s)")
