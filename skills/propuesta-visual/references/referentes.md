# Protocolo de referentes reales

> Regla de Angie: **siempre referentes reales**. Un referente inventado es peor que no tener
> referente, porque te hace buscar algo que no existe o, peor, presentarle al cliente algo
> falso.

## Qué cuenta como referente real
- **Cine y TV**: título, año, director, **DP** (director de fotografía) y **PD** (production
  designer). Los créditos se verifican.
- **Fotografía**: fotógrafo, serie o proyecto, año y link.
- **Arte e ilustración**: artista, obra, año y museo o fuente.
- **Lugares y objetos reales**: arquitectura, productos, interfaces reales (con link oficial).
- **Animación y videojuegos**: título, estudio, año y, si se sabe, art director o background
  artist.

## Cómo verificar (en orden)
1. **Con búsqueda web disponible** (Claude.ai con búsqueda o Claude Code): buscar y confirmar
   los créditos y que el material visual exista. Fuentes buenas:
   - Créditos: Wikipedia, IMDb, AFI Catalog, American Cinematographer (theasc.com), British
     Cinematographer, Art Directors Guild.
   - Fotogramas: film-grab.com, screenmusings.org, shotdeck.com (requiere cuenta), flim.ai
     (requiere cuenta).
   - Entrevistas de PD y DP: muy valiosas para el modo mentor.
2. Si **los créditos están verificados pero el fotograma exacto no**: `"verified": true` en los
   créditos y en `take` se aclara: `⚠ falta confirmar el fotograma exacto en Flim o FilmGrab`.
3. **Sin búsqueda web**: se puede proponer desde la memoria, pero **siempre**
   `"verified": false`. El tablero lo marca ⚠ y entra a la lista de pendientes.
4. **Nunca** inventar URLs. Si no hay URL confirmada, se deja vacío.

## Flim, ShotDeck y plataformas de pago
No tienen API pública ni conector para Claude, así que Claude no puede buscar adentro. El
flujo es:
1. La skill genera **búsquedas listas** (botón para copiar en el tablero): cortas, en inglés y
   con lenguaje visual (`server room blue light night`, `kitchen 1990s tungsten practical`).
2. Angie las pega en Flim o ShotDeck, elige fotogramas y los pega en la columna REFERENCE del
   desglose.
3. **Opcional, el mejor ciclo**: Angie sube a Claude las capturas que eligió. Claude las mira,
   extrae la paleta real (HEX), la lógica de luz y la composición, y ajusta los prompts para
   que se parezcan a SU selección.

## Qué tomar de cada referente
Cada referente lleva un `take` concreto: qué copiar y qué no. Ejemplo: "la luz cenital fría y
el contraste, no la arquitectura". Un referente sin `take` no le sirve a nadie.

## Mezcla recomendada por ítem
- 1–2 de cine o TV (lenguaje cinematográfico y luz).
- 1 del mundo real (foto de locación, producto o interfaz real), que es lo que más ancla al
  generador de imagen.
- Opcional: 1 de pintura, ilustración o animación (color e intención), que es la tradición de
  Angie.
