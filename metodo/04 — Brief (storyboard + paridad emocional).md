# Método: Brief (storyboard + paridad emocional)

Este documento es la **plantilla canónica del brief de producción por bache**. Convierte un bache aprobado (concept + ángulo + avatar + deseo + hipótesis + sus M anuncios) en un paquete que un editor/productor puede rodar o generar sin volver a preguntarte nada. Es *product-agnostic*: todo lo específico entra por el INPUT (el Spine + los scripts ganadores + los anuncios del bache). Reemplaza cada `<MARCADOR>` con lo que venga del bache.

> **Un brief = un bache.** Si el roadmap tiene N baches, produces N briefs con esta misma estructura.

---

## Qué es la PARIDAD EMOCIONAL (criterio de QA de este documento)

La paridad emocional es la regla que separa un guion que *convierte* de una "cabeza parlante plana". Significa: **cada línea del script tiene una escena cuya emoción, encuadre, luz, color, ritmo y sonido REFUERZAN lo que se dice.** No basta con que el actor diga la frase; la imagen tiene que *hacer sentir* la frase.

El **storyboard con paridad emocional** (sección 3 de cada anuncio) es la herramienta de QA: es una tabla donde **cada fila amarra una línea del guion a (a) una emoción objetivo y (b) una decisión visual/sonora concreta**. Si una fila tiene línea pero no tiene emoción clara, o tiene emoción pero la dirección visual no la sostiene, esa fila **no pasa QA** y se reescribe. El arco emocional del anuncio completo debe **subir, llegar a un clímax y resolver** — nunca quedarse plano.

**Cómo se lee la tabla del storyboard (columnas EXACTAS, no cambiar el orden ni los nombres):**

| Columna | Qué contiene |
|---|---|
| **#** | Número de plano/beat, correlativo. |
| **Tiempo** | Rango en segundos del plano (ej. `0-2s`). |
| **Línea del script (fragmento)** | El fragmento textual que se dice/escribe en ese plano. |
| **Emoción objetivo** | La emoción que el espectador debe sentir en ese beat (ej. tensión, alivio, esperanza, urgencia). |
| **Dirección visual (encuadre/acción/expresión/luz/color)** | La instrucción de cámara y puesta en escena que *produce* esa emoción. |
| **B-roll/inserto** | El plano de apoyo o inserto que corta sobre la línea. |
| **Texto en pantalla** | El overlay/caption exacto de ese plano (incluye disclaimers si aplican). |
| **Audio (VO/música/SFX)** | Voz en off, cambio musical o efecto de sonido de ese beat. |

---

## Cómo usar esta plantilla

1. Toma **un** bache del Creative Roadmap.
2. Llena la **Sección 1 (Ficha estratégica)** con el veredicto del Spine + los campos del bache. Aquí defines el **arco emocional troncal** que todos los anuncios del bache van a respetar.
3. Llena la **Sección 2 (Producción base)**: lo que se comparte entre los M anuncios (casting, locación, props, specs técnicas).
4. Por cada uno de los **M anuncios** del bache, llena la **Sección 3** completa: script verbatim → storyboard → arco → arte → prompts IA.
5. Cierra con la **Sección 4 (Checklist)** de rodaje/entrega.
6. QA final: recorre cada storyboard fila por fila y valida la paridad emocional antes de mandar a producir.

---

# BRIEF — BATCH `<N>` — `<NOMBRE DEL BACHE>`

> **Clasificación dominante del bache:** `<IMITACIÓN | ITERACIÓN | IDEACIÓN>` · **Ganador(es) de referencia:** `<ID/nombre de anuncio(s) del competidor que se imitan, si aplica>`

---

## 1. Ficha estratégica

Todo lo que sigue baja del **Spine** (INPUT de la etapa 1) y del schema del bache. Es el contrato estratégico: si un anuncio del bache se desvía de esto, está mal.

| Campo | Valor |
|---|---|
| **Concepto (concept)** | `<la idea central del bache en una frase>` |
| **Ángulo (angle)** | `<el ángulo de ataque: p.ej. anti-mecanismo, demostración, testimonio, comparativa, etc.>` |
| **Avatar** | `<avatar núcleo del Spine: quién es, en su lenguaje>` |
| **Deseo masivo (mass_desire)** | `Quiero <...>` (redactado en primera persona, como lo diría el avatar) |
| **Emoción troncal** | `<la emoción raíz del Spine que este bache explota>` |
| **Nivel de awareness** | `<Unaware | Problem Aware | Solution Aware | Product Aware | Most Aware>` |
| **Villano (villain)** | `<el enemigo común: mecanismo del problema, creencia falsa, la industria, etc.>` |
| **Mecanismo (UMP/UMS/USP)** | `<el mecanismo único del problema / de la solución / propuesta única de venta>` |
| **Prueba (proof)** | `<la evidencia troncal: demo, testimonio, dato, antes/después — con su ID EVxxxx si viene del banco VoC>` |
| **Objeción raíz** | `<la objeción #1 que este bache debe desactivar>` |
| **Hipótesis del test (hypothesis)** | `Creemos que <ángulo/hook> sobre <avatar> disparará <métrica objetivo> porque <razón anclada en el deseo/emoción>.` |
| **Promesa / Big Idea** | `<la promesa central que el anuncio hace, en el lenguaje del avatar>` |
| **CTA** | `<llamado a la acción y destino>` |

### Arco emocional TRONCAL del bache

Este es el arco que **todos** los M anuncios del bache respetan (cada anuncio lo ejecuta con su propio hook, pero el viaje emocional es el mismo). Descríbelo como una secuencia de estados:

`<Estado inicial (ej. frustración/reconocimiento del dolor)>` → `<Giro (ej. villano desenmascarado / esperanza)>` → `<Clímax (ej. mecanismo + prueba)>` → `<Resolución (ej. alivio + acción)>`

- **Punto de dolor de entrada:** `<qué siente el avatar en el segundo 0>`
- **Giro / promesa:** `<qué cambia su estado emocional>`
- **Clímax de prueba:** `<el momento de máxima convicción>`
- **Resolución / CTA:** `<con qué sensación queda y qué hace>`

### Reglas de compliance de este bache

Baja del bloque de compliance del Spine. Rellena el léxico prohibido específico del producto.

- **Claims prohibidos:** `<lista de palabras/afirmaciones vetadas: p.ej. "cura", "garantizado", "elimina el 100%">`
- **Afirmaciones fuertes:** SIEMPRE en boca de `<testimonio/creencia>`, nunca como claim del anunciante.
- **Disclaimers/overlays obligatorios:** `<texto exacto del disclaimer y en qué planos aparece — p.ej. "Resultados no garantizados. Individuales.">`
- **Framing de categoría (si aplica, p.ej. salud):** mecanismos como `<testimonio/creencia>`, no como claim clínico.

---

## 2. Producción base (compartida por los `<M>` anuncios)

Lo que se define una vez y sirve para todos los anuncios del bache. Ahorra decisiones repetidas y garantiza consistencia de marca.

### Casting

| Rol | Descripción | Notas de dirección |
|---|---|---|
| `<Protagonista/UGC>` | `<edad, look, arquetipo que representa al avatar>` | `<tono: cercano, autoridad, par del avatar, etc.>` |
| `<Secundario/experto/testimonio>` | `<...>` | `<...>` |

### Locación y ambiente

- **Locación(es):** `<casa real / clínica / exterior / set neutro — coherente con el nivel de "raw/UGC" vs "producido">`
- **Mood general:** `<cálido/clínico/urbano/aspiracional>`

### Props y wardrobe

- **Props clave:** `<producto, packaging, objetos de demostración, elementos de prueba>`
- **Wardrobe:** `<vestuario que refuerza al avatar/testimonio>`

### Specs técnicas (por defecto)

| Spec | Valor por defecto |
|---|---|
| **Formato/aspect ratio** | `<9:16 vertical (Reels/TikTok) — ajustar si el ad es Static>` |
| **Duración objetivo** | `<15-30s para video; N/A para static>` |
| **Resolución** | `<1080×1920 mínimo>` |
| **Subtítulos** | `<sí, quemados/hardcoded — la mayoría ve sin sonido>` |
| **Estilo de captions** | `<fuente, color, posición coherente con el arco>` |
| **Safe zones** | `<respetar zonas de UI de la plataforma>` |

---

## 3. Los `<M>` anuncios del bache

> Repite el bloque **3.x** completo por cada anuncio del bache. Por defecto son **3** anuncios, **mayoritariamente IMITACIONES** de ganadores re-ancladas al Spine (no fuerces una-de-cada-tipo: si la jugada es apoyarse en ideas ganadoras del competidor, casi todos serán imitaciones).

---

### 3.1 — Anuncio `<N.1>` — `<título corto>`

| Meta | Valor |
|---|---|
| **Clasificación** | `<IMITACIÓN | ITERACIÓN | IDEACIÓN>` |
| **Imita a (si aplica)** | `<ID/nombre del ganador del competidor + qué arco/estructura se conserva>` |
| **Formato (ad_format)** | `<Video | Static>` |
| **Hook (primeros 3s)** | `<el gancho verbatim>` |
| **Nota** | `<por qué este anuncio, qué variable prueba dentro del bache>` |

#### Script verbatim

> Escribe el guion **palabra por palabra**, tal como se dirá/leerá. Marca `[VO]`, `[EN CÁMARA]`, `[TEXTO EN PANTALLA]` cuando ayude. Para Static, escribe el copy del creativo (headline + cuerpo + CTA) y el texto de cada frame.

```
<GUION VERBATIM COMPLETO>
```

#### Storyboard con paridad emocional

Cada fila amarra una línea del guion a una emoción y a una decisión visual/sonora. **Columnas exactas, en este orden:**

| # | Tiempo | Línea del script (fragmento) | Emoción objetivo | Dirección visual (encuadre/acción/expresión/luz/color) | B-roll/inserto | Texto en pantalla | Audio (VO/música/SFX) |
|---|---|---|---|---|---|---|---|
| 1 | `<0-2s>` | `<fragmento>` | `<emoción>` | `<encuadre/acción/expresión/luz/color>` | `<b-roll/inserto>` | `<overlay>` | `<VO/música/SFX>` |
| 2 | `<2-5s>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 3 | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| … | `<…>` | `<…>` | `<…>` | `<…>` | `<…>` | `<…>` | `<…>` |

#### Arco emocional (throughline) de este anuncio

`<estado inicial>` → `<giro>` → `<clímax de prueba>` → `<resolución/CTA>`

Confirma que este arco **ejecuta** el arco troncal del bache (sección 1) con el hook propio de este anuncio.

#### Dirección de arte / luz / color

- **Paleta:** `<colores dominantes y qué emoción sostienen a lo largo del arco>`
- **Luz:** `<dura/suave, cálida/fría, cómo evoluciona del dolor a la resolución>`
- **Ritmo de edición:** `<cortes rápidos en el hook, respiración en el clímax, etc.>`
- **Grafismos/overlays:** `<estilo de kinetic text, flechas, círculos de énfasis>`

#### Prompts de generación IA (uno por CADA escena del storyboard)

**Regla:** un prompt por **CADA escena** del storyboard — tantos prompts como filas tenga la tabla, sin saltarte ninguna (Escena 1, 2, 3 … hasta la última). Cada prompt es autosuficiente: sujeto + acción/expresión + encuadre + luz + color + emoción + estilo + aspect ratio. El editor debe poder generar cada plano sin adivinar.

- **Escena `1` (`<qué plano>`):**
  ```
  <PROMPT IA verbatim: sujeto + acción + encuadre + luz + color + emoción + estilo + aspect ratio>
  ```
- **Escena `2` (`<qué plano>`):**
  ```
  <PROMPT IA verbatim>
  ```
- **… (una entrada por cada fila del storyboard, hasta la última escena)**

---

### 3.2 — Anuncio `<N.2>` — `<título corto>`

*(Misma estructura que 3.1: Meta → Script verbatim → Storyboard con paridad emocional → Arco emocional → Dirección de arte/luz/color → Prompts IA.)*

| Meta | Valor |
|---|---|
| **Clasificación** | `<IMITACIÓN | ITERACIÓN | IDEACIÓN>` |
| **Imita a (si aplica)** | `<...>` |
| **Formato (ad_format)** | `<Video | Static>` |
| **Hook (primeros 3s)** | `<...>` |
| **Nota** | `<qué variable cambia respecto a 3.1 — mismo arco troncal, distinto hook/apertura>` |

#### Script verbatim

```
<GUION VERBATIM COMPLETO>
```

#### Storyboard con paridad emocional

| # | Tiempo | Línea del script (fragmento) | Emoción objetivo | Dirección visual (encuadre/acción/expresión/luz/color) | B-roll/inserto | Texto en pantalla | Audio (VO/música/SFX) |
|---|---|---|---|---|---|---|---|
| 1 | `<0-2s>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| … | `<…>` | `<…>` | `<…>` | `<…>` | `<…>` | `<…>` | `<…>` |

#### Arco emocional (throughline) de este anuncio

`<estado inicial>` → `<giro>` → `<clímax de prueba>` → `<resolución/CTA>`

#### Dirección de arte / luz / color

- **Paleta:** `<...>`
- **Luz:** `<...>`
- **Ritmo de edición:** `<...>`
- **Grafismos/overlays:** `<...>`

#### Prompts de generación IA (uno por CADA escena del storyboard)

- **Escena `<#>`:**
  ```
  <PROMPT IA verbatim>
  ```

---

### 3.3 — Anuncio `<N.3>` — `<título corto>`

*(Misma estructura. Añade tantos bloques 3.x como anuncios tenga el bache.)*

| Meta | Valor |
|---|---|
| **Clasificación** | `<IMITACIÓN | ITERACIÓN | IDEACIÓN>` |
| **Imita a (si aplica)** | `<...>` |
| **Formato (ad_format)** | `<Video | Static>` |
| **Hook (primeros 3s)** | `<...>` |
| **Nota** | `<qué variable cambia respecto a 3.1 y 3.2>` |

#### Script verbatim

```
<GUION VERBATIM COMPLETO>
```

#### Storyboard con paridad emocional

| # | Tiempo | Línea del script (fragmento) | Emoción objetivo | Dirección visual (encuadre/acción/expresión/luz/color) | B-roll/inserto | Texto en pantalla | Audio (VO/música/SFX) |
|---|---|---|---|---|---|---|---|
| 1 | `<0-2s>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| … | `<…>` | `<…>` | `<…>` | `<…>` | `<…>` | `<…>` | `<…>` |

#### Arco emocional (throughline) de este anuncio

`<estado inicial>` → `<giro>` → `<clímax de prueba>` → `<resolución/CTA>`

#### Dirección de arte / luz / color

- **Paleta:** `<...>`
- **Luz:** `<...>`
- **Ritmo de edición:** `<...>`
- **Grafismos/overlays:** `<...>`

#### Prompts de generación IA (uno por CADA escena del storyboard)

- **Escena `<#>`:**
  ```
  <PROMPT IA verbatim>
  ```

---

## 4. Checklist de rodaje / entrega

Antes de mandar a producir y antes de dar por cerrado el bache. Marca cada ítem.

### Pre-producción

- [ ] Ficha estratégica (sección 1) validada contra el Spine — nada se desvía del avatar/deseo/villano/mecanismo.
- [ ] Arco emocional troncal definido y **compartido** por los `<M>` anuncios.
- [ ] Casting confirmado y coherente con el avatar/testimonio.
- [ ] Locación, props y wardrobe listos.
- [ ] Ganador(es) de referencia revisados (si el bache es IMITACIÓN): arco/estructura a conservar está claro.

### Guion y paridad emocional (QA por anuncio)

- [ ] Cada anuncio tiene **script verbatim** completo.
- [ ] Cada anuncio tiene **storyboard** con las 8 columnas exactas.
- [ ] **QA de paridad emocional:** cada fila del storyboard tiene emoción objetivo Y una dirección visual/sonora que la sostiene. Ninguna "cabeza parlante plana".
- [ ] El arco de cada anuncio **sube → clímax → resolución** y ejecuta el arco troncal del bache.
- [ ] Hooks (primeros 3s) distintos entre los anuncios del bache; mismo arco troncal.

### Compliance

- [ ] Sin claims prohibidos (revisado contra la lista del léxico del Spine).
- [ ] Afirmaciones fuertes en boca de testimonio/creencia.
- [ ] Disclaimers/overlays presentes en los planos indicados.
- [ ] Framing de categoría correcto (p.ej. salud: mecanismo como testimonio, no claim clínico).

### Specs y entrega

- [ ] Formato/aspect ratio, resolución y duración según specs.
- [ ] Subtítulos quemados y captions con el estilo definido.
- [ ] Safe zones respetadas.
- [ ] Prompts de generación IA: **uno por cada escena** del storyboard (tantos como filas de la tabla, sin saltarse ninguna), autosuficientes.
- [ ] Volcado del bache al **Creative Roadmap** (Excel) actualizado.
- [ ] Nombres de archivo/versión: `<convención: BATCH-N_ADx_vY>`.

---

> **Recordatorio de QA final:** el brief no está listo hasta que **cada fila de cada storyboard** pase la prueba de paridad emocional. Un guion sin paridad emocional se rueda plano y se muere en el feed. La imagen no ilustra: **hace sentir**.
