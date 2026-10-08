# Criterio de Angie: ingeniería inversa del par de oro (EP42)

Fuente: guion `EPISODE 42 — THE DEADLINE` (escenas 169–170) y el desglose manual de Angie
(`examples/EP42_angie_original.json`). El resultado del skill está en
`examples/EP42_generado.json` y `examples/BREAKDOWN_EP42.xlsx`.

## Lo que hace Angie y el skill replica

| Guion | Angie | Regla |
|---|---|---|
| Escenas 169 y 170, ambas en el command center | **1 fila** de SET con "versión adicional con tazas de café vacías…" | Fusionar por locación; variantes como versiones |
| "No windows. Blue light from server racks…" | "noche, sin ventanas, luz azul proveniente de los servidores…" | Traducir la luz descrita: es información de arte |
| "3 AM on a wall clock", "guard asleep in a chair by the door" | Va dentro de la descripción del SET | El set dressing va en el set, no en PROPS |
| `GUARDS` | `Sofia's henchman 01`, `Sofia's henchman 02` | Renombrar a su nomenclatura y numerar |
| `ENGINEERS` (tres) | `Engineers (3)`, sin descripción | La cantidad va en el nombre y la descripción solo si aporta |
| "Tape across his broken nose. Bare feet. No linen tonight." | "cinta en la nariz rota, pies descalzos, no lleva ropa de lino, pijama?" | Lo explícito se traduce y la duda se marca con `?` |
| "His watch LIGHTS UP" + mapa con puntos | Tactical watch en PROPS **y** en GRAPHIC DESIGN | Objeto físico y gráfica por separado |
| "HANDSHAKE REJECTED", "REBUILDING 11%", mapa de nodos | `screens` con versiones en guiones | Una fila por superficie gráfica, con sus estados |

## Lo que Angie sabe y el guion no dice (el skill NO lo inventa)

| Angie escribió | Por qué el skill no lo pone | Qué pone el skill |
|---|---|---|
| Sofia: "ropa blanca" | Es continuidad de la serie y no está en este guion | `⚠ vestuario no especificado en el guion: definir continuidad` |
| Wyatt: "con y sin bolso" | Continuidad de la serie | Igual, marcado ⚠ |
| Watch: "la de **dixie**" | El guion dice "hers" | La escribe, pero como `⚠ el guion dice "hers": ¿Dixie? confirmar` |

Si hay biblia de continuidad (capa 3), estos campos se pueden prellenar desde ahí con la marca
`(biblia)`.

## Lo que el skill agrega y Angie no tenía (revisar si le sirve)

- Columna **ESC.** con números de escena. Sirve para ubicar rápido y es clave en largometrajes.
- Wyatt: **nudillos partidos** (explícito en la 169: "His knuckles are split").
- Screens: estado **12 %**, el **mapa ya arreglado** (nodos apagados, líneas rectas) y el
  **número de latencia bajando**: son estados gráficos distintos que hay que generar.
- Henchman 01: versión **dormido en la silla** (170).
- HSM: "cableado a la terminal".

## Estilo de redacción
- Descripciones en español, frases cortas separadas por coma. Sin adornos literarios.
- Variantes en líneas que empiezan con `- `.
- Duda: `?` dentro de la frase. Pendiente fuerte: línea que empieza con `⚠`.
