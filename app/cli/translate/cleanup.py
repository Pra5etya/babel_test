import os, click

def cleanup_po_files():
    """Remove all #, fuzzy in .po files"""
    po_dir = "translations"
    count = 0

    for root, _, files in os.walk(po_dir):
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
