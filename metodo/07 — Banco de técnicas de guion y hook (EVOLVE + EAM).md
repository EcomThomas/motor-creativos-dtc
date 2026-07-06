# Método: Banco de técnicas de guion y hook (EVOLVE + EAM)

Este documento es el **arsenal táctico** del motor: las técnicas concretas de hook, arco, cuerpo y producción destiladas de dos sistemas externos de escritura de video ads —**EVOLVE** ($100k Viral Video/UGC Ads) y **EAM** (Elite Video Ad Script Creator)—, mapeadas a las fases del motor.

> **Qué NO es.** No reemplaza el canon. El motor sigue siendo **imitación-first** ([metodo/02](02%20—%20Clasificación%20(imitación%20·%20iteración%20·%20ideación).md)): el ARCO lo pone un ganador probado; el re-anclaje al Spine manda. Este banco **alimenta** Fase 1 (baches), Fase 2 (imitaciones/copy) y Fase 4 (brief), sin cambiar su lógica.
>
> **Product-agnostic.** Todo va con `<MARCADORES>`; lo específico entra por el INPUT (Spine + scripts ganadores + VoC). Ninguna técnica trae un producto/nicho hardcodeado.

---

## 0. Los dos sistemas fuente (en una línea)

- **EVOLVE** — SOP conversacional que funde la *fórmula de video orgánico viral* (Hook → Suspense → Payoff → Raise Stakes → Engagement → CTA) con Schwartz. Aporta la **capa viral y de retención**.
- **EAM** — system-prompt de psicología de venta ("arqueología emocional"): 6 hooks + 1 hold, modos General/Organic (el modo *Storytelling* solo aparece en la versión base de EAM). Aporta la **capa de arquitectura psicológica del cuerpo**.

Ambos comparten el modelo: **1 hook scroll-stopping (<3s) + 1 cuerpo que sostiene y paga la promesa, ambos ensamblados —no inventados— a partir de deseos preexistentes (Schwartz).**

---

## 1. Técnicas de HOOK → Fase 1/2

### 1.1 Banco de hooks por bache
Genera **6–9 hooks** por bache, cada uno atacando un ángulo emocional distinto pero todos ejecutables sobre el mismo arco troncal. Alimenta el requisito ya existente ("un hook distinto por anuncio", [metodo/04:294](04%20—%20Brief%20(storyboard%20+%20paridad%20emocional).md)). Por hook: 2 variaciones + visual sugerido + `mass_desire` + qué testea + de qué fuente/VoC salió.

> **Estado real:** hoy **no** hay componente que produzca este banco. El schema de Fase 2 ([scripts/wf_imitaciones.js](../scripts/wf_imitaciones.js) / [wf_motor.js](../scripts/wf_motor.js)) pide `{imita_competidor, ad_format, copy, nota}` — un ad por competidor distinto, no un cuerpo fijo con N hooks. Es una **capacidad a añadir** al agente de guion, no algo que el script ya emita.

### 1.2 Three-Element Test (rúbrica de aceptación del hook)
Un hook pasa solo si tiene los **tres**:
1. **Intensidad emocional** — se siente algo en <3s (miedo, curiosidad, reconocimiento, deseo).
2. **Relevancia personal** — es sobre SU vida, no sobre el producto/marca.
3. **Curiosity gap** — obliga a saber qué sigue (específico, no vago).

### 1.3 Checklist scroll-stop (QA binario del hook)
- [ ] ¿Engancha Y retiene en los primeros 1–2s?
- [ ] ¿Crea una imagen/visual clara en la mente?
- [ ] ¿Tiene un *label* de a quién le habla ("si caminas a un perro que jala…")?
- [ ] ¿Es relatable / auténtico?
- [ ] **¿Parece un anuncio? → si SÍ, está mal.**
- [ ] ¿Se entiende sin sonido (soundless understanding)?

### 1.4 Mecánicas de hook (EVOLVE)
Combine Unlikely Elements · Start in Action + Zero Backstory · Avoid Chaos (un solo foco) · Avoid Mentioning Time (no revelar cuánto tarda el payoff).

**Longitud (dos reglas distintas, no confundir):**
- **EVOLVE:** todos los hooks/headlines **6–8 palabras máx** (regla general, cualquier formato).
- **EAM (text-on-screen):** **5–7 palabras por bloque** de texto en pantalla.

### 1.5 Palabras-gatillo por intención (usar SIEMPRE filtradas por `LÉXICO_PROHIBIDO`)
Fiel a la fuente (EAM): **Curiosidad** — secret/discover/reveal/truth/actually/real. **Autoridad** — proven/scientific/expert/professional/certified. **Pertenencia** — us/them/community/together/exclusive. (**Miedo/urgencia** — ver Anexo de alto riesgo §7; casi todas caen en `LÉXICO_PROHIBIDO`.)

---

## 2. Técnicas de ARCO y CUERPO → Fase 2 (re-anclaje) / Fase 4

Estas rellenan el **hueco del molde imitado** sin arrastrar el claim ajeno (Paso 4 de [metodo/03](03%20—%20Imitación%20(clonar%20un%20ganador%20y%20re-anclar).md)):

| Técnica | Qué hace | Cómo se usa en el motor |
|---|---|---|
| **Gradualization / belief ladder** | Yes-ladder: de una verdad aceptada a un claim grande, un peldaño a la vez | Estructura del cuerpo re-anclado; cada frase prepara la siguiente |
| **Mechanism library** | Explicar *por qué* funciona (UMP/UMS) para vencer "too good to be true" | Rellena `spine_refs.mechanism` como creencia (compliant, [metodo/05 §4](05%20—%20Compliance%20de%20creativos.md)) |
| **Intensification** | Agitar dolor/deseo desde múltiples ángulos; "sit in the problem longer" | Sube la tensión del arco antes del giro |
| **Layer Benefits** | Apilar Funcional → Emocional → Social → Identidad | Checklist de completitud del cuerpo |
| **Information gap** | Abrir loops y cerrarlos estratégicamente (Zeigarnik) | Retención a lo largo del guion |
| **Identification** | Lenguaje/casting/POV del avatar; "quién quiero ser" | Casting de [metodo/04 §2](04%20—%20Brief%20(storyboard%20+%20paridad%20emocional).md) + registro del copy |
| **Objection-reframe map** | Banco de reencuadres: "ya lo probé todo"→mecanismo; "me van a juzgar"→grupo iluminado; "no puedo fallar otra vez"→primer paso sin riesgo | Alimenta el bache-objeción ([metodo/01 §3.2](01%20—%20Bache%20(definición%20+%20schema).md)) |
| **Preemptive skepticism** | "Yo también dudaba, pero…" | Va en boca de testimonio ([metodo/05 §5](05%20—%20Compliance%20de%20creativos.md)) |
| **Concentration** | Eliminar alternativas: por qué fallan las otras opciones | Diferenciación de categoría |
| **Doctrina cold-traffic** | No conoce la marca; los primeros 3s son sobre ÉL, nunca features | Frame de los prompts (`FRAME`/`CTX` en los workflows) |
| **Two Ways In** | *Mirror* (reflejar su mundo interno) o *Hijack* (secuestrar un interés que ya tiene) | Elección de ángulo de entrada del bache |

---

## 3. Registros de ad (perillas de voz) → Fase 4 (guion)

Un mismo insight se re-expresa en varios registros para multiplicar creativos sin nuevo research. **Son una perilla de PROMPT/guion, no un campo del schema** (ver nota de §6):

- **General / mini-documental** — educa/entretiene con autoridad de marca; entra por un evento histórico/científico. Awareness bajo (Unaware/Problem Aware). **Esqueleto de arco reusable** (EAM): `gancho histórico → stakes vida/muerte → viaje del héroe → verdad revelada → aplicación moderna → producto como legado`.
- **Organic / UGC camuflado** — se disfraza de experiencia personal ("no parece ad"): descubrimiento personal ("acabo de descubrir…"), problema relatable, reacción auténtica, prueba social natural, FOMO ("ojalá lo hubiera sabido antes"). Awareness Problem/Solution Aware.

> El tercer registro de EAM, **Storytelling / revelación** (mini-documental de "verdad oculta"), es de **alto riesgo** y NO es un registro canónico: vive **exclusivamente** en el Anexo §7, con gate obligatorio. No se usa por defecto ni se siembra en la taxonomía normativa.

---

## 4. Técnicas de PRODUCCIÓN y EDICIÓN → Fase 4

- **Beat-map en timestamps** — esqueleto por defecto del storyboard: `0:00 Hook > Suspense/Agitación > Giro/Mecanismo > Prueba/Clímax > Resolución/CTA`. Enchufa en la columna **Tiempo** de las 8 columnas de [metodo/04](04%20—%20Brief%20(storyboard%20+%20paridad%20emocional).md).
- **Stretch / subdivisión del concepto** (EVOLVE, motor de retención) — dividir un concepto simple en **pasos progresivos** que construyen hacia el payoff, introduciendo un elemento/acción nuevo en cada paso para mantener sensación de avance y **extender watch-time**. Se mapea a la secuencia de beats del storyboard (más filas = más progresión), sin caer en relleno vacío.
- **Completion tactics** — Cut-Off a mitad de la última palabra (sube completion + rewatch) · Prompt End <5s tras el payoff · single payoff (no revelar múltiples) · Payoff-as-Hook (flash-forward si es muy visual).
- **Raise the stakes** — locación (pública + reacciones reales de bystanders como validación) · props con suspenso · wardrobe que cuenta otro lado · casting que profundiza la conexión (niños/ancianos/pares).
- **Engagement sin bait** — errores intencionales, mal uso de props, retention anchor (apartar un objeto del hook para retomarlo). **Respetar** la regla anti-engagement-bait de plataforma ([metodo/05 §7](05%20—%20Compliance%20de%20creativos.md)).
- **Soundless understanding** — subtítulos quemados + buena luz + color (la mayoría ve en mute). Ya es default en [metodo/04:117](04%20—%20Brief%20(storyboard%20+%20paridad%20emocional).md).
- **UGC brief (Creator Type)** — variables estructuradas (sexo/edad/etnia/setup, realismo iPhone) + tabla Module/Speech/Action + B-roll/Action; nota-por-línea para blindar el copy si el creador reescribe en su voz. Complemento **opcional** para UGC-first, no reemplaza el storyboard de 8 columnas.

---

## 5. Nota crítica sobre "6 hooks + 1 HOLD" (evitar el mal mapeo)

La técnica EAM de "6 hooks compatibles + 1 cuerpo universal" **NO** es el generador por defecto de las imitaciones del arranque. En la taxonomía del motor ([metodo/02](02%20—%20Clasificación%20(imitación%20·%20iteración%20·%20ideación).md)), "1 cuerpo fijo + varía solo el hook para aislar la variable" es la definición de **ITERACIÓN**, que idealmente parte de un anuncio propio con señal previa (nace del feedback loop, Etapa 4). Además, el bache exige que los M anuncios ataquen la hipótesis por **caminos distintos** (hook, prueba, formato), no solo por el hook ([metodo/01:16](01%20—%20Bache%20(definición%20+%20schema).md)).

**Uso correcto:**
- El **banco de hooks** (§1.1) alimenta el "hook distinto por anuncio" que ya se pide en imitación.
- El patrón "1 cuerpo + solo varía el hook" se reserva para **Iteración**: exprimir un ganador propio aislando el hook.

---

## 6. Mapa rápido: técnica → fase → componente

| Técnica | Fase | Componente del motor |
|---|---|---|
| Three-Element Test + checklist scroll-stop | 1/2 | Spec (criterio "hecho bien"), [metodo/03](03%20—%20Imitación%20(clonar%20un%20ganador%20y%20re-anclar).md) |
| Banco de hooks | 2 | **Sin componente hoy** — capacidad a añadir al agente de guion (el schema de wf_imitaciones/wf_motor solo pide `copy`+`nota`) |
| Belief-ladder · mechanism · layer benefits · objection map | 2 | Guía de guion en [metodo/03](03%20—%20Imitación%20(clonar%20un%20ganador%20y%20re-anclar).md) (Paso 4); el prompt de [scripts/wf_imitaciones.js](../scripts/wf_imitaciones.js) lo puede incorporar |
| Doctrina cold-traffic · Two Ways In | 1/2 | `FRAME`/`CTX` en [scripts/wf_motor.js](../scripts/wf_motor.js), [scripts/wf_baches.js](../scripts/wf_baches.js) |
| Registros General/Organic (perilla de guion) | 4 | Prompt de [scripts/wf_briefs.js](../scripts/wf_briefs.js) — **no** hay campo de schema para el registro (ver nota abajo) |
| Beat-map · stretch · completion tactics · raise-the-stakes | 4 | [metodo/04](04%20—%20Brief%20(storyboard%20+%20paridad%20emocional).md), [scripts/wf_briefs.js](../scripts/wf_briefs.js) |
| 6-hooks+1-hold (solo Iteración) | Etapa 4 | [metodo/02](02%20—%20Clasificación%20(imitación%20·%20iteración%20·%20ideación).md) |
| Storytelling / revelación | — | **Anexo §7, gate obligatorio** (no canónico) |

> **Nota — colisión de nombres a limpiar en el motor.** Los registros General/Organic **no tienen slot** en el schema actual (son una perilla de guion). Y ojo: el motor usa el nombre `ad_type` para **dos cosas distintas** — en el canon ([metodo/01:45](01%20—%20Bache%20(definición%20+%20schema).md)) `ad_type` = *rol* del anuncio (hook-test/prueba-social/demo-mecanismo), pero en el **código** ([wf_baches.js](../scripts/wf_baches.js), [config.json](../config.json), [persist.py](../scripts/persist.py)) `ad_type` es el enum `Imitation/Iteration/Ideation` (lo que el canon llama `classification`). Si se quiere trazar el registro (General/Organic), debería ser un campo NUEVO (p. ej. `registro`), no colgarlo de `ad_type`. Conviene unificar `classification` (canon) vs `ad_type` (código) en un futuro cleanup.

---

## 7. ANEXO DE ALTO RIESGO — explorar con GATE de compliance obligatorio

> ⚠️ **Lo de esta sección NO entra al canon.** Son técnicas de alto rendimiento *y* alto riesgo, documentadas para **explorar y decidir a mano**. Ningún creativo que las use se produce/lanza sin **veredicto PASA** de la checklist completa de [metodo/05 §8](05%20—%20Compliance%20de%20creativos.md) (A–G) **adjunto al bache** + revisión humana. Si `CATEGORÍA_SENSIBLE = true`, el default es la versión declawed; la cruda casi nunca sobrevive el gate.

### 7.1 Storytelling Conspirativo (mini-documental de "verdad oculta")

**Qué es (técnica cruda).** El arco no vende: **revela**. El espectador siente que lo dejan entrar en un secreto. En su forma cruda nombra a una industria/gremio como supresor ("lo que <INDUSTRIA> te oculta"), usa acusación ("mintieron") y fear-mongering. Fuente del *modo* Storytelling: la versión base de EAM; el aparato Zeigarnik/information gap que lo potencia viene de la versión enhanced de EAM (es un principio general de todos los guiones, no exclusivo de este modo).

**Arco (crudo):**
```
Hook-revelación (verdad oculta / descubrimiento suprimido / acusación)
 → construir el misterio (cifras, fechas, "los tests salieron limpios…")
 → la revelación (el mecanismo/ingrediente "secreto")
 → nombrar al VILLANO (en crudo: la industria / lo que todos hacen)
 → producto como escape o legado
 → prueba → CTA
```

**Por qué funciona:** information gap (Zeigarnik) + villain framing (le quita la culpa al avatar) + authority-by-story (usa un evento real como "prueba prestada").

**Kits de hook crudos (NO usar tal cual — pasar por el gate):**
- `Lo que <INDUSTRIA/CATEGORÍA> no quiere que sepas sobre <PROBLEMA>`
- `Cómo <GRUPO INESPERADO> logró <RESULTADO> con un método de <AÑO/ORIGEN>`
- `El rumor de que <CREENCIA CÓMODA> te está <CONSECUENCIA>`
- `Te dijeron que <X> era <seguro/normal>. Mintieron.`  *(este kit casi nunca pasa en `CATEGORÍA_SENSIBLE`)*

**Superficie de riesgo (lo que mira el gate):**

| Elemento tóxico | Regla que viola ([metodo/05](05%20—%20Compliance%20de%20creativos.md)) |
|---|---|
| "Mintieron / te lo ocultan / prohibido / antes de que lo bajen" | §3 regla 1 (claims absolutos), §8-A |
| Villano = industria/gremio que "oculta/miente" | §7 (sensacionalismo/plataforma), §8-E/G, roza difamación de categoría |
| Villano = enfermedad o competidor nombrado | §6 (claim de enfermedad), §8-D |
| Fear-mongering de salud como voz de marca | §3 regla 2 + §5 (debe ir en testimonio), §6, §8-A/B |
| Power-words crudos (banned/exposed/cure/destroy) | `LÉXICO_PROHIBIDO`, §3 regla 1, §8-A |
| "La evidencia muestra / los estudios / está comprobado" en voz de marca | §3 regla 2 + §5 (afirmación fuerte = testimonio), §8-A/B |
| Evento histórico presentado como prueba del resultado del producto | §3 reglas 5 y 8 (prueba honesta / regla de la captura), §8-B |
| 2ª persona que implique condición personal ("tú que sufres de <X>") | §7 (segmentación personal), §8-G |

**GATE de declaw (sub-checklist — conservar el arco, pasar [metodo/05 §8](05%20—%20Compliance%20de%20creativos.md)):**
- [ ] **Villano = mecanismo o hábito IMPERSONAL** (*"la pastilla que solo tapa el síntoma"*). **Prohibido** nombrar/aludir a una industria/gremio como que "oculta o miente", a una enfermedad, o a un competidor. → §8-D/E
- [ ] **Sin acusación ni desmentido de autoridad.** "Te lo ocultan / mintieron / la evidencia muestra" → reencuadrar como **creencia o testimonio del personaje** ("a mí lo que me hizo click fue…", "yo empecé a creer que…"), nunca como voz en off de marca. → §3 regla 2, §5, §8-A
- [ ] **Toda afirmación fuerte en boca de testimonio**, con overlay *"testimonio real · resultados individuales"*. → §5, §8-C
- [ ] **Cero claims de enfermedad**; mecanismo como creencia, no claim clínico. → §6, §8-D
- [ ] **Hooks pasados por `LÉXICO_PROHIBIDO`** (incluidos "oculta", "no quiere que sepas", "mintieron"). → §8-A
- [ ] **Sin 2ª persona** que implique atributo/condición personal; reformular a 1ª/3ª persona. → §7, §8-G
- [ ] **Anti "prueba prestada":** un evento histórico/deportivo puede ser *gancho de atención*, nunca *evidencia* de que el producto da ese resultado. → §3 reglas 5/8, §8-B
- [ ] **Landing coherente** con el creativo (la política mira el destino). → §7, §8-G
- Resultado: **"mini-documental de verdad incómoda"** en vez de teoría conspirativa — mismo scroll-stop, dentro del corral.

### 7.2 Power-words agresivos / fear-mongering
Alta intensidad, colisión frontal con `LÉXICO_PROHIBIDO` y "sin claims absolutos". El testimonio **amplía** lo decible pero **no anula** el léxico prohibido ([metodo/05 §5](05%20—%20Compliance%20de%20creativos.md)): un término prohibido sigue prohibido aunque lo diga un cliente. Tabla de sustitución:

| Power-word crudo | Sustituto compliant | ¿Válido en testimonio? |
|---|---|---|
| exposed / "te lo ocultan" | "lo que no me habían contado" | Sí (experiencia) |
| banned / prohibido | (eliminar; sin equivalente) | **No** |
| cure / cura | "apoyar / ayudar a" | Sí, suavizado |
| destroy / "está destruyendo tu <órgano>" | (eliminar; claim de daño/enfermedad) | **No** |
| shocking / "Russian roulette con tu salud" | (eliminar; sensacionalismo + claim) | **No** |
| guaranteed / garantizado | "en mi caso empecé a notar…" | Sí (individual) |

Los marcados **No** están prohibidos incluso en boca de testimonio.

### 7.3 Regla del anexo
Ninguna técnica de §7 se libera sin: (1) veredicto **PASA** de la checklist completa [metodo/05 §8 A–G](05%20—%20Compliance%20de%20creativos.md) adjunta al bache, (2) revisión humana explícita, (3) landing coherente. Si `CATEGORÍA_SENSIBLE = true`, default = versión declawed.

---

## 8. Qué NO se adopta (rompe el diseño del motor)

- **MCP research en vivo / "archaeological dig"** (EAM) — rompe la separación Etapa 1↔2 y la trazabilidad `EVxxxx`. El Spine ya trae el VoC destilado.
- **Flujo conversacional de chatbot** (First Response fija, "elige tu top 3") — el motor es batch con schema forzado.
- **Ejemplos de producto/nicho hardcodeados** — el motor es product-agnostic; entran como referencia de arco, nunca como plantilla.
