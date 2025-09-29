import subprocess, click

def compile_translations():
    """Compile translations to .mo files"""
    subprocess.run(
        ["pybabel", "compile", "-d", "translations"],
        check=True
    )
    click.echo("\n✅ Translations compiled")
