from flask import Flask

from .translate.extract import extract_messages
from .translate.init_lang import init_languages
from .translate.run_compile import compile_translations
from .translate.auto_translate import auto_translate
from .translate.update_lang import update_languages
from .translate.cleanup import cleanup_po_files

def register_translate_cli(app: Flask):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    translate.command("extract")(extract_messages)
    translate.command("init")(init_languages)
    translate.command("run")(compile_translations)
    translate.command("auto")(auto_translate)
    translate.command("update")(update_languages)
    translate.command("clean")(cleanup_po_files)
