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
├── RUNBOOK.md                                      <- cómo correr el motor end-to-end (secuencia operativa)
├── HANDOFF.md                                     <- estado vivo, decisiones y backlog de refinamiento
├── config.json                                    <- fuente única de defaults (N, M, awareness, ángulos base, paths)
├── MOTOR DE CREATIVOS v1.0 — Spec Operativo.md    <- la máquina: fases, schemas, criterios de "hecho bien"
├── INTERFACE — Contrato con el Motor de Research.md <- contrato de entrada (Spine + scripts ganadores + VoC)
├── metodo/                                         <- el método (lo reusable)
│   ├── 01 — Bache (definición + schema).md
│   ├── 02 — Clasificación (imitación · iteración · ideación).md
│   ├── 03 — Imitación (clonar un ganador y re-anclar).md
│   ├── 04 — Brief (storyboard + paridad emocional).md
│   ├── 05 — Compliance de creativos.md
│   └── 06 — Convención Creative Roadmap (Excel).md
├── scripts/                                        <- generación (Workflow) + persistencia (Python)
│   ├── wf_motor.js                                 <- ORQUESTADOR end-to-end (Fase 1→2→4)
│   ├── wf_baches.js · wf_imitaciones.js · wf_briefs.js  <- workflows por fase (uso granular)
│   ├── intake.py                                   <- Fase 0: valida input + congela snapshot
│   ├── persist.py                                  <- Fases 3-4: escribe el bundle a casos/<slug>/
│   ├── motor_config.py                             <- loader de config.json + helpers de paths
│   └── build_roadmap.py · md2docx.py               <- builders de Excel y Word
├── plantillas/                                     <- moldes de entrada/salida
│   └── INPUT — Spine (plantilla).md
└── casos/                                          <- ejecuciones de referencia (un producto por caso)
```

## Quickstart

La secuencia operativa completa está en **[`RUNBOOK.md`](RUNBOOK.md)**. En resumen, el motor alterna dos capas — **Python valida/escribe** (tiene disco) y **Workflow genera** (lo invoca Claude, sin disco):

1. **Lee `INTERFACE — Contrato con el Motor de Research.md`** y consigue el INPUT: **Spine** + **2–5 scripts ganadores** del competidor (+ banco **VoC** opcional con IDs `EVxxxx`). Sin un Spine válido, el motor no arranca.
2. **Fase 0 — `python scripts/intake.py …`**: valida el Spine (bloquea si falta un obligatorio) y congela el snapshot en `casos/<slug>/input/`.
3. **Fases 1·2·4 — `Workflow(scriptPath: scripts/wf_motor.js, args)`**: el orquestador genera N baches → M imitaciones re-ancladas por bache → un brief por bache, y devuelve el *bundle*.
4. **Fases 3·4 — `python scripts/persist.py --bundle … [--docx] [--xlsx]`**: escribe baches, ads, briefs y `roadmap_rows.json` a `casos/<slug>/` (y opcional puebla el Excel).
5. **Fase 5 — handoff a Media Buying**: cada fila del roadmap = un asset a producir/lanzar, trazable a su bache e hipótesis.

Los defaults (N=5, M=3, ángulos base) están en [`config.json`](config.json). Para iterar una sola fase, usa los workflows granulares (`wf_baches`/`wf_imitaciones`/`wf_briefs`) — ver RUNBOOK.

## Estado

**v1.0 — corrible end-to-end.** La arquitectura, el vocabulario canónico y los contratos están definidos, y el motor ya **corre de punta a punta**: Fase 0 (intake + snapshot), orquestador (`wf_motor`), VoC cableado, config de defaults y capa de persistencia (ver `RUNBOOK.md` y `HANDOFF.md`). **Pendiente:** validación viva con un Spine real (primer caso dentro del repo), compliance por categoría y roadmap idempotente. Espera ajustes en el schema del bache y el formato del brief conforme se corran productos.

## Seguridad

**Los tokens y credenciales viven FUERA del repo.** Las conexiones a servicios externos (ad-spy tipo TrendTrack, APIs de generación, Apify) se configuran vía variables de entorno locales. Nunca se commitean claves, tokens ni secretos: el repo contiene solo la lógica del motor, nunca credenciales.
