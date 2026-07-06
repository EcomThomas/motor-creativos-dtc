export const meta = {
  name: 'wf-briefs',
  description: 'Un brief de producción por bache: ficha + scripts verbatim + storyboard escena-por-escena con paridad emocional + prompts de generación. Product-agnostic.',
  phases: [{ title: 'Briefs', detail: 'un brief completo por bache' }],
}

// -------------------------------------------------------------------
// args esperados:
// {
//   spinePath: "ruta/al/Spine.md",
//   vocPath:   "ruta/al/voc_bank.md",   // OPCIONAL: banco VoC con IDs EVxxxx
//   bundles: [ { n, slug, meta:{concept,angle,avatar,mass_desire,awareness,hypothesis}, ads:[{ad_format, copy, imita_competidor?, nota?}] }, ... ]
// }
// Devuelve { briefs: [ { n, slug, md } ] }.
// -------------------------------------------------------------------
const A = args || {}
const SPINE = A.spinePath
const VOC = A.vocPath || null
const bundles = A.bundles || []
if (!SPINE || !bundles.length) {
  throw new Error('wf-briefs requiere args.spinePath y args.bundles[]')
}
const VOC_SRC = VOC
  ? `\n- Banco VoC (lenguaje literal del mercado, con IDs EVxxxx): "${VOC}". Úsalo para que las líneas y las escenas de PRUEBA suenen a boca real del avatar; no inventes IDs.`
  : ''

phase('Briefs')
const briefs = await parallel(bundles.map((b, i) => () => agent(
`Eres director creativo + guionista de performance ads DTC (metodología Schwartz). Entregable: el BRIEF DE PRODUCCIÓN COMPLETO del BACHE #${b.n || (i + 1)}, en MARKDOWN, listo para que un editor/productor (o un motor de generación de video IA) lo ejecute sin más contexto.

FUENTES:
- Spine (frame estratégico y emocional VIGENTE, fuente de verdad del re-anclaje y del compliance): "${SPINE}"${VOC_SRC}
- Metadata y anuncios de ESTE bache (los scripts ya están escritos, van VERBATIM, NO los reescribas): ${JSON.stringify(b)}

OBJETIVO CENTRAL:
- Colocar el SCRIPT de cada ad verbatim.
- Recomendar CÓMO generar/rodar las escenas para que TRANSMITAN EMOCIONALIDAD a lo largo de TODO el video y tengan PARIDAD con el script: cada línea del guion -> una escena cuya emoción, encuadre, luz, color, ritmo y sonido REFUERZAN lo que se dice. El arco emocional sube, tiene clímax y resolución. Nada de "cabezas parlantes planas".

ESTRUCTURA EXACTA (arranca directo con "# ", sin preámbulo):

# BRIEF DE PRODUCCIÓN — BACHE #${b.n || (i + 1)}: <título del concepto>

## 1. Ficha estratégica
Concepto, ángulo, avatar núcleo, deseo masivo, awareness, hipótesis (del meta). Luego el **arco emocional troncal del bache** (la secuencia de emociones que TODO video de este bache recorre). Villano, mecanismo (cómo nombrarlo respetando el léxico prohibido del Spine), prueba, objeción a neutralizar. **Reglas de compliance visual** (qué NO mostrar/decir, según el Spine).

## 2. Producción base del bache (común a los ads)
Casting/talento (perfiles exactos según el avatar del Spine), locación, props clave, especificaciones técnicas (relación de aspecto, duración objetivo, subtítulos, música, color).

## 3. LOS ANUNCIOS
Por CADA ad:
### AD <n>.<x> — imita: <imita_competidor si aplica> · formato: <Video/Static>
**Script (verbatim):**
> (pega el copy EXACTO respetando saltos de línea)

**Storyboard con paridad emocional** — TABLA con columnas EXACTAS:
| # | Tiempo | Línea del script (fragmento) | Emoción objetivo | Dirección visual (encuadre/acción/expresión/luz/color) | B-roll / inserto | Texto en pantalla | Audio (VO/música/SFX) |
Descompón TODO el script en escenas (una fila por beat). Cada fila demuestra la paridad.

**Arco emocional (throughline):** cómo escala la emoción, dónde está el pico, cómo la resolución empuja al CTA.
**Dirección de arte, luz y color:** cómo el grading cambia con la emoción.
**Prompts de generación (IA) — OBLIGATORIO: UNO POR CADA ESCENA del storyboard, tantos prompts como FILAS tenga la tabla, sin saltarte ninguna (Escena 1, 2, 3 … hasta la última):** por cada escena, un prompt visual COMPLETO y autosuficiente (sujeto + acción/expresión + encuadre + luz + color + emoción + estilo + 9:16) listo para pegar en un generador de imagen/video.
(Si el ad es Static: entrega el LAYOUT visual jerárquico con la misma lógica de paridad emocional + prompts de generación de la imagen.)

## 4. Checklist de rodaje/entrega del bache

REGLAS: idioma/registro del mercado del Spine; la paridad emocional es el corazón (cada escena amarrada a una línea concreta y a una emoción concreta); compliance estricto según el Spine; documento COMPLETO (tablas escritas de verdad). Sin texto de proceso.`,
  { label: `brief-bache-${b.n || (i + 1)}`, phase: 'Briefs', effort: 'high' }
).then(md => ({ n: b.n || (i + 1), slug: b.slug || `bache-${i + 1}`, md }))))

return { briefs }
