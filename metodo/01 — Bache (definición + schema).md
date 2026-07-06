# Método: el Bache

El **bache** (batch) es la unidad de trabajo fundamental del Motor de Creativos. Es el puente entre el veredicto estratégico (el **Spine**, output de la Etapa 1) y los anuncios concretos que salen a testear. Sin bache no hay hipótesis; sin hipótesis, un test no enseña nada.

Este documento define el bache a fondo, entrega su **schema JSON completo**, explica **cómo derivar los ángulos** de los baches desde el Spine, y recomienda **cuántos baches** correr en un arranque.

---

## 1. Definición

> Un **bache** es un concepto creativo que alinea cuatro cosas en una sola apuesta: **ÁNGULO + AVATAR + DESEO MASIVO + HIPÓTESIS**. Agrupa todos los anuncios que comparten ese concepto.

En términos operativos:

- **Un bache = una hipótesis falsable.** Cada test nace una hipótesis ("si le hablo a `<AVATAR>` desde `<ÁNGULO>` apelando a `<DESEO>`, entonces convierte porque `<RAZÓN>`"). El bache existe para probar o refutar esa apuesta.
- **Un bache agrupa anuncios, no los mezcla al azar.** Los 3 anuncios (por defecto) dentro de un bache son variaciones que atacan **la misma hipótesis** por caminos distintos (distinto hook, distinta prueba, distinto formato). Si dos anuncios prueban cosas distintas, son de baches distintos.
- **El bache es la unidad de lectura del test.** Cuando la Etapa 3 (media buying) devuelve datos, lees a nivel de bache: no "¿ganó el anuncio X?" sino "¿ganó la hipótesis de este bache?". Eso es lo que retroalimenta la Etapa 1.

Un bache **no** es un ángulo suelto, **no** es un solo anuncio, y **no** es un formato. Es la apuesta estratégica completa, empaquetada para testear.

---

## 2. Schema JSON del bache

```json
{
  "batch_id": "B01",
  "concept": "<nombre corto y memorable del concepto creativo>",
  "angle": "<el ángulo: el punto de entrada psicológico al deseo>",
  "avatar": "<a quién le habla ESTE bache — segmento del avatar núcleo del Spine>",
  "mass_desire": "Quiero <resultado que el avatar ya anhela, en su lenguaje>",
  "awareness": "Unaware | Problem Aware | Solution Aware | Product Aware | Most Aware",
  "hypothesis": "Si <ángulo/mensaje> a <avatar> apelando a <deseo>, entonces <resultado esperado> porque <razón anclada en VoC/prueba>.",
  "spine_refs": {
    "villain": "<villano del Spine que este bache activa>",
    "mechanism": "<UMP/UMS/USP que sostiene la promesa>",
    "proof": "<prueba/evidencia que respalda — ID EVxxxx si existe>",
    "objection": "<objeción raíz que este bache desarma o esquiva>"
  },
  "ads": [
    {
      "ad_id": "B01-A1",
      "classification": "Imitación | Iteración | Ideación",
      "imita_competidor": "<ref del anuncio ganador imitado — vacío si no aplica>",
      "ad_role": "<rol del anuncio: hook-test | prueba-social | demo-mecanismo | testimonio | ...>",
      "ad_format": "Video | Static",
      "copy": "<copy principal / guion del anuncio>",
      "nota": "<qué variable cambia este anuncio respecto a sus hermanos del bache>"
    }
  ]
}
```

### Explicación campo por campo

| Campo | Qué es | Regla de oro |
|---|---|---|
| `batch_id` | Identificador estable (B01, B02…). | Nunca se recicla; permite trazar el test en el feedback loop. |
| `concept` | Nombre corto y memorable del concepto. | Debe caber en una frase; es el "nombre del test". |
| `angle` | El **ángulo**: el punto de entrada psicológico al deseo (el "por dónde le entro"). | Un solo ángulo por bache. Si hay dos, son dos baches. |
| `avatar` | El segmento del avatar núcleo del Spine al que le habla **este** bache. | Hereda del Spine, pero puede afinar a un sub-segmento. |
| `mass_desire` | El deseo masivo, redactado como **"Quiero…"** en el lenguaje del avatar. | Es deseo pre-existente, no se crea; se canaliza (Schwartz). |
| `awareness` | Nivel de consciencia del avatar frente al problema/producto. | Determina cuánto contexto necesita el hook. Uno por bache. |
| `hypothesis` | La apuesta falsable, con la fórmula **Si… entonces… porque…**. | El "porque" debe anclar en VoC o prueba, no en opinión. |
| `spine_refs.villain` | El villano del Spine que el bache activa. | El enemigo común contra el que se alinea el avatar. |
| `spine_refs.mechanism` | El mecanismo (UMP/UMS/USP) que sostiene la promesa. | Es el "por qué funciona" único; diferencia de la categoría. |
| `spine_refs.proof` | La prueba que respalda la promesa (ID EVxxxx si existe). | Sin prueba, la promesa es un claim vacío. |
| `spine_refs.objection` | La objeción raíz que el bache desarma o esquiva. | Todo bache debe saber contra qué fricción pelea. |
| `ads[]` | Los anuncios (por defecto 3) que comparten la hipótesis. | Todos atacan la MISMA hipótesis por caminos distintos. |
| `ads[].classification` | Imitación / Iteración / Ideación (ver Canon). | Son opciones, no una cuota. Al apoyarse en ganadores, mayoría **Imitación**. |
| `ads[].imita_competidor` | Ref del anuncio ganador imitado. | Se conserva su ARCO; solo se re-ancla el contenido al Spine. |
| `ads[].ad_role` | El rol del anuncio dentro del bache. | Ej. hook-test, prueba-social, demo-mecanismo, testimonio. |
| `ads[].ad_format` | Video o Static. | El formato es una variable de test, no un default. |
| `ads[].copy` | El copy/guion principal. | Debe ser fiel al ángulo y al awareness del bache. |
| `ads[].nota` | Qué variable cambia este anuncio vs. sus hermanos. | Hace explícito el "por dónde ataca" cada variación. |

---

## 3. Cómo derivar los ángulos de los baches desde el Spine

El Spine trae las piezas; el bache las **ensambla en apuestas**. Cada componente del Spine sugiere un tipo de bache natural. Estos son los **arquetipos de bache** que se derivan casi mecánicamente:

### 3.1 Bache-núcleo (del Deseo Masivo #1)
El bache ancla. Ataca de frente el **deseo masivo #1** del Spine con el ángulo más directo posible. Es la apuesta base contra la cual se miden las demás.
- **Ángulo:** promesa directa del resultado más deseado.
- **Ejemplo de hipótesis:** *"Si le prometo a `<AVATAR>` el `<DESEO #1>` de forma directa, entonces convierte porque es el resultado que más anhela."*

### 3.2 Bache-objeción (desarma la objeción raíz)
Toma la **objeción raíz** del Spine y construye el anuncio alrededor de desactivarla. Útil cuando la fricción de compra es alta.
- **Ángulo:** "sé lo que estás pensando, y aquí está por qué no aplica".
- **Ejemplo de hipótesis:** *"Si desarmo la objeción `<OBJECIÓN>` con `<PRUEBA>`, entonces convierte porque removí el freno #1."*

### 3.3 Bache-villano (activa el enemigo común)
Se apoya en el **villano** del Spine: nombra al enemigo, canaliza la frustración del avatar hacia él y posiciona el producto como el aliado.
- **Ángulo:** "el problema no es tu culpa, es `<VILLANO>`".
- **Ejemplo de hipótesis:** *"Si culpo a `<VILLANO>` del dolor del avatar, entonces convierte porque le quito la culpa y le doy un enemigo."*

### 3.4 Bache-prueba (lidera con la evidencia)
Lidera con la **prueba** más fuerte del Spine (demo, testimonio, dato, before/after). Ideal para awareness alto o mercados escépticos.
- **Ángulo:** "no me creas a mí, mira esto".
- **Ejemplo de hipótesis:** *"Si abro con `<PRUEBA>` en vez de con promesa, entonces convierte porque el escéptico necesita ver antes de creer."*

### 3.5 Bache-mecanismo (el "por qué funciona")
Centra el anuncio en el **mecanismo único** (UMP/UMS/USP): explica *por qué* funciona distinto a todo lo demás. Diferencia de la categoría.
- **Ángulo:** "esto funciona por una razón que nadie más tiene: `<MECANISMO>`".
- **Ejemplo de hipótesis:** *"Si explico `<MECANISMO>`, entonces convierte porque le doy una razón creíble y única para creer la promesa."*

### 3.6 Bache-cabeza-de-playa (hipótesis a validar)
El bache exploratorio. Apuesta a un sub-segmento del avatar, un deseo secundario o un ángulo lateral que la VoC insinúa pero aún no está probado. Su función es **descubrir**, no confirmar.
- **Ángulo:** un insight fresco de la VoC aún no explotado.
- **Ejemplo de hipótesis:** *"Si le hablo al sub-segmento `<AVATAR SECUNDARIO>` desde `<ÁNGULO LATERAL>`, entonces convierte porque la VoC sugiere un deseo latente no atendido."*

> **Regla de mapeo:** un componente del Spine → un ángulo → un bache. Si un ángulo mezcla dos componentes con igual peso (p. ej. villano **y** mecanismo), decide cuál domina y hazlo la columna vertebral; el otro entra como soporte dentro del guion, no como segundo ángulo.

---

## 4. ¿Cuántos baches para un arranque?

**Recomendación: 5 baches en el arranque.** Es el punto dulce entre aprender y no dispersar el presupuesto.

Por qué 5:

- **Cubre el mapa estratégico sin huecos.** Cinco baches permiten correr los arquetipos de mayor rendimiento —núcleo, objeción, villano, prueba/mecanismo— **más uno exploratorio** (cabeza-de-playa). Cada pilar del Spine queda representado por al menos una apuesta.
- **Da señal estadística sin diluir.** Menos de 3 baches no cubre el mapa y te ata a pocas apuestas; más de 6-7 al arranque fragmenta el presupuesto y ninguna hipótesis junta datos suficientes para leerse.
- **Mantiene el feedback loop legible.** Con 5 baches, la Etapa 3 devuelve un veredicto claro por hipótesis y la Etapa 1 sabe exactamente qué re-anclar en la siguiente vuelta.

**Reparto sugerido para el arranque (5 baches):**

| # | Bache | Rol en el arranque | Riesgo |
|---|---|---|---|
| B01 | Núcleo (Deseo #1) | Apuesta base / control | Bajo |
| B02 | Objeción | Desarma el freno de compra | Bajo |
| B03 | Villano | Canaliza la frustración | Medio |
| B04 | Prueba **o** Mecanismo | Convence al escéptico | Bajo-Medio |
| B05 | Cabeza-de-playa | Descubre territorio nuevo | Alto |

> Regla práctica: **≥3 de los 5 baches deben ser de bajo riesgo** (anclados en ganadores del competidor vía Imitación), y **como máximo 1-2 exploratorios**. El arranque busca tracción, no arte. Escala lo que gana, mata lo que no, y en la siguiente vuelta reemplaza los baches muertos por nuevas hipótesis derivadas del feedback.

Cada bache produce por defecto **3 anuncios** (mayoritariamente Imitaciones re-ancladas al Spine), de modo que un arranque de 5 baches = **~15 anuncios** listos para volcar al Creative Roadmap.

---

## 5. Plantilla vacía de un bache

Copia este bloque y llénalo por cada bache. Un bache por tabla.

| Campo | Valor |
|---|---|
| **batch_id** | `B0_` |
| **concept** | `<nombre corto y memorable>` |
| **angle** | `<el punto de entrada psicológico al deseo>` |
| **avatar** | `<segmento del avatar núcleo del Spine>` |
| **mass_desire** | `Quiero <resultado en lenguaje del avatar>` |
| **awareness** | `Unaware | Problem Aware | Solution Aware | Product Aware | Most Aware` |
| **hypothesis** | `Si <ángulo> a <avatar> apelando a <deseo>, entonces <resultado> porque <razón VoC/prueba>.` |
| **spine_refs.villain** | `<villano del Spine>` |
| **spine_refs.mechanism** | `<UMP/UMS/USP>` |
| **spine_refs.proof** | `<prueba / EVxxxx>` |
| **spine_refs.objection** | `<objeción raíz>` |

**Anuncios del bache** (por defecto 3, mayoría Imitación):

| ad_id | classification | imita_competidor | ad_role | ad_format | copy | nota |
|---|---|---|---|---|---|---|
| `B0_-A1` | `Imitación` | `<ref ganador>` | `<hook-test / prueba-social / demo-mecanismo…>` | `Video / Static` | `<copy / guion>` | `<qué variable cambia>` |
| `B0_-A2` | `Imitación` | `<ref ganador>` | `<...>` | `Video / Static` | `<copy / guion>` | `<qué variable cambia>` |
| `B0_-A3` | `Iteración / Ideación` | `<vacío o propio>` | `<...>` | `Video / Static` | `<copy / guion>` | `<qué variable cambia>` |

---

> **Checklist de un bache bien formado:** (1) un solo ángulo; (2) una hipótesis falsable con "porque" anclado; (3) awareness explícito; (4) todos los anuncios atacan la misma hipótesis; (5) referencias al Spine completas (villano, mecanismo, prueba, objeción); (6) mayoría de anuncios en Imitación si se apoya en ganadores del competidor.
