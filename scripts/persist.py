# -*- coding: utf-8 -*-
"""
persist.py — persiste el BUNDLE del orquestador a disco (datos + briefs).

Los workflows (wf_*.js) corren en el sandbox de Workflow (sin filesystem): generan y
DEVUELVEN datos. Este script los materializa en la estructura de caso (casos/README.md).

Escribe en casos/<producto>/:
  baches/batches_meta.json   -> los N baches con sus ads (fuente de verdad de la corrida)
  scripts-ads/ads.json       -> lista plana de anuncios
  briefs/bache-<n>-<slug>.md -> el brief de producción por bache
  briefs/*.docx              -> (si --docx) versión Word de cada brief

NOTA (cambio de salida): el motor YA NO vuelca al Excel "Creative Roadmap" (se hacía a
mano y se corrompía). El entregable operativo de Fase 3 es ahora el formato ClickUp
(tarea madre + subtareas) que produce `clickup_export.py`. Ver RUNBOOK.md.

Uso:
    python persist.py --bundle bundle.json [--root .] [--docx]
    # luego: python clickup_export.py --bundle bundle.json ...   (entregable ClickUp)
"""
import argparse
import json
import os
import sys

from motor_config import case_paths, ensure_dirs

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def _write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _flat_ads(batches):
    flat = []
    for b in batches:
        for j, ad in enumerate(b.get("ads", []), 1):
            row = {"batch": b.get("n"), "batch_slug": b.get("slug"), "ad_n": j}
            row.update(ad)
            flat.append(row)
    return flat


def main():
    ap = argparse.ArgumentParser(description="Persiste el bundle del orquestador (datos + briefs).")
    ap.add_argument("--bundle", required=True, help="Ruta al JSON del bundle (resultado de wf_motor).")
    ap.add_argument("--root", default=None, help="Raíz alternativa para casos/ (default: raíz del repo).")
    ap.add_argument("--docx", action="store_true", help="Además convierte los briefs .md a .docx.")
    args = ap.parse_args()

    with open(args.bundle, encoding="utf-8") as f:
        bundle = json.load(f)

    producto = bundle.get("producto") or "caso"
    batches = bundle.get("batches", [])
    briefs = bundle.get("briefs", [])

    if not batches:
        print("ERROR: el bundle no trae 'batches'. Nada que persistir.", file=sys.stderr)
        sys.exit(1)

    paths = ensure_dirs(case_paths(producto, root=args.root))

    # --- baches (fuente de verdad de la corrida) ---
    batches_meta_path = os.path.join(paths["baches"], "batches_meta.json")
    _write_json(batches_meta_path, batches)

    # --- ads planos ---
    _write_json(os.path.join(paths["ads"], "ads.json"), _flat_ads(batches))

    # --- briefs ---
    brief_files = []
    for b in briefs:
        n = b.get("n")
        slug = b.get("slug") or f"bache-{n}"
        fname = f"bache-{n}-{slug}.md" if not str(slug).startswith("bache") else f"{slug}.md"
        fpath = os.path.join(paths["briefs"], fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(b.get("md", ""))
        brief_files.append(fpath)

    total_ads = sum(len(b.get("ads", [])) for b in batches)
    print("=" * 60)
    print(f"PERSISTIDO — {producto}")
    print("=" * 60)
    print(f"Baches            : {len(batches)}")
    print(f"Ads (total)       : {total_ads}")
    print(f"Briefs            : {len(brief_files)}")
    print(f"batches_meta.json : {batches_meta_path}")
    print(f"briefs/           : {paths['briefs']}")

    # --- opcional: docx de briefs ---
    if args.docx and brief_files:
        try:
            from md2docx import convert_folder
            print("\nConvirtiendo briefs a .docx:")
            convert_folder(paths["briefs"])
        except Exception as e:
            print(f"[!] no se pudieron generar .docx: {e}", file=sys.stderr)

    print("\nSiguiente paso (Fase 3 — entregable): genera el formato ClickUp con")
    print(f"  python clickup_export.py --bundle {args.bundle} --batch-num <#> --carpeta <LINK> --cta <LINK>")
    print("El Excel Creative Roadmap ya no se usa (se llena a mano si hace falta).")


if __name__ == "__main__":
    main()
