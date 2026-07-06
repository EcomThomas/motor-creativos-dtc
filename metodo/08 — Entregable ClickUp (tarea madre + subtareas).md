# Método: Entregable ClickUp (tarea madre + subtareas)

Este documento define el **entregable operativo de la Fase 3** del motor: cómo se convierte un bache (concepto + sus M piezas) en **una tarea madre + N subtareas en texto plano**, listas para pegar en ClickUp. **Reemplaza el volcado al Excel "Creative Roadmap"** ([metodo/06](06%20—%20Convención%20Creative%20Roadmap%20(Excel).md), ahora legacy).

> **Por qué el cambio.** El Excel se llenaba a mano, se corrompía y cargaba demasiada info para procesarla ahí. El flujo real es: el motor entrega estos baches en formato ClickUp → el dueño los pasa a su flujo de trabajo → el equipo de Media Buying genera el reporte / lo lleva al Growth Guide. El motor produce el **texto pegable**; los links y el número de batch los completa el humano al montar en ClickUp.

Lo genera **`scripts/clickup_export.py`** de forma **determinística** a partir del bundle (no es un prompt que redacta: ensambla campos ya generados, para garantizar el formato exacto y no inventar datos).

---

## 1. Reglas del formato (no negociables)

- **Texto simple, limpio, pegable en ClickUp. SIN tablas. Sin párrafos largos.**
- La **tarea madre va primero**; luego **una subtarea por pieza**, en el orden lógico del bache.
- El campo **`Brief` de cada subtarea SIEMPRE es un placeholder** — el brief real es un documento aparte (Fase 4, [metodo/04](04%20—%20Brief%20(storyboard%20+%20paridad%20emocional).md)). Nunca se rellena aquí.
- Datos que no estén claros → **`[FALTA DEFINIR]`**. Links no provistos → **`[LINK]`**.
- El **número de batch del INPUT manda** (no se infiere): `--batch-num` lo fija.
- `valence`, `emociones_83` y `trigger_emocional` **no se inventan en el export**: vienen del bundle (los generó el motor, anclados en la emoción troncal del Spine + el copy). Si una pieza no trae trigger propio, hereda el del batch con `[HEREDADO DEL BATCH]`.

---

## 2. Campos que el motor debe generar (extensión del bache)

Además del schema base del bache ([metodo/01](01%20—%20Bache%20(definición%20+%20schema).md)), el formato ClickUp exige:

**A nivel de bache:**
| Campo | Qué es |
|---|---|
| `sub_avatar` | Segmento específico dentro del avatar (edad, situación, dolor puntual). |
| `valence` | Valence emocional dominante: `Positiva` / `Negativa` / `Mixta`. |
| `emociones_83` | Las 1–3 emociones que cubren ~83% del batch (del Spine + el copy). |
| `trigger_batch` | Trigger emocional troncal del batch (se hereda a piezas sin trigger propio). |

**A nivel de pieza (cada ad):**
| Campo | Qué es |
|---|---|
| `nombre_creativo` | Nombre interno claro y utilizable por el equipo. |
| `concepto_corto` | Idea PUNTUAL de la pieza (no estratégica), breve — va en el título de la subtarea. |
| `trigger_emocional` | Qué activa la respuesta emocional del avatar en ESA pieza. |

Todos se generan en Fase 1/2 (schemas de [wf_motor.js](../scripts/wf_motor.js) / [wf_baches.js](../scripts/wf_baches.js) / [wf_imitaciones.js](../scripts/wf_imitaciones.js)).

---

## 3. Estructura del entregable (por bache)

### 3.1 Etiqueta corta
```
ETIQUETA CORTA: BATCH #[N] · [PRODUCTO] | [CONCIENCIA] | [ÁNGULO] | [FORMATO] | [PLATAFORMA] | [VALENCE + EMOCIÓN 83%]
```
`[FORMATO]` = `Video` / `Gráfica` / `Mixto` según las piezas del batch.

### 3.2 Tarea madre
Texto plano con: Nombre batch · Carpeta de carga · Destino del CTA · Ad Concept · Ángulo · Hipótesis · Avatar · Sub avatar · Deseo masivo · Valence dominante · Emociones 83% · Nivel de conciencia · Tipo de ad (`ITERACIÓN`/`IMITACIÓN`/`IDEACIÓN`, del `classification` dominante) · Assets necesarios (bullets).

### 3.3 Subtareas (una por pieza)
- **Título:** `V<k> BATCH #<N> - <CONCEPTO CORTO>` si la pieza es **video**; `G<k> ...` si es **gráfica**. Numeración **por tipo** (V1, V2… / G1, G2…), derivada de `ad_format` (Video→V, Static→G).
- Campos: Concepto · Nombre creativo · Carga de creativos (link) · Destino del CTA (link) · **Brief: placeholder** · Trigger emocional.

Cada bloque va envuelto en `— COPIAR DESDE AQUÍ —` / `— FIN DEL TEXTO —` para pegado limpio.

---

## 4. INPUT operativo (lo pone el humano al exportar)

El motor no inventa links ni el número de batch de la cuenta. Se pasan al exportar (o quedan como placeholder para completar en ClickUp):

```bash
python scripts/clickup_export.py --bundle casos/<slug>/bundle.json \
  --batch-num 7 --producto "<PRODUCTO>" --plataforma "Meta" \
  --carpeta "<LINK carpeta de creativos>" --cta "<LINK destino CTA>" \
  --assets "Asset 1 — <link>; Asset 2 — <link>"
```
Salida: `casos/<slug>/clickup/batch_<N>.txt` (uno por bache).

---

## 5. Handoff a Media Buying (Fase 5)

El `.txt` de cada bache es lo que se pega en ClickUp como tarea madre + subtareas. Desde ahí el dueño lo pasa a su flujo y el equipo de Media Buying genera el reporte / lo lleva al Growth Guide. La trazabilidad (qué bache, qué hipótesis, qué valence/emoción) viaja en la tarea madre; el brief de producción (paridad emocional) viaja como documento externo referenciado por el placeholder `Brief`.
