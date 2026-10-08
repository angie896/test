# Caja de herramientas de Angie Vélez: dirección de arte con IA

👉 **Versión visual (para ver, no para editar):** https://claude.ai/artifact/87QwxvekksAH3VBKaoeSpD

Skills, prompts y plantillas para preproducción de arte. Sirve para cualquier proyecto
(serie, corto, largo, videoclip, comercial o videojuego), no solo para un estudio.

| Carpeta | Qué hay |
|---|---|
| `00_BASE/reglas.md` | Quién eres y tus reglas duras. Todas las skills las heredan. |
| `skills/desglose-arte/` | Pide el link de tu hoja del proyecto, lee el guion y escribe el desglose en la hoja. |
| `skills/propuesta-visual/` | Página visual con referentes reales, paleta, luz y notas "por qué"; escribe y ajusta los prompts en la hoja. |
| `00_BASE/compartido/` | Las reglas de la hoja del proyecto y su script, que usan las dos skills. |
| `dist/` | Las skills empaquetadas en .zip, listas para subir. |
| `tools/empaquetar.sh` | Regenera los .zip después de editar algo. |
| `PROPUESTA_SISTEMA_ANGIE.md` | El plan general, el roadmap y las preguntas abiertas. |

## Flujo
```
guion ──► [desglose-arte] ──► BREAKDOWN.xlsx + desglose.json
                                         │
                                         ▼
                              [propuesta-visual] ──► PROPUESTA.html (referentes, paleta, luz, prompts)
                                         │
                       (pronto) biblia de continuidad ◄── imágenes FINAL aprobadas
```

## Cómo instalar las skills

**En la app de Claude (web o escritorio)**
1. Descarga `dist/desglose-arte.zip` y `dist/propuesta-visual.zip` (en GitHub: abrir el
   archivo → *Download raw file*).
2. Claude → *Settings* → *Capabilities* → *Skills* → subir el .zip.
3. Activa la búsqueda web en el chat, porque la propuesta visual la usa para verificar
   referentes.
4. Sube un guion y escribe "sácame el desglose de arte".

**En Claude Code**
```bash
cp -r skills/* ~/.claude/skills/
```

## Cómo actualizar
- Edita el `SKILL.md` o los archivos de `references/` (es texto plano).
- Si cambias tus reglas base, edítalas en `00_BASE/reglas.md` y corre
  `bash tools/empaquetar.sh`.
- Vuelve a subir el .zip. Git guarda el historial: si una versión anterior funcionaba mejor, se
  recupera.
