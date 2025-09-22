from flask import Flask
from config.translate import LANGS

import subprocess, click


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
    def update():
        """Update translations for all LANGS"""
        subprocess.run(
            ["pybabel", "update", "-i", "messages.pot", "-d", "translations"],
            check=True
        )

        click.echo("\n✅ Translations updated")

    @translate.command()
    def compile():
        """Compile translations to .mo files"""
        subprocess.run(
            ["pybabel", "compile", "-d", "translations"],
            check=True
        )

        click.echo("\n✅ Translations compiled")
