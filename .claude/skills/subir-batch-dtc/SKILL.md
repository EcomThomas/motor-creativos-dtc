---
name: subir-batch-dtc
description: >-
  Genera y monta un BATCH de creativos DTC con el formato de la casa: bundle →
  briefs (storyboard de paridad emocional + un prompt de generación IA por CADA
  escena) → ClickUp en estado "idea" (tarea madre + subtareas) → Google Drive (1
  carpeta por batch, 1 Doc por video) → links enlazados en cada subtarea. Úsala
  cuando el usuario quiera subir/montar un batch de anuncios, convertir scripts o
  videos ganadores en variantes, iterar un ganador (perspective-shift) o llevar
  creativos a su flujo de ClickUp. Multi-tienda: cada persona usa su propio perfil
  (config.local.json) y sus tokens (.env), en el mismo workspace de ClickUp pero
  distinta lista/tienda.
---

# Subir un BATCH de creativos (ClickUp + Drive)

Toma un input creativo (scripts/videos ganadores, un bundle ya hecho, o un concepto)
y lo deja **montado y trazable**: subtareas en ClickUp (estado `idea`) + un brief por
video en Google Drive, con el **mismo formato** para todo el equipo.

El formato lo garantizan scripts **deterministas** (no los reescribas): tú generas la
creatividad (bundle + briefs); los scripts arman ClickUp igual para todos. Fuente de
verdad del formato: **`metodo/04`** (brief), **`metodo/05`** (compliance) y **`metodo/08`**
(entregable ClickUp). Ante cualquier duda de formato, gana el método, no esta skill.

---

## 0. Preflight (una sola vez por persona)

Si falta algo, sigue `SETUP.md` (misma carpeta) y detente hasta resolverlo:

1. **`.env`** en la raíz con `CLICKUP_TOKEN=` (tu token personal `pk_`). Verifica que
   los secretos resuelven de verdad (esto SÍ lee el token; no imprime su valor):
   ```bash
   python -c "from scripts.motor_config import secrets_path, get_token; print('secretos:', secrets_path()); print('clickup ok:', bool(get_token('CLICKUP_TOKEN')))"
   ```
2. **`config.local.json`** en la raíz (copia de `config.local.example.json`) con TU
   `clickup_list_id`, `clickup_status` (= `idea`), `drive_parent_folder_id`, `producto`
   y `spine_path`. Verifica: `python -c "from scripts.motor_config import store; print(store())"`.
3. **Conector de Google Drive** conectado en tu Claude (para crear los Docs). Si no lo
   tienes, genera los briefs como `.md` locales y súbelos a mano.

---

## 1. Recibe el input y clasifícalo

Define la **clasificación** del batch:

- **Ganador tuyo** que quieres multiplicar → **Iteration** (ej. perspective-shift: mismo
  esqueleto, rota el narrador; usa la skill `perspective-shift`).
- **Referencia de competencia** a adaptar a tu producto → **Imitation** (clona el ganador
  y re-ancla al Spine; ver `metodo/03`). **Es el default** cuando te apoyas en ganadores.
- **Concepto nuevo desde el Spine** → **Ideation**.

Si te dan un **video**, la transcripción y el desglose por escena son fiables, pero
**aterriza SIEMPRE la interpretación con el Spine** — sin contexto de producto, el
análisis de video alucina el "significado comercial".

**Lee el Spine** (`spine_path` de tu `config.local.json`): mecanismo, villano, avatar,
oferta y **léxico prohibido / compliance**. Todo lo que generes lo respeta.

## 2. Construye el bundle

`bundle.json` = `{ "producto", "plataforma", "batches": [ ... ] }`. Referencia de schema:
`plantillas/bundle.example.json`. **Composición por defecto (metodo/04 §3): ~3 piezas por
batch, mayoritariamente `Imitation`** salvo indicación contraria (no fuerces una-de-cada-tipo).

Cada batch lleva los campos que exige `metodo/08 §2`:

- **Batch:** `concept`, `angle`, `hypothesis`, `avatar`, `sub_avatar`, `mass_desire`,
  `valence` (`Positiva`/`Negativa`/`Mixta`), `emociones_83` (1–3), `awareness`,
  `classification` (`Imitation`/`Iteration`/`Ideation`), `trigger_batch`, `assets` (lista),
  `ads: [...]`.
- **Cada ad:** `ad_format` (`Video`/`Static`), `nombre_creativo`, `concepto_corto` (va en el
  título de la subtarea), `trigger_emocional`.

No inventes `valence`/`emociones`/`trigger`: sácalos del Spine + el copy. Guarda el bundle
en `casos/<tu-producto>/bundle_<n>.json` (los `casos/` son locales, gitignored).

## 3. Genera los briefs (uno por pieza) — formato metodo/04 EXACTO

Un brief por cada pieza del batch, en el formato de `metodo/04`, **completo**. Secciones
por anuncio **en este orden** (igual que metodo/04 §3.x):

**Meta → Script verbatim → Storyboard → Arco emocional → Dirección de arte/luz/color → Prompts IA.**

1. **Meta** (tabla): `Clasificación` · `Imita a (si aplica)` · `Formato (ad_format)` ·
   `Hook (primeros 3s)` · `Nota`.
2. **Script verbatim** — el guion **palabra por palabra** (OBLIGATORIO; sin esto el brief
   no pasa QA). Si es Static, el copy de cada frame.
3. **Storyboard con paridad emocional** — tabla con estas **8 columnas EXACTAS, en este
   orden y con estos nombres (NO renombrar ni reordenar):**
   ```
   | # | Tiempo | Línea del script (fragmento) | Emoción objetivo | Dirección visual (encuadre/acción/expresión/luz/color) | B-roll/inserto | Texto en pantalla | Audio (VO/música/SFX) |
   ```
   Descompón TODO el guion: una fila por beat. Cada fila amarra una línea a una emoción y a
   una decisión visual/sonora que la sostiene (paridad emocional).
4. **Arco emocional (throughline):** estado inicial → giro → clímax de prueba → resolución/CTA.
5. **Dirección de arte / luz / color.**
6. **Prompts de generación IA — uno por CADA escena del storyboard.** Tantos prompts como
   filas tenga la tabla, sin saltarte ninguna. **Rotula cada prompt `Escena k`** correlativo
   a la fila `k` del storyboard (verificación 1:1). Cada prompt es autosuficiente: sujeto +
   acción/expresión + encuadre + luz + color + emoción + estilo + aspect ratio.

Además, en la **Ficha estratégica** (§1) el brief DEBE incluir el bloque **"Reglas de
compliance de este bache"** (metodo/04 §1, ver metodo/05) como CONTENIDO, no como chequeo
mental: (a) **Claims prohibidos** (lista del léxico del Spine); (b) **Afirmaciones fuertes**
siempre en boca de testimonio/creencia; (c) **Disclaimers/overlays** con el **texto exacto**
y en qué planos aparecen; (d) **Framing de categoría** (salud: mecanismo como testimonio, no
claim clínico). Si es whitelisting, marca el **tipo de página** de cada pieza.

Si tienes el tool Workflow, lánzalo con **un agente por pieza** (leen la variante + el Spine
y devuelven el brief). Guárdalos en `casos/<tu-producto>/briefs-<n>/brief_<k>.md`, donde `k`
es la **posición** del ad en el bundle (1, 2, 3…).

## 4. Sube a ClickUp (estado `idea`)

```bash
python scripts/clickup_upload.py --bundle casos/<tu-producto>/bundle_<n>.json \
  --start-num <n> --status idea
```
- El **estado canónico es `idea`** para todo el equipo. Ponlo en `clickup_status` de tu
  `config.local.json` y no hace falta pasar `--status`; si lo pasas, que sea `idea`.
- `--list` sale de tu `config.local.json` (no lo pases salvo override puntual).
- **Numeración `--start-num`:** en una lista nueva/vacía empieza en `1`; si ya tienes batches,
  usa el **número más alto (BATCH #N) que exista en tu lista de ClickUp + 1** (míralo en la lista).
- Crea la tarea madre + una subtarea por pieza y **emite** el estado de montaje en
  `casos/<tu-producto>/clickup/finalize_<n>.json` con los IDs reales, y `folder_url`/`docs`
  **en blanco** para completar.

> Numeración de subtareas: **V=Video, G=Static**, contador por tipo (V1,V2… / G1,G2…),
> derivado de `ad_format`. En `finalize_<n>.json` la clave de `subtasks` y `docs` es la
> **POSICIÓN del ad en el bundle** (1..M en orden), NO la letra V/G.

## 5. Sube los briefs a Google Drive

1. Crea la subcarpeta del batch bajo tu `drive_parent_folder_id` (`create_file` con
   `mimeType: application/vnd.google-apps.folder`), nombre `BATCH #<n> — <concepto>`.
2. Por cada brief, crea un **Google Doc nativo**: `create_file` con `parentId` = la carpeta
   del batch, `contentMimeType: text/markdown`, `textContent` = el brief completo (verbatim).
   Guarda el `viewUrl` de cada Doc, emparejado con la **posición** del ad (1, 2, 3…).

## 6. Completa y finaliza

1. Abre `casos/<tu-producto>/clickup/finalize_<n>.json` y rellena:
   - `folder_url`: link de la carpeta del batch en Drive.
   - `docs`: `{ "1": <Doc de la pieza 1>, "2": ..., ... }` (misma clave posicional que `subtasks`).
2. Corre:
```bash
python scripts/clickup_finalize.py --bundle casos/<tu-producto>/bundle_<n>.json \
  --config casos/<tu-producto>/clickup/finalize_<n>.json --start-num <n>
```
Reescribe la madre y cada subtarea con: **Carga de creativos** = carpeta del batch ·
**Destino del CTA** = manual (varía por advertorial/PDP) · **Brief** = link del Doc · +
concepto/nombre/trigger.

## 7. Reporta

Tabla: por pieza → narrador/ángulo · (tipo de página si aplica) · link de subtarea ClickUp ·
link del brief en Drive. Más el link de la tarea madre y la carpeta del batch.

---

## Reglas duras

- **Nada de Excel.** El entregable es ClickUp (campos vía API) + Docs en Drive.
- **Storyboard = 8 columnas literales** de metodo/04 (nombres y orden EXACTOS, no parafrasear).
- **Script verbatim obligatorio** en cada brief; y **un prompt IA por CADA escena** (rotulado
  `Escena k`), no 2–3 "clave": todas.
- **Compliance como contenido:** el brief incluye el bloque de compliance (claims prohibidos,
  afirmaciones en boca de testimonio, disclaimers con texto exacto + planos, framing). Nunca
  nombres a la competencia. Si dudas de un claim, márcalo `[REVISAR COMPLIANCE]` (fallback, no
  sustituto del bloque).
- **Estado ClickUp = `idea`** para todos (reproducible con las corridas del equipo).
- **No inventes IDs ni links.** Los de ClickUp salen de `finalize_<n>.json`; los de Drive, de
  `create_file`.
- **Secretos y datos de cliente son locales:** `.env`, `config.local.json`, `casos/` y
  `descargas*/` están gitignored. Nunca los comitees ni imprimas el valor de un token.
