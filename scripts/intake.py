# -*- coding: utf-8 -*-
"""
intake.py — FASE 0 del Motor de Creativos: valida el input y congela el snapshot.

Implementa el contrato de la INTERFACE (§6 protocolo de faltantes, §8 checklist de
aceptación, §5 snapshot). Product-agnostic.

Qué hace:
  1. Valida el SPINE contra los campos obligatorios (INTERFACE §2). El motor NO rellena
     huecos: si falta un obligatorio, BLOQUEA y devuelve el reporte "INPUT INCOMPLETO".
  2. Verifica que existan los SCRIPTS ganadores (degrada a solo-ideación si faltan).
  3. Declara si hay o no banco VoC (no bloquea; cambia cómo se citan los hooks).
  4. Escribe el SNAPSHOT congelado en casos/<producto>/input/ + _meta.md (fecha, versión
     del Spine, hash del input, quién ejecutó).

Validación estricta del Spine:
  - Spine .json  -> se parsea y valida el schema de §2 campo por campo.
  - Spine .md    -> si trae un bloque fenced ```json ... ``` con el objeto Spine, se valida
                    estricto; si no, se hace un chequeo heurístico de secciones y se AVISA
                    (la validación dura requiere Spine estructurado).

Uso:
    python intake.py --producto "Suplemento Hepatico MX" \
        --spine ruta/Spine.md --scripts ruta/competitor_scripts.md \
        [--voc ruta/voc_bank.md] [--spine-version "v3.2"] [--autor "Thomas"] [--root .]

Salida:
    exit 0  -> input aceptado (revisa WARN por degradaciones). Snapshot escrito.
    exit 2  -> BLOQUEADO por faltantes obligatorios. NO se generan baches.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import sys

from motor_config import CONFIG, case_paths, ensure_dirs, slugify

# La consola de Windows suele ser cp1252; forzamos UTF-8 para no romper con acentos/símbolos.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _extract_spine_object(spine_path):
    """Devuelve (obj, modo). modo ∈ {'json','md-embedded','md-freeform'}.

    - .json           -> parse directo.
    - .md con ```json``` -> parse del primer bloque fenced json.
    - .md sin bloque   -> None (validación heurística).
    """
    text = _read(spine_path)
    if spine_path.lower().endswith(".json"):
        try:
            return json.loads(text), "json"
        except json.JSONDecodeError as e:
            # No reventar con traceback: se convierte en bloqueo formal (§6).
            raise ValueError(f"el Spine .json está malformado y no se puede parsear ({e})")
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1)), "md-embedded"
        except json.JSONDecodeError:
            pass
    return None, "md-freeform"


def _is_empty(v):
    if v is None:
        return True
    if isinstance(v, str) and not v.strip():
        return True
    if isinstance(v, (list, dict)) and len(v) == 0:
        return True
    return False


def _validate_spine_object(spine):
    """Valida el objeto Spine estructurado. Devuelve (faltantes, avisos)."""
    faltantes, avisos = [], []
    obligatorios = CONFIG["spine_campos_obligatorios"]
    for campo in obligatorios:
        if campo not in spine or _is_empty(spine.get(campo)):
            # INTERFACE §6: un compliance PRESENTE pero vacío NO bloquea — se pide
            # confirmación explícita a la etapa 1 (nunca se asume "sin restricciones").
            if campo == "compliance" and isinstance(spine.get(campo), dict):
                avisos.append("spine.compliance vino VACÍO → confirmar explícitamente con la etapa 1. "
                              "No se asume 'sin restricciones' (crítico en salud/finanzas).")
            else:
                faltantes.append(f"spine.{campo}  (ausente o vacío)")

    # sub-objeto mecanismo
    mec = spine.get("mecanismo")
    if isinstance(mec, dict):
        for sub in CONFIG["spine_mecanismo_subcampos"]:
            if sub not in mec or _is_empty(mec.get(sub)):
                # lexico_prohibido vacío no bloquea, pero es sospechoso -> aviso fuerte
                if sub == "lexico_prohibido":
                    avisos.append("spine.mecanismo.lexico_prohibido vacío → confirmar con etapa 1 "
                                  "(un compliance vacío es sospechoso en salud/finanzas).")
                else:
                    faltantes.append(f"spine.mecanismo.{sub}  (ausente o vacío)")
    elif "mecanismo" not in faltantes and mec is not None:
        faltantes.append("spine.mecanismo  (debe ser objeto con tipo/nombre/explicacion/lexico_prohibido)")

    # sub-objeto compliance
    comp = spine.get("compliance")
    if isinstance(comp, dict):
        vacios = [s for s in CONFIG["spine_compliance_subcampos"]
                  if s not in comp or _is_empty(comp.get(s))]
        if vacios:
            avisos.append("spine.compliance con subcampos vacíos "
                          f"({', '.join(vacios)}) → confirmar con etapa 1. No se asume 'sin restricciones'.")

    # awareness enum
    aw = spine.get("awareness")
    if aw and aw not in CONFIG["enums"]["awareness"]:
        faltantes.append(f"spine.awareness = {aw!r} no es uno de {CONFIG['enums']['awareness']}")

    return faltantes, avisos


def _heuristic_md_check(spine_path):
    """Chequeo blando para Spine markdown freeform. Devuelve lista de avisos (nunca bloquea)."""
    text = _read(spine_path).lower()
    # marcadores de sección de la plantilla INPUT — Spine
    marcadores = {
        "avatar": ["avatar"],
        "deseo masivo": ["deseo masivo", "quiero"],
        "awareness": ["awareness", "conciencia", "consciencia"],
        "emoción troncal": ["emoción troncal", "emocion troncal", "arco emocional"],
        "mecanismo": ["mecanismo", "ump", "ums", "usp"],
        "villano": ["villano"],
        "prueba": ["prueba"],
        "objeción raíz": ["objeción", "objecion"],
        "compliance / léxico prohibido": ["compliance", "léxico prohibido", "lexico prohibido"],
        "scripts ganadores": ["scripts ganadores", "competidor"],
    }
    ausentes = [nombre for nombre, keys in marcadores.items()
                if not any(k in text for k in keys)]
    avisos = []
    if ausentes:
        avisos.append("Spine markdown freeform: no se detectaron secciones para → "
                      + ", ".join(ausentes) + ". Revisar a mano.")
    avisos.append("Spine en markdown freeform: validación estricta NO aplicada. "
                  "Para validación dura, entrega el Spine como .json o con un bloque ```json``` embebido.")
    return avisos


def _report_bloqueo(producto, faltantes, degradaciones):
    lines = ["", "=" * 60, "INPUT INCOMPLETO — ejecución BLOQUEADA", "=" * 60,
             f"Producto: {producto}", "", "Faltan (obligatorios):"]
    for f in faltantes:
        lines.append(f"  - {f}")
    if degradaciones:
        lines.append("")
        lines.append("Degradaciones (no bloquean, se avisa):")
        for d in degradaciones:
            lines.append(f"  - {d}")
    lines += ["", "Acción requerida: la etapa 1 (research) debe surtir los campos "
              "obligatorios antes de re-ejecutar.", "=" * 60, ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Fase 0 — intake y snapshot del Motor de Creativos.")
    ap.add_argument("--producto", required=True, help="Nombre interno del producto (define casos/<slug>/).")
    ap.add_argument("--spine", required=True, help="Ruta al Spine (.json o .md).")
    ap.add_argument("--scripts", required=True, help="Ruta a los scripts ganadores del competidor.")
    ap.add_argument("--voc", default=None, help="Ruta al banco VoC (opcional).")
    ap.add_argument("--spine-version", default="(sin declarar)", help="Versión del Spine origen (para _meta).")
    ap.add_argument("--autor", default="AI", help="Quién ejecuta el intake.")
    ap.add_argument("--allow-freeform", action="store_true",
                    help="Permite un Spine markdown SIN bloque ```json```. SALTA la validación "
                         "estricta de INTERFACE §2 — bajo tu responsabilidad.")
    ap.add_argument("--root", default=None, help="Raíz alternativa donde escribir casos/ (default: raíz del repo).")
    args = ap.parse_args()

    degradaciones, avisos = [], []

    # --- Existencia de archivos obligatorios ---
    if not os.path.isfile(args.spine):
        print(f"ERROR: no existe el Spine en {args.spine!r}", file=sys.stderr)
        sys.exit(2)
    scripts_ok = os.path.isfile(args.scripts)
    if not scripts_ok:
        degradaciones.append("Faltan scripts ganadores (Input B) → ejecución solo IDEACIÓN "
                             "(mayor riesgo). Surtir ganadores desde etapa 1 / ad-spy.")
    voc_ok = bool(args.voc) and os.path.isfile(args.voc)
    if not voc_ok:
        degradaciones.append("Sin banco VoC (Input C) → hooks derivados del Spine, NO de VoC literal. "
                             "Los agentes NO deben inventar IDs EVxxxx.")

    # --- Validación del Spine ---
    try:
        spine_obj, modo = _extract_spine_object(args.spine)
    except ValueError as e:
        print(_report_bloqueo(args.producto, [f"spine: {e}"], degradaciones))
        sys.exit(2)

    if spine_obj is not None:
        faltantes, av = _validate_spine_object(spine_obj)
        avisos += av
    else:
        # Spine markdown FREEFORM: no se puede validar campo por campo. Por la regla de la
        # INTERFACE (§6/§8 — el motor NO rellena huecos) esto BLOQUEA por defecto; antes
        # pasaba sin validar nada, que es peor que no validar: da falsa confianza.
        avisos += _heuristic_md_check(args.spine)
        if args.allow_freeform:
            faltantes = []
            avisos.append("⚠️ --allow-freeform: validación estricta OMITIDA bajo tu responsabilidad. "
                          "Los baches pueden construirse sobre un Spine incompleto.")
        else:
            faltantes = [
                "spine: markdown freeform SIN bloque ```json``` → no se puede validar contra INTERFACE §2.\n"
                "      Soluciones: (a) entrega el Spine como .json — lo emite la skill /master-spine;\n"
                "                  (b) embebe el objeto Spine en un bloque ```json``` dentro del .md;\n"
                "                  (c) si aun así quieres correr sin validar, usa --allow-freeform."
            ]

    # --- Decisión de bloqueo ---
    if faltantes:
        print(_report_bloqueo(args.producto, faltantes, degradaciones))
        sys.exit(2)

    # --- Snapshot (INTERFACE §5) ---
    paths = ensure_dirs(case_paths(args.producto, root=args.root))
    ext_spine = ".json" if modo == "json" else ".md"
    snap = {
        "spine": os.path.join(paths["input"], f"spine.snapshot{ext_spine}"),
        "scripts": os.path.join(paths["input"], "scripts.snapshot.md") if scripts_ok else None,
        "voc": os.path.join(paths["input"], "voc.snapshot.md") if voc_ok else None,
    }
    shutil.copyfile(args.spine, snap["spine"])
    if scripts_ok:
        shutil.copyfile(args.scripts, snap["scripts"])
    if voc_ok:
        shutil.copyfile(args.voc, snap["voc"])

    hashes = {"spine": _sha256(snap["spine"])[:16]}
    if snap["scripts"]:
        hashes["scripts"] = _sha256(snap["scripts"])[:16]
    if snap["voc"]:
        hashes["voc"] = _sha256(snap["voc"])[:16]

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    meta_md = f"""# _meta — snapshot del input

| Campo | Valor |
|---|---|
| Producto | {args.producto} |
| Slug | {slugify(args.producto)} |
| Fecha de la corrida | {now} |
| Versión del Spine origen | {args.spine_version} |
| Modo de validación del Spine | {modo} |
| Ejecutó | {args.autor} |
| Hash Spine (sha256/16) | {hashes.get('spine','-')} |
| Hash Scripts (sha256/16) | {hashes.get('scripts','-')} |
| Hash VoC (sha256/16) | {hashes.get('voc','-')} |
| Contrato | INTERFACE v1.0 |

**Regla de reproducibilidad:** este snapshot es la copia CONGELADA del input consumido.
Todo el output de esta corrida (baches, roadmap, briefs) referencia ESTE snapshot, no el
Spine "vivo" del research. Si el research publica un Spine nuevo, se hace una corrida NUEVA
con su propio snapshot; este no se toca.
"""
    with open(os.path.join(paths["input"], "_meta.md"), "w", encoding="utf-8") as f:
        f.write(meta_md)

    # --- Reporte de aceptación ---
    print("=" * 60)
    print(f"INPUT ACEPTADO — {args.producto}")
    print("=" * 60)
    print(f"Modo de validación del Spine : {modo}")
    print(f"Scripts ganadores            : {'sí' if scripts_ok else 'NO (degradado a ideación)'}")
    print(f"Banco VoC                    : {'sí' if voc_ok else 'NO (hooks Spine-derived)'}")
    print(f"Snapshot escrito en          : {paths['input']}")
    if avisos or degradaciones:
        print("\nAVISOS:")
        for a in avisos + degradaciones:
            print(f"  [!] {a}")
    print("\nSiguiente paso: correr wf_motor (ver RUNBOOK.md) con los paths del snapshot.")
    # emitir los paths del snapshot como JSON en la última línea, para encadenar en scripts
    print("\nSNAPSHOT_JSON " + json.dumps({
        "producto": args.producto,
        "slug": slugify(args.producto),
        "spinePath": snap["spine"],
        "scriptsPath": snap["scripts"],
        "vocPath": snap["voc"],
        "paths": paths,
        "voc_presente": voc_ok,
        "scripts_presente": scripts_ok,
    }, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
