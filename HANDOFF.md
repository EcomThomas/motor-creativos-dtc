# HANDOFF — Motor de Creativos DTC (Etapa 2)

**Documento de traspaso para la próxima sesión de refinamiento.**
Léelo completo antes de tocar nada. Al final tienes el backlog accionable, las preguntas abiertas de diseño y la nota operativa de deploy.

---

## 1. Por qué existe este repo

Este repo nació de **separar la etapa de creativos del Motor de Research**. Antes, "research" y "creativos" vivían mezclados en el mismo sistema; eso los acoplaba y hacía imposible iterar uno sin romper el otro.

La decisión de diseño es tratar el pipeline DTC como **4 etapas desacopladas**, cada una con su propio contrato de entrada/salida:

```
Research  ->  CREATIVOS (este repo)  ->  Media Buying / Test  ->  Feedback
   ^                                                                  |
   +------------------------------------------------------------------+
```

Beneficios de la separación:

- **Replicabilidad:** el Motor de Creativos es una máquina que funciona para CUALQUIER producto DTC (ads Meta/TikTok, metodología Eugene Schwartz). No está atado a ningún producto; los específicos entran por el INPUT.
- **Iteración independiente:** puedes refinar el método de creativos sin tocar el motor de research.
- **Contrato explícito:** la etapa 1 entrega un **Spine** (veredicto estratégico) + **scripts ganadores del competidor**; este repo los consume y produce baches de anuncios listos para producción.
- **Feedback loop limpio:** la etapa 3 (media buying) devuelve señales de performance que reabren la etapa 1, sin ambigüedad sobre quién es dueño de qué.

**Regla de oro:** este repo NUNCA hardcodea un producto. Todo lo específico (avatar, deseo, villano, mecanismo, compliance) llega vía el Spine y la plantilla de input.

---

## 2. Qué YA está montado

El scaffold base está completo y funcional como método (aún no del todo parametrizado como código — ver backlog).

### 2.1 Scaffold del repo
- Estructura de carpetas para docs de método, workflows, specs e input.
- README con el canon del motor y el vocabulario canónico (bache, imitación/iteración/ideación, paridad emocional, compliance).

### 2.2 Los 8 docs de método
Los documentos que definen CÓMO se generan los creativos, product-agnostic (numeración = archivos en `metodo/`):

| # | Doc | Qué define |
|---|-----|-----------|
| 01 | **Bache** (definición + schema) | Schema del bache: concept, angle, avatar, sub_avatar, mass_desire, awareness, hypothesis, valence, emociones_83, trigger_batch, ads[] |
| 02 | **Clasificación** (imitación · iteración · ideación) | Cuándo usar cada una (imitación = mayoría cuando te apoyas en ganadores; son opciones, no cuota) |
| 03 | **Imitación** (clonar un ganador y re-anclar) | Cómo conservar el ARCO del ganador y cambiar solo el CONTENIDO al Spine |
| 04 | **Brief** (storyboard + paridad emocional) | Script + storyboard con paridad emocional + prompts de generación por bache |
| 05 | **Compliance** de creativos | Marco general: sin claims absolutos, afirmaciones fuertes en boca de testimonio, disclaimers/overlays |
| 06 | **Convención Creative Roadmap (Excel)** — LEGACY | El volcado a Excel; superado por el entregable ClickUp (`metodo/08`) |
| 07 | **Banco de técnicas de guion y hook** (EVOLVE + EAM) | Tráfico frío (Mirror/Hijack) + Three-Element hook test + técnicas de guion |
| 08 | **Entregable ClickUp** (tarea madre + subtareas) | Formato de salida de Fase 3: tarea madre + subtareas en texto plano |

### 2.3 Spec
- Definición del contrato de INPUT (Spine + scripts ganadores + VoC opcional) y del OUTPUT (N baches, M ads/bache, entregable ClickUp, brief por bache).
- Schemas de bache y de ad, con los campos ClickUp (`valence`, `emociones_83`, `trigger_batch`; y por pieza `nombre_creativo`, `concepto_corto`, `trigger_emocional`).

### 2.4 Interfaz
- Definición de cómo se invoca el motor y qué consume/produce cada módulo.

### 2.5 Los 3 workflows generalizados
Los workflows del método, ya escritos de forma product-agnostic (pendiente parametrizarlos como scripts que reciban paths por argumento — ver backlog):

1. **Generar baches** — del Spine + scripts ganadores a N conceptos con hipótesis.
2. **Expandir bache a ads** — de un bache a M anuncios (mayoría imitaciones re-ancladas).
3. **Producir brief** — de un bache a script + storyboard + prompts de generación.

### 2.6 Plantilla de input
- Plantilla vacía para el Spine + slot para pegar scripts ganadores + slot para VoC opcional. Los marcadores (`<PRODUCTO>`, `<AVATAR>`, `<DESEO>`, `<VILLANO>`, `<MECANISMO>`, `<PRUEBA>`, `<OBJECION>`) se rellenan por producto.

---

## 3. Backlog de refinamiento (accionable)

Ordenado por prioridad. Cada tarea es concreta y cerrable.

### P0 — Corribilidad end-to-end ✅ HECHO (2026-07-05)

> **Corrección al handoff anterior:** el P0 original decía "parametrizar los 3 workflows por argumento". Al revisar el código, **eso ya estaba hecho**: los tres workflows reciben todo por `args` (`spinePath`, `scriptsPath`, `product`, `adsPerBatch`, `focos`/`batches`/`bundles`). El P0 real eran otros cuatro gaps que impedían correr el motor de punta a punta. Se cerraron en esta sesión:

- [x] **VoC cableado (bug de contrato).** Antes, los 3 workflows instruían a los agentes a citar `IDs EVxxxx` y el Spec (Fase 2, "hecho bien") *exigía* 2–4 por ad, pero **ningún workflow recibía la VoC** → el agente no podía cumplir y podía alucinar IDs. Ahora los 3 aceptan `vocPath` y aplican el contrato de la INTERFACE §4 en ambos sentidos: **con** banco VoC citan IDs reales del archivo; **sin** banco, declaran hooks derivados del Spine y **tienen prohibido inventar IDs**.
- [x] **Persistencia (`--out`).** Los workflows corren en el sandbox de Workflow (sin filesystem): generan y *devuelven* datos. Se añadió la capa Python que escribe a disco: `scripts/persist.py` materializa el bundle en `casos/<slug>/` (`baches/batches_meta.json`, `scripts-ads/ads.json`, briefs `.md`/`.docx`). Ya NO toca Excel; el entregable operativo es el ClickUp de Fase 3 (`clickup_export.py`).
- [x] **Config de defaults en un solo lugar.** `config.json` (raíz) + `scripts/motor_config.py`: `N_BACHES` (5), `M_ADS` (3), awareness default, política de clasificación (mayoría imitación), enums, los 5 ángulos base y la convención de paths de `casos/`.
- [x] **Orquestador.** `scripts/wf_motor.js`: un solo Workflow que enhebra Fase 1 → 2 → 4 en memoria (pipeline por foco, sin barreras) y devuelve el bundle completo, VoC-wired.
- [x] **Fase 0 que no existía en código.** `scripts/intake.py`: valida el Spine contra los obligatorios (INTERFACE §6/§8), aplica el protocolo de faltantes (bloquea con reporte `INPUT INCOMPLETO` si falta un obligatorio) y congela el snapshot en `casos/<slug>/input/` con `_meta.md` (§5).
- [x] **Runbook.** `RUNBOOK.md`: la secuencia operativa exacta (intake → wf_motor → persist → handoff), dado que los Workflow los invoca Claude, no un CLI.

**Cómo se probó:** `motor_config.py`, `intake.py` (caso válido → exit 0 + snapshot; caso con faltantes → exit 2 + reporte) y `persist.py` (bundle simulado → estructura de caso completa + `.docx`) corren OK end-to-end. Los 4 workflows pasan `node --check`. **Falta la validación viva:** correr `wf_motor.js` con un Spine real (gasta agentes/tokens) para ver la calidad del output generado.

### P1 — Generalización del método

- [ ] **Generalizar el compliance por categoría de producto.** Hoy el compliance es un marco general. Convertirlo en una tabla por categoría (salud/suplementos, finanzas, belleza, gadgets, etc.) donde el Spine seleccione la categoría y se cargue el léxico prohibido + reglas específicas. El caso de referencia (suplemento hepático) sirve de primer ejemplo de la categoría salud.

- [x] ~~**Builder de la hoja "Creative Roadmap" (Excel)** idempotente~~ — **DESCARTADO.** El motor ya no vuelca al Excel; la Fase 3 es el entregable ClickUp (`clickup_export.py`, `metodo/08`). `metodo/06` y `build_roadmap.py` quedan legacy.

### P2 — Conexión al resto del pipeline

- [ ] **Conectar la SALIDA a la etapa 3 (media buying / test).** Definir el contrato de handoff: qué campos de cada ad necesita el media buyer (naming convention, hipótesis, mapping bache->campaña/adset).

- [ ] **Cerrar el loop de feedback.** Definir cómo vuelven las señales de performance (ROAS, CTR, hook rate, etc.) y cómo re-alimentan la etapa 1 (research) para el siguiente ciclo. Mapear qué métrica valida/mata qué hipótesis de bache.

### P3 — Calidad y ejemplos

- [ ] **Añadir 1–2 casos de ejemplo end-to-end.** Usar el caso de referencia (suplemento hepático MX) como primer ejemplo completo: Spine -> baches -> ads -> brief. Añadir un segundo caso de otra categoría para probar que el motor es agnóstico.

- [ ] **Escribir tests / QA del método.** Checklist verificable por bache y por ad:
  - ¿Cada bache tiene los 7 campos del schema?
  - ¿Cada ad de imitación declara `imita_competidor` y conserva el arco del ganador?
  - ¿Cada línea del brief tiene paridad emocional (escena que refuerza)?
  - ¿El copy pasa el compliance de su categoría (sin claims absolutos, afirmaciones fuertes en testimonio)?
  - ¿El re-anclaje cambió SOLO el contenido, no el arco?

---

## 4. Preguntas abiertas de diseño

- **¿Cuántos baches por defecto?** El canon fija 3 ads/bache, pero N de baches queda abierto. ¿Lo fija el motor, el Spine, o el presupuesto de test de la etapa 3?
- **¿Formato canónico del Spine?** ¿JSON estricto (mejor para parsear) o Markdown (mejor para leer/editar a mano)? Afecta cómo parametrizamos los workflows.
- **¿Quién es dueño de la naming convention** de campañas/adsets? ¿La define este repo (etapa 2) o la etapa 3? Impacta el contrato de handoff.
- **Mezcla de clasificación:** el canon dice "mayoría imitación", pero ¿cuál es el umbral? ¿100% imitación es válido para un bache? ¿Conviene forzar al menos 1 iteración/ideación por concepto para no depender solo del competidor?
- **VoC obligatorio u opcional:** hoy es opcional. ¿Debería ser obligatorio para baches de ideación (que nacen del insight de VoC)?
- **Compliance:** ¿tabla estática por categoría, o el Spine trae su propio léxico prohibido ya resuelto desde la etapa 1?
- **Versionado de baches:** cuando el feedback mata una hipótesis, ¿se versiona el bache (v2) o se crea uno nuevo? Impacta la trazabilidad del loop.

---

## 5. Nota operativa (deploy)

**Crear el repo remoto y hacer `push` está BLOQUEADO en auto-mode** (el clasificador de exfiltración detiene la operación). Por lo tanto:

- El **push lo corre el usuario** manualmente, o
- Se habilita vía **regla de permiso** explícita en la config del harness.

El resto del trabajo (editar docs, workflows, specs, plantillas, builders locales) NO está bloqueado y puede hacerse en auto-mode. Solo la creación/push del remoto requiere acción del usuario.

---

## 6. Estado y fecha

- **Estado:** scaffold + 6 docs de método + spec + interfaz + plantilla de input **montado**, y **P0 (corribilidad end-to-end) cerrado**: Fase 0 (intake+snapshot), config de defaults, VoC cableado, orquestador y capa de persistencia — el motor ya corre de punta a punta (ver `RUNBOOK.md`). Falta la **validación viva con un Spine real**, P1 (compliance por categoría + roadmap idempotente) y P2 (conexiones al resto del pipeline).
- **Fecha de este handoff:** 2026-07-05 (actualizado esta sesión).
- **Próximo paso recomendado:** correr `wf_motor.js` con un Spine + scripts reales (primer caso de referencia dentro de este repo, P3) para validar la calidad del output, ya con el entregable ClickUp y el hook gate activos.

> **Cambio de salida (importante).** El motor **ya NO vuelca al Excel** "Creative Roadmap" (se hacía a mano, se corrompía, demasiada info). La Fase 3 entrega ahora el **formato ClickUp** (tarea madre + subtareas en texto plano) vía `scripts/clickup_export.py`, según el prompt de batch del equipo. Flujo: baches en ClickUp → flujo del dueño → Media Buying genera reporte / lo lleva al Growth Guide. `metodo/06` (Excel) y `build_roadmap.py` quedan **legacy**. El bache se extendió con `sub_avatar`, `valence`, `emociones_83`, `trigger_batch` y, por pieza, `nombre_creativo`/`concepto_corto`/`trigger_emocional` (ver `metodo/08`). Esto **cierra el P1 de "roadmap idempotente"**: ya no aplica (no hay Excel).

---

## 7. Archivos nuevos de esta sesión (mapa rápido)

| Archivo | Rol |
|---|---|
| `config.json` | Fuente única de defaults (N, M, awareness, enums, 5 ángulos base, paths). |
| `RUNBOOK.md` | Cómo correr el motor end-to-end (modelo de 2 capas: Python valida/escribe, Workflow genera). |
| `scripts/motor_config.py` | Loader de `config.json` + helpers de paths (`case_paths`, `slugify`). |
| `scripts/intake.py` | Fase 0: valida Spine (INTERFACE §6/§8) + congela snapshot (§5). |
| `scripts/persist.py` | Escribe el bundle (datos + briefs) a `casos/<slug>/`. Ya NO toca Excel. |
| `scripts/clickup_export.py` | **Fase 3 (nueva salida):** genera el entregable ClickUp (tarea madre + subtareas) por bache. |
| `scripts/wf_motor.js` | Orquestador: Fase 1→2→4 en una corrida, VoC-wired, hook gate + cold-traffic, campos ClickUp; devuelve el bundle. |
| `scripts/wf_baches.js`·`wf_imitaciones.js`·`wf_briefs.js` | `vocPath` + hook gate + campos ClickUp (`valence`, `emociones_83`, `trigger_*`, etc.). |
| `scripts/md2docx.py` | Refactor: ahora es importable (`convert`, `convert_folder`) además de CLI. |
| `metodo/07`, `metodo/08` | Banco de técnicas EVOLVE+EAM · Formato del entregable ClickUp. |
| `scripts/build_roadmap.py`, `metodo/06` | **LEGACY** (Excel, fuera del flujo estándar). |
