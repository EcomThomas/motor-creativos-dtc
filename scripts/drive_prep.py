# -*- coding: utf-8 -*-
"""
drive_prep.py — Parte cada brief de BATCH (1 doc con los 3 videos) en 3 docs por video
(V1/V2/V3), cada uno autosuficiente: Ficha + Produccion base (comun) + su bloque de
anuncio + Checklist. Emite los .md por video + un manifest.json para la subida a Drive.

La creacion de carpetas/Docs en Google Drive la hace el asistente via el conector MCP,
leyendo este manifest. Product-agnostic.

Uso:
    python drive_prep.py --bundle bundle.json --briefs-dir <dir> --start-num 147 --outdir <dir>
"""
import argparse
import glob
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def split_brief(md, ad_conceptos):
    """Devuelve lista de per-video markdown. header(1+2) + bloque AD + tail(checklist)."""
    m3 = re.search(r'^## 3\. ', md, re.M)
    m4 = re.search(r'^## 4\. ', md, re.M)
    if not m3 or not m4:
        return [md]  # fallback: no se pudo partir
    header = md[:m3.start()].rstrip()
    sec3 = md[m3.start():m4.start()]
    tail = md[m4.start():].rstrip()
    # bloques de anuncio dentro de sec3
    ad_blocks = re.split(r'(?=^### AD )', sec3, flags=re.M)
    ad_blocks = [b for b in ad_blocks if b.strip().startswith('### AD ')]
    docs = []
    for k, block in enumerate(ad_blocks):
        concepto = ad_conceptos[k] if k < len(ad_conceptos) else ""
        doc = (f"{header}\n\n---\n\n## EL ANUNCIO — VIDEO {k+1}\n\n{block.rstrip()}\n\n---\n\n{tail}\n")
        docs.append((k + 1, concepto, doc))
    return docs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--briefs-dir", required=True)
    ap.add_argument("--start-num", type=int, required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    bundle = json.load(open(args.bundle, encoding="utf-8"))
    os.makedirs(args.outdir, exist_ok=True)
    manifest = []

    for i, b in enumerate(bundle["batches"]):
        n = args.start_num + i
        # localizar el brief de este batch (bache-<i+1>-*.md)
        cands = sorted(glob.glob(os.path.join(args.briefs_dir, f"bache-{i+1}-*.md")))
        if not cands:
            print(f"[!] sin brief para batch idx {i+1}", file=sys.stderr)
            continue
        md = open(cands[0], encoding="utf-8").read()
        ad_conceptos = [a.get("concepto_corto", "") for a in b.get("ads", [])]
        docs = split_brief(md, ad_conceptos)
        folder_title = f"BATCH #{n} — {b.get('concept','')}"
        videos = []
        for vk, concepto, doc in docs:
            fname = f"BATCH{n}_V{vk}.md"
            fpath = os.path.join(args.outdir, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(doc)
            title = f"V{vk} BATCH #{n} - {concepto}"[:250]
            videos.append({"video": vk, "title": title, "path": fpath.replace("\\", "/"), "chars": len(doc)})
        manifest.append({"batch": n, "folder_title": folder_title, "concept": b.get("concept", ""), "videos": videos})

    mpath = os.path.join(args.outdir, "manifest.json")
    json.dump(manifest, open(mpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"OK: {sum(len(x['videos']) for x in manifest)} docs por video, {len(manifest)} batches.")
    for x in manifest:
        print(f"  {x['folder_title'][:60]}")
        for v in x["videos"]:
            print(f"     V{v['video']}: {v['title'][:70]}  ({v['chars']} chars)")
    print(f"manifest: {mpath}")


if __name__ == "__main__":
    main()
