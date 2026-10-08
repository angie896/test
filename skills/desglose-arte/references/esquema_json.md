# Esquema del JSON de desglose

Este mismo JSON alimenta `build_breakdown.py` (Excel), el skill `propuesta-visual` y, más
adelante, la biblia de continuidad.

```json
{
  "project": {
    "title": "SWIPE RIGHT",
    "type": "serie | largometraje | cortometraje | videoclip | comercial | videojuego",
    "unit": "EP42",
    "unit_title": "THE DEADLINE"
  },
  "options": { "tracking": false, "scenes": true },
  "sheets": [
    {
      "name": "EP42",                       // nombre de la pestaña (máx. 31 caracteres)
      "title": "BREAKDOWN EP42 — THE DEADLINE",
      "items": [
        {
          "category": "SETS",               // SETS | CHARACTERS | PROPS | GRAPHIC DESIGN | VEHICLES | MAKEUP / SFX | VFX
          "item": "Int. Sofia's command center",   // inglés
          "scenes": "169, 170",
          "description": "español…\n- versión LATER: …\n⚠ pendiente…",  // opcional
          "level": "Medium",                // opcional (solo con --tracking)
          "status": "TO DO",                // opcional
          "assignment": "AV"                // opcional
        }
      ]
    }
  ]
}
```

- Varias entradas en `sheets` (varios episodios o secuencias) generan además la pestaña
  `SETS MASTER`, con todas las locaciones fusionadas y en qué unidades aparecen.
- Las líneas de `description` que empiezan con `⚠` salen en naranja negrita.
- El orden de las categorías es fijo: SETS, CHARACTERS, PROPS, GRAPHIC DESIGN y después las
  extras.
