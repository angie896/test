# Esquema del JSON de propuesta visual

Ejemplo completo: `examples/EP42_propuesta.json` → `examples/PROPUESTA_EP42.html`.

```json
{
  "project": {"title": "SWIPE RIGHT", "unit": "EP42", "unit_title": "THE DEADLINE", "type": "serie"},
  "items": [
    {
      "category": "SETS",
      "item": "Int. Sofia's command center",       // igual que en el desglose
      "scenes": "169, 170",
      "intent": "intención narrativa en español",
      "flags": ["⚠ todo lo asumido / no escrito en el guion"],
      "palette": [
        {"hex": "#0B1220", "name": "función del color", "pct": 60},
        {"hex": "#1E6091", "name": "…", "pct": 30},
        {"hex": "#D7263D", "name": "…", "pct": 10}
      ],
      "lighting": "lógica de luz",
      "camera": "ángulo, lente, foco",
      "references": [
        {"title": "Blackhat", "year": 2015,
         "credits": "Dir. … · DP … · PD …",
         "url": "https://…   (solo si está confirmada)",
         "verified": true,
         "take": "qué tomar de este referente"}
      ],
      "searches": ["búsquedas cortas para Flim / ShotDeck / FilmGrab"],
      "prompts": [
        {"label": "Plate base — esc. 169", "tool": "Nano Banana Pro", "text": "prompt completo en inglés"}
      ],
      "mentor": "por qué: principio de PD/DP detrás de la decisión"
    }
  ]
}
```

Todos los campos excepto `category` e `item` son opcionales: el tablero muestra lo que haya.
