import subprocess, click

def update_languages():
    """Update translations for all LANGS"""
    subprocess.run(
        ["pybabel", "update", "-i", "messages.pot", "-d", "translations"],
        check=True
    )
    click.echo("\n✅ Translations updated")
