import subprocess, click

def extract_messages():
    """Extract messages and generate messages.pot"""
    subprocess.run(
        ["pybabel", "extract", "-F", "babel.cfg", "-o", "messages.pot", "app"],
        check=True
    )
    click.echo("\n✅ Extraction complete: messages.pot generated")
