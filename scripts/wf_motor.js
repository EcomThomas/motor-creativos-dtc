export const meta = {
  name: 'wf-motor',
  description: 'ORQUESTADOR end-to-end del Motor de Creativos: enhebra Fase 1 (N baches) -> Fase 2 (M imitaciones re-ancladas por bache) -> Fase 4 (brief de produccion por bache) en una sola corrida, en memoria. VoC-wired. Devuelve el bundle que persist.py escribe a disco. Product-agnostic.',
  phases: [
    { title: 'Baches', detail: 'concepto+angulo+hipotesis, un agente por foco' },
    { title: 'Imitaciones', detail: 'M imitaciones re-ancladas, un agente por bache' },
    { title: 'Briefs', detail: 'brief de produccion con paridad emocional, uno por bache' },
  ],
}

// -------------------------------------------------------------------
// Orquestador. Corre en el sandbox de Workflow (SIN filesystem): genera y DEVUELVE datos.
// La persistencia (snapshot, escritura de baches/briefs/roadmap) la hace el harness Python
// (intake.py antes, persist.py despues). Ver RUNBOOK.md.
//
// args esperados (Workflow({ scriptPath: 'scripts/wf_motor.js', args })):
// {
//   spinePath:   "casos/<prod>/input/spine.snapshot.md|json",   // OBLIGATORIO (del snapshot de intake.py)
//   scriptsPath: "casos/<prod>/input/scripts.snapshot.md",      // OBLIGATORIO para imitar
//   vocPath:     "casos/<prod>/input/voc.snapshot.md" | null,   // OPCIONAL: banco VoC con IDs EVxxxx
//   product:     "Suplemento Hepatico MX (es-MX, Meta)",        // descripcion corta
//   adsPerBatch: 3,                                             // M (default 3)
//   focos: [ { key, title, desc }, ... ]                        // N angulos; si se omite, usa los 5 base
// }
// Devuelve el BUNDLE:
// { producto, slug, snapshot:{spinePath,scriptsPath,vocPath},
//   batches:[ {n,slug,concept,angle,avatar,mass_desire,awareness,hypothesis, ads:[...]} ],
//   briefs:[ {n,slug,md} ] }
// -------------------------------------------------------------------
const A = args || {}
const SPINE = A.spinePath
const SCRIPTS = A.scriptsPath
const VOC = A.vocPath || null
const PRODUCT = A.product || '<PRODUCTO>'
const M = A.adsPerBatch || 3

// Set base de 5 angulos (espejo de config.json > angulos_base; el sandbox no puede leer el archivo).
const FOCOS_BASE = [
  { key: 'nucleo', title: 'Nucleo', desc: 'Abre por el deseo #1 y la emocion troncal, directo sobre el avatar nucleo. El angulo recto.' },
  { key: 'objecion', title: 'Objecion', desc: 'Desarma la objecion raiz (seguridad, precio, esfuerzo, credibilidad). Convierte el bloqueo de compra en el gancho.' },
  { key: 'villano', title: 'Villano', desc: 'Nombra y ataca al villano del Spine (incluida la anti-solucion/DIY). El producto es el reemplazo limpio.' },
  { key: 'prueba', title: 'Prueba', desc: 'Testimonio/demostracion con la prueba nativa del Spine (metrica, antes/despues). Suele ser Product/Most Aware.' },
  { key: 'cabeza_playa', title: 'Cabeza de playa', desc: 'Sub-avatar o sintoma de entrada mas barato de captar que puentea al deseo nucleo. Hipotesis marcada A VALIDAR.' },
]
const focos = (A.focos && A.focos.length) ? A.focos : FOCOS_BASE

if (!SPINE || !SCRIPTS) {
  throw new Error('wf-motor requiere args.spinePath y args.scriptsPath (rutas del snapshot de intake.py)')
}

const slugify = (s) => String(s || '')
  .normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/[^a-zA-Z0-9]+/g, '-').replace(/^-+|-+$/g, '').toLowerCase() || 'bache'

const AW = ['Unaware', 'Problem Aware', 'Solution Aware', 'Product Aware', 'Most Aware']

// --- Contrato de VoC (INTERFACE §4) ---
const VOC_RULE = VOC
  ? `Banco VoC (municion literal del mercado, con IDs de evidencia): "${VOC}". LEELO. Re-ancla con lenguaje LITERAL del mercado y cita IDs EVxxxx REALES de ese archivo. NO inventes IDs.`
  : `NO hay banco VoC en esta corrida: re-ancla con el lenguaje del Spine. NO inventes IDs EVxxxx (si no hay cita real, no cites ninguna).`

// --- Schemas ---
const META_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['concept', 'angle', 'avatar', 'sub_avatar', 'mass_desire', 'awareness', 'hypothesis', 'valence', 'emociones_83', 'trigger_batch'],
  properties: {
    concept: { type: 'string', description: 'nombre pegajoso del concepto' },
    angle: { type: 'string' },
    avatar: { type: 'string', description: 'nucleo o sub-avatar' },
    sub_avatar: { type: 'string', description: 'segmento especifico dentro del avatar (edad, situacion, dolor puntual)' },
    mass_desire: { type: 'string', description: 'formato "Quiero..."' },
    awareness: { type: 'string', enum: AW },
    hypothesis: { type: 'string', description: 'falsable; si es cabeza de playa, marcar A VALIDAR' },
    valence: { type: 'string', enum: ['Positiva', 'Negativa', 'Mixta'], description: 'valence emocional dominante del batch, anclada en la emocion troncal del Spine' },
    emociones_83: { type: 'array', minItems: 1, maxItems: 3, items: { type: 'string' }, description: 'las 1-3 emociones que cubren ~83% del batch (del Spine + el copy), no inventadas' },
    trigger_batch: { type: 'string', description: 'trigger emocional troncal del batch (se hereda a las piezas sin trigger propio)' },
  },
}
const AD_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['imita_competidor', 'ad_format', 'copy', 'nota', 'nombre_creativo', 'concepto_corto', 'trigger_emocional'],
  properties: {
    imita_competidor: { type: 'string', description: 'competidor/ad cuya estructura se imita (del archivo de scripts)' },
    ad_format: { type: 'string', enum: ['Video', 'Static'] },
    copy: { type: 'string', description: 'guion/copy completo, listo para producir, en el registro del mercado del Spine' },
    nota: { type: 'string', description: 'que estructura se conservo + que se re-anclo + IDs EVxxxx (si hay VoC)' },
    nombre_creativo: { type: 'string', description: 'nombre interno claro y utilizable de la pieza (para ClickUp)' },
    concepto_corto: { type: 'string', description: 'concepto puntual (no estrategico) de ESTA pieza, breve, para el titulo de subtarea' },
    trigger_emocional: { type: 'string', description: 'que activa la respuesta emocional del avatar en ESTA pieza' },
  },
}
const ADS_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['ads'],
  properties: { ads: { type: 'array', minItems: M, maxItems: M, items: AD_SCHEMA } },
}

const FRAME = `Motor de Creativos DTC (metodologia Schwartz) para: ${PRODUCT}.
El Spine es la FUENTE DE VERDAD del frame (avatar, deseo, emocion troncal, mecanismo con su lexico prohibido, villano, prueba, objecion raiz, awareness, compliance). Spine: "${SPINE}". Estructuras ganadoras del competidor: "${SCRIPTS}".
${VOC_RULE}
No inventes nada fuera del Spine.
TRAFICO FRIO: el avatar NO conoce la marca ni busca comprar; esta scrolleando. Los primeros 3s son sobre EL (su mundo/dolor/interes), NUNCA sobre la marca/producto/features. Entra por Mirror (reflejar su mundo interno) o Hijack (secuestrar un interes que ya tiene).
HOOK (Three-Element Test): cada hook = intensidad emocional <3s + relevancia personal (habla de el, no del producto) + curiosity gap especifico. Si "parece un anuncio", esta mal; entendible sin sonido.`

// Pipeline por foco: cada angulo recorre baches -> imitaciones -> brief SIN barrera entre etapas.
const results = await pipeline(
  focos,

  // Fase 1 — metadata del bache (concepto/angulo/avatar/deseo/awareness/hipotesis)
  (foco, _orig, i) => agent(
    `${FRAME}

GENERA LA METADATA DE UN BACHE: concepto + angulo + avatar + sub_avatar + deseo masivo "Quiero..." + nivel de awareness + hipotesis falsable + valence dominante + emociones_83 + trigger_batch.
ANGULO ESTRATEGICO DE ESTE BACHE:
${foco.title} — ${foco.desc}
El deseo, el avatar y el sub_avatar (segmento especifico: edad/situacion/dolor puntual) salen del Spine (o de un sub-avatar legitimo si el angulo es cabeza de playa).
CAMPOS EMOCIONALES (anclalos en la EMOCION TRONCAL del Spine, NO los inventes): valence = Positiva/Negativa/Mixta segun el registro dominante; emociones_83 = las 1-3 emociones que recorren ~83% del batch; trigger_batch = el detonante emocional troncal del batch.
Devuelve SOLO la metadata (los anuncios se generan aparte). Sin texto de proceso.`,
    { label: `bache${i + 1}:${foco.key || foco.title}`, phase: 'Baches', schema: META_SCHEMA }
  ).then(m => ({ n: i + 1, slug: slugify(foco.key || m.concept), foco, meta: m })),

  // Fase 2 — M imitaciones re-ancladas (cada una imita un competidor DISTINTO)
  (acc, _foco, i) => agent(
    `${FRAME}

Genera ${M} ANUNCIOS DE IMITACION para ESTE bache (no cambies su metadata, es tu concepto):
${JSON.stringify(acc.meta)}

QUE ES IMITACION: te basas ~90-100% en la ESTRUCTURA de un anuncio ganador del competidor. Conservas su ARCO (patron de hook, secuencia problema->giro->mecanismo->prueba->CTA, ritmo, formato). SOLO re-anclas el CONTENIDO al Spine: avatar, emocion, villano, mecanismo (respetando el lexico prohibido), prueba, objecion.
REGLAS:
- Cada uno de los ${M} ads imita la estructura de un COMPETIDOR DISTINTO del archivo de scripts (nombralo en "imita_competidor").
- Copy USABLE tal cual (hook + cuerpo corto), en el idioma/registro del mercado del Spine.
- Compliance segun el Spine: afirmaciones fuertes en boca de testimonio; nada del lexico prohibido; en categorias sensibles el mecanismo va como creencia/testimonio, no como claim clinico.
- ad_format Video o Static segun la estructura imitada.
- "nota": competidor imitado + elementos estructurales conservados + que se re-anclo + IDs EVxxxx (solo si hay banco VoC).
- Por CADA pieza (para el montaje en ClickUp): nombre_creativo (nombre interno claro y utilizable), concepto_corto (la idea PUNTUAL de esa pieza, breve, no estrategica) y trigger_emocional (que activa la respuesta emocional del avatar en ESA pieza; si no difiere, deja el trigger troncal del batch). NO inventes: anclalos en el copy y en la emocion del Spine.
Devuelve EXACTAMENTE ${M} ads en el schema. Sin texto de proceso.`,
    { label: `ads-${i + 1}`, phase: 'Imitaciones', schema: ADS_SCHEMA }
  ).then(r => ({ ...acc, ads: r.ads })),

  // Fase 4 — brief de produccion con paridad emocional (una fila por beat del guion)
  (acc, _foco, i) => agent(
    `Eres director creativo + guionista de performance ads DTC (Schwartz). Entregable: el BRIEF DE PRODUCCION COMPLETO del BACHE #${acc.n}, en MARKDOWN, listo para que un editor/productor (o un motor de generacion de video IA) lo ejecute sin mas contexto.

FUENTES:
- Spine (frame estrategico y emocional VIGENTE, fuente del re-anclaje y del compliance): "${SPINE}"${VOC ? `\n- Banco VoC (lenguaje literal del mercado, IDs EVxxxx): "${VOC}". Usalo para que las lineas y escenas de PRUEBA suenen a boca real del avatar; no inventes IDs.` : ''}
- Metadata y anuncios de ESTE bache (los scripts van VERBATIM, NO los reescribas): ${JSON.stringify({ n: acc.n, ...acc.meta, ads: acc.ads })}

OBJETIVO: colocar el SCRIPT de cada ad verbatim y recomendar COMO generar/rodar cada escena para que TRANSMITA emocionalidad a lo largo de TODO el video, con PARIDAD: cada linea del guion -> una escena cuya emocion, encuadre, luz, color, ritmo y sonido REFUERZAN lo que se dice. El arco emocional sube, tiene climax y resolucion. Nada de "cabezas parlantes planas".

ESTRUCTURA EXACTA (arranca directo con "# ", sin preambulo):

# BRIEF DE PRODUCCION — BACHE #${acc.n}: <titulo del concepto>

## 1. Ficha estrategica
Concepto, angulo, avatar, deseo masivo, awareness, hipotesis. Luego el **arco emocional troncal del bache**. Villano, mecanismo (como nombrarlo respetando el lexico prohibido del Spine), prueba, objecion a neutralizar. **Reglas de compliance visual** (que NO mostrar/decir, segun el Spine).

## 2. Produccion base del bache (comun a los ads)
Casting/talento (perfiles segun el avatar del Spine), locacion, props, especificaciones (relacion de aspecto, duracion objetivo, subtitulos, musica, color).

## 3. LOS ANUNCIOS
Por CADA ad:
### AD ${acc.n}.<x> — imita: <imita_competidor> · formato: <Video/Static>
**Script (verbatim):**
> (pega el copy EXACTO respetando saltos de linea)

**Storyboard con paridad emocional** — TABLA con columnas EXACTAS:
| # | Tiempo | Linea del script (fragmento) | Emocion objetivo | Direccion visual (encuadre/accion/expresion/luz/color) | B-roll / inserto | Texto en pantalla | Audio (VO/musica/SFX) |
Descompon TODO el script en escenas (una fila por beat).

**Arco emocional (throughline):** como escala la emocion, donde esta el pico, como la resolucion empuja al CTA.
**Prompts de generacion (IA):** 2-3 escenas clave, prompt visual listo para pegar en un generador de imagen/video.
(Si el ad es Static: entrega el LAYOUT visual jerarquico con la misma logica de paridad + prompts de generacion.)

## 4. Checklist de rodaje/entrega del bache

REGLAS: idioma/registro del mercado del Spine; la paridad emocional es el corazon; compliance estricto segun el Spine; documento COMPLETO (tablas escritas de verdad). Sin texto de proceso.`,
    { label: `brief-${i + 1}`, phase: 'Briefs', effort: 'high' }
  ).then(md => ({ ...acc, brief_md: md })),
)

const ok = results.filter(Boolean)
const batches = ok.map(r => ({
  n: r.n, slug: r.slug,
  concept: r.meta.concept, angle: r.meta.angle, avatar: r.meta.avatar, sub_avatar: r.meta.sub_avatar,
  mass_desire: r.meta.mass_desire, awareness: r.meta.awareness, hypothesis: r.meta.hypothesis,
  valence: r.meta.valence, emociones_83: r.meta.emociones_83, trigger_batch: r.meta.trigger_batch,
  ads: r.ads || [],
}))
const briefs = ok.map(r => ({ n: r.n, slug: r.slug, md: r.brief_md || '' }))

log(`wf-motor: ${batches.length} baches, ${batches.reduce((a, b) => a + b.ads.length, 0)} ads, ${briefs.length} briefs.`)

return {
  producto: PRODUCT,
  slug: slugify(PRODUCT),
  snapshot: { spinePath: SPINE, scriptsPath: SCRIPTS, vocPath: VOC },
  batches,
  briefs,
}
