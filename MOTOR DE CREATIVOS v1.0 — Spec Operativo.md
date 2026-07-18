# MOTOR DE CREATIVOS v1.0 — Spec Operativo

Este documento es el detalle de la máquina. Describe, fase por fase, cómo el Motor de Creativos convierte el **INPUT** (Spine + scripts ganadores + VoC opcional) en el **OUTPUT** (N baches, cada uno con M imitaciones re-ancladas, entregados en **formato ClickUp** —tarea madre + subtareas— + un brief de producción por bache). Es **product-agnostic**: nada aquí está atado a una categoría. Los específicos entran por el input mediante marcadores: `<PRODUCTO>`, `<AVATAR>`, `<DESEO>`, `<VILLANO>`, `<MECANISMO>`, `<PRUEBA>`, `<OBJECION>`, `<AWARENESS>`, `<COMPLIANCE>`.

Recordatorio de posición en el pipeline:

```
Research (Etapa 1) → CREATIVOS (Etapa 2, este motor) → Media Buying/Test (Etapa 3) → Feedback (Etapa 4) → vuelve a Research
```

El motor NO inventa estrategia. La estrategia ya viene decidida en el **Spine** (Etapa 1). El motor **traduce** ese veredicto en anuncios producibles y testeables, apoyándose mayoritariamente en la ingeniería inversa de anuncios ganadores del competidor.

---

## Resumen de las fases

| Fase | Nombre | Input | Output | Quién lo hace |
|------|--------|-------|--------|---------------|
| 0 | Intake del input | Spine + scripts ganadores + VoC (opcional) | Contexto validado (`CTX` + rutas) | Humano (curaduría) + workflow (carga) |
| 1 | Generar N baches | CTX + Spine | `batches_meta.json` (N objetos bache SIN ads finales, o con borrador de ads) | Workflow → N agentes en paralelo |
| 2 | Generar M imitaciones por bache | 1 bache + scripts ganadores + Spine + VoC | N × M anuncios de imitación | Workflow → N agentes en paralelo |
| 3 | Entregable ClickUp | Baches + ads (con campos ClickUp) | `.txt` por bache: tarea madre + subtareas | `clickup_export.py` (ensambla) + humano (links + pega) |
| 4 | Brief de producción por bache | 1 bache + sus ads | N briefs (script + storyboard con paridad emocional + prompts) | Agente por bache + humano (aprobación) |
| 5 | Handoff a producción/media buying | Roadmap + briefs | Paquete accionable para grabar/diseñar y para levantar campañas | Humano (director creativo / media buyer) |

El criterio general de "hecho bien" atraviesa todo: **todo anuncio es trazable** (a un ganador imitado y/o a un ID de VoC) y **todo anuncio respeta el Spine** (avatar, deseo, emoción, mecanismo, villano, prueba, objeción, awareness, compliance). Si un ad no se puede anclar al Spine ni a una estructura probada, no entra.

---

## Fase 0 — Intake del input

**Input**
- **SPINE** (obligatorio): el veredicto estratégico de la Etapa 1. Debe traer, como mínimo:
  - `<AVATAR>` núcleo, `<DESEO>` masivo #1, emoción troncal, `<MECANISMO>` (UMP/UMS/USP), `<VILLANO>`, `<PRUEBA>`, `<OBJECION>` raíz, `<AWARENESS>` dominante, y las reglas de `<COMPLIANCE>` (léxico prohibido específico del producto).
- **SCRIPTS GANADORES DEL COMPETIDOR** (obligatorio): transcripciones/guiones de anuncios probados de un ad-spy (p. ej. TrendTrack). "Ganador" = muchos días corriendo / alto reach / longevidad. Idealmente ≥ 3× M estructuras distintas disponibles para no repetir molde.
- **BANCO VoC** (opcional pero recomendado): citas reales con IDs de evidencia (`EVxxxx`) para re-anclar con lenguaje literal del mercado.

**Output**
- Un bloque de **contexto operativo** (`CTX`) que fija el frame v-actual: el Spine resumido en imperativo + las prohibiciones de compliance + la definición de "imitación". Es el mismo texto que reciben todos los agentes de las fases 1–2.
- Las **rutas** a los tres artefactos (Spine, scripts, VoC) listas para que el workflow las lea.

**Quién lo hace**: humano (cura el Spine y verifica que los scripts sean realmente ganadores) + workflow (resuelve rutas y compone `CTX`).

**Criterio de "hecho bien"**
- El Spine está **reconciliado y vigente** (no un borrador de mitad de research).
- Cada campo del Spine tiene valor (nada `<TBD>`); si algo es hipótesis y no hecho (p. ej. un puente causal riesgoso), está marcado como **testimonio/creencia**, no como claim.
- Hay al menos M estructuras ganadoras distinguibles en el archivo de scripts.
- El léxico de compliance prohibido está explícito (p. ej. términos que no se pueden usar como claim clínico).

---

## Fase 1 — Generar N baches (uno por ángulo estratégico)

Un **bache** es un concepto creativo que alinea **ángulo + avatar + deseo masivo + awareness + hipótesis**. Cada bache es un test: nace de una hipótesis y agrupa los anuncios que la comparten.

**Input**: `CTX` (Fase 0) + Spine. (La VoC entra aquí solo para inspirar ángulos; el anclaje fino ocurre en Fase 2.)

**Output**: `batches_meta.json` — un array de N objetos con el **schema de bache** (abajo). En la práctica hay dos modos:
- **Modo borrador**: cada bache trae ya 3 ads de arranque (imitación/iteración/ideación) para tener algo tangible. Estos ads son provisionales.
- **Modo canónico (recomendado)**: los baches se fijan como concepto/ángulo/hipótesis, y los anuncios **finales** se generan en Fase 2 como imitaciones. Fase 2 sobrescribe o completa el campo `ads`.

**Quién lo hace**: el workflow lanza **N agentes en paralelo**, uno por ángulo. Cada agente devuelve **datos estructurados** (schema forzado), no prosa.

### Cómo elegir los N ángulos a partir del Spine

Los ángulos no se inventan: se **derivan** de los ejes del Spine. Set base de ángulos (elige/expande según el Spine; este es el patrón por defecto de 5):

1. **Núcleo** — abre por el `<DESEO>` #1 y la emoción troncal directo sobre el `<AVATAR>` núcleo. Es el ángulo "recto".
2. **Objeción** — desarma la `<OBJECION>` raíz (p. ej. seguridad, precio, esfuerzo, credibilidad). Convierte el bloqueo de compra en el gancho.
3. **Villano** — nombra y ataca al `<VILLANO>` del Spine (incluido el "anti-solución" o el DIY que el avatar ya sufre). El producto se posiciona como el reemplazo limpio.
4. **Prueba** — testimonio/demostración con la `<PRUEBA>` nativa del Spine (métrica, antes/después, evidencia dura). Suele ser el ángulo de mayor awareness (Product/Most Aware).
5. **Cabeza de playa** — un **sub-avatar** o síntoma de entrada más barato de captar (a menudo para una plataforma concreta), que **puentea** al deseo núcleo. Va marcado en la hipótesis como **A VALIDAR** (no núcleo).

Reglas para escalar el número de ángulos: si el Spine tiene varios sub-avatares, varias objeciones o varios niveles de awareness relevantes, **añade un bache por cada eje diferenciado**. No dupliques ángulos que testean lo mismo. Un buen set de baches cubre **distintos niveles de awareness** y **distintas emociones de entrada**, no cinco variantes del mismo hook.

### Schema del bache

```
BATCH = {
  concept:      string   // nombre pegajoso del concepto, ej. "El Diagnóstico que Reversé"
  angle:        string   // el ángulo estratégico (núcleo | objeción | villano | prueba | cabeza de playa | ...)
  avatar:       string   // a quién le habla este bache (núcleo o sub-avatar)
  sub_avatar:   string   // segmento específico dentro del avatar (edad, situación, dolor puntual)
  mass_desire:  string   // en formato "Quiero..."  (el deseo masivo que activa)
  awareness:    enum      { Unaware | Problem Aware | Solution Aware | Product Aware | Most Aware }
  hypothesis:   string   // qué se está testeando; si es cabeza de playa, marcar "A VALIDAR"
  valence:      enum      { Positiva | Negativa | Mixta }   // valence emocional dominante del batch (anclada en la emoción troncal del Spine)
  emociones_83: string[]  // las 1-3 emociones que cubren ~83% del batch (del Spine + el copy), no inventadas
  trigger_batch: string   // trigger emocional troncal del batch (se hereda a las piezas sin trigger propio)
  ads:          Ad[]      // por defecto 3 (ver Fase 2). En modo borrador ya vienen; en canónico se llenan en Fase 2
}
```

**Criterio de "hecho bien"**
- Cada bache es **un concepto distinto** (ángulo + hipótesis únicos); no se solapan.
- `mass_desire` está redactado en primera persona "Quiero…" y corresponde al deseo del Spine (o a un sub-deseo legítimo del sub-avatar).
- `awareness` es coherente con el ángulo (p. ej. Prueba suele ser Product/Most Aware; Cabeza de playa suele ser Problem Aware).
- La `hypothesis` es **falsable** por el test (dice qué esperamos que gane y por qué), y los ángulos exploratorios están marcados como A VALIDAR.
- El set completo cubre un **espectro** de awareness/emoción, no un solo registro.

---

## Fase 2 — Generar M imitaciones por bache

Esta es la fase de producción de anuncios. Por defecto **M = 3 anuncios por bache**, y por defecto son **imitaciones** (así lo pidió el usuario: cuando la jugada es apoyarse en las ideas ganadoras del competidor, los ads son imitaciones en su mayoría; no se fuerza "una de cada tipo").

**Qué significa IMITACIÓN** (definición canónica, no negociable):
- Te basas **~90–100% en la IDEA/ESTRUCTURA** de un anuncio ganador del competidor.
- **Conservas** del ganador: el **arco** narrativo, el patrón de **hook**, la **secuencia** (problema → giro → mecanismo → prueba → CTA), el **ritmo** y el **formato**.
- **Solo cambias (re-anclas)** el **contenido** al Spine: avatar, emoción, villano, mecanismo, prueba, objeción — con lenguaje del mercado (VoC).

Las otras dos clasificaciones existen como **opciones**, no como cuota:
- **ITERACIÓN**: variación de un anuncio **propio** ya existente (otro hook/apertura/orden de prueba/formato).
- **IDEACIÓN**: ángulo **original** nacido de la VoC/insight, sin molde externo.

Se usan iteración/ideación solo cuando aportan algo que ninguna estructura ganadora cubre. El grueso del volumen sale de imitaciones porque es **menor riesgo para salir a mercado**.

**Input** (por agente): el **bache i** (de `batches_meta.json`, sin cambiarlo) + el archivo de **scripts ganadores** + el **Spine** + (si existe) la **VoC** con IDs.

**Output**: para cada bache, un array de **M ads de imitación** (schema abajo). N baches × M ads = el lote total de anuncios.

**Quién lo hace**: el workflow lanza **N agentes en paralelo** (uno por bache); cada agente produce M imitaciones. Salida estructurada forzada por schema; nada de texto de proceso.

### Regla de distribución de estructuras

Cada uno de los M ads de un mismo bache imita la estructura de un **competidor DISTINTO** (M estructuras diferentes). En el campo que nombra al competidor se registra cuál. Esto evita que los 3 ads de un bache sean el mismo molde y maximiza la diversidad de patrones que salen a test.

### Schema del ad de imitación

```
Ad (imitación) = {
  imita_competidor:  string           // nombre del competidor/ad cuya estructura se imita (del archivo de scripts)
  ad_format:         enum { Video | Static }   // Video por defecto (testimonial/narrativo);
                                               // Static solo si la estructura imitada es imagen+texto
  copy:              string           // guion/copy COMPLETO, listo para grabar/diseñar, en el idioma/registro del avatar
  nota:              string           // 1) qué estructura del competidor se conservó,
                                      // 2) qué se re-ancló al Spine,
                                      // 3) IDs EVxxxx de VoC que sostienen el re-anclaje (solo si hay banco VoC)
  nombre_creativo:   string           // nombre interno claro y utilizable de la pieza (para ClickUp)
  concepto_corto:    string           // idea PUNTUAL de esta pieza, breve — va en el título de la subtarea
  trigger_emocional: string           // qué activa la respuesta emocional del avatar en ESTA pieza
}
```

Schema del genérico (cuando quieras permitir los tres tipos en un mismo bache, p. ej. en modo borrador de Fase 1):

```
Ad (genérico) = {
  classification: enum { Imitation | Iteration | Ideation }
  ad_format: enum { Video | Static }
  copy:      string
  nota:      string   // qué imita/itera/idea + ID de VoC o competidor de referencia
}
```

**Criterio de "hecho bien"**
- El `copy` es **usable tal cual** (hook + cuerpo corto; longitud acorde al formato/plataforma), en el registro/idioma del `<AVATAR>` — no jerga ajena, no estética que no corresponde al avatar.
- El **hook** (primeros 3s) pasa el **Three-Element Test** (intensidad emocional + relevancia personal + curiosity gap) y no "parece un anuncio"; abre por el avatar (**tráfico frío**), no por la marca/features. Ver el banco de técnicas en [metodo/07](metodo/07%20—%20Banco%20de%20técnicas%20de%20guion%20y%20hook%20(EVOLVE%20+%20EAM).md).
- Cada ad **respeta compliance**: afirmaciones fuertes en boca de **testimonio**; sin claims absolutos (p. ej. "cura/garantizado"); sin el léxico prohibido del Spine; en categorías sensibles, el mecanismo se enmarca como **creencia/testimonio**, no como claim clínico. Los puentes causales riesgosos van como testimonio.
- Cada ad es **trazable**: nombra el competidor imitado y trae 2–4 `EVxxxx` que sostienen el re-anclaje.
- Los M ads de un bache imitan **M estructuras distintas**.
- El re-anclaje es **completo**: no queda emoción/villano/mecanismo "prestado" del competidor extranjero; todo está traducido al frame del Spine.

---

## Fase 3 — Entregable ClickUp (tarea madre + subtareas)

> **Cambio de salida.** El motor **ya NO vuelca al Excel "Creative Roadmap"** (se llenaba a mano, se corrompía y cargaba demasiada info). La salida de Fase 3 es ahora el **formato ClickUp**: por cada bache, una **tarea madre + N subtareas en texto plano** pegables. El detalle canónico está en [metodo/08](metodo/08%20—%20Entregable%20ClickUp%20(tarea%20madre%20+%20subtareas).md). El Excel ([metodo/06](metodo/06%20—%20Convención%20Creative%20Roadmap%20(Excel).md)) queda como legacy manual.

**Input**: los N baches (Fase 1) + sus N × M ads (Fase 2), con los campos del formato ClickUp (`sub_avatar`, `valence`, `emociones_83`, `trigger_batch`; y por pieza `nombre_creativo`, `concepto_corto`, `trigger_emocional`) + el INPUT operativo del humano (número de batch, links de carga y CTA, assets).

**Output**: por bache, un `.txt` con **etiqueta corta + tarea madre + subtareas** (`casos/<slug>/clickup/batch_<N>.txt`), listo para pegar en ClickUp. Lo genera de forma determinística `scripts/clickup_export.py`.

**Quién lo hace**: el workflow genera los campos creativos; `clickup_export.py` ensambla el texto; el humano completa los links y pega en ClickUp, desde donde pasa a su flujo y al equipo de Media Buying.

**Criterio de "hecho bien"**
- Formato exacto de [metodo/08](metodo/08%20—%20Entregable%20ClickUp%20(tarea%20madre%20+%20subtareas).md): sin tablas, texto plano, tarea madre primero, una subtarea por pieza.
- El campo **`Brief` de cada subtarea queda como placeholder** (el brief real es el documento de Fase 4).
- `valence`/`emociones_83`/`trigger` vienen del batch (no inventados en el export); trigger heredado se marca `[HEREDADO DEL BATCH]`.
- Títulos `V<k>`/`G<k> BATCH #<N> - <concepto corto>` numerados por tipo de pieza.

---

## Fase 4 — Brief de producción por bache

Convierte cada bache (y sus ads) en un documento que producción puede grabar/diseñar sin volver a preguntar.

**Input**: un bache + sus M ads.

**Output**: por bache, un **BRIEF DE PRODUCCIÓN** con:
1. **Script** — el guion final del/los ad(s), línea por línea.
2. **Storyboard con paridad emocional** — por cada línea del guion, la **escena** cuya emoción/encuadre/luz/color/ritmo/sonido **refuerza** lo que se dice. El arco emocional **sube, tiene clímax y resolución**. Prohibido el "cabeza parlante plana".
3. **Prompts de generación** — prompts listos para las herramientas de generación (imagen/video/voz) de cada escena, más overlays/disclaimers de compliance cuando apliquen.

**Quién lo hace**: un agente por bache redacta el brief; un humano (director creativo) aprueba antes de producir.

**Criterio de "hecho bien"** (**paridad emocional** es el criterio de calidad rector)
- **Cada línea del guion tiene una escena** con intención emocional explícita; ninguna escena es decorativa ni contradice el texto.
- El **arco emocional** es visible en el storyboard (entrada → tensión → giro/mecanismo → prueba/clímax → resolución/CTA).
- Los **overlays/disclaimers** de compliance están indicados donde el Spine lo exige (p. ej. "resultados no típicos", claims en boca de testimonio).
- Los prompts de generación son **autosuficientes** (un tercero podría producir la escena sin contexto adicional).

---

## Fase 5 — Handoff a producción / media buying

**Input**: entregable ClickUp poblado (Fase 3) + briefs aprobados (Fase 4).

**Output**: un **paquete accionable**:
- Assets a producir por prioridad (qué se graba/diseña primero).
- Mapa **ad → campaña/ad set** para el media buyer, con el nivel de awareness (para casar con audiencia/ubicación) y la hipótesis (para leer el resultado del test).
- Convenciones de **nomenclatura** que amarran cada asset a su subtarea de ClickUp / bache (para que el feedback de Etapa 4 vuelva trazable a bache/hipótesis).

**Quién lo hace**: humano (director creativo entrega producción; media buyer levanta las campañas de Etapa 3).

**Criterio de "hecho bien"**
- Cada asset producido mapea **1:1** a una subtarea de ClickUp (bache) y a una **hipótesis** testeable.
- La nomenclatura permite que la Etapa 4 (Feedback) devuelva ganadores/perdedores **al bache y a la hipótesis** que los originó, cerrando el loop hacia Research.

---

## Cómo escalar el motor

El motor está parametrizado por **N** (baches) y **M** (ads por bache).

**Escalar N (más baches)**
- N = número de **ángulos estratégicos diferenciados** que el Spine soporta. Añade un bache por cada eje nuevo: un sub-avatar adicional, otra objeción raíz, otro villano, otro nivel de awareness, otra plataforma-cabeza-de-playa.
- No subas N con ángulos redundantes: dos baches que testean el mismo deseo/awareness/emoción son un solo test disfrazado.
- Cada bache extra = un agente extra en paralelo en Fase 1 y otro en Fase 2. El coste crece lineal; el patrón no cambia.

**Escalar M (más ads por bache)**
- M por defecto = 3. Súbelo cuando tengas **más estructuras ganadoras distintas** disponibles (regla: 1 estructura ≠ por ad). Si solo hay 3 estructuras buenas, M = 3.
- Al subir M, mantén la **diversidad de molde** (M competidores distintos) y la **cobertura de formato** (mezcla Video/Static según lo que la estructura imitada dicte).

**Palancas de calidad al escalar** (no negociables aunque crezca el volumen)
- **Traza siempre**: todo ad nombra su ganador imitado + IDs de VoC.
- **Anclaje siempre**: todo ad pasa por el Spine (avatar/deseo/emoción/mecanismo/villano/prueba/objeción/awareness/compliance).
- **Diversidad siempre**: baches con ángulos distintos y awareness distintos; dentro del bache, estructuras distintas.
- **Compliance siempre**: el léxico prohibido del Spine se aplica a cada `copy` y a cada overlay del brief.

Si un ad no se puede **trazar** ni **anclar**, se descarta: en este motor, volumen sin trazabilidad no es escala, es ruido.
