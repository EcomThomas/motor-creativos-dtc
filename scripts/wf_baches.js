export const meta = {
  name: 'wf-baches',
  description: 'Genera N baches (concepto creativo + M anuncios) a partir del Spine y los scripts ganadores del competidor. Product-agnostic: todo lo específico entra por args + los archivos de input.',
  phases: [{ title: 'Baches', detail: 'un agente por foco estratégico' }],
}

// -------------------------------------------------------------------
// args esperados (Workflow({ scriptPath, args })):
// {
//   spinePath:   "ruta/al/Spine.md",             // el veredicto estratégico (etapa 1 / research)
//   scriptsPath: "ruta/al/competitor_scripts.md",// guiones de anuncios GANADORES del competidor
//   vocPath:     "ruta/al/voc_bank.md",          // OPCIONAL: banco VoC con IDs EVxxxx (etapa 1)
//   product:     "descripción corta del producto y mercado",
//   adsPerBatch: 3,                              // opcional (default 3)
//   focos: [ { title, desc }, ... ]             // UN objeto por bache = un ángulo estratégico del Spine
// }
// -------------------------------------------------------------------
const A = args || {}
const SPINE = A.spinePath
const SCRIPTS = A.scriptsPath
const VOC = A.vocPath || null
const PRODUCT = A.product || '<PRODUCTO>'
const M = A.adsPerBatch || 3
const focos = A.focos || []
if (!SPINE || !SCRIPTS || !focos.length) {
  throw new Error('wf-baches requiere args.spinePath, args.scriptsPath y args.focos[] (uno por bache)')
}

// Contrato de VoC (INTERFACE §4): si hay banco VoC, se cita con IDs reales; si NO, se prohíbe inventarlos.
const VOC_RULE = VOC
  ? `BANCO VoC (munición literal del mercado, con IDs de evidencia): "${VOC}". LÉELO. Cuando un hook/línea nazca de una cita real, referencia su ID EVxxxx en "nota". Usa SOLO IDs que existan en ese archivo; NO inventes IDs.`
  : `NO hay banco VoC en esta corrida. Los hooks son DERIVADOS DEL SPINE, no de VoC literal. NO inventes IDs EVxxxx: si no hay cita real, no cites ninguna.`

const AW = ['Unaware', 'Problem Aware', 'Solution Aware', 'Product Aware', 'Most Aware']
const AD = {
  type: 'object', additionalProperties: false,
  required: ['ad_type', 'ad_format', 'copy', 'nota'],
  properties: {
    ad_type: { type: 'string', enum: ['Imitation', 'Iteration', 'Ideation'] },
    ad_format: { type: 'string', enum: ['Video', 'Static'] },
    copy: { type: 'string' },
    nota: { type: 'string', description: 'qué imita/itera/idea + competidor de referencia o ID de VoC' },
  },
}
const PATCH = {
  type: 'object', additionalProperties: false,
  required: ['concept', 'angle', 'avatar', 'mass_desire', 'awareness', 'hypothesis', 'ads'],
  properties: {
    concept: { type: 'string', description: 'nombre pegajoso del concepto' },
    angle: { type: 'string' },
    avatar: { type: 'string' },
    mass_desire: { type: 'string', description: 'formato "Quiero..."' },
    awareness: { type: 'string', enum: AW },
    hypothesis: { type: 'string' },
    ads: { type: 'array', minItems: M, maxItems: M, items: AD },
  },
}

const CTX = `Generas UN BACHE creativo (concepto + ${M} anuncios) para: ${PRODUCT}.
LEE el Spine (estrategia VIGENTE) en "${SPINE}" y las estructuras ganadoras reales del competidor en "${SCRIPTS}".
${VOC_RULE}
El Spine es la FUENTE DE VERDAD del frame (avatar, deseo, emoción, mecanismo con su léxico prohibido, villano, prueba, objeción raíz, awareness, compliance). No inventes nada fuera del Spine.

REGLA CREATIVA (imitación/iteración/ideación son OPCIONES, no una cuota de una-de-cada):
- IMITACIÓN: toma la ESTRUCTURA/arco de un ad ganador real del archivo de scripts (nómbralo en "nota") y RE-ANCLA su contenido al frame del Spine. NO copies la emoción foránea del competidor.
- ITERACIÓN: variación de un ad propio (otro hook/apertura/prueba, mismo concepto).
- IDEACIÓN: ángulo original nacido de la VoC, sin molde externo.
Si la jugada es apoyarse en ganadores para salir a mercado, la mayoría de los ads serán IMITACIONES.
Cada ad: copy USABLE (hook + cuerpo corto), en el idioma/registro del mercado del Spine, compliance-safe según el Spine. Marca formato Video o Static.

Un BACHE alinea Ángulo + Avatar + Deseo Masivo ("Quiero...") + Nivel de Conciencia + Hipótesis de testeo. Devuelve datos estructurados.`

phase('Baches')
const patches = await parallel(focos.map((f, i) => () =>
  agent(`${CTX}\n\nGENERA ESTE BACHE:\n${f.title || ('BACHE ' + (i + 1))} — ${f.desc || ''}`,
    { label: `bache${i + 1}`, phase: 'Baches', schema: PATCH })
))
return { patches }
