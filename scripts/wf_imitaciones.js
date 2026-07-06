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
//   vocPath:     "ruta/al/voc_bank.md",   // OPCIONAL: banco VoC con IDs EVxxxx
//   batches: [ {concept, angle, avatar, mass_desire, awareness, hypothesis}, ... ], // metadata de cada bache
//   adsPerBatch: 3
// }
// Devuelve { batches: [ { ads: [ {imita_competidor, ad_format, copy, nota} x M ] }, ... ] }
// alineado por índice con args.batches.
// -------------------------------------------------------------------
const A = args || {}
const SPINE = A.spinePath
const SCRIPTS = A.scriptsPath
const VOC = A.vocPath || null
const M = A.adsPerBatch || 3
const batches = A.batches || []
if (!SPINE || !SCRIPTS || !batches.length) {
  throw new Error('wf-imitaciones requiere args.spinePath, args.scriptsPath y args.batches[]')
}

// Contrato de VoC (INTERFACE §4). El criterio "hecho bien" de Fase 2 pide 2-4 EVxxxx por ad:
// eso SOLO es exigible si hay banco VoC. Sin banco, se prohíbe inventar IDs.
const VOC_BLOCK = VOC
  ? `- Banco VoC (munición literal, con IDs de evidencia): "${VOC}". LÉELO y re-ancla con lenguaje LITERAL del mercado. Cada ad debe citar 2-4 IDs EVxxxx REALES de ese archivo en "nota". NO inventes IDs.`
  : `- NO hay banco VoC en esta corrida. Re-ancla con el lenguaje del Spine. En "nota" NO cites IDs EVxxxx (no inventes): declara "sin VoC — re-anclaje derivado del Spine".`

const AD = {
  type: 'object', additionalProperties: false,
  required: ['imita_competidor', 'ad_format', 'copy', 'nota', 'nombre_creativo', 'concepto_corto', 'trigger_emocional'],
  properties: {
    imita_competidor: { type: 'string', description: 'competidor/ad cuya estructura se imita (del archivo de scripts)' },
    nombre_creativo: { type: 'string', description: 'nombre interno claro y utilizable de la pieza (para ClickUp)' },
    concepto_corto: { type: 'string', description: 'idea PUNTUAL de esta pieza, breve, para el título de subtarea' },
    trigger_emocional: { type: 'string', description: 'qué activa la respuesta emocional del avatar en ESTA pieza' },
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
${VOC_BLOCK}
- Metadata de ESTE bache (no la cambies, es tu concepto): ${JSON.stringify(b)}

QUÉ ES IMITACIÓN: te basas ~90-100% en la ESTRUCTURA de un anuncio ganador del competidor. Conservas su ARCO (patrón de hook, secuencia problema->giro->mecanismo->prueba->CTA, ritmo, formato). SOLO re-anclas el CONTENIDO al Spine: avatar, emoción, villano, mecanismo (respetando el léxico prohibido del Spine), prueba, objeción.

REGLAS:
- Cada uno de los ${M} ads imita la estructura de un COMPETIDOR DISTINTO del archivo de scripts (nómbralo en "imita_competidor").
- TRÁFICO FRÍO: cada ad abre por el mundo/dolor del avatar en los primeros 3s, NUNCA por la marca/producto/features (entra por Mirror o Hijack).
- HOOK (Three-Element Test): cada ad debe pasar (1) intensidad emocional <3s + (2) relevancia personal (habla de él, no del producto) + (3) curiosity gap específico; NO puede "parecer un anuncio" y debe entenderse sin sonido.
- Copy en el idioma/registro del mercado del Spine, tono del avatar.
- Compliance según el Spine: afirmaciones fuertes en boca de testimonio; nada de claims prohibidos.
- ad_format Video o Static según la estructura imitada.
- "nota": qué competidor imitas + qué elementos estructurales conservaste + qué re-anclaste al Spine + (si hay banco VoC) los IDs EVxxxx reales que lo sostienen; sin banco VoC, no cites IDs.

Devuelve EXACTAMENTE ${M} ads en el schema. Sin texto de proceso.`,
  { label: `bache-${i + 1}`, phase: 'Imitaciones', schema: SCHEMA }
)))

return { batches: results }
