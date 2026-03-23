"""
bundle.py — Génère un fichier HTML unique auto-suffisant
Usage : python3 bundle.py
Résultat : onco_complet.html (tout-en-un, partageable sans dépendances)
"""

import html
from pathlib import Path

BASE = Path(__file__).parent.resolve()

IFRAMES = {
    'flashcards.html':      BASE / 'flashcards.html',
    'fiches_revision.html': BASE / 'fiches_revision.html',
}

def bundle():
    hub_path = BASE / 'revision.html'
    if not hub_path.exists():
        print("ERREUR : revision.html introuvable dans", BASE)
        return

    content = hub_path.read_text(encoding='utf-8')

    for fname, fpath in IFRAMES.items():
        if not fpath.exists():
            print(f"ATTENTION : {fname} introuvable, ignoré")
            continue
        inner = fpath.read_text(encoding='utf-8')
        escaped = html.escape(inner, quote=True)
        # Remplacer src="fname" par srcdoc="..."
        content = content.replace(
            f'src="{fname}"',
            f'srcdoc="{escaped}"'
        )
        print(f"  Inliné : {fname} ({len(inner)//1024} Ko)")

    out = BASE / 'onco_complet.html'
    out.write_text(content, encoding='utf-8')
    size = out.stat().st_size
    print(f"\nOK → onco_complet.html ({size//1024} Ko)")

if __name__ == '__main__':
    bundle()
