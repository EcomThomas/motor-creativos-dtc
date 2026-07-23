---
name: master-spine
description: >-
  Consolida los documentos de un research VoC (docs 14-21, B0/B1, 10 del Motor de Research v4.0)
  en el MASTER SPINE (doc 00) — el veredicto estratégico final — y emite ADEMÁS un `spine.json`
  estructurado que el Motor de Creativos consume sin traducción manual (contrato INTERFACE §2).
  Es la FASE 6 del research y el puente hacia creativos. Úsala al CERRAR un research: "consolidar
  el spine", "cerrar el research", "doc 00", "master spine", "spine.json", "handoff a creativos",
  "generar el veredicto estratégico final". Requiere que los docs 14-21 + B0/B1 + 10 estén escritos,
  validados (anti-fabricación) y con QC cerrado. NO define oferta/pricing (eso es SOP-MKT-04).
---

# Master Spine — consolidación del research (doc 00) + contrato para creativos

Esta skill es la **FASE 6** del Motor de Research v4.0 y el **puente hacia el Motor de Creativos**. Toma los documentos MASTER ya producidos y valida­dos, y emite el veredicto estratégico final en **dos formas del MISMO contenido**:

1. **`00 — Master Spine.md`** — el veredicto **narrativo** (INDEX + spine estratégico + nota de acceso honesta). Autoridad humana-legible.
2. **`spine.json`** — el MISMO veredicto en **contrato estructurado** que el Motor de Creativos (`intake.py`) consume sin traducción manual. Cierra el handoff research→creativos.

El `.md` es para leer y decidir; el `.json` es para encadenar. Ambos salen de los MISMOS docs y deben coincidir.

> **Por qué existe el `spine.json`:** el Master Spine v4 es un INDEX narrativo; el Motor de Creativos exige un objeto de campos nombrados (INTERFACE §2). Sin esta skill, alguien traduce a mano cada corrida (frágil y no reproducible). Esta skill hace esa traducción determinista y trazable.

---

## 1. Cuándo se corre (precondición dura)

Solo cuando el research está **cerrado**: docs **14, 15, 16, 17, 18, 19, 20, 21, B0, B1 y 10** escritos, con **anti-fabricación pasada** y **QC cerrado**, y con la **doble vía (F4b)** y los **avatares Evolve (F5)** ya reconciliados. El **Core Avatar elegido** (doc 21) debe existir — en F4 aún no. Si falta un doc obligatorio o su QC no cerró, **no se corre**: se devuelve a la fase que corresponda.

## 2. Inputs

- Los **docs MASTER** del research del producto (14-21, B0/B1, 10), en la carpeta del producto / Drive.
- La **versión del Spine** (`vN`) y el **target de lanzamiento** (idioma + país).
- (**No confundir**) Los **scripts ganadores del competidor** NO salen de aquí: son el **Input B** del Motor de Creativos y vienen del ad-spy (TrendTrack / Foreplay / GetHookd / Kalodata). Esta skill produce el **Spine (Input A)** y la lista de `prueba`; los guiones del competidor se surten aparte.

## 3. El contrato estructurado (`spine.json`)

Debe validar contra **`spine.schema.json`** (idéntico al contrato INTERFACE §2 del Motor de Creativos). Campos obligatorios y de dónde sale cada uno:

| Campo | Tipo | Fuente (doc) | Regla de extracción |
|---|---|---|---|
| `producto` | texto | **B0** | Nombre del producto/marca y categoría (ficha real). |
| `spine_version` | texto | — | `vN` del research (para compat INTERFACE §7). |
| `target_market` | `{lang, country}` | 00/17 | Mercado de LANZAMIENTO (no el de inteligencia). |
| `avatar_nucleo` | texto | **15 + 21** | El **Core Avatar ELEGIDO** (uno solo), retrato condensado: quién es + situación + estado emocional. |
| `deseo_masivo_1` | texto `"Quiero…"` | **18** | El deseo dominante, en primera persona, en el lenguaje real del corpus. |
| `emocion_troncal` | texto | **20 §4.2** | La emoción de compra **PRIMARIA** (la que abre el copy). |
| `mecanismo` | objeto | **19** (+16, gate 7) | El mecanismo canónico que LIDERA (ver colapso §4). |
| `villano` | texto | **20 / 16** | El culpable común (us-vs-them / causa raíz), NO un competidor. |
| `prueba` | lista | **14 / 17** | Los elementos de prueba disponibles (demo, dato, testimonio, autoridad, antes/después). |
| `objecion_raiz` | texto | **20 §5** | La objeción #1 (mayor nº de quotes; desempate por engagement). |
| `awareness` | enum | **17** | Histograma → UN valor (ver colapso §4). |
| `compliance` | objeto | **gate 7 + 19 + 16** | Ver §5. |

`mecanismo` = `{tipo: UMP|UMS|USP, nombre, explicacion, lexico_prohibido: []}`.
`compliance` = `{claims_prohibidos: [], requiere_testimonio: [], disclaimers: [], notas_categoria: ""}`.

## 4. Colapsos de cardinalidad (resuelven el impedance research↔creativos)

El research produce estructuras ricas (varios avatares, UMP+UMS+USP, histograma de conciencia); el contrato pide **un** valor. Reglas **deterministas** (dos ejecutores producen lo mismo):

- **`mecanismo`** — el research da UMP **+** UMS **+** USP. Para el contrato se emite el mecanismo **que LIDERA** según la palanca Big-3 del doc 17: sofisticación 3-4 → `tipo=UMP` (el reencuadre de la causa); si la palanca es un USP demostrable → `tipo=USP`; si el diferenciador es el atributo de solución → `tipo=UMS`. `nombre`/`explicacion` del doc 19. **La cadena completa UMP→UMS→USP va en el doc 00 narrativo — no se pierde**, solo se elige el líder para el contrato.
- **`awareness`** — histograma del doc 17 → el nivel **DOMINANTE**. **Regla anti-sobreestimación:** si dos niveles quedan a ≤10 puntos, se elige el **MENOR** (educar de más es más barato). El histograma completo va en el doc 00.
- **`avatar_nucleo`** — doc 21 da varios core+sub. El contrato lleva **UNO** (el core elegido para liderar). Los **sub-avatares NO** van aquí: alimentan los baches "cabeza de playa" del creativo (van en el doc 00, sección handoff).
- **`villano` / `emocion_troncal` / `objecion_raiz`** — se **NOMBRAN** como un valor. Si el research no los aísla como campo: `villano` = culpable us-vs-them dominante (doc 20/16); `emocion_troncal` = `buying_emotion` PRIMARIA (doc 20 §4.2); `objecion_raiz` = objeción #1 por nº de quotes (doc 20 §5).
- **`prueba`** — NO colapsa: es la lista de elementos de prueba del doc 14/17.

## 5. Construcción de `compliance`

- `claims_prohibidos` ← verbos prohibidos por vertical/jurisdicción (gate 7: curar/tratar/revertir/eliminar…) **+** los claims que el gate de sustanciación del doc 19 marcó **"hipótesis persuasiva"** (causa sin respaldo externo).
- `requiere_testimonio` ← afirmaciones fuertes cuya CAUSA no tiene respaldo externo (doc 19): solo pueden ir en boca de testimonio, nunca como voz de marca.
- `disclaimers` ← overlays legales obligatorios de la categoría y cuándo aplican.
- `notas_categoria` ← reglas del vertical (salud: framear el mecanismo como **creencia/testimonio**, no como claim clínico).

> **`compliance` vacío NO es válido en salud/finanzas.** Si el research no lo trae, se marca FALTA (§6) — jamás se asume "sin restricciones".

## 6. Anti-fabricación (regla madre, heredada del research)

Cada valor del `spine.json` debe ser **TRAZABLE** a un doc/quote del research. **Prohibido inventar** para "completar" el contrato. Si un obligatorio no tiene sustento:

- se emite con valor `null`,
- se añade su nombre a `_faltantes: []`, y
- el **handoff a creativos queda BLOQUEADO** (mismo espíritu que `intake.py` §6 del Motor de Creativos).

El research no se rellena a ojo: se devuelve a F4/F5 a resolver el hueco.

## 7. El Master Spine narrativo (`00 — Master Spine.md`)

Spec canónica en `voc-research/synthesis.md §3.00` — aquí se hace concreta. Estructura:

1. **INDEX** — mapa de los docs MASTER (14-21, B0/B1, 10) con su ubicación.
2. **Spine estratégico** — deseo masivo elegido + su **test 3D** · **Big-3** (mecanismo/información/identidad) + evidencia · **Core Avatar elegido** (de F5) · **matriz Conciencia×Sofisticación + palanca** · el **mecanismo canónico** completo (UMP→UMS→USP con estatus de sustanciación) · **villano** · **emoción primaria** · **objeción raíz + disolvente**. **SIN oferta** (pricing/bundles/garantía = SOP-MKT-04, después del Spine).
3. **Nota de acceso honesta** — cobertura por canal, % de corpus proxy, cuadre leídas-vs-scrapeadas, resultado de la verificación anti-fabricación, y lo **NO minado** con razón + evidencia del intento.
4. **Bloque de handoff a creativos** — referencia al `spine.json` emitido + los **5 ángulos base** sugeridos (del doc 10) para los baches (núcleo/objeción/villano/prueba/cabeza-de-playa) + los sub-avatares candidatos a "cabeza de playa".

El doc 00 y el `spine.json` deben expresar el **mismo veredicto** en distinta forma.

## 8. Versionado y handoff a creativos

- `spine.json` declara `spine_version` (`vN`) y `target_market`. El Motor de Creativos (INTERFACE §7) debe declarar que sabe consumir esa versión; si el creativo aún referencia una versión anterior, **se actualiza el contrato del creativo** — no se bloquea a ciegas.
- Se entrega a `intake.py` del Motor de Creativos como `--spine spine.json`. **Usar JSON (no markdown freeform)**: la validación estricta de JSON evita el bypass de validación que tiene el path markdown.
- `intake.py` **congela** el `spine.json` en `casos/<producto>/input/spine.snapshot.json` (regla del snapshot, INTERFACE §5).

## 9. QC — criterio de "hecho bien"

- [ ] `spine.json` valida contra `spine.schema.json` (todos los obligatorios; tipos y enums correctos).
- [ ] Cada campo es **trazable** a un doc/quote (cero inventado); `_faltantes` vacío, o handoff BLOQUEADO.
- [ ] Cardinalidad colapsada por §4 (un mecanismo con `tipo`, un `awareness`, un `avatar_nucleo`).
- [ ] `compliance` no vacío (o FALTA declarado) — obligatorio en verticales sensibles.
- [ ] `villano`, `emocion_troncal`, `objecion_raiz` **nombrados** (no dispersos).
- [ ] `deseo_masivo_1` en primera persona "Quiero…".
- [ ] El doc 00 narrativo **coincide** con el `spine.json` (mismo veredicto).
- [ ] Nota de acceso honesta presente (cobertura + anti-fab + no-minado).
- [ ] `spine_version` + `target_market` presentes.

## 10. Artefactos de esta skill

- `spine.schema.json` — el contrato (JSON Schema) que el `spine.json` debe cumplir. Espejo de INTERFACE §2 del Motor de Creativos.
- `spine.template.json` — esqueleto rellenable con marcadores, para arrancar la extracción.

> **Frontera:** esta skill NO hace research (eso es `/voc-research`) ni genera creativos (eso es el Motor de Creativos). Solo **consolida** el veredicto y **emite el contrato**. Si un dato no está en los docs, se pide a la fase de research, no se inventa.
