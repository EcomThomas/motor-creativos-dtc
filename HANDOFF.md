# HANDOFF — Motor de Creativos DTC (Etapa 2)

**Documento de traspaso para la próxima sesión de refinamiento.**
Léelo completo antes de tocar nada. Al final tienes el backlog accionable, las preguntas abiertas de diseño y la nota operativa de deploy.

---

## 1. Por qué existe este repo

Este repo nació de **separar la etapa de creativos del Motor de Research**. Antes, "research" y "creativos" vivían mezclados en el mismo sistema; eso los acoplaba y hacía imposible iterar uno sin romper el otro.

La decisión de diseño es tratar el pipeline DTC como **4 etapas desacopladas**, cada una con su propio contrato de entrada/salida:

```
Research  ->  CREATIVOS (este repo)  ->  Media Buying / Test  ->  Feedback
   ^                                                                  |
   +------------------------------------------------------------------+
```

Beneficios de la separación:

- **Replicabilidad:** el Motor de Creativos es una máquina que funciona para CUALQUIER producto DTC (ads Meta/TikTok, metodología Eugene Schwartz). No está atado a ningún producto; los específicos entran por el INPUT.
- **Iteración independiente:** puedes refinar el método de creativos sin tocar el motor de research.
- **Contrato explícito:** la etapa 1 entrega un **Spine** (veredicto estratégico) + **scripts ganadores del competidor**; este repo los consume y produce baches de anuncios listos para producción.
- **Feedback loop limpio:** la etapa 3 (media buying) devuelve señales de performance que reabren la etapa 1, sin ambigüedad sobre quién es dueño de qué.

**Regla de oro:** este repo NUNCA hardcodea un producto. Todo lo específico (avatar, deseo, villano, mecanismo, compliance) llega vía el Spine y la plantilla de input.

---

## 2. Qué YA está montado

El scaffold base está completo y funcional como método (aún no del todo parametrizado como código — ver backlog).

### 2.1 Scaffold del repo
- Estructura de carpetas para docs de método, workflows, specs e input.
- README con el canon del motor y el vocabulario canónico (bache, imitación/iteración/ideación, paridad emocional, compliance).

### 2.2 Los 6 docs de método
Los documentos que definen CÓMO se generan los creativos, product-agnostic:

| # | Doc | Qué define |
|---|-----|-----------|
| 1 | Concepto de **bache** | Schema del bache: concept, angle, avatar, mass_desire, awareness, hypothesis, ads[] |
| 2 | **Clasificación de anuncios** | Imitación / Iteración / Ideación — cuándo usar cada una (imitación = mayoría cuando te apoyas en ganadores) |
| 3 | **Paridad emocional** | Cada línea del guion tiene escena que refuerza emoción, luz, color, ritmo, sonido; arco con clímax y resolución |
| 4 | **Compliance** | Marco general: sin claims absolutos, afirmaciones fuertes en boca de testimonio, disclaimers/overlays |
| 5 | **Re-anclaje al Spine** | Cómo conservar el ARCO del ganador y cambiar solo el CONTENIDO al Spine |
| 6 | **Brief de producción** | Script + storyboard con paridad emocional + prompts de generación por bache |

### 2.3 Spec
- Definición del contrato de INPUT (Spine + scripts ganadores + VoC opcional) y del OUTPUT (N baches, M ads/bache, volcado a Creative Roadmap, brief por bache).
- Schemas de bache y de ad (imitación/iteración/ideación).

### 2.4 Interfaz
- Definición de cómo se invoca el motor y qué consume/produce cada módulo.

### 2.5 Los 3 workflows generalizados
Los workflows del método, ya escritos de forma product-agnostic (pendiente parametrizarlos como scripts que reciban paths por argumento — ver backlog):

1. **Generar baches** — del Spine + scripts ganadores a N conceptos con hipótesis.
2. **Expandir bache a ads** — de un bache a M anuncios (mayoría imitaciones re-ancladas).
3. **Producir brief** — de un bache a script + storyboard + prompts de generación.

### 2.6 Plantilla de input
- Plantilla vacía para el Spine + slot para pegar scripts ganadores + slot para VoC opcional. Los marcadores (`<PRODUCTO>`, `<AVATAR>`, `<DESEO>`, `<VILLANO>`, `<MECANISMO>`, `<PRUEBA>`, `<OBJECION>`) se rellenan por producto.

---

## 3. Backlog de refinamiento (accionable)

Ordenado por prioridad. Cada tarea es concreta y cerrable.

### P0 — Parametrización (lo que desbloquea todo lo demás)

- [ ] **Parametrizar los 3 workflows por argumento.** Que cada workflow reciba:
  - `--spine <path>` — ruta al Spine (JSON/MD) que entrega la etapa 1.
  - `--winners <path>` — ruta al archivo de scripts ganadores del competidor.
  - `--voc <path>` (opcional) — ruta al banco VoC con IDs de evidencia (EVxxxx).
  - `--out <path>` — dónde escribir baches/briefs/roadmap.
  Hoy los workflows asumen el input; deben dejar de asumirlo.

- [ ] **Definir defaults del motor** en un solo lugar (config):
  - `N_BACHES` por defecto (propuesta: 3–5).
  - `M_ADS` por bache (canon actual: **3**).
  - Mezcla por defecto de clasificación (canon: mayoría imitación; NO forzar una-de-cada).
  - Awareness default si el Spine no lo especifica.

### P1 — Generalización del método

- [ ] **Generalizar el compliance por categoría de producto.** Hoy el compliance es un marco general. Convertirlo en una tabla por categoría (salud/suplementos, finanzas, belleza, gadgets, etc.) donde el Spine seleccione la categoría y se cargue el léxico prohibido + reglas específicas. El caso de referencia (suplemento hepático) sirve de primer ejemplo de la categoría salud.

- [ ] **Builder de la hoja "Creative Roadmap" (Excel)** que respete validaciones:
  - Columnas canónicas (bache, concepto, ángulo, avatar, deseo, awareness, hipótesis, ad_type, ad_format, copy, nota, estado).
  - Validaciones/enums en las columnas categóricas (awareness, ad_type ∈ {Imitación, Iteración, Ideación}, ad_format ∈ {Video, Static}).
  - Que sea idempotente: re-correr no duplica filas.

### P2 — Conexión al resto del pipeline

- [ ] **Conectar la SALIDA a la etapa 3 (media buying / test).** Definir el contrato de handoff: qué campos de cada ad necesita el media buyer (naming convention, hipótesis, mapping bache->campaña/adset).

- [ ] **Cerrar el loop de feedback.** Definir cómo vuelven las señales de performance (ROAS, CTR, hook rate, etc.) y cómo re-alimentan la etapa 1 (research) para el siguiente ciclo. Mapear qué métrica valida/mata qué hipótesis de bache.

### P3 — Calidad y ejemplos

- [ ] **Añadir 1–2 casos de ejemplo end-to-end.** Usar el caso de referencia (suplemento hepático MX) como primer ejemplo completo: Spine -> baches -> ads -> brief. Añadir un segundo caso de otra categoría para probar que el motor es agnóstico.

- [ ] **Escribir tests / QA del método.** Checklist verificable por bache y por ad:
  - ¿Cada bache tiene los 7 campos del schema?
  - ¿Cada ad de imitación declara `imita_competidor` y conserva el arco del ganador?
  - ¿Cada línea del brief tiene paridad emocional (escena que refuerza)?
  - ¿El copy pasa el compliance de su categoría (sin claims absolutos, afirmaciones fuertes en testimonio)?
  - ¿El re-anclaje cambió SOLO el contenido, no el arco?

---

## 4. Preguntas abiertas de diseño

- **¿Cuántos baches por defecto?** El canon fija 3 ads/bache, pero N de baches queda abierto. ¿Lo fija el motor, el Spine, o el presupuesto de test de la etapa 3?
- **¿Formato canónico del Spine?** ¿JSON estricto (mejor para parsear) o Markdown (mejor para leer/editar a mano)? Afecta cómo parametrizamos los workflows.
- **¿Quién es dueño de la naming convention** de campañas/adsets? ¿La define este repo (etapa 2) o la etapa 3? Impacta el contrato de handoff.
- **Mezcla de clasificación:** el canon dice "mayoría imitación", pero ¿cuál es el umbral? ¿100% imitación es válido para un bache? ¿Conviene forzar al menos 1 iteración/ideación por concepto para no depender solo del competidor?
- **VoC obligatorio u opcional:** hoy es opcional. ¿Debería ser obligatorio para baches de ideación (que nacen del insight de VoC)?
- **Compliance:** ¿tabla estática por categoría, o el Spine trae su propio léxico prohibido ya resuelto desde la etapa 1?
- **Versionado de baches:** cuando el feedback mata una hipótesis, ¿se versiona el bache (v2) o se crea uno nuevo? Impacta la trazabilidad del loop.

---

## 5. Nota operativa (deploy)

**Crear el repo remoto y hacer `push` está BLOQUEADO en auto-mode** (el clasificador de exfiltración detiene la operación). Por lo tanto:

- El **push lo corre el usuario** manualmente, o
- Se habilita vía **regla de permiso** explícita en la config del harness.

El resto del trabajo (editar docs, workflows, specs, plantillas, builders locales) NO está bloqueado y puede hacerse en auto-mode. Solo la creación/push del remoto requiere acción del usuario.

---

## 6. Estado y fecha

- **Estado:** scaffold + 6 docs de método + spec + interfaz + 3 workflows generalizados + plantilla de input = **montado**. Falta la parametrización (P0) y las conexiones al resto del pipeline (P2).
- **Fecha de este handoff:** 2026-07-05.
- **Próximo paso recomendado:** arrancar por P0 (parametrizar los 3 workflows por argumento y fijar defaults), porque desbloquea todo el backlog posterior.
