---
name: hoja-proyecto
description: Mantiene la hoja de arte de cada proyecto en Google Sheets como el registro permanente de todo, para que nada se quede solo en un chat. Incluye el desglose general (una fila por set, personaje, prop o gráfica, con dónde aparece), el estado de cada cosa, el prompt vigente listo para copiar y el historial de prompts anteriores. Úsala al empezar cualquier trabajo de un proyecto, cuando Angie diga "agrégalo a la hoja", "actualiza el desglose", "ajusta el prompt de…", "qué prompt usé para…", o cuando las skills desglose-arte o propuesta-visual produzcan algo nuevo. Sirve para cualquier proyecto (serie, corto, largo, videoclip, comercial).
---

# Hoja de arte del proyecto

Lee `references/reglas.md` (la base de Angie).

**Idea central:** la hoja vive en la nube (Google Drive de Angie) y es la memoria del
proyecto. Todo lo que se desglosa, propone o ajusta en un chat **termina escrito en la hoja**.

## Paso 1, siempre: preguntar por la hoja
Antes de desglosar, proponer o ajustar nada de un proyecto, pregunta:

> ¿Ya tienes la hoja de este proyecto? Si sí, pásame el link.
> Si no, créala en tu Google Drive (*Nuevo → Hojas de cálculo de Google*), ponle el nombre del
> proyecto y pásame el link. Yo le armo las columnas.

- **Claude no crea la hoja.** La crea Angie en su Drive, así es suya y queda en su nube.
- Si el link ya está en las instrucciones del Proyecto de Claude o en la conversación, úsalo
  sin volver a preguntar (solo confirma el nombre de la hoja).
- Recomiéndale una vez: crear un **Proyecto en Claude** por cada proyecto suyo y pegar el link
  en sus instrucciones, para no tener que pasarlo en cada chat.
- Si el conector de Google Sheets no está conectado, explícale cómo conectarlo
  (*Configuración → Conectores → Google Sheets*) y espera. Sin conector, usa el modo archivo
  (abajo).

## Paso 2: preparar la hoja (solo si está vacía)
Si la hoja está vacía, créale esta estructura. Si ya tiene contenido, **léela y respétala**:
no muevas ni renombres columnas de Angie. Si sus columnas son distintas, pregúntale cómo
mapearlas.

**Pestaña `DESGLOSE GENERAL`**:

| Col | Encabezado | Quién la llena |
|---|---|---|
| A | CATEGORY | Claude: SETS, CHARACTERS, PROPS, GRAPHIC DESIGN (y VEHICLES, MAKEUP / SFX, VFX si aplican) |
| B | ITEM | Claude (inglés) |
| C | APARECE EN | Claude: unidad + escenas, una línea por unidad: `EP42: esc. 169, 170`. En un largo: `SEQ 03: esc. 12`. En un corto, solo las escenas |
| D | DESCRIPTION | Claude (español). Las líneas con ⚠ son las que Angie debe definir |
| E | REFERENCE | **Angie** (imágenes). Claude NUNCA escribe aquí |
| F | FINAL | **Angie** (imágenes). Claude NUNCA escribe aquí |
| G | STATUS | Menú desplegable: `TO DO`, `WIP`, `IN REVIEW`, `ADJUSTMENTS`, `DONE`. Claude pone `TO DO` al crear y no lo cambia salvo que Angie lo pida |
| H | PROMPT | Claude: el prompt vigente, completo y listo para copiar |

Formato: encabezado gris oscuro con texto blanco, filas agrupadas por categoría, PROMPT con
fondo amarillo claro, y la fila 1 y las columnas A–B fijas.

**Pestaña `HISTORIAL PROMPTS`**: `FECHA | ITEM | PROMPT | QUÉ CAMBIÓ | ¿FUNCIONÓ?`.
Cada prompt que alguna vez existió queda aquí. `¿FUNCIONÓ?` (sí / no / a medias) la marca
Angie.

## Reglas de escritura
1. **Un ítem = una fila para todo el proyecto.** Se identifica por CATEGORY + ITEM (el mismo
   nombre puede estar en PROPS y en GRAPHIC DESIGN, como un reloj y su interfaz). Si un
   episodio nuevo trae algo que ya existe, NO se duplica: se agrega una línea en APARECE EN y
   lo nuevo de la descripción como `[EP43] …`. Si el nombre es parecido pero no igual,
   **pregunta**.
2. **Un prompt por fila.** Si un ítem tiene variantes con prompt propio (día/noche, versión
   LATER, pantallas 1–4), cada variante va en una fila justo debajo:
   `Int. Kitchen — night`.
3. **Ajustar un prompt**: primero copia el prompt actual al HISTORIAL (si no está), después
   escribe el nuevo en PROMPT y regístralo en el HISTORIAL con "qué cambió" en una frase.
4. **Volver a un prompt anterior**: búscalo en el HISTORIAL por ITEM y fecha y vuelve a
   ponerlo en PROMPT ("restaurado del 2026-10-08").
5. **Antes de escribir**, dile a Angie en una línea qué va a cambiar ("3 ítems nuevos, 2
   actualizados, prompt ajustado en Int. Kitchen"). Después confirma qué quedó escrito.
6. Nunca borres filas ni columnas, ni lo que Angie escribió.
7. **Lee siempre la hoja antes de escribir**: lo que está en la hoja manda sobre lo que
   recuerdes del chat, porque Angie la edita a mano.

## Con el conector de Google Sheets (lo normal)
Herramientas: `get_spreadsheet` (pestañas y estructura), `get_values` (leer),
`update_values` (escribir celdas), `insert_dimension` (abrir filas para variantes o para
agrupar por categoría) y `update_spreadsheet` (crear pestañas, menú desplegable de STATUS,
formato, filas fijas).

## Sin conector (modo archivo, respaldo)
`scripts/hoja_proyecto.py` hace lo mismo sobre un .xlsx:
```bash
python scripts/hoja_proyecto.py crear   PROYECTO.xlsx
python scripts/hoja_proyecto.py agregar PROYECTO.xlsx desglose.json --propuesta propuesta.json
python scripts/hoja_proyecto.py prompt  PROYECTO.xlsx "Int. Kitchen" "nuevo prompt…" --cambio "más cálido" [--categoria SETS]
```
Angie sube el .xlsx a su Drive y lo abre con Google Sheets. `assets/PLANTILLA_HOJA_PROYECTO.xlsx`
es la hoja vacía. Recuérdale que **con el conector no tendría que subir ni bajar nada**.

## Entregar
- En el chat: qué filas cambiaron (por nombre de ítem) y el link de la hoja. No pegues la hoja
  en el chat.
- Si hubo propuesta visual, muestra también la página visual de `propuesta-visual`.
