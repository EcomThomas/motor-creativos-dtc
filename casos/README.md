# casos/ — Ejecuciones de referencia

Cada vez que el motor se corre para un producto real, esa corrida completa se archiva aquí como **`casos/<producto>/`**. El *método* (en `metodo/`) es lo reusable; los *casos* son las pruebas de que funciona y el material del que se aprende.

## Estructura de un caso

```
casos/<producto>/
├── input/          <- SNAPSHOT congelado del INPUT que se consumió (regla de la INTERFACE)
│   ├── Spine.md                       (la versión exacta del veredicto estratégico usada)
│   ├── competitor_scripts.md          (los guiones ganadores del competidor)
│   └── (opcional) voc_bank.*          (evidencia VoC con IDs)
├── baches/         <- los N baches generados (JSON + volcado a Creative Roadmap)
├── scripts-ads/    <- los guiones de los anuncios (N baches × M ads)
└── briefs/         <- el brief de producción por bache (.md + .docx)
```

**Por qué el snapshot:** el motor de research sigue evolucionando; para que un caso sea **reproducible**, se congela aquí la versión exacta del Spine y de los scripts que alimentaron esa corrida. Ver `INTERFACE — Contrato con el Motor de Research.md`.

## Caso de referencia inicial — Suplemento hepático MX

La **primera ejecución** de este método (5 baches × 3 imitaciones + 5 briefs con storyboard y paridad emocional) se hizo **antes de separar este repo**, dentro del **Motor de Research** (`motor-research-dtc`). Sus artefactos viven allí:

- Baches → hoja **Creative Roadmap** del Excel `Growth Guide '26.xlsx`.
- Scripts de imitación y briefs → `v3.1/briefs/` del repo de research.
- Input consumido → `v3.1/DOC 00 — Master Spine v3.2` + `v3.1/research/competitor_scripts_trendtrack.md`.

Queda como referencia histórica. La próxima corrida ya nace dentro de este repo siguiendo la estructura de arriba.
