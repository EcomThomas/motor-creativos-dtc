# -*- coding: utf-8 -*-
"""
clickup_upload.py — Sube los BATCH del bundle a ClickUp vía API REST (tarea madre +
subtareas por pieza), en la lista del flujo creativo. Complemento de clickup_export.py.

- Token: lee CLICKUP_TOKEN de C:\\Users\\Thomas\\research_secrets.env (no se imprime).
- Tarea madre: nombre "BATCH #<n> — <concepto>", descripción con los campos del batch.
- Subtareas: una por pieza (V1/G1 BATCH #<n> - <concepto corto>), colgando de la madre.
- El campo "Brief" queda como placeholder (doc externo).

Uso:
    python clickup_upload.py --bundle bundle.json --list 901112908802 --start-num 147 \
        [--only 1] [--carpeta LINK] [--cta LINK] [--dry-run]
"""
import argparse
import json
import re
import sys
import urllib.request

from clickup_export import val, tipo_ad_batch, FORMATO_LETRA, BRIEF_PH, FALTA

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

API = "https://api.clickup.com/api/v2"
ENV = r"C:\Users\Thomas\research_secrets.env"
LINKPH = "[LINK]"


def token():
    env = open(ENV, encoding="utf-8", errors="ignore").read()
    return re.search(r'^CLICKUP_TOKEN=(.+)$', env, re.M).group(1).strip()


def post(path, payload, tok):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API + path, data=data, method="POST",
                                 headers={"Authorization": tok, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def madre_desc(b, carpeta, cta):
    emos = " · ".join(b.get("emociones_83") or []) or FALTA
    return "\n".join([
        f"**Ad Concept:** {val(b.get('concept'))}",
        f"**Ángulo:** {val(b.get('angle'))}",
        f"**Hipótesis:** {val(b.get('hypothesis'))}",
        f"**Avatar:** {val(b.get('avatar'))}",
        f"**Sub avatar:** {val(b.get('sub_avatar'))}",
        f"**Deseo masivo:** {val(b.get('mass_desire'))}",
        f"**Valence dominante:** {val(b.get('valence'))}",
        f"**Emociones 83%:** {emos}",
        f"**Nivel de conciencia:** {val(b.get('awareness'))}",
        f"**Tipo de ad:** {tipo_ad_batch(b)}",
        "",
        f"**Carpeta de carga de creativos:** {carpeta}",
        f"**Destino del CTA:** {cta}",
    ])


def sub_desc(ad, carpeta, cta, batch_trigger):
    trig = ad.get("trigger_emocional")
    if not (trig and trig.strip()):
        trig = f"{batch_trigger} [HEREDADO DEL BATCH]" if batch_trigger else FALTA
    return "\n".join([
        f"**Concepto:** {val(ad.get('concepto_corto'))}",
        f"**Nombre creativo:** {val(ad.get('nombre_creativo'))}",
        f"**Carga de creativos:** {carpeta}",
        f"**Destino del CTA:** {cta}",
        f"**Brief:** {BRIEF_PH}",
        f"**Trigger emocional:** {trig}",
    ])


def main():
    ap = argparse.ArgumentParser(description="Sube los BATCH del bundle a ClickUp.")
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--list", required=True, help="list_id destino en ClickUp.")
    ap.add_argument("--start-num", type=int, required=True, help="Número del primer BATCH (ej. 147).")
    ap.add_argument("--only", type=int, default=None, help="Subir solo el bache i (1-based) del bundle (para probar).")
    ap.add_argument("--status", default=None, help="Estado ClickUp para las tareas (ej. 'idea').")
    ap.add_argument("--carpeta", default=LINKPH)
    ap.add_argument("--cta", default=LINKPH)
    ap.add_argument("--dry-run", action="store_true", help="No crea nada; muestra qué haría.")
    args = ap.parse_args()

    tok = token()
    bundle = json.load(open(args.bundle, encoding="utf-8"))
    batches = bundle.get("batches", [])
    created = []

    for i, b in enumerate(batches):
        if args.only and (i + 1) != args.only:
            continue
        n = args.start_num + i
        name = f"BATCH #{n} — {b.get('concept', '')}"
        if args.dry_run:
            print(f"[dry] madre: {name}  (+{len(b.get('ads',[]))} subtareas)")
            continue
        mpayload = {"name": name, "markdown_description": madre_desc(b, args.carpeta, args.cta)}
        if args.status:
            mpayload["status"] = args.status
        parent = post(f"/list/{args.list}/task", mpayload, tok)
        pid, purl = parent["id"], parent.get("url", "")
        counters = {"V": 0, "G": 0}
        batch_trigger = b.get("trigger_batch")
        subs = []
        for ad in b.get("ads", []):
            letra = FORMATO_LETRA.get(ad.get("ad_format", "Video"), "V")
            counters[letra] += 1
            title = f"{letra}{counters[letra]} BATCH #{n} - {val(ad.get('concepto_corto'))}"
            spayload = {"name": title, "markdown_description": sub_desc(ad, args.carpeta, args.cta, batch_trigger),
                        "parent": pid}
            if args.status:
                spayload["status"] = args.status
            st = post(f"/list/{args.list}/task", spayload, tok)
            subs.append(st["name"])
        created.append((n, name, purl, subs))
        print(f"✓ BATCH #{n} creado ({len(subs)} subtareas)\n  {purl}")
        for s in subs:
            print(f"    · {s}")

    if not args.dry_run:
        print(f"\n{len(created)} BATCH subido(s) a ClickUp.")


if __name__ == "__main__":
    main()
