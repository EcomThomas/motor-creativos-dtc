# -*- coding: utf-8 -*-
"""
clickup_upload.py — Sube los BATCH del bundle a ClickUp vía API REST (tarea madre +
subtareas por pieza), en la lista del flujo creativo. Complemento de clickup_export.py.

- Token: CLICKUP_TOKEN vía motor_config (MOTOR_SECRETS -> <repo>/.env). Cada usuario usa SUS tokens. No se imprime.
- Lista/estado destino: de config.local.json (clickup_list_id / clickup_status) o por CLI.
- Tarea madre: nombre "BATCH #<n> — <concepto>", descripción con los campos del batch.
- Subtareas: una por pieza (V1/G1 BATCH #<n> - <concepto corto>), colgando de la madre.
- El campo "Brief" queda como placeholder (doc externo).
- Emite casos/<producto>/clickup/finalize_<n>.json con los IDs reales (madre + subtareas),
  con folder_url/docs en blanco para completar tras subir los briefs a Drive.

Uso:
    python clickup_upload.py --bundle bundle.json --start-num 147 --status idea \
        [--list 901xxxxxxxxx] [--only 1] [--carpeta LINK] [--cta LINK] [--dry-run]
"""
import argparse
import json
import os
import sys
import urllib.request

from clickup_export import val, tipo_ad_batch, render_etiqueta, FORMATO_LETRA, BRIEF_PH, FALTA
from motor_config import get_token, store, case_paths, ensure_dirs

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

API = "https://api.clickup.com/api/v2"
LINKPH = "[LINK]"


def token():
    # CLICKUP_TOKEN del archivo de secretos resuelto por motor_config
    # (MOTOR_SECRETS -> <repo>/.env). Nunca se imprime.
    return get_token("CLICKUP_TOKEN")


def post(path, payload, tok):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API + path, data=data, method="POST",
                                 headers={"Authorization": tok, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))


# --- IDEMPOTENCIA -----------------------------------------------------------
# Registro de lo YA subido a ClickUp: casos/<producto>/clickup/uploaded.json
# Se escribe INCREMENTALMENTE (la madre se registra apenas se crea), así un fallo
# de red a mitad de las subtareas NO produce una madre duplicada al reintentar.
def _ledger_path(producto):
    paths = ensure_dirs(case_paths(producto))
    outdir = os.path.join(paths["base"], "clickup")
    os.makedirs(outdir, exist_ok=True)
    return os.path.join(outdir, "uploaded.json")


def _load_ledger(producto):
    p = _ledger_path(producto)
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_ledger(producto, ledger):
    with open(_ledger_path(producto), "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)


def madre_desc(b, carpeta, cta, n=None, producto=None, plataforma=None):
    # Formato canónico de la tarea madre (metodo/08 §3.1-3.2). Si se pasan n+producto,
    # antepone la ETIQUETA CORTA. Cierra con "Assets necesarios" (de b["assets"] o FALTA).
    emos = " · ".join(b.get("emociones_83") or []) or FALTA
    assets = b.get("assets") or []
    lines = []
    if n is not None and producto:
        lines += [render_etiqueta(b, n, producto, plataforma), ""]
    lines += [
        f"**Nombre batch:** {val(b.get('etiqueta_breve') or b.get('concept'))}",
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
        "**Assets necesarios:**",
    ]
    lines += [f"• {a}" for a in assets] if assets else [f"• {FALTA}"]
    return "\n".join(lines)


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
    ap.add_argument("--list", default=None, help="list_id destino. Default: clickup_list_id de config.local.json.")
    ap.add_argument("--start-num", type=int, required=True, help="Número del primer BATCH (ej. 147).")
    ap.add_argument("--only", type=int, default=None, help="Subir solo el bache i (1-based) del bundle (para probar).")
    ap.add_argument("--status", default=None, help="Estado ClickUp (ej. 'idea'). Default: clickup_status de config.local.json.")
    ap.add_argument("--carpeta", default=LINKPH)
    ap.add_argument("--cta", default=LINKPH)
    ap.add_argument("--dry-run", action="store_true", help="No crea nada; muestra qué haría.")
    ap.add_argument("--force", action="store_true",
                    help="Re-sube un BATCH aunque ya figure como subido (CREA DUPLICADOS a propósito).")
    args = ap.parse_args()

    sp = store()
    list_id = args.list or sp.get("clickup_list_id")
    status = args.status or sp.get("clickup_status")
    if not list_id and not args.dry_run:
        sys.exit("ERROR: falta list_id. Pásalo con --list o define clickup_list_id en config.local.json "
                 "(ver config.local.example.json).")

    tok = None if args.dry_run else token()
    bundle = json.load(open(args.bundle, encoding="utf-8"))
    batches = bundle.get("batches", [])
    producto = bundle.get("producto") or "caso"
    plataforma = bundle.get("plataforma")
    created = []
    mount_cfg = []  # config listo para clickup_finalize (folder_url/docs se completan tras subir a Drive)

    ledger = _load_ledger(producto)

    for i, b in enumerate(batches):
        if args.only and (i + 1) != args.only:
            continue
        n = args.start_num + i
        name = f"BATCH #{n} — {b.get('concept', '')}"
        ya = ledger.get(str(n))
        if ya and not args.force:
            print(f"⏭  BATCH #{n} ya estaba subido — se OMITE (no se duplica).\n   {ya.get('url','')}")
            mount_cfg.append({"n": n, "mother_id": ya.get("mother_id", ""), "folder_url": "",
                              "subtasks": ya.get("subtasks", {}),
                              "docs": {k: "" for k in ya.get("subtasks", {})}})
            continue
        if args.dry_run:
            estado = " (ya subido — se omitiría)" if ya else ""
            print(f"[dry] madre: {name}  (+{len(b.get('ads',[]))} subtareas)  -> list {list_id or '[FALTA]'}{estado}")
            continue
        mpayload = {"name": name, "markdown_description": madre_desc(b, args.carpeta, args.cta, n=n, producto=producto, plataforma=plataforma)}
        if status:
            mpayload["status"] = status
        parent = post(f"/list/{list_id}/task", mpayload, tok)
        pid, purl = parent["id"], parent.get("url", "")
        # Registrar la madre YA: si falla una subtarea, el reintento no la duplica.
        ledger[str(n)] = {"mother_id": pid, "url": purl, "name": name, "subtasks": {}}
        _save_ledger(producto, ledger)
        counters = {"V": 0, "G": 0}
        batch_trigger = b.get("trigger_batch")
        subs = []
        sub_ids = {}
        for k, ad in enumerate(b.get("ads", []), 1):
            letra = FORMATO_LETRA.get(ad.get("ad_format", "Video"), "V")
            counters[letra] += 1
            title = f"{letra}{counters[letra]} BATCH #{n} - {val(ad.get('concepto_corto'))}"
            spayload = {"name": title, "markdown_description": sub_desc(ad, args.carpeta, args.cta, batch_trigger),
                        "parent": pid}
            if status:
                spayload["status"] = status
            st = post(f"/list/{list_id}/task", spayload, tok)
            subs.append(st["name"])
            sub_ids[str(k)] = st["id"]
            # Persistir subtarea a subtarea: un corte de red no deja estado fantasma.
            ledger[str(n)]["subtasks"] = dict(sub_ids)
            _save_ledger(producto, ledger)
        created.append((n, name, purl, subs))
        mount_cfg.append({"n": n, "mother_id": pid, "folder_url": "",
                          "subtasks": sub_ids, "docs": {k: "" for k in sub_ids}})
        print(f"✓ BATCH #{n} creado ({len(subs)} subtareas)\n  {purl}")
        for s in subs:
            print(f"    · {s}")

    if not args.dry_run and mount_cfg:
        # Emite el config de finalize CON los IDs reales, para no re-consultar ClickUp después.
        # folder_url + docs (links de los Google Docs) se completan tras subir los briefs a Drive.
        paths = ensure_dirs(case_paths(producto))
        outdir = os.path.join(paths["base"], "clickup")
        os.makedirs(outdir, exist_ok=True)
        # Sufijo desde los batches REALMENTE montados (no len(batches)): con --only el
        # rango era incorrecto y pisaba/creaba archivos con nombre equivocado.
        ns = [c["n"] for c in mount_cfg]
        lo, hi = min(ns), max(ns)
        suffix = f"{lo}" if lo == hi else f"{lo}-{hi}"
        cfgpath = os.path.join(outdir, f"finalize_{suffix}.json")
        with open(cfgpath, "w", encoding="utf-8") as f:
            json.dump(mount_cfg, f, ensure_ascii=False, indent=2)
        print(f"\n{len(created)} BATCH subido(s) a ClickUp.")
        print(f"Estado de montaje -> {cfgpath}")
        print("Siguiente: sube los briefs a Drive, completa folder_url + docs en ese JSON y corre clickup_finalize.py.")


if __name__ == "__main__":
    main()
