# RUNBOOK — Cómo correr el Motor de Creativos end-to-end

Guía operativa para producir baches + briefs de un producto, de principio a fin. Es el "cómo se ejecuta" que complementa al *qué es* (README) y al *cómo funciona por dentro* (Spec Operativo).

## Modelo de ejecución (leer una vez)

El motor tiene **dos capas** que corren en sitios distintos:

| Capa | Qué hace | Dónde corre | Acceso a disco |
|------|----------|-------------|----------------|
| **Generación** (`scripts/wf_*.js`) | Escribe baches, imitaciones y briefs con agentes | Sandbox de **Workflow** (lo invoca Claude) | **NO** — genera y *devuelve* datos |
| **Persistencia/validación** (`scripts/*.py`) | Valida input, congela snapshot, escribe el caso a disco, genera el entregable ClickUp | Terminal (Python) | Sí |

Por eso el flujo alterna: **Python valida y congela** → **Workflow genera** → **Python escribe**. Los workflows no pueden tocar archivos; solo los agentes que lanzan leen los paths que se les pasan (Spine, scripts, VoC).

Los **defaults** (N=5 baches, M=3 ads, awareness default, los 5 ángulos base) viven en un solo lugar: [`config.json`](config.json).

---

## Paso 0 — Preparar el INPUT

Duplica [`plantillas/INPUT — Spine (plantilla).md`](plantillas/INPUT%20—%20Spine%20(plantilla).md) por producto y rellénalo, o trae el Spine del Motor de Research. Necesitas:

- **Spine** — `.json` (recomendado: lo emite la skill `/master-spine`) **o** `.md` **con** el bloque ` ```json … ``` ` del §13 de la plantilla. ⚠️ Un `.md` **sin** ese bloque **BLOQUEA** el intake (no se puede validar contra INTERFACE §2); si aun así quieres correr sin validar, usa `--allow-freeform` bajo tu responsabilidad.
- **Scripts ganadores** del competidor (`.md`). Sin ellos la corrida degrada a solo-ideación.
- **Banco VoC** (opcional, `.md` o `.json`) con IDs `EVxxxx`. Sin él, los hooks se declaran *derivados del Spine* y **los agentes no inventan IDs**.

Contrato completo de estos tres inputs: [`INTERFACE — Contrato con el Motor de Research.md`](INTERFACE%20—%20Contrato%20con%20el%20Motor%20de%20Research.md).

---

## Paso 1 — Fase 0: intake (validar + congelar snapshot)

```bash
python scripts/intake.py \
  --producto "Suplemento Hepatico MX" \
  --spine   ruta/al/Spine.json \
  --scripts ruta/al/competitor_scripts.md \
  --voc     ruta/al/voc_bank.md          # opcional; omite si no hay
  --spine-version "v3.2" --autor "Thomas"
```

- **exit 0** → input aceptado. Escribe el snapshot congelado en `casos/<slug>/input/` (`spine.snapshot.*`, `scripts.snapshot.md`, `voc.snapshot.md`, `_meta.md`) y **imprime una línea `SNAPSHOT_JSON {…}`** con los paths listos para el siguiente paso.
- **exit 2** → **BLOQUEADO**: falta un campo obligatorio del Spine. Imprime el reporte `INPUT INCOMPLETO`; se devuelve a la etapa 1. No se genera nada. (El motor **no** rellena huecos.)

Copia los paths de `SNAPSHOT_JSON` (`spinePath`, `scriptsPath`, `vocPath`) para el Paso 2.

---

## Paso 2 — Fases 1·2·4: generar (Workflow, lo corre Claude)

Claude invoca el orquestador **una vez**; enhebra baches → imitaciones → briefs en memoria:

```
Workflow({
  scriptPath: 'scripts/wf_motor.js',
  args: {
    spinePath:   'casos/<slug>/input/spine.snapshot.json',
    scriptsPath: 'casos/<slug>/input/scripts.snapshot.md',
    vocPath:     'casos/<slug>/input/voc.snapshot.md',   // o null
    product:     'Suplemento Hepatico MX (es-MX, Meta)',
    adsPerBatch: 3
    // focos: [...]  // opcional; si se omite usa los 5 ángulos base de config.json
  }
})
```

**Devuelve el BUNDLE** (JSON en memoria):

```
{ producto, slug, snapshot:{spinePath,scriptsPath,vocPath},
  batches:[ {n,slug,concept,angle,avatar,mass_desire,awareness,hypothesis, ads:[{imita_competidor,ad_format,copy,nota}]} ],
  briefs:[ {n,slug,md} ] }
```

Claude guarda ese bundle a un archivo, p. ej. `casos/<slug>/bundle.json`.

> **Personalizar los ángulos:** pasa `args.focos` como `[{key,title,desc}, …]` (uno por bache) tomándolos de `config.json > angulos_base`, o añade ejes propios del Spine (otro sub-avatar, otra objeción). N = `focos.length`.

---

## Paso 3 — persistir los datos + briefs a disco

```bash
python scripts/persist.py --bundle casos/<slug>/bundle.json [--docx]
```

Escribe en `casos/<slug>/`:

- `baches/batches_meta.json` — los N baches con sus ads (fuente de verdad de la corrida).
- `scripts-ads/ads.json` — lista plana de anuncios.
- `briefs/bache-<n>-<slug>.md` — el brief de producción por bache (+ `.docx` si `--docx`).

> El motor **ya NO vuelca al Excel**. El entregable operativo se genera en el Paso 4.

---

## Paso 4 — Fase 3: entregable ClickUp (lo que se pega/pasa al flujo)

```bash
python scripts/clickup_export.py --bundle casos/<slug>/bundle.json \
  --batch-num 7 --producto "<PRODUCTO>" --plataforma "Meta" \
  --carpeta "<LINK carga>" --cta "<LINK destino CTA>" \
  --assets "Asset 1 — <link>; Asset 2 — <link>"
```

Genera `casos/<slug>/clickup/batch_<N>.txt` por bache: **etiqueta corta + tarea madre + subtareas** en texto plano, pegable en ClickUp (formato de [metodo/08](metodo/08%20—%20Entregable%20ClickUp%20(tarea%20madre%20+%20subtareas).md)). Los links y el número de batch los pones aquí; lo que falte queda como `[LINK]`/`[FALTA DEFINIR]`. El campo `Brief` queda como placeholder (el brief real es el `.md` del Paso 3).

---

## Paso 5 — Fase 5: handoff a Media Buying (Etapa 3)

El `.txt` de cada bache se pega en ClickUp como tarea madre + subtareas. Desde ahí el dueño lo pasa a su flujo y el equipo de Media Buying genera el reporte / lo lleva al Growth Guide. La trazabilidad (bache, hipótesis, valence/emoción) viaja en la tarea madre; el brief de producción (paridad emocional) viaja como documento externo referenciado por el placeholder `Brief`.

---

## Alternativa granular (correr una fase a la vez)

`wf_motor.js` es lo normal. Si quieres iterar una sola fase (p. ej. regenerar solo los briefs), corre los workflows sueltos — todos aceptan `vocPath`:

| Workflow | Args clave | Devuelve |
|----------|-----------|----------|
| `scripts/wf_baches.js` | `spinePath, scriptsPath, vocPath?, product, adsPerBatch, focos[]` | `{ patches:[bache con ads borrador] }` |
| `scripts/wf_imitaciones.js` | `spinePath, scriptsPath, vocPath?, batches[], adsPerBatch` | `{ batches:[{ads[]}] }` (alineado por índice) |
| `scripts/wf_briefs.js` | `spinePath, vocPath?, bundles[]` | `{ briefs:[{n,slug,md}] }` |

Enhebras sus salidas a mano y las pasas a `persist.py` con la misma forma de bundle.

---

## Checklist de una corrida sana

- [ ] `intake.py` salió con **exit 0** (o se resolvieron los faltantes con la etapa 1).
- [ ] Snapshot escrito en `casos/<slug>/input/` con `_meta.md`.
- [ ] Cada ad nombra un **competidor imitado**; si hubo VoC, cita **IDs EVxxxx reales**; si no, **no** inventa IDs.
- [ ] Cada bache es un **ángulo/hipótesis distinto** (no cinco variantes del mismo hook).
- [ ] Cada brief tiene la **tabla de storyboard** con una fila por beat (paridad emocional).
- [ ] El `copy` respeta el **léxico prohibido** del Spine (compliance).
