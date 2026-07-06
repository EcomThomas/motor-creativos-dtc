# -*- coding: utf-8 -*-
"""
persist.py — FASES 3-4 del Motor de Creativos: escribe el BUNDLE del orquestador a disco.

Los workflows (wf_*.js) corren en el sandbox de Workflow y NO tienen acceso a filesystem:
generan y DEVUELVEN datos. Este script es la capa de persistencia: toma el bundle que
devuelve wf_motor (un JSON) y lo materializa en la estructura de caso definida en
casos/README.md, respetando la convención de Creative Roadmap.

Escribe en casos/<producto>/:
  baches/batches_meta.json   -> los N baches con sus ads (compatible con build_roadmap.py)
  baches/roadmap_rows.json   -> una fila por ad, con las columnas de la convención (A..U)
  scripts-ads/ads.json       -> lista plana de anuncios (batch + ad_n + campos del ad)
  briefs/bache-<n>-<slug>.md -> el brief de producción por bache
  briefs/*.docx              -> (si --docx) versión Word de cada brief

Opcional:
  --xlsx <template.xlsx>     -> además puebla la hoja Creative Roadmap del Excel (build_roadmap.py)

Uso:
    python persist.py --bundle bundle.json [--root .] [--xlsx plantilla.xlsx] [--docx]

El <bundle.json> lo produce el runbook a partir del resultado de wf_motor. Forma esperada:
{
  "producto": "...", "slug": "...",
  "snapshot": { "spinePath": "...", "scriptsPath": "...", "vocPath": null },
  "batches": [ { "n":1, "slug":"nucleo", "concept","angle","avatar","mass_desire",
                 "awareness","hypothesis", "ads":[ {imita_competidor, ad_format, copy, nota, ad_type?} ] } ],
  "briefs":  [ { "n":1, "slug":"nucleo", "md":"# BRIEF ..." } ]
}
"""
import argparse
import json
import os
import subprocess
import sys

from motor_config import CONFIG, case_paths, ensure_dirs, defaults

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def _write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _roadmap_rows(batches, author):
    """Aplana los baches a una fila por ad, con las columnas de la convención Creative Roadmap.
    La metadata del concepto (Concept..Hypothesis) va SOLO en la primera fila de cada bache."""
    rows = []
    for b in batches:
        n = b.get("n")
        ads = b.get("ads", [])
        for j, ad in enumerate(ads):
            head = (j == 0)
            rows.append({
                "Status": "Ideando" if head else "",
                "Batch #": n,
                "Author": author if head else "",
                "Ad Concept": b.get("concept", "") if head else "",
                "Angle": b.get("angle", "") if head else "",
                "Avatar": b.get("avatar", ""),
                "Mass Desire": b.get("mass_desire", "") if head else "",
                "Awareness": b.get("awareness", "") if head else "",
                "Hypothesis": b.get("hypothesis", "") if head else "",
                "Ad #": f"{n}.{j + 1}",
                "Ad Type": ad.get("ad_type", "Imitation"),
                "Ad Format": ad.get("ad_format", defaults()["ad_format_default"]),
                "Copy": ad.get("copy", ""),
                "Nota (traza)": (("IMITA: " + ad["imita_competidor"] + " | ") if ad.get("imita_competidor") else "")
                                + ad.get("nota", ""),
            })
    return rows


def _flat_ads(batches):
    flat = []
    for b in batches:
        for j, ad in enumerate(b.get("ads", []), 1):
            row = {"batch": b.get("n"), "batch_slug": b.get("slug"), "ad_n": j}
            row.update(ad)
            flat.append(row)
    return flat


def main():
    ap = argparse.ArgumentParser(description="Fases 3-4 — persiste el bundle del orquestador.")
    ap.add_argument("--bundle", required=True, help="Ruta al JSON del bundle (resultado de wf_motor).")
    ap.add_argument("--root", default=None, help="Raíz alternativa para casos/ (default: raíz del repo).")
    ap.add_argument("--xlsx", default=None, help="Plantilla xlsx: si se da, puebla la hoja Creative Roadmap.")
    ap.add_argument("--docx", action="store_true", help="Además convierte los briefs .md a .docx.")
    args = ap.parse_args()

    with open(args.bundle, encoding="utf-8") as f:
        bundle = json.load(f)

    producto = bundle.get("producto") or "caso"
    batches = bundle.get("batches", [])
    briefs = bundle.get("briefs", [])
    author = defaults()["author_roadmap"]

    if not batches:
        print("ERROR: el bundle no trae 'batches'. Nada que persistir.", file=sys.stderr)
        sys.exit(1)

    paths = ensure_dirs(case_paths(producto, root=args.root))

    # --- baches ---
    batches_meta_path = os.path.join(paths["baches"], "batches_meta.json")
    _write_json(batches_meta_path, batches)
    _write_json(os.path.join(paths["baches"], "roadmap_rows.json"), _roadmap_rows(batches, author))

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

    # --- opcional: poblar Excel Creative Roadmap ---
    if args.xlsx:
        if not os.path.isfile(args.xlsx):
            print(f"[!] --xlsx {args.xlsx!r} no existe; se omite el volcado a Excel. "
                  f"(roadmap_rows.json queda disponible.)", file=sys.stderr)
        else:
            print(f"\nPoblando Creative Roadmap en {args.xlsx} …")
            r = subprocess.run(
                [sys.executable, os.path.join(_SCRIPTS_DIR, "build_roadmap.py"),
                 args.xlsx, batches_meta_path, "Creative Roadmap", "auto", author],
                capture_output=True, text=True)
            sys.stdout.write(r.stdout)
            if r.returncode != 0:
                sys.stderr.write(r.stderr)

    print("\nSiguiente paso: revisar los baches/briefs y, en Media Buying (Etapa 3), "
          "mapear cada fila del roadmap a campaña/adset (ver Fase 5 del Spec).")


if __name__ == "__main__":
    main()
