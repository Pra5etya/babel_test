from flask import Flask

from .translate.extract import extract_messages
from .translate.init_lang import init_languages
from .translate.run_compile import compile_translations
from .translate.auto_translate import auto_translate
from .translate.update_lang import update_languages
from .translate.cleanup import cleanup_po_files

def register_translate_cli(app: Flask):
    @app.cli.group()
    def trans():
        """Translation and localization commands."""
        pass

    trans.command("extract")(extract_messages)
    trans.command("init")(init_languages)
    trans.command("run")(compile_translations)
    trans.command("auto")(auto_translate)
    trans.command("update")(update_languages)
    trans.command("clean")(cleanup_po_files)
