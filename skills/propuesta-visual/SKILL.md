---
name: propuesta-visual
description: Toma un desglose de arte (JSON o Excel de la skill desglose-arte, o una lista de sets, personajes, props o gráficos) y genera la propuesta visual completa de cada ítem. Incluye intención narrativa, paleta 60-30-10 en HEX, lógica de luz, cámara del plate, referentes REALES verificados con fuente, búsquedas listas para Flim, ShotDeck y FilmGrab, prompts de imagen en inglés listos para copiar y una nota "por qué" para aprender production design y fotografía. Entrega un tablero HTML visual. Úsala cuando Angie diga "propuesta visual", "arma la propuesta", "dame los prompts del desglose", "referentes para…", "cómo se debería ver…" o pida el paso siguiente al desglose. Sirve para serie, corto, largo, videoclip, comercial o videojuego. No genera prompts de video.
---

# Propuesta visual (desglose → tablero con referentes y prompts)

Lee primero `references/reglas.md` (la base de Angie). Después:
`references/referentes.md` (protocolo de referentes reales: **obligatorio**),
`references/prompt_imagen.md` (anatomía de prompts) y `references/esquema_propuesta.md`.

## 0. Entrada y alcance
- Entrada ideal: el JSON del desglose. Si llega un Excel, léelo. Si llega texto, arma la lista.
- Si hay biblia de continuidad del proyecto, **léela primero**: paletas, luz y vestuario ya
  aprobados mandan sobre cualquier propuesta nueva.
- Pregunta cuántos ítems trabajar si son más de ~8. Mejor por tandas (primero SETS, luego
  CHARACTERS) que todo a medias.
- Pregunta, o toma de la biblia, el **tono del proyecto** (thriller, comedia, fantasía…) y su
  look general si ya existe.

## 1. Por cada ítem
1. **Intención narrativa** (1–3 frases): qué tiene que sentir el espectador y qué cuenta este
   espacio, objeto o personaje en ESTE momento del guion. Es la base de todo lo demás.
2. **Paleta 60-30-10** en HEX, con nombre y función de cada color. Justifica el 10 %.
3. **Luz**: fuentes motivadas, temperatura, contraste y cómo cambia entre versiones.
4. **Cámara / plate**: sets en **3/4** siempre, altura, rango de lente y foco. Personajes:
   character sheet de identidad primero.
5. **Referentes reales** (ver protocolo): 2–4 por ítem, cada uno con qué tomar de él.
6. **Búsquedas** listas para pegar en Flim, ShotDeck, FilmGrab o Pinterest (en inglés, cortas
   y visuales).
7. **Prompts** completos en inglés, listos para copiar. Uno por versión o estado. Las
   variantes se piden como edición del aprobado ("same … as the reference image").
8. **Por qué (modo mentor)**: 2–4 frases que expliquen el principio de production design o
   fotografía detrás de la decisión, para que Angie aprenda el oficio.
9. **Flags ⚠**: todo lo asumido, inferido o propuesto que no esté en el guion.

## 2. Generar el tablero
Escribe el JSON (`references/esquema_propuesta.md`) y corre:

```bash
python scripts/build_board.py propuesta.json PROPUESTA_<UNIDAD>.html --desglose desglose.json
```

La página tiene pestañas (desglose y propuesta visual), los pendientes ⚠ arriba, franjas de
paleta, links a los referentes, botones para copiar búsquedas y prompts, y modo claro/oscuro.

**Angie quiere VER la página, no el código.** Siempre muéstrasela renderizada:
- En la app de Claude: publícala como **Artifact** (página visual) o muéstrala con la vista
  previa de HTML. Nunca le entregues solo el archivo `.html` ni el JSON para que los abra.
- Si solo se puede entregar un archivo, genéralo con `--standalone` y dile que lo abra con
  doble clic en el navegador.
- El JSON es interno (sirve para iterar): no se lo muestres a menos que lo pida.

## 2b. Guardar los prompts en la hoja del proyecto (siempre que exista)
Cada prompt va a la columna PROMPT de su fila en la hoja maestra (skill `hoja-proyecto`). Las
variantes van en filas `.2`, `.3`, y cada versión queda en HISTORIAL PROMPTS. Cuando Angie
pida un ajuste ("SET-003 más cálido"), se ajusta **en la hoja**, no solo en el chat.

## 3. Entregar
- La página visual renderizada (ver arriba). Guarda el JSON por tu lado para iterar.
- En el chat: un resumen corto y la lista de ⚠ pendientes. No repitas los prompts en el chat:
  ya están en el tablero.
- Proponer el siguiente paso: cuando Angie apruebe imágenes FINAL, sus paletas y su luz se
  guardan en la biblia de continuidad.

## Reglas que no se rompen
- **Nunca inventar referentes.** Si no se verificó, va `"verified": false` y el tablero lo
  marca. Más vale un referente verificado que cuatro inventados.
- Sets en 3/4. Caras de extras visibles y nítidas. Prompt completo.
- No escribir prompts de video ni shotlists.
