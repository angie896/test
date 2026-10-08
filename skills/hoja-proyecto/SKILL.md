---
name: hoja-proyecto
description: Mantiene la hoja maestra de arte de un proyecto (Google Sheets o Excel) como el registro permanente de todo, para que nada se quede solo en un chat. Incluye el desglose general (una fila por set, personaje, prop o gráfica, con los episodios o secuencias donde aparece), el prompt vigente de cada cosa listo para copiar y el historial de todas las versiones de prompts. Úsala siempre que Angie trabaje un proyecto que tenga hoja, cuando diga "agrégalo a la hoja", "actualiza el desglose general", "ajusta el prompt de SET-003", "qué prompt usé para…", "crea la hoja del proyecto", o cuando las skills desglose-arte o propuesta-visual produzcan algo nuevo. Sirve para cualquier proyecto (serie, corto, largo, videoclip, comercial).
---

# Hoja maestra del proyecto

Lee `references/reglas.md` (la base de Angie).

**Idea central:** la hoja es la memoria del proyecto. Todo lo que se desglosa, propone o
ajusta en un chat **termina escrito en la hoja**. El chat es desechable; la hoja no.

## Estructura (no cambiarla sin preguntar)

**Pestaña `DESGLOSE GENERAL`**, una fila por cosa del proyecto:

| Col | Encabezado | Quién la llena |
|---|---|---|
| A | ID | Claude. Fijo para siempre: `SET-001`, `CHR-004`, `PRP-002`, `GD-003` (`VEH`, `MUP`, `VFX` si aplican). Variantes: `SET-001.2`, `.3`… |
| B | CATEGORY | Claude |
| C | ITEM | Claude (inglés) |
| D | UNIDADES | Claude: dónde aparece (`EP42, EP43` / `SEQ 03` / `CORTO`) |
| E | ESC. | Claude: `EP42: 169, 170`, una línea por unidad |
| F | DESCRIPTION | Claude (español). ⚠ en naranja = definir |
| G | REFERENCE | **Angie** (imágenes). Claude NUNCA escribe aquí |
| H | FINAL | **Angie** (imágenes). Claude NUNCA escribe aquí |
| I | STATUS | Claude pone `TO DO` al crear y después solo lo cambia si Angie lo pide |
| J | PROMPT | Claude: el prompt vigente, completo y listo para copiar |
| K | VERSIÓN | Claude: `v1`, `v2`… |
| L | HERRAMIENTA | Claude (Nano Banana Pro, Imagen…) |
| M | NOTAS / AJUSTES | Ambos. Claude solo agrega texto, nunca borra lo de Angie |

**Pestaña `HISTORIAL PROMPTS`**: `FECHA | ID | ITEM | VERSIÓN | PROMPT | QUÉ CAMBIÓ | ¿FUNCIONÓ?`.
Cada prompt que alguna vez existió queda aquí. `¿FUNCIONÓ?` la marca Angie.

**Pestaña `LÉEME`**: instrucciones para humanos.

## Reglas de escritura
1. **Un ítem = una fila para todo el proyecto.** Si el desglose de un episodio nuevo trae algo
   que ya existe (misma CATEGORY + mismo ITEM), NO se duplica: se agrega la unidad en
   UNIDADES, sus escenas en ESC. y lo nuevo de la descripción como línea `[EP43] …`.
   Si el nombre es parecido pero no igual ("Sofia's office" vs "Sofia office"), **pregunta**.
2. **Un prompt por fila.** Si un ítem tiene variantes (set día/noche, versión LATER, pantallas
   1–4), cada variante va en una fila propia debajo, con ID de sufijo (`SET-001.2`).
3. **Ajustar un prompt = primero historial, después la celda.** Copia el prompt actual al
   HISTORIAL (si no está), escribe el nuevo en PROMPT, sube VERSIÓN y registra en el
   HISTORIAL la nueva versión con "qué cambió" en una frase.
4. **Volver a un prompt viejo**: búscalo en HISTORIAL por ID y versión. Si Angie quiere
   restaurarlo, vuelve a PROMPT como versión nueva ("restaurado desde v2").
5. **Antes de escribir**, dile a Angie en una línea qué va a cambiar ("3 ítems nuevos, 2
   actualizados, 1 prompt ajustado en SET-003"). Después confirma qué quedó escrito.
6. Nunca borrar filas ni columnas. Lo descartado se marca `DESCARTADO` en STATUS.

## Con el conector de Google Sheets (lo ideal)
Herramientas del conector: `get_spreadsheet`, `get_values`, `update_values`,
`insert_dimension`, `update_spreadsheet`.

1. **Ubicar la hoja**: Angie pega el link una vez. Recomiéndale crear un **Proyecto en
   Claude** por cada proyecto y guardar el link en sus instrucciones: así todos los chats de
   ese proyecto saben cuál es la hoja.
2. **Leer siempre antes de escribir**: `get_values` de `DESGLOSE GENERAL!A1:M` y arma el
   mapa ID → fila y (CATEGORY, ITEM) → fila. Ella puede haber editado cosas a mano: lo que
   está en la hoja manda sobre lo que recuerdes del chat.
3. **Ítems nuevos**: escríbelos en las primeras filas vacías con `update_values`.
   **Variantes**: `insert_dimension` para abrir una fila debajo del ítem padre.
4. **Ajuste de prompt**: lee la fila → agrega al final de `HISTORIAL PROMPTS` con
   `update_values` → actualiza PROMPT y VERSIÓN.
5. **Hoja nueva**: lo más fácil es que Angie suba `assets/PLANTILLA_DESGLOSE_GENERAL.xlsx` a
   Google Drive y la abra con Google Sheets (*Archivo → Guardar como Hoja de cálculo de
   Google*). Después te pasa el link.

## Sin conector (archivo .xlsx)
Usa `scripts/hoja_proyecto.py`:
```bash
python scripts/hoja_proyecto.py crear  PROYECTO.xlsx --titulo "Nombre" --tipo serie
python scripts/hoja_proyecto.py agregar PROYECTO.xlsx desglose.json --propuesta propuesta.json
python scripts/hoja_proyecto.py prompt PROYECTO.xlsx SET-003 "nuevo prompt…" --cambio "más cálido"
```
Pídele a Angie que suba su versión más reciente de la hoja antes de cada cambio y entrégale
la versión actualizada. Avísale que **con el conector no tendría que subir ni bajar nada**.

## Entregar
- Confirma en el chat qué filas cambiaron (por ID). No pegues la hoja en el chat.
- Si cambió algo visual (propuesta nueva), muestra también la página visual de
  `propuesta-visual`.
