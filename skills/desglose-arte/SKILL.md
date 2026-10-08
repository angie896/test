---
name: desglose-arte
description: Convierte un guion (PDF, .docx, .txt, .fountain o texto pegado) en el desglose de arte de Angie en Excel con cuatro categorías (SETS, CHARACTERS, PROPS, GRAPHIC DESIGN), ítems en inglés, descripciones en español y la continuidad no escrita marcada con ⚠. Úsala cuando Angie suba un guion o escenas y pida "desglose", "breakdown", "sácame lo de arte", "lista de arte", "qué necesito para este capítulo" o algo parecido, para cualquier tipo de proyecto (serie, corto, largo, videoclip, comercial). No hace shotlists ni prompts de video.
---

# Desglose de arte (guion → Excel)

Lee primero `references/reglas.md` (la base de Angie) y `references/criterio.md`, que es la
ingeniería inversa de cómo desglosa ella, con el par de oro del EP42.

## 0. Antes de empezar: tipo de proyecto
Identifica o pregunta el tipo de proyecto. Cambia cómo se divide el Excel:

| Tipo | Unidad = una pestaña | Extra |
|---|---|---|
| Serie | episodio (`EP42`) | Varios episodios a la vez → pestaña `SETS MASTER` automática |
| Largometraje | secuencia o bloque (`SEQ 03`, `ACTO 1`) | `SETS MASTER` para saber qué sets se repiten |
| Cortometraje | una sola pestaña | — |
| Videoclip o comercial | una pestaña por concepto o versión | Suele pesar más GRAPHIC DESIGN (marca, packshot) |
| Videojuego | nivel o zona | Agrega VEHICLES y VFX si aparecen |

Si el guion ya trae numeración de escenas, consérvala. Si no la trae, numera tú y avisa.

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

## 4. Frontera de honestidad (no negociable)
- Lo explícito se llena.
- Lo inferido se escribe, pero en una línea que empieza con `⚠` y que dice de dónde salió.
  Ejemplo: `⚠ el guion dice "hers": ¿Dixie? confirmar`.
- La continuidad que no está escrita (ropa recurrente, accesorios) **no se inventa**. Se marca
  `⚠ vestuario no especificado en el guion: definir continuidad`.
- Si existe una biblia de continuidad del proyecto y Angie pide usarla, se puede prellenar
  desde ahí con la marca `(biblia)` para que se sepa de dónde vino.
- Las líneas con ⚠ salen en naranja en el Excel.

## 5. Escribir el JSON y generar el Excel
Arma el JSON según `references/esquema_json.md` y corre:

```bash
python scripts/build_breakdown.py desglose.json BREAKDOWN_<UNIDAD>.xlsx            # formato base
python scripts/build_breakdown.py desglose.json BREAKDOWN_<UNIDAD>.xlsx --tracking # + LEVEL/STATUS/ASSIGNMENT
```

- Formato base (el preferido de Angie): `CATEGORY | ☐ | ESC. | ITEM | DESCRIPTION | REFERENCE | FINAL`.
- `--tracking` agrega lo útil de su segunda versión: LEVEL (Easy/Medium/Hard), STATUS y
  ASSIGNMENT con menús desplegables. Úsalo cuando hay equipo repartiéndose el trabajo.
- `--no-scenes` quita la columna ESC.
- REFERENCE y FINAL **siempre vacías**: ahí Angie pega imágenes.

## 6. Entregar
1. El `.xlsx`.
2. Un resumen corto: cuántos ítems por categoría, lista de todos los ⚠ pendientes y qué
   escenas fusionaste.
3. Ofrecer el siguiente paso: **propuesta visual** (skill `propuesta-visual`), que toma este
   mismo JSON.

Guarda también el JSON junto al Excel: es la entrada de la propuesta visual y de la biblia de
continuidad.
