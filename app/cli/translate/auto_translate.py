import os, click
from config.translate import LANGS, normalize_lang, format_po_multiline
from .batch_lang import LANG_FUNCTIONS


class PoTranslator:
    def __init__(self, lines, lang, translate_func):
        self.lines = lines
        self.lang = lang
        self.translate_func = translate_func
        self.new_lines = []
        self.translated_count = 0
        self.i = 0

    def parse_msgid(self):
        """Ambil msgid + continuation"""
        msgid_lines = [self.lines[self.i]]
        msgid_text = self.lines[self.i].strip()[6:].strip('"')
        self.i += 1

        while self.i < len(self.lines) and self.lines[self.i].strip().startswith('"'):
            msgid_text += self.lines[self.i].strip().strip('"')
            msgid_lines.append(self.lines[self.i])
            self.i += 1

        return msgid_text, msgid_lines

    def skip_old_msgstr(self):
        """Lompati blok msgstr lama"""
        start = self.i

        if self.i < len(self.lines) and self.lines[self.i].strip().startswith("msgstr"):
            self.i += 1

            while self.i < len(self.lines) and self.lines[self.i].strip().startswith('"'):
                self.i += 1

            click.echo(f"\n[DEBUG] Removing old msgstr from line {start} to {self.i-1}")

        return self.i

    def write_block(self, msgid_text, msgid_lines):
        """Tulis ulang msgid + msgstr baru"""
        self.new_lines.extend(msgid_lines)
        if msgid_text == "":  # header
            self.new_lines.append('msgstr ""\n')
            click.echo(f"\n[DEBUG] Empty header msgid on language {self.lang} → wrote empty header msgstr")

        else:
            translation = self.translate_func(msgid_text)
            if "\n" in translation:
                self.new_lines.append('msgstr ""\n')
                self.new_lines.extend(format_po_multiline(translation))

            else:
                self.new_lines.append(f'msgstr "{translation}"\n')
                
            click.echo(f"[INFO] Wrote translation: {translation[:60]} \n")

        self.translated_count += 1

    def process(self):
        """Loop semua baris dan proses"""
        while self.i < len(self.lines):
            if self.lines[self.i].strip().startswith("msgid"):
                msgid_text, msgid_lines = self.parse_msgid()
                self.skip_old_msgstr()
                self.write_block(msgid_text, msgid_lines)

            else:
                self.new_lines.append(self.lines[self.i])
                self.i += 1

        return self.new_lines, self.translated_count


def process_po_file(po_path, lang, translate_func):
    with open(po_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    translator = PoTranslator(lines, lang, translate_func)
    new_lines, count = translator.process()

    with open(po_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    click.echo(f"✅ Finished {po_path} → {count} strings translated")
    return count


def auto_translate():
    po_dir = "translations"
    total_files = 0

    if not os.path.exists(po_dir):
        click.echo(f"❌ Directory '{po_dir}' does not exist.")
        return

    for lang in LANGS:
        # lang_code = normalize_lang(lang)
        lang_path = os.path.join(po_dir, lang, "LC_MESSAGES")

        if not os.path.exists(lang_path):
            click.echo(f"⚠️  No folder for '{lang}' → skipped")
            continue

        if lang not in LANG_FUNCTIONS:
            click.echo(f"⚠️  No translation function for '{lang}' → skipped")
            continue

        po_files = [f for f in os.listdir(lang_path) if f.endswith(".po")]

        for file in po_files:
            po_path = os.path.join(lang_path, file)
            click.echo(f"\n🌍 Translating {po_path} → {lang}...")

            process_po_file(po_path, lang, LANG_FUNCTIONS[lang])
            total_files += 1

    click.echo(f"\n🎉 Auto-translation completed in {total_files} file(s)")