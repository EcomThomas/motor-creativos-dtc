# -*- coding: utf-8 -*-
"""
clickup_finalize.py — Rellena TODOS los campos de las tareas ClickUp de un caso una vez
que existen la carpeta de Drive del BATCH y los Google Docs de los briefs. Reescribe la
descripción de la tarea madre y de cada subtarea (sin dejar campos a medias):

  Tarea madre  : Carpeta de carga de creativos = carpeta Drive del BATCH · Destino del CTA = manual.
  Subtareas    : Carga de creativos = carpeta Drive del BATCH · Destino del CTA = manual ·
                 Brief = link al Google Doc del video · + concepto/nombre/trigger.

Convención (feedback del usuario): la "carpeta de carga de creativos" es la MISMA carpeta
del BATCH en Drive (ahí van briefs + creativos finales). El "destino del CTA" se completa a
mano porque varía por advertorial/PDP.

Uso:
    python clickup_finalize.py --bundle bundle.json --config finalize_config.json [--start-num 147]

finalize_config.json:
[
  { "n": 147, "mother_id": "868k8pvjt",
    "folder_url": "https://drive.google.com/drive/folders/...",
    "subtasks": { "1": "<id>", "2": "<id>", "3": "<id>" },
    "docs":     { "1": "https://docs.google.com/document/d/...", "2": "...", "3": "..." } },
  ...
]
"""
import argparse
import json
import re
import sys
import urllib.request

from clickup_export import val, FALTA
from clickup_upload import madre_desc  # madre_desc(b, carpeta, cta)

API = "https://api.clickup.com/api/v2"
ENV = r"C:\Users\Thomas\research_secrets.env"
CTA_MANUAL = "[Se completa manual — según el advertorial/PDP del caso]"

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def token():
    env = open(ENV, encoding="utf-8", errors="ignore").read()
    return re.search(r'^CLICKUP_TOKEN=(.+)$', env, re.M).group(1).strip()


def put(tid, payload, tok):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{API}/task/{tid}", data=data, method="PUT",
                                 headers={"Authorization": tok, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def sub_desc(ad, carpeta, brief_url, batch_trigger):
    trig = ad.get("trigger_emocional")
    if not (trig and trig.strip()):
        trig = f"{batch_trigger} [HEREDADO DEL BATCH]" if batch_trigger else FALTA
    return "\n".join([
        f"**Concepto:** {val(ad.get('concepto_corto'))}",
        f"**Nombre creativo:** {val(ad.get('nombre_creativo'))}",
        f"**Carga de creativos:** {carpeta}",
        f"**Destino del CTA:** {CTA_MANUAL}",
        f"**Brief:** {brief_url}",
        f"**Trigger emocional:** {trig}",
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--start-num", type=int, default=None, help="Número del primer BATCH del bundle (para alinear índices).")
    args = ap.parse_args()

    tok = token()
    bundle = json.load(open(args.bundle, encoding="utf-8"))
    cfg = json.load(open(args.config, encoding="utf-8"))
    base = args.start_num if args.start_num is not None else cfg[0]["n"]

    for entry in cfg:
        n = entry["n"]
        b = bundle["batches"][n - base]
        carp = entry["folder_url"]
        put(entry["mother_id"], {"markdown_description": madre_desc(b, carp, CTA_MANUAL)}, tok)
        trg = b.get("trigger_batch")
        for k, ad in enumerate(b.get("ads", []), 1):
            sid = entry["subtasks"][str(k)]
            put(sid, {"markdown_description": sub_desc(ad, carp, entry["docs"][str(k)], trg)}, tok)
        print(f"✓ BATCH #{n}: madre + {len(b.get('ads', []))} subtareas finalizadas.")


if __name__ == "__main__":
    main()
