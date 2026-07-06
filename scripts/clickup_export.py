# -*- coding: utf-8 -*-
"""
clickup_export.py — FASE 3 (nueva): convierte el bundle del motor en el entregable
ClickUp (tarea madre + subtareas en TEXTO PLANO pegable), según el prompt de batch
que usa el equipo. Reemplaza el volcado a Excel (deprecado).

Un archivo por bache: casos/<slug>/clickup/batch_<n>.txt

Reglas del formato (no negociables, del prompt del equipo):
- Texto simple, limpio, pegable en ClickUp. SIN tablas. Sin párrafos largos.
- La tarea madre va primero; luego una subtarea por pieza.
- El campo "Brief" de cada subtarea SIEMPRE queda como placeholder (va en doc externo).
- Títulos de subtarea: "V<k> BATCH #<N> - <CONCEPTO CORTO>" (video) / "G<k> ..." (gráfica),
  numerados por tipo de pieza (V1,V2,V3 / G1,G2,G3).
- Datos que no estén claros → "[FALTA DEFINIR]". Links no provistos → "[LINK]".
- El número de batch del INPUT manda (no se infiere): --batch-num lo fija.
- valence/emociones/trigger NO se inventan aquí: vienen del bundle (los generó el motor).

Uso:
    python clickup_export.py --bundle bundle.json [--root .] \
        [--batch-num 7] [--producto "..."] [--plataforma "Meta"] \
        [--carpeta LINK] [--cta LINK] [--assets "Asset1 — Link; Asset2 — Link"]

Si --batch-num se da, se aplica al PRIMER bache (uso típico: un batch por corrida);
el resto conserva su `n`. Sin --batch-num, cada bache usa su propio `n`.
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

FALTA = "[FALTA DEFINIR]"
LINKPH = "[LINK]"
BRIEF_PH = "[PENDIENTE — documento externo, se agrega manualmente]"

CLASSIFICACION_ES = {"Imitation": "IMITACIÓN", "Iteration": "ITERACIÓN", "Ideation": "IDEACIÓN"}
FORMATO_LETRA = {"Video": "V", "Static": "G", "Promo": "G"}


def val(x, default=FALTA):
    if x is None:
        return default
    if isinstance(x, str) and not x.strip():
        return default
    return x


def batch_formato(ads):
    """Formato del batch para la etiqueta: Video / Gráfica / Mixto."""
    fmts = {a.get("ad_format", "Video") for a in ads}
    if fmts == {"Video"}:
        return "Video"
    if fmts <= {"Static", "Promo"}:
        return "Gráfica"
    return "Mixto"


def tipo_ad_batch(b):
    """Tipo de ad dominante del batch (ITERACIÓN/IMITACIÓN/IDEACIÓN)."""
    c = b.get("classification")
    if c:
        return CLASSIFICACION_ES.get(c, str(c).upper())
    # deducir de las piezas: el más frecuente
    counts = {}
    for a in b.get("ads", []):
        k = a.get("classification", "Imitation")
        counts[k] = counts.get(k, 0) + 1
    if not counts:
        return "IMITACIÓN"
    top = max(counts, key=counts.get)
    return CLASSIFICACION_ES.get(top, top.upper())


def _short(text, maxlen=70):
    """Versión corta para la etiqueta: corta en el primer ':' o '.', o a maxlen chars."""
    if not text:
        return FALTA
    t = str(text).strip()
    for sep in (":", ". ", " —", " ("):
        i = t.find(sep)
        if 0 < i <= maxlen:
            return t[:i].strip()
    return (t[:maxlen].rsplit(" ", 1)[0] + "…") if len(t) > maxlen else t


def render_etiqueta(b, n, producto, plataforma):
    emos = b.get("emociones_83") or []
    valence = val(b.get("valence"))
    ve = f"{valence} · {'/'.join(emos)}" if emos and valence != FALTA else (valence if valence != FALTA else FALTA)
    partes = [
        f"BATCH #{n} · {val(producto)}",
        val(b.get("awareness")),
        _short(b.get("angle")),
        batch_formato(b.get("ads", [])),
        val(plataforma),
        ve,
    ]
    return "ETIQUETA CORTA: " + " | ".join(partes)


def render_tarea_madre(b, n, carpeta, cta, assets):
    emos = b.get("emociones_83") or []
    emos_txt = " · ".join(emos) if emos else FALTA
    assets_lines = "\n".join(f"• {a}" for a in assets) if assets else "• " + FALTA
    return "\n".join([
        "==================== TAREA MADRE ====================",
        "",
        "— COPIAR DESDE AQUÍ —",
        "",
        f"Nombre batch: {val(b.get('etiqueta_breve') or b.get('concept'))}",
        f"Carpeta de carga de creativos: {carpeta}",
        f"Destino del CTA: {cta}",
        f"Ad Concept: {val(b.get('concept'))}",
        f"Ángulo: {val(b.get('angle'))}",
        f"Hipótesis: {val(b.get('hypothesis'))}",
        f"Avatar: {val(b.get('avatar'))}",
        f"Sub avatar: {val(b.get('sub_avatar'))}",
        f"Deseo masivo: {val(b.get('mass_desire'))}",
        f"Valence dominante: {val(b.get('valence'))}",
        f"Emociones 83%: {emos_txt}",
        f"Nivel de conciencia: {val(b.get('awareness'))}",
        f"Tipo de ad: {tipo_ad_batch(b)}",
        "Assets necesarios:",
        assets_lines,
        "",
        "— FIN DEL TEXTO —",
    ])


def render_subtareas(b, n, carpeta, cta):
    out = ["==================== SUBTAREAS ===================="]
    counters = {"V": 0, "G": 0}
    batch_trigger = b.get("trigger_batch") or b.get("trigger_emocional")
    for ad in b.get("ads", []):
        letra = FORMATO_LETRA.get(ad.get("ad_format", "Video"), "V")
        counters[letra] += 1
        k = counters[letra]
        concepto_corto = val(ad.get("concepto_corto") or ad.get("nombre_creativo") or b.get("concept"))
        titulo = f"{letra}{k} BATCH #{n} - {concepto_corto}"
        # trigger: si la pieza no lo trae, hereda el del batch y se anota
        trig = ad.get("trigger_emocional")
        if trig and trig.strip():
            trigger = trig
        elif batch_trigger:
            trigger = f"{batch_trigger} [HEREDADO DEL BATCH]"
        else:
            trigger = FALTA
        out += [
            "",
            "— COPIAR DESDE AQUÍ —",
            "",
            titulo,
            f"Concepto: {val(ad.get('concepto_corto'))}",
            f"Nombre creativo: {val(ad.get('nombre_creativo'))}",
            f"Carga de creativos: {carpeta}",
            f"Destino del CTA: {cta}",
            f"Brief: {BRIEF_PH}",
            f"Trigger emocional: {trigger}",
            "",
            "— FIN DEL TEXTO —",
        ]
    return "\n".join(out)


def render_batch(b, n, producto, plataforma, carpeta, cta, assets):
    return "\n\n".join([
        render_etiqueta(b, n, producto, plataforma),
        render_tarea_madre(b, n, carpeta, cta, assets),
        render_subtareas(b, n, carpeta, cta),
    ]) + "\n"


def parse_assets(s):
    if not s:
        return []
    # separadores admitidos: ';' o salto de línea
    raw = s.replace("\r", "").split(";") if ";" in s else s.split("\n")
    return [a.strip() for a in raw if a.strip()]


def main():
    ap = argparse.ArgumentParser(description="Fase 3 — entregable ClickUp (tarea madre + subtareas).")
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--root", default=None)
    ap.add_argument("--batch-num", default=None, help="Número de batch del INPUT (aplica al primer bache).")
    ap.add_argument("--producto", default=None, help="Nombre del producto (para la etiqueta). Default: del bundle.")
    ap.add_argument("--plataforma", default=None, help="Meta / TikTok / ambas (para la etiqueta).")
    ap.add_argument("--carpeta", default=LINKPH, help="Link de la carpeta de carga de creativos.")
    ap.add_argument("--cta", default=LINKPH, help="Link destino del CTA.")
    ap.add_argument("--assets", default=None, help="Assets: 'Asset — Link; Asset — Link'.")
    args = ap.parse_args()

    with open(args.bundle, encoding="utf-8") as f:
        bundle = json.load(f)
    producto = args.producto or bundle.get("producto") or FALTA          # nombre para la ETIQUETA (display)
    path_producto = bundle.get("producto") or args.producto or "caso"     # define casos/<slug>/ (no lo cambia --producto)
    plataforma = args.plataforma or bundle.get("plataforma")
    assets = parse_assets(args.assets)
    batches = bundle.get("batches", [])
    if not batches:
        print("ERROR: el bundle no trae 'batches'.", file=sys.stderr)
        sys.exit(1)

    paths = ensure_dirs(case_paths(path_producto, root=args.root))
    outdir = os.path.join(paths["base"], "clickup")
    os.makedirs(outdir, exist_ok=True)

    written = []
    for i, b in enumerate(batches):
        n = args.batch_num if (args.batch_num and i == 0) else b.get("n", i + 1)
        # plataforma por bache si el bundle la trae a ese nivel
        plat = b.get("plataforma") or plataforma
        text = render_batch(b, n, producto, plat, args.carpeta, args.cta, assets)
        fpath = os.path.join(outdir, f"batch_{n}.txt")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(text)
        written.append((n, fpath))

    print("=" * 60)
    print(f"ENTREGABLE CLICKUP — {producto}")
    print("=" * 60)
    for n, p in written:
        print(f"  BATCH #{n} -> {p}")
    print(f"\n{len(written)} bache(s). Texto plano pegable en ClickUp (tarea madre + subtareas).")
    print("Recordatorio: el campo 'Brief' queda como placeholder — el brief real es el doc de Fase 4.")


if __name__ == "__main__":
    main()
