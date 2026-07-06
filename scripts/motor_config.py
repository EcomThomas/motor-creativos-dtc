# -*- coding: utf-8 -*-
"""
motor_config.py — Loader de la config canónica del Motor de Creativos.

Fuente única de defaults: ../config.json (en la raíz del repo).
Lo usan intake.py y persist.py. Product-agnostic: no hardcodea ningún producto.

Uso:
    from motor_config import CONFIG, defaults, enums, case_paths, slugify
"""
import json
import os
import re
import unicodedata

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CONFIG_PATH = os.path.join(_REPO_ROOT, "config.json")


def _load():
    with open(_CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


CONFIG = _load()


def defaults():
    return CONFIG["defaults"]


def enums():
    return CONFIG["enums"]


def repo_root():
    return _REPO_ROOT


def slugify(text):
    """Slug ASCII, minúsculas, guiones. 'Suplemento Hepático MX' -> 'suplemento-hepatico-mx'."""
    text = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "caso"


def case_paths(producto, root=None):
    """Devuelve el dict de rutas canónicas de un caso: casos/<slug>/{input,baches,scripts-ads,briefs}.

    root: raíz alternativa (por defecto la del repo). Útil para tests o para escribir fuera del repo.
    """
    p = CONFIG["paths"]
    base = os.path.join(root or _REPO_ROOT, p["casos_root"], slugify(producto))
    return {
        "base": base,
        "input": os.path.join(base, p["input_dir"]),
        "baches": os.path.join(base, p["baches_dir"]),
        "ads": os.path.join(base, p["ads_dir"]),
        "briefs": os.path.join(base, p["briefs_dir"]),
    }


def ensure_dirs(paths):
    """Crea las carpetas del caso si no existen. Acepta el dict de case_paths()."""
    for k, d in paths.items():
        os.makedirs(d, exist_ok=True)
    return paths


if __name__ == "__main__":
    # Smoke test: imprime la config resuelta.
    import sys
    print("config.json:", _CONFIG_PATH)
    print("version:", CONFIG.get("version"))
    print("defaults:", json.dumps(defaults(), ensure_ascii=False))
    prod = sys.argv[1] if len(sys.argv) > 1 else "Suplemento Hepático MX"
    print(f"case_paths({prod!r}):")
    for k, v in case_paths(prod).items():
        print(f"  {k}: {v}")
