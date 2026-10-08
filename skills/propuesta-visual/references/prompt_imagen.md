# Anatomía de un prompt de imagen (sets, personajes, props, gráficos)

Los prompts van en inglés, completos y en un solo bloque listo para copiar. Orden recomendado
(de lo general a lo específico, que es como "lee" la mayoría de los modelos):

1. **Tipo de imagen**: `Cinematic environment plate` / `Character identity sheet` /
   `Product shot of a prop` / `Flat front-facing screen graphic`.
2. **Ángulo**: sets → `three-quarter view from a corner of the room` (nunca frontal plano).
3. **Qué y dónde**: locación, época, región o país, momento del día.
4. **Elementos clave del desglose**: lo explícito del guion, con los textos de pantalla entre
   comillas exactas.
5. **Materiales y textura**: concreto pulido, linóleo, madera gastada, papel de colgadura
   desgastado…
6. **Luz**: fuentes motivadas, temperatura, contraste, atmósfera (haze o polvo).
7. **Paleta**: `Color palette: 60% … (#HEX), 30% … (#HEX), 10% … (#HEX)`.
8. **Cámara**: altura, lente en mm, profundidad de campo.
9. **Acabado**: `photorealistic, cinematic <género> look, high detail`.
10. **Exclusiones**: plates → `empty room, no people`. Extras → `faces clearly visible and
    sharp` (nunca blur).

## Plantillas

### Set / plate
```
Cinematic environment plate, three-quarter view from a corner of the room, of [LOCACIÓN], [ÉPOCA/LUGAR], [MOMENTO DEL DÍA]. [ELEMENTOS DEL DESGLOSE]. [MATERIALES]. Lighting: [FUENTES MOTIVADAS], [TEMPERATURA], [CONTRASTE], [ATMÓSFERA]. Color palette: 60% [..] (#), 30% [..] (#), 10% [..] (#). Eye-level camera, [24–35]mm lens, deep focus, photorealistic, cinematic [GÉNERO] look, high detail, empty room, no people.
```

### Variante de un set aprobado (editar, no regenerar)
```
Same [LOCACIÓN] as the reference image, same three-quarter camera angle and layout, now [CAMBIO DE ESTADO/HORA]. [CAMBIOS EXACTOS]. Keep the same lighting logic and color palette. Photorealistic, high detail, no people.
```

### Character sheet de identidad (siempre primero)
```
Character identity sheet, full body, front view, standing neutral pose, plain medium-grey seamless background, neutral even studio lighting, no dramatic shadows. [EDAD, ETNIA, COMPLEXIÓN, ROSTRO, PELO]. Wearing [VESTUARIO]. [MARCAS FÍSICAS]. Photorealistic, high detail, sharp face, neutral expression.
```
Después, desde el sheet aprobado: turnaround (frente, 3/4, perfil, espalda), expresiones y
versión en escena.

### Prop
```
Product shot of [PROP], [MATERIAL, ESTADO, ÉPOCA], three-quarter angle, plain light-grey background, soft studio lighting, photorealistic, high detail.
```

### Gráfica / UI
```
Flat front-facing [screen/sign/document] graphic, [PROPORCIÓN], [ESTILO DE UI/ÉPOCA]. [TEXTO EXACTO ENTRE COMILLAS]. [COLORES HEX]. Crisp legible text, high resolution.
```
Las demás pantallas del mismo software se piden con `same design system as the reference`.

## Por herramienta (actualizar con el benchmark)
- **Nano Banana Pro**: muy bueno para editar desde una referencia (variantes de un set,
  derivar escena desde el sheet). Texto en pantalla bastante fiable.
- **Imagen (AI Studio)**: buena calidad fotográfica en plates.
- ⚠ Estas notas son generales. Las reemplaza lo que Angie mida en su propio benchmark.
