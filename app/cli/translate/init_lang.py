import subprocess, click
from config.translate import LANGS

def init_languages():
    """Initialize translations for all LANGS"""
    for lang in LANGS:
        subprocess.run(
            ["pybabel", "init", "-i", "messages.pot", "-d", "translations", "-l", lang],
            check=True
        )
        click.echo(f"✅ Initialized translation for {lang} \n")
