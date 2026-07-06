# Motor de Creativos DTC v1.0

**La máquina replicable para producir anuncios ganadores de cualquier producto DTC (Meta / TikTok), con metodología Eugene Schwartz.**

El Motor de Creativos toma un veredicto estratégico ya destilado (el **Spine**) y un puñado de **scripts ganadores del competidor**, y los convierte en baches de anuncios listos para producir. Su apuesta central no es "inventar desde cero": es **imitar lo que ya está probado en el mercado y re-anclarlo a tu Spine**. Cada anuncio nace de una hipótesis, hereda el arco de un ganador real y cambia solo el contenido (avatar, deseo, mecanismo, prueba, objeción) para que hable de TU producto.

Es **product-agnostic** por diseño. No hay ningún producto hardcodeado: los específicos —`<PRODUCTO>`, `<AVATAR>`, `<DESEO>`, `<VILLANO>`, `<MECANISMO>`, `<PRUEBA>`, `<OBJECION>`— entran por el INPUT, siempre. Cambias el Spine y los scripts de entrada, y el mismo motor produce creativos para otra categoría sin tocar su lógica.

## Posición en el pipeline

El motor es la **ETAPA 2** de un pipeline de 4 etapas que se retroalimenta en ciclo:

```
   +-----------------+     +==================+     +------------------+     +-----------------+
   |   1. RESEARCH   | --> |  2. CREATIVOS    | --> | 3. MEDIA BUYING  | --> |  4. FEEDBACK    |
   | (motor research)|     |  <ESTE MOTOR>    |     |   / TEST         |     |                 |
   |                 |     |                  |     |  (Meta / TikTok) |     |                 |
   | Spine + scripts |     | baches + brief   |     |  correr y medir  |     | señales, datos  |
   +-----------------+     +==================+     +------------------+     +-----------------+
          ^                                                                          |
          |                                                                          |
          +--------------------------------------------------------------------------+
                              el feedback vuelve a alimentar el Research
```

- **Entra:** el Spine (veredicto estratégico) + scripts ganadores del competidor + (opcional) banco VoC con IDs de evidencia.
- **Sale:** N baches de creativos, cada uno con M anuncios (por defecto 3, mayoritariamente imitaciones), volcados a la hoja **Creative Roadmap** + un **brief de producción** por bache.

## Regla núcleo

> **Imita ganadores probados y re-áncralos al Spine, con paridad emocional en cada escena.**

Tres ideas cargan esta regla:

1. **Imitación primero.** Cuando la jugada es apoyarse en las ideas ganadoras del competidor, los anuncios son **mayoritariamente imitaciones**: conservas el arco del ganador (patrón de hook, secuencia problema → giro → mecanismo → prueba → CTA, ritmo, formato) y solo cambias el contenido para re-anclarlo al Spine. Menor riesgo para salir a mercado. No se fuerza "una de cada tipo" (imitación / iteración / ideación son opciones, no una cuota).
2. **Re-anclaje al Spine.** Nada sale sin pasar por el veredicto estratégico: avatar núcleo, deseo masivo #1, emoción troncal, mecanismo, villano, prueba, objeción raíz, nivel de awareness y las reglas de compliance del producto.
3. **Paridad emocional.** Cada línea del guion tiene una escena cuya emoción, encuadre, luz, color, ritmo y sonido refuerzan lo que se dice. El arco emocional sube, tiene clímax y resolución. Prohibido el "cabeza parlante plana".

## Estructura del repo

```
motor-creativos-dtc/
├── README.md                                      <- este documento: qué es y cómo empezar
├── HANDOFF.md                                     <- estado vivo, decisiones y backlog de refinamiento
├── MOTOR DE CREATIVOS v1.0 — Spec Operativo.md    <- la máquina: fases, schemas, criterios de "hecho bien"
├── INTERFACE — Contrato con el Motor de Research.md <- contrato de entrada (Spine + scripts ganadores)
├── metodo/                                         <- el método (lo reusable)
│   ├── 01 — Bache (definición + schema).md
│   ├── 02 — Clasificación (imitación · iteración · ideación).md
│   ├── 03 — Imitación (clonar un ganador y re-anclar).md
│   ├── 04 — Brief (storyboard + paridad emocional).md
│   ├── 05 — Compliance de creativos.md
│   └── 06 — Convención Creative Roadmap (Excel).md
├── scripts/                                        <- los workflows del motor + utilidades
│   ├── wf_baches.js · wf_imitaciones.js · wf_briefs.js
│   └── build_roadmap.py · md2docx.py
├── plantillas/                                     <- moldes de entrada/salida
│   └── INPUT — Spine (plantilla).md
└── casos/                                          <- ejecuciones de referencia (un producto por caso)
```

## Quickstart

Para correr el motor en un producto nuevo:

1. **Lee `INTERFACE — Contrato con el Motor de Research.md`.** Entiende el contrato exacto: qué campos del Spine necesitas y en qué forma llegan los scripts ganadores del competidor. Sin un Spine válido, el motor no arranca.
2. **Consigue el INPUT.** Trae de la Etapa 1 el **Spine** (avatar, deseo masivo #1, emoción troncal, mecanismo, villano, prueba, objeción raíz, awareness, compliance) y **2–5 scripts ganadores** del competidor (transcripciones de un ad-spy tipo TrendTrack; "ganador" = muchos días corriendo / alto reach).
3. **Corre `wf_baches`.** Genera los N conceptos creativos (baches): cada uno alinea ángulo + avatar + deseo masivo + hipótesis + nivel de awareness.
4. **Corre `wf_imitaciones`.** Por cada bache, produce los M anuncios (por defecto 3), mayoritariamente imitaciones de ganadores re-ancladas al Spine.
5. **Vuelca a `Creative Roadmap`.** Escribe cada anuncio como fila en la hoja (Excel), usando la plantilla de fila.
6. **Corre `wf_briefs`.** Por bache, genera el brief de producción: script + storyboard con paridad emocional + prompts de generación.

## Estado

**v1.0 — scaffold.** La arquitectura, el vocabulario canónico y los contratos están definidos; los workflows y plantillas están en su primera versión y **pendientes de refinar** con casos reales. Espera ajustes en el schema del bache, el formato del brief y las reglas de volcado a Creative Roadmap conforme se corran productos.

## Seguridad

**Los tokens y credenciales viven FUERA del repo.** Las conexiones a servicios externos (ad-spy tipo TrendTrack, APIs de generación, Apify) se configuran vía variables de entorno locales. Nunca se commitean claves, tokens ni secretos: el repo contiene solo la lógica del motor, nunca credenciales.
