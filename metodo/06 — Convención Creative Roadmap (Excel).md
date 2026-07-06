# Convención de la hoja "Creative Roadmap" (Excel)

Este documento define la hoja **Creative Roadmap**: la superficie donde el Motor de Creativos (ETAPA 2) vuelca sus baches y anuncios, y donde luego Media Buying (ETAPA 3) registra resultados que alimentan el feedback (ETAPA 4). Es una convención **product-agnostic**: la misma estructura se copia tal cual a cualquier producto DTC; lo específico (`<PRODUCTO>`, `<AVATAR>`, `<DESEO>`, etc.) entra por el INPUT (Spine + scripts ganadores).

La hoja tiene una lógica de dos niveles: cada **bache** ocupa una fila-cabecera con la metadata del concepto, y debajo cuelgan N **filas de anuncio** que comparten ese concepto. Así una sola vista mezcla estrategia (el concepto) y ejecución (cada creativo testeable).

---

## 1. Columnas (A..U)

| Col | Nombre | Nivel | Qué contiene |
|-----|--------|-------|--------------|
| A | Status | Bache | Estado del bache en el pipeline. Dropdown. |
| B | BATCH # | Bache | Identificador del bache (entero incremental: 1, 2, 3…). Ancla los anuncios a su concepto. |
| C | Author | Bache | Quién creó el concepto. |
| D | Ad Concept | Bache | Nombre corto del concepto creativo (el `concept` del schema). |
| E | Angle | Bache | Ángulo psicológico (el `angle`: p. ej. villano, atajo, prueba social). |
| F | Avatar | Bache | Avatar núcleo al que apunta el bache (`<AVATAR>` del Spine). |
| G | Mass Desire | Bache | Deseo masivo en primera persona: "Quiero…" (`<DESEO>`). |
| H | Awareness Level | Bache | Nivel de consciencia del prospecto. Dropdown. |
| I | hypothesis | Bache | La hipótesis que este bache pone a prueba (cada test nace una hipótesis). |
| J | Ad Type | Anuncio | Clasificación del anuncio. Dropdown. |
| K | Ad Format | Anuncio | Formato del creativo. Dropdown. |
| L | Landing Page | Anuncio | URL/nombre de la landing a la que apunta el anuncio. |
| M | Link To Brief | Anuncio | Enlace al brief de producción de ese anuncio/bache. |
| N | Link To Ad | Anuncio | Enlace al creativo final (Drive/Meta/asset). |
| O | Results | Anuncio | Veredicto grueso del test. Dropdown. |
| P | Metricas | Anuncio | Métricas crudas del test (ROAS, CPA, CTR, hook rate…). |
| Q | Learnings | Anuncio | Aprendizaje de la primera ronda. |
| R | COPY DEL CREATIVO | Anuncio | El copy/guion del anuncio. La `nota` de imitación va como **comentario** de esta celda. |
| S | Ad Variable | Anuncio | Qué variable aísla el test (el elemento que cambia). Dropdown. |
| T | Test Result | Anuncio | Veredicto del re-test tras iterar la variable. Dropdown. |
| U | Learnings 2 | Anuncio | Aprendizaje de la segunda ronda. |

---

## 2. Valores EXACTOS de los dropdowns

Reprodúcelos idénticos (con emoji incluido) al configurar la Validación de Datos en el Excel de cualquier producto:

| Columna | Valores permitidos |
|---------|--------------------|
| **A — Status** | `Ideando`, `Working`, `Learning`, `Filming`, `Done` |
| **H — Awareness Level** | `Unaware`, `Problem Aware`, `Solution Aware`, `Product Aware`, `Most Aware` |
| **J — Ad Type** | `🔄 Iteration`, `🎭 Imitation`, `💡 Ideation`, `🦥 Kalodata` |
| **K — Ad Format** | `🖼️ Static`, `🎬 Video`, `🏷️ Promo` |
| **O — Results** | `Losing Ad`, `Winning Ad` |
| **S — Ad Variable** | `🪝 Hook`, `🖼️ Visual` |
| **T — Test Result** | `Losing Ad`, `Winning Ad` |

Notas de mapeo con el Canon:

- **J — Ad Type** implementa la CLASIFICACIÓN del anuncio. `🎭 Imitation`, `🔄 Iteration` y `💡 Ideation` son las tres clases canónicas (imitación / iteración / ideación). `🦥 Kalodata` marca un anuncio cuya idea vino de una fuente de spy/scraping tipo Kalodata. Recuerda: son **opciones**, no una cuota de una-de-cada; cuando la jugada es apoyarse en ganadores del competidor, la mayoría serán `🎭 Imitation`.
- **K — Ad Format** implementa `ad_format`. `Video` y `Static` son los dos del schema; `🏷️ Promo` es una variante de formato promocional (oferta/descuento).
- **O — Results** y **T — Test Result** comparten vocabulario (`Losing Ad`/`Winning Ad`): O es el primer veredicto, T el veredicto tras iterar la variable aislada en S.

---

## 3. Layout: 1 bache = 1 fila-cabecera + N filas de anuncio

La regla de oro: **un bache es un bloque de filas**. La primera fila del bloque lleva la metadata del concepto (columnas D..I) más su Status (A), BATCH # (B) y Author (C). Las filas siguientes del mismo bloque son los anuncios de ese bache y solo rellenan las columnas de nivel-anuncio (J en adelante).

Esquema visual de un bache con 3 anuncios (el default del Canon):

```
 A        B    C       D           E       F        G            H          I            J             K            L..U
┌────────┬────┬───────┬───────────┬───────┬────────┬────────────┬──────────┬────────────┬─────────────┬────────────┬─────
│Ideando │ 7  │ TH    │<CONCEPTO> │<ÁNGULO>│<AVATAR>│"Quiero…"   │Problem…  │<HIPÓTESIS> │             │            │      │ ← fila-cabecera del bache
├────────┼────┼───────┼───────────┼───────┼────────┼────────────┼──────────┼────────────┼─────────────┼────────────┼─────
│        │ 7  │       │           │       │        │            │          │            │🎭 Imitation │🎬 Video    │ copy…│ ← anuncio 1
│        │ 7  │       │           │       │        │            │          │            │🎭 Imitation │🖼️ Static   │ copy…│ ← anuncio 2
│        │ 7  │       │           │       │        │            │          │            │🎭 Imitation │🎬 Video    │ copy…│ ← anuncio 3
└────────┴────┴───────┴───────────┴───────┴────────┴────────────┴──────────┴────────────┴─────────────┴────────────┴─────
```

Reglas del layout:

1. **BATCH # (B) se repite** en todas las filas del bloque (cabecera + anuncios). Es la llave que agrupa; si filtras/ordenas, B mantiene unido el bache. (Alternativa válida: escribir B solo en la cabecera y dejarlo vacío en los anuncios, si prefieres la vista limpia y no vas a reordenar filas.)
2. **La metadata del concepto (D..I) va SOLO en la fila-cabecera.** No la repitas en cada anuncio: el concepto es del bache, no del anuncio.
3. **Cada fila de anuncio rellena, como mínimo:** `J Ad Type`, `K Ad Format` y `R COPY DEL CREATIVO`. Lo demás (L..Q, S..U) se llena cuando el anuncio avanza en el pipeline.
4. **La `nota` de la imitación NO ocupa una columna:** va como **comentario/nota de la celda R** de ese anuncio (clic derecho sobre la celda R → Insertar comentario). Ahí anotas qué ganador imitas y qué re-anclaste al Spine (p. ej. "imita [ganador X]; re-anclado a `<VILLANO>`/`<MECANISMO>`").
5. **Status (A)** describe al bache entero y vive en la cabecera; avanza `Ideando → Working → Filming → Learning → Done` a medida que el bache se produce y testea.

---

## 4. Cómo se replica en el Excel de otro producto

1. **Copia la hoja** (o su plantilla vacía) al libro del nuevo producto. La estructura A..U y los dropdowns son idénticos: no se tocan.
2. **Reconfigura la Validación de Datos** de las columnas con dropdown (A, H, J, K, O, S, T) con los valores EXACTOS del §2. Cópialos con emoji y todo; si el Excel te separa el emoji, pega desde una celda fuente para conservar el glifo.
3. **Congela la fila de encabezados** (fila 1) y activa Filtro. Así puedes filtrar por `BATCH #`, por `Ad Type` o por `Results` sin perder los títulos.
4. **Formato condicional opcional** para lectura rápida: colorea `O`/`T` (`Winning Ad` en verde, `Losing Ad` en rojo) y `A Status` por etapa.
5. Todo lo específico del producto (`<PRODUCTO>`, `<AVATAR>`, `<DESEO>`, `<VILLANO>`, `<MECANISMO>`) entra en las celdas D..I y R **desde el INPUT** (Spine + scripts ganadores). La hoja no hardcodea nada del producto.

---

## 5. Cómo enlazar M (Link To Brief) y N (Link To Ad)

Ambas columnas son **hipervínculos** — texto legible por fuera, URL por dentro. Así la hoja se mantiene como índice navegable del bache.

- **M — Link To Brief:** apunta al BRIEF DE PRODUCCIÓN de ese bache (el documento con script + storyboard de paridad emocional + prompts de generación que produce este mismo motor). Un brief por bache: puedes poner el mismo enlace en las filas de los anuncios de ese bache, o solo en la primera fila de anuncio.
  - En Excel: selecciona la celda M → `Insertar > Vínculo` (o `Ctrl+K`) → pega la URL del brief (Google Doc/Notion/archivo) → en "Texto para mostrar" escribe algo legible como `Brief B7`.
  - Alternativa por fórmula: `=HYPERLINK("https://…/brief-b7", "Brief B7")`.
- **N — Link To Ad:** apunta al creativo final ya producido (asset en Drive, preview en Meta/TikTok Ads Manager, o el archivo de video/imagen). Se rellena cuando el anuncio pasa de `Filming` a `Done`.
  - Mismo método: `Ctrl+K` en la celda N → URL del asset → texto para mostrar `Ad B7-1`, `Ad B7-2`, etc. (un enlace por fila de anuncio, porque cada anuncio tiene su propio creativo).
  - Por fórmula: `=HYPERLINK("https://…/ad-b7-1", "Ad B7-1")`.

Convención de nombres sugerida para que M y N se lean solos: `Brief B<batch>` para el brief y `Ad B<batch>-<n>` para cada anuncio (p. ej. `Ad B7-2` = segundo anuncio del bache 7). Así, leyendo solo las columnas M y N, sabes a qué bache y a qué anuncio apunta cada enlace.
