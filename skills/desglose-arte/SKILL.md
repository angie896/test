---
name: desglose-arte
description: Desglose de arte de Angie conectado a la hoja de su proyecto en Google Sheets. Primero pide el link de la hoja del proyecto (Angie la crea en su Drive). Después lee el guion (PDF, .docx, .txt, .fountain o texto pegado) y escribe en la hoja todo lo visual en SETS, CHARACTERS, PROPS y GRAPHIC DESIGN, con ítems en inglés, descripciones en español y la continuidad no escrita marcada con ⚠, sin duplicar lo que ya estaba de episodios anteriores. Úsala cuando Angie diga "desglose", "breakdown", "sácame lo de arte", "qué necesito para este capítulo", "empecemos el proyecto…", "agrégalo a la hoja" o "actualiza el desglose", para serie, corto, largo, videoclip o comercial. No hace shotlists ni prompts de video.
---

# Desglose de arte (guion → hoja del proyecto)

Lee primero:
- `references/reglas.md`: la base de Angie.
- `references/hoja.md`: cómo funciona la hoja del proyecto. **Obligatorio.**
- `references/criterio.md`: cómo desglosa ella, con el par de oro del EP42.

## 0. Antes de empezar
1. **Pide el link de la hoja del proyecto** (`references/hoja.md`, sección 1). Si la hoja está
   vacía, ármale la estructura. Si tiene contenido, léela entera: así sabes qué ítems ya
   existen.
2. **Tipo de proyecto**: identifícalo o pregúntalo. Define cómo se escribe APARECE EN:

| Tipo | Unidad en APARECE EN |
|---|---|
| Serie | episodio: `EP42: esc. 169, 170` |
| Largometraje | secuencia o bloque: `SEQ 03: esc. 12` |
| Cortometraje | solo escenas: `esc. 4, 5` |
| Videoclip / comercial | concepto o versión: `V1: plano 3` (pesa más GRAPHIC DESIGN: marca, packshot) |
| Videojuego | nivel o zona (agrega VEHICLES y VFX si aparecen) |

Si el guion trae numeración de escenas, consérvala. Si no la trae, numera tú y avisa.

## 1. Leer TODO el guion antes de clasificar
No desgloses mientras lees. Una locación que aparece en la escena 169 puede tener un estado
nuevo en la 170 y tienen que quedar en la misma fila.

## 2. Extraer escena por escena solo lo explícito
- **SETS**: locación, momento del día, luz descrita (ventanas, fuentes), set dressing nombrado
  y estados (antes/después, "LATER").
- **CHARACTERS**: cada personaje con presencia física, incluidos extras con función y guardias.
  Marcas físicas (heridas, vendas, suciedad) y ropa mencionada.
- **PROPS**: objetos físicos que se usan o tienen importancia narrativa.
- **GRAPHIC DESIGN**: todo lo que es una gráfica: pantallas, UIs, textos en pantalla, letreros,
  documentos, logos y marcas ficticias.
- Categorías extra solo si el guion las exige: `VEHICLES`, `MAKEUP / SFX`, `VFX`. Si agregas
  una, avísale a Angie.

## 3. Aplicar el criterio de Angie (ver `references/criterio.md`)
- Fusionar por locación: una fila por set, con sus variantes como líneas `- versión …`.
- Ítems en inglés y descripciones en español.
- Descripción solo si aporta. Si el nombre basta, va vacía.
- Renombrar genéricos a su nomenclatura: `GUARDS` → `Sofia's henchman 01`, `02`.
- Separar el objeto físico de su gráfica: el reloj va en PROPS y su interfaz en GRAPHIC
  DESIGN. Lo mismo con pantallas y celulares.
- El set dressing (tazas, platos, reloj de pared) va en la descripción del set, no como prop,
  salvo que un personaje lo use de forma narrativa.
- Antes de crear un ítem, **busca si ya existe en la hoja** (mismo set con otro nombre, por
  ejemplo). Si existe, se agrega a esa fila.

## 4. Frontera de honestidad (no negociable)
- Lo explícito se llena.
- Lo inferido se escribe, pero en una línea que empieza con `⚠` y que dice de dónde salió.
  Ejemplo: `⚠ el guion dice "hers": ¿Dixie? confirmar`.
- La continuidad que no está escrita (ropa recurrente, accesorios) **no se inventa**. Se marca
  `⚠ vestuario no especificado en el guion: definir continuidad`. Si la hoja ya tiene esa
  continuidad de un episodio anterior, úsala y avísale ("tomé de la hoja: Sofia, ropa blanca").

## 5. Escribir en la hoja
- Sigue las reglas de `references/hoja.md`, sección 3. Antes de escribir, dile en una línea
  qué va a cambiar ("12 ítems nuevos, 4 ya existían: les sumo EP43").
- **Con conector**: escribe directo en la hoja.
- **Sin conector**: arma el JSON del desglose (`references/esquema_json.md`) y usa
  `scripts/hoja_proyecto.py agregar` sobre la hoja que Angie te suba
  (`assets/PLANTILLA_HOJA_PROYECTO.xlsx` si es nueva).
- Excel suelto con su formato clásico, solo si Angie lo pide:
  `python scripts/build_breakdown.py desglose.json BREAKDOWN_<UNIDAD>.xlsx [--tracking]`.

## 6. Entregar
1. El link de la hoja y qué quedó escrito: cuántos ítems nuevos y actualizados por categoría.
2. La lista de los ⚠ pendientes, para que Angie los defina.
3. Ofrece el siguiente paso: **la propuesta visual** (skill `propuesta-visual`), que trabaja
   sobre estas mismas filas.
4. **No le muestres JSON ni código**: son internos.
