export const meta = {
  name: 'wf-imitaciones',
  description: 'Por cada bache, genera M anuncios de IMITACIÓN (cada uno clona la estructura de un ganador distinto del competidor y la re-ancla al Spine). Product-agnostic.',
  phases: [{ title: 'Imitaciones', detail: 'un agente por bache' }],
}

// -------------------------------------------------------------------
// args esperados:
// {
//   spinePath:   "ruta/al/Spine.md",
//   scriptsPath: "ruta/al/competitor_scripts.md",
//   batches: [ {concept, angle, avatar, mass_desire, awareness, hypothesis}, ... ], // metadata de cada bache
//   adsPerBatch: 3
// }
// Devuelve { batches: [ { ads: [ {imita_competidor, ad_format, copy, nota} x M ] }, ... ] }
// alineado por índice con args.batches.
// -------------------------------------------------------------------
const A = args || {}
const SPINE = A.spinePath
const SCRIPTS = A.scriptsPath
const M = A.adsPerBatch || 3
const batches = A.batches || []
if (!SPINE || !SCRIPTS || !batches.length) {
  throw new Error('wf-imitaciones requiere args.spinePath, args.scriptsPath y args.batches[]')
}

const AD = {
  type: 'object', additionalProperties: false,
  required: ['imita_competidor', 'ad_format', 'copy', 'nota'],
  properties: {
    imita_competidor: { type: 'string', description: 'competidor/ad cuya estructura se imita (del archivo de scripts)' },
    ad_format: { type: 'string', enum: ['Video', 'Static'] },
    copy: { type: 'string', description: 'guion/copy completo, listo para producir, en el registro del mercado del Spine' },
    nota: { type: 'string', description: 'qué estructura se conservó + qué se re-ancló + IDs de VoC que lo sostienen' },
  },
}
const SCHEMA = {
  type: 'object', additionalProperties: false, required: ['ads'],
  properties: { ads: { type: 'array', minItems: M, maxItems: M, items: AD } },
}

phase('Imitaciones')
const results = await parallel(batches.map((b, i) => () => agent(
`Generas ${M} ANUNCIOS DE IMITACIÓN para el BACHE #${i + 1}.

FUENTES:
- Spine (frame estratégico VIGENTE, fuente de verdad): "${SPINE}"
- Estructuras ganadoras del competidor: "${SCRIPTS}"
- Metadata de ESTE bache (no la cambies, es tu concepto): ${JSON.stringify(b)}

QUÉ ES IMITACIÓN: te basas ~90-100% en la ESTRUCTURA de un anuncio ganador del competidor. Conservas su ARCO (patrón de hook, secuencia problema->giro->mecanismo->prueba->CTA, ritmo, formato). SOLO re-anclas el CONTENIDO al Spine: avatar, emoción, villano, mecanismo (respetando el léxico prohibido del Spine), prueba, objeción.

REGLAS:
- Cada uno de los ${M} ads imita la estructura de un COMPETIDOR DISTINTO del archivo de scripts (nómbralo en "imita_competidor").
- Copy en el idioma/registro del mercado del Spine, tono del avatar.
- Compliance según el Spine: afirmaciones fuertes en boca de testimonio; nada de claims prohibidos.
- ad_format Video o Static según la estructura imitada.
- "nota": qué competidor imitas + qué elementos estructurales conservaste + qué re-anclaste + IDs de VoC.

Devuelve EXACTAMENTE ${M} ads en el schema. Sin texto de proceso.`,
  { label: `bache-${i + 1}`, phase: 'Imitaciones', schema: SCHEMA }
)))

return { batches: results }
