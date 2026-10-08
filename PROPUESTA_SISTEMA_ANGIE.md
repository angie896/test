# Sistema de trabajo de Angie Vélez: propuesta v0.1

> Documento vivo. Lo armó Claude desde el punto de vista de un director de arte o productor
> senior. Es para leerlo, tachar, reordenar y volver a pedir cambios. Nada de esto está
> construido todavía: primero van las preguntas (sección 6).

---

## 0. Cómo leo tu perfil (corrígeme)

- Vienes de **animación tradicional y 2D/3D**: ilustración, color, diseño de personajes y
  fondos. Esa formación es tu mayor ventaja en IA, porque la mayoría de la gente que genera
  imágenes no sabe qué es un *color script*, un *model sheet* o un *layout*, y tú sí.
- Hoy eres **directora de arte en Dead Camera**: preproducción de arte para series 100 % IA
  (sets, personajes, props, gráficos, colorimetría, continuidad).
- Tu objetivo es **menos tiempo mecánico y más tiempo de criterio**. También quieres
  herramientas que **sean tuyas** y que te sirvan fuera de Dead Camera.

> ⚠️ El documento de contexto que adjuntaste habla de **"Lau"**, fundadora y directora
> creativa. Tú eres **Angie**, directora de arte. Antes de construir nada tengo que saber qué
> reglas de ese documento son tuyas y cuáles son de Laura o del estudio (ver pregunta 1).

---

## 1. La idea central: tu "caja de herramientas" portátil

Todo vive en **este repositorio**: textos planos (Markdown, YAML, CSV) versionados con git.
Esto te da tres cosas:

1. **Lo descargas y lo usas donde quieras**: Claude.ai (subiendo skills como .zip), Claude Code,
   Projects o incluso pegado en otro modelo.
2. **Historial**: cada cambio en un prompt o una regla queda registrado. Si una versión
   funcionaba mejor, vuelves a ella.
3. **Separación clara**: lo que es **tuyo** (tu método, tus plantillas, tu estilo) queda
   separado de lo que es **de Dead Camera** (guiones, biblias de series), que no debería vivir
   en un repo personal.

```
/
├── 00_BASE/                ← quién eres + reglas duras (se escribe UNA vez)
│   ├── perfil.md
│   └── reglas_generacion_imagen.md
├── skills/                 ← motores que se disparan con una frase
│   ├── desglose-arte/
│   ├── prompt-sets-plates/
│   ├── character-sheet/
│   ├── props-graphic-design/
│   ├── paleta-colorimetria/
│   ├── qa-continuidad/
│   └── ... (freelance, portafolio, etc.)
├── prompts/                ← biblioteca de prompts probados (con resultado y modelo)
├── plantillas/             ← biblias, briefs, cotizaciones, case studies
└── proyectos/              ← SOLO si es privado y permitido (biblias de continuidad)
```

---

## 2. Frente A: Dead Camera (pipeline de preproducción)

Ordenado por **retorno / esfuerzo**, como lo priorizaría un productor.

| # | Herramienta | Qué hace | Ahorro estimado* | Esfuerzo |
|---|---|---|---|---|
| A1 | **Base personal (system prompt)** | Tus reglas duras escritas una vez: 3/4 en sets, caras visibles, prompt completo, sheet de identidad primero, idioma. Todo lo demás la hereda. | Bajo directo, alto indirecto | 🟢 1 sesión |
| A2 | **Skill: desglose de arte** | Guion → Excel con tu formato (SETS / CHARACTERS / PROPS / GRAPHIC DESIGN). La prueba con EP42 ya funcionó. | Alto (cada episodio) | 🟢 ya hay base |
| A3 | **Biblia de continuidad (formato único)** | Una ficha por set, personaje y prop: paleta 60-30-10 en HEX, lógica de luz, vestuario por episodio, links a la imagen *FINAL* aprobada. Se puede leer como texto y también verla como página visual. | Muy alto (evita retakes) | 🟡 consolidar notas |
| A4 | **Skill: prompts de sets/plates** | Descripción o fila del desglose + ficha de la biblia → prompt maestro en inglés, 3/4, listo para copiar, con variantes (día/noche, antes/después). | Alto | 🟢 |
| A5 | **Skill: character sheet** | Identidad (frontal, cuerpo completo, fondo gris, luz neutra) → versión en escena derivada. Incluye *turnaround* y expresiones, como un model sheet de animación. | Alto | 🟢 |
| A6 | **Skill: props y graphic design** | Separa el objeto físico de su gráfica (pantallas, UIs, logos ficticios, documentos, carteles) y genera prompts y *specs* para cada uno. | Medio | 🟢 |
| A7 | **Skill: QA de continuidad** | Le pasas la imagen generada y la ficha de la biblia, y te devuelve un checklist de desvíos (paleta, vestuario, props, luz, raccord). Claude puede *ver* imágenes. | Alto | 🟡 |
| A8 | **Prompt ledger** | Registro de prompt → modelo/versión → imagen → aprobado/sí/no. Con el tiempo es tu dataset de qué funciona en cada herramienta. | Medio, crece | 🟢 CSV simple |
| A9 | **Color script por episodio** | Del desglose sale una tira de color por escena (como en animación): ves el arco emocional del capítulo antes de generar. | Medio, mucho valor creativo | 🟡 |
| A10 | **Hoja de handoff a dirección/video** | Por escena: assets aprobados, referencias bloqueadas y notas de continuidad. No es tu trabajo hacer video, pero sí entregar limpio y evitar que te pregunten diez veces. | Medio (menos interrupciones) | 🟢 |
| A11 | **Benchmark de modelos** | Mismo prompt en Nano Banana, Imagen, Flux, Midjourney, etc. Tabla comparativa por tipo de asset (sets, caras, texto en gráficos). Se actualiza cuando sale un modelo nuevo. | Decisiones más rápidas | 🟢 |

\* Son estimaciones razonadas, no medidas. Para medirlas de verdad necesito tus tiempos
actuales (pregunta 4).

**Cómo se conectan:**
`guion → [A2 desglose] → [A9 color script] → [A4/A5/A6 prompts] ← lee → [A3 biblia]`
`imagen generada → [A7 QA] → aprobada → [A3 biblia + A8 ledger] → [A10 handoff]`

---

## 3. Frente B: tu carrera, fuera de Dead Camera

Esto es lo que buscaría en un perfil senior que viene de animación y ahora dirige arte con IA.

| # | Herramienta | Para qué |
|---|---|---|
| B1 | **Generador de art bible / style guide** | Plantilla y skill para armar la biblia visual de cualquier proyecto (cliente, corto, serie). Es un entregable que puedes **vender**. |
| B2 | **Brief intake** | Cuestionario para cliente → brief estructurado (objetivo, público, tono, referentes, entregables, restricciones). Evita proyectos mal definidos. |
| B3 | **Cotizador y propuesta freelance** | Scope, entregables, rondas de revisión, derechos de uso, tiempos y precio, más una plantilla de propuesta en PDF o doc. Incluye cláusulas específicas de IA (propiedad, uso de modelos, datasets). |
| B4 | **Case study de portafolio** | De cada proyecto: reto → proceso → decisiones → resultado, en ES/EN, listo para tu web y LinkedIn. Mostrar *proceso con IA* es justo lo que hoy buscan los estudios. |
| B5 | **"Style lock" de tu ilustración** | Ficha de tu lenguaje visual (línea, color, formas, texturas, influencias) para dirigir exploraciones con IA *a partir de tu propio trabajo* y explicarle tu estilo a un equipo. |
| B6 | **Pipeline híbrido de animación** | Model sheets, BG layouts y color scripts asistidos con IA para proyectos de animación tradicional, donde tu experiencia vale más. |
| B7 | **Contenido de posicionamiento** | Posts o hilos sobre tu proceso ("de animación a dirección de arte con IA"). Material con mucha demanda y poca gente que lo explique con criterio de oficio. |
| B8 | **Radar de herramientas** | Un registro mensual de qué salió, qué probaste y qué vale la pena. Se alimenta del benchmark (A11). |

---

## 4. Roadmap propuesto (4 semanas, ajustable)

| Semana | Entregable | Por qué primero |
|---|---|---|
| 1 | A1 base personal + A2 skill desglose empaquetado | Ya hay prueba de concepto: se gana tiempo desde el episodio siguiente. |
| 2 | A3 biblia de continuidad (formato + migrar 3–5 sets) + A4 prompts de sets | Es donde más duele (sets/plates + continuidad). |
| 3 | A5 character sheets + A7 QA de continuidad | Cierra el ciclo de generar y verificar. |
| 4 | Un ítem del frente B (sugiero **B4 case study** o **B3 cotizador**) + A8 ledger | Empieza a construir lo tuyo. |

---

## 5. Reglas de cómo trabajo contigo (propuestas)

- **Preguntar antes de construir.**
- **Visual cuando sirva**: paletas como swatches, biblias como páginas HTML y tablas antes que
  párrafos.
- **Exactitud antes que exhaustividad**: todo lo inferido o inventado se marca con ⚠️. La
  continuidad que no está escrita no se rellena.
- **Prompts completos y listos para copiar.**

---

## 6. Preguntas (respóndelas en el orden que quieras)

**Identidad y rol**
1. El documento de contexto describe a "Lau" (fundadora, creator, production designer). ¿Es tu
   documento, el de Laura o uno compartido? ¿Qué reglas son **tuyas** (3/4, caras visibles,
   sheet de identidad primero…) y cuáles son del estudio?
2. ¿Qué haces tú y qué hace el resto del equipo? ¿Diriges a otros artistas o generadores? ¿A
   quién le entregas y quién te aprueba?

**Operación**
3. ¿Qué herramientas usas hoy, todas? (generación de imagen, edición como Photoshop o Krea,
   organización como Notion, Sheets, Drive, Miro o Figma). ¿Dónde vive hoy la información del
   equipo?
4. Volumen y tiempos: ¿cuántos episodios por semana, cuántos assets por episodio y cuánto te
   toma hoy cada fase (desglose, referentes, prompts, iteraciones, continuidad)?
5. Si mañana desapareciera **una** tarea de tu semana, ¿cuál sería?

**Fuera de Dead Camera**
6. ¿Haces freelance, ilustración personal, docencia o proyectos de autor? ¿Hacia dónde quieres
   crecer en 1–2 años (dirección de arte de series, estudio propio, autoría, consultoría IA)?

**Técnico y confidencialidad**
7. ¿Dónde vas a usar esto: la app de Claude (web o escritorio), Claude Code o ambas? ¿Usas
   Projects en Claude.ai?
8. Este repositorio (`angie896/test`), ¿es privado? ¿Dead Camera te permite tener guiones o
   biblias de sus series fuera de sus sistemas? Si no, separamos: tu método en este repo y los
   datos del estudio en otro lado.
9. Para cerrar el skill de desglose: ¿tienes a mano el **par de oro** (guion EP42 + tu Excel
   manual)? ¿Y el script de la prueba de concepto?
10. Sobre el desglose: ¿las 4 categorías son fijas o a veces sumas VEHICLES, VFX o
    MAKEUP? ¿Las filas de continuidad no escrita van vacías o marcadas con "⚠ definir"?
