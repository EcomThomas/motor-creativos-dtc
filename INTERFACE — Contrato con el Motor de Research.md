# INTERFACE — Contrato con el Motor de Research

Este documento define el **contrato** entre la ETAPA 1 (motor de research) y la ETAPA 2 (este Motor de Creativos). Especifica **exactamente** qué recibe este motor, en qué forma, qué hacer si algo falta, y cómo se congela y versiona ese input para que cada ejecución sea reproducible.

**Regla de oro:** este motor NO hace research. Si un dato no vino en el input, se **pide a la etapa 1** — no se inventa, no se deduce "a ojo", no se rellena con un placeholder plausible. Un creativo construido sobre un dato inventado contamina todo el pipeline aguas abajo (test, feedback, decisiones de escala).

---

## 1. Los tres inputs

| # | Input | Obligatorio | Función |
|---|-------|-------------|---------|
| A | **SPINE** | Sí | El veredicto estratégico del research. Es la fuente de verdad de TODO re-anclaje. |
| B | **SCRIPTS GANADORES DEL COMPETIDOR** | Sí (para imitar) | Los moldes probados que este motor re-ancla al Spine. Sin ellos no hay imitaciones, solo ideación. |
| C | **BANCO VoC** (con IDs de evidencia) | Opcional | Munición literal (frases reales del mercado) para hooks y copy, y para respaldar prueba/objeción con trazabilidad. |

---

## 2. Input A — El SPINE (contrato de campos)

El Spine llega como un objeto estructurado (JSON o Markdown con front-matter). **Campos mínimos obligatorios**; si falta cualquiera de ellos, el Spine se considera **incompleto** y se aplica el protocolo de la sección 6.

| Campo | Tipo | Descripción | Ejemplo de forma (product-agnostic) |
|-------|------|-------------|-------------------------------------|
| `avatar_nucleo` | texto | Quién es el comprador central: demografía + situación + estado emocional. | `<AVATAR>` |
| `deseo_masivo_1` | texto ("Quiero…") | El deseo dominante #1 del mercado, en primera persona. | "Quiero `<DESEO>` sin `<FRICCIÓN>`." |
| `emocion_troncal` | texto | La emoción raíz que mueve la compra (miedo, vergüenza, esperanza, orgullo…). | `<EMOCIÓN>` |
| `mecanismo` | objeto | El mecanismo único. Ver sub-tabla abajo. | — |
| `villano` | texto | El enemigo común contra el que se posiciona (causa raíz del problema, no un competidor). | `<VILLANO>` |
| `prueba` | lista | Los elementos de prueba disponibles (demostración, data, testimonio, autoridad, antes/después). | `[<PRUEBA_1>, <PRUEBA_2>]` |
| `objecion_raiz` | texto | La objeción #1 que frena la compra (no la superficial, la de fondo). | `<OBJECIÓN>` |
| `awareness` | enum | Nivel de consciencia del mercado (Schwartz). | `Unaware` \| `Problem Aware` \| `Solution Aware` \| `Product Aware` \| `Most Aware` |
| `compliance` | objeto | Reglas de compliance específicas del producto. Ver sub-tabla abajo. | — |

### 2.1 Sub-objeto `mecanismo`

| Sub-campo | Tipo | Descripción |
|-----------|------|-------------|
| `tipo` | enum | `UMP` (Unique Mechanism of the Problem) \| `UMS` (Unique Mechanism of the Solution) \| `USP` (Unique Selling Proposition). |
| `nombre` | texto | El nombre/etiqueta del mecanismo tal como se comunica al mercado. |
| `explicacion` | texto | Cómo funciona, en lenguaje de mercado (no técnico de más). |
| `lexico_prohibido` | lista | **Palabras/frases que NO se pueden usar** al comunicar este mecanismo (claims prohibidos, términos regulados). Este motor las trata como veto duro. |

### 2.2 Sub-objeto `compliance`

| Sub-campo | Tipo | Descripción |
|-----------|------|-------------|
| `claims_prohibidos` | lista | Afirmaciones vetadas (p. ej. "cura", "garantizado", "elimina en X días"). |
| `requiere_testimonio` | lista | Afirmaciones fuertes que SOLO pueden ir en boca de testimonio, nunca como voz de marca. |
| `disclaimers` | lista | Textos legales / overlays obligatorios y cuándo aplican. |
| `notas_categoria` | texto | Reglas propias de la categoría (salud, finanzas, etc.), p. ej. "framear mecanismos como creencia/testimonio, no como claim clínico". |

---

## 3. Input B — Scripts ganadores del competidor (contrato de formato)

Llegan como una **lista** de anuncios. Cada anuncio es el molde que este motor imita y re-ancla. Un anuncio es "ganador" cuando lleva **muchos días corriendo** o tiene **alto reach** (señal de que el competidor lo escala porque le funciona).

**Campos por anuncio:**

| Campo | Obligatorio | Descripción |
|-------|-------------|-------------|
| `id` | Sí | Identificador único del script (para trazar qué imitación salió de qué molde). |
| `competidor` / `fuente` | Sí | Marca/anunciante de origen y plataforma (Meta / TikTok / ad-spy tipo TrendTrack). |
| `senal_ganador` | Sí | La evidencia de que es ganador: días corriendo y/o reach/impresiones estimadas. |
| `formato` | Sí | `Video` \| `Static` \| `Carrusel`. |
| `transcripcion` / `guion` | Sí | El texto/guion completo del anuncio. En video: transcripción con marcas de tiempo o beats si se tienen. |
| `arco` | Recomendado | El patrón estructural identificado: hook → problema → giro → mecanismo → prueba → CTA (o el que sea). Si no viene, este motor lo infiere de la transcripción y lo anota. |
| `notas` | Opcional | Observaciones (idioma, on-screen text, música, oferta mostrada). |

Si `arco` no viene, no bloquea: este motor lo deriva de la transcripción. Si falta `transcripcion`, el anuncio **no es imitable** (no hay molde) y se descarta con nota.

---

## 4. Input C — Banco VoC (opcional, con IDs)

Munición literal del mercado. Cuando viene, cada pieza de evidencia trae un **ID estable** (formato `EVxxxx`) para poder citar la fuente en el copy y en el brief.

| Campo | Descripción |
|-------|-------------|
| `id` | ID de evidencia estable, p. ej. `EV0137`. |
| `texto` | La cita literal del mercado (reseña, comentario, post, ticket). |
| `fuente` | De dónde salió (reseñas, Reddit, TikTok comments, encuesta…). |
| `tags` | Etiquetas: a qué deseo / objeción / villano / prueba mapea. |

**Uso:** los hooks y las líneas de copy que nacen de VoC citan el `id` en su nota, para que en test se pueda rastrear qué frase real generó qué anuncio. Si NO hay banco VoC, el motor opera solo con Spine + scripts, y lo declara (los hooks se marcan como derivados del Spine, no de VoC literal).

---

## 5. La regla del SNAPSHOT (reproducibilidad)

El research **sigue evolucionando** (el Spine se reconcilia y versiona en la etapa 1). Para que una ejecución de creativos sea **reproducible** aunque el research cambie después, este motor **congela una copia** del input exacto que consumió.

**Mecánica:**

1. Al arrancar una ejecución para un producto, se copia el input **tal cual** a:

   ```
   casos/<producto>/input/
   ├── spine.snapshot.md        (o .json)   — copia congelada del Spine consumido
   ├── scripts.snapshot.md      — los scripts ganadores usados
   ├── voc.snapshot.md          — el banco VoC usado (si hubo)
   └── _meta.md                 — fecha, versión del Spine origen, hash/commit, quién ejecutó
   ```

2. **Todo el output de esa ejecución** (baches, roadmap, briefs) referencia ESE snapshot, no el Spine "vivo".

3. Si mañana el research publica un Spine nuevo, **no se toca** el snapshot viejo. Se hace una **ejecución nueva** con su propio snapshot. Así cada bache es auditable contra el input exacto del que nació.

**Por qué:** sin snapshot, un bache que funcionó no se puede re-explicar (¿contra qué versión del deseo se escribió?), y el feedback loop hacia research pierde trazabilidad.

---

## 6. Qué hacer si falta un input (protocolo de faltantes)

Este motor **no rellena huecos con research propio**. Ante un faltante:

| Situación | Acción |
|-----------|--------|
| Falta un **campo obligatorio del Spine** (sección 2). | **Bloquear** la ejecución. Devolver a la etapa 1 la lista exacta de campos faltantes. No se genera ningún bache hasta que el Spine esté completo. |
| Falta el **Spine completo**. | Bloqueo total. No hay fuente de verdad; no se puede re-anclar nada. |
| Faltan **scripts ganadores** (Input B). | No se bloquea, pero se **degrada**: sin moldes no hay imitaciones. Se avisa que la ejecución será solo **ideación** (mayor riesgo) y se pide a la etapa 1 (o al ad-spy) surtir ganadores. |
| Falta el **banco VoC** (Input C). | No se bloquea. Se opera con Spine + scripts y se **declara** que los hooks son derivados del Spine, no de VoC literal. |
| Un campo vino **vacío o ambiguo** (p. ej. `objecion_raiz: ""`). | Se trata como faltante obligatorio → bloqueo y solicitud a etapa 1. No se interpreta ni se completa. |
| El `lexico_prohibido` / `compliance` vino vacío. | **No** se asume "no hay restricciones". Se pide confirmación explícita a la etapa 1: un compliance vacío es sospechoso, sobre todo en salud/finanzas. |

**Formato de la solicitud de faltantes** (lo que este motor devuelve a la etapa 1):

```
INPUT INCOMPLETO — ejecución bloqueada
Producto: <PRODUCTO>
Faltan (obligatorios):
  - spine.objecion_raiz  (vino vacío)
  - spine.mecanismo.lexico_prohibido  (ausente)
Degradaciones (no bloquean, se avisa):
  - Sin banco VoC → hooks derivados del Spine
Acción requerida: etapa 1 debe surtir los campos obligatorios antes de re-ejecutar.
```

---

## 7. Versionado del contrato

Este contrato es en sí un artefacto versionado. Cambios en la forma de los inputs (agregar un campo obligatorio, cambiar un enum) suben la versión del contrato.

| Elemento | Cómo se versiona |
|----------|------------------|
| **Versión del contrato** | SemVer: `INTERFACE vMAJOR.MINOR`. `MAJOR` sube si cambia un campo obligatorio o un enum (rompe compatibilidad con Spines viejos). `MINOR` sube si se agrega un campo opcional. |
| **Versión del Spine origen** | Se registra en `_meta.md` del snapshot (p. ej. Spine `v3.3`). El contrato declara **qué versiones del Spine sabe consumir**. |
| **Compatibilidad** | Si llega un Spine de una versión que el contrato no reconoce, se trata como faltante estructural → bloqueo y aviso a etapa 1, no se adivina el mapeo de campos. |
| **Registro de cambios** | Cada cambio del contrato deja entrada en un changelog (qué campo, por qué, desde qué versión aplica). |

---

## 8. Checklist de aceptación del input (antes de generar baches)

Antes de producir un solo bache, este motor valida:

- [ ] Spine presente y **todos** los campos obligatorios de la sección 2 llenos y no ambiguos.
- [ ] `mecanismo.lexico_prohibido` y `compliance` presentes (si vacíos, confirmados explícitamente por etapa 1).
- [ ] `awareness` es uno de los cinco valores del enum.
- [ ] Scripts ganadores: cada uno con `id`, `fuente`, `senal_ganador`, `formato` y `transcripcion`. Los que no tengan transcripción se descartan con nota.
- [ ] Si hay VoC: cada evidencia con `id` estable. Si no hay VoC, queda declarado en el output.
- [ ] Snapshot escrito en `casos/<producto>/input/` con `_meta.md` (fecha, versión del Spine, hash/commit).
- [ ] Ningún campo obligatorio fue "inventado" por este motor para desbloquear la ejecución.

Si el checklist no pasa completo, la ejecución **no arranca**: se devuelve el reporte de faltantes de la sección 6 a la etapa 1.
