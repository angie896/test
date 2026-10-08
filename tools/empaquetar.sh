#!/usr/bin/env bash
# Empaqueta cada skill como .zip listo para subir a Claude.ai (Settings → Capabilities → Skills)
# y copia la base (00_BASE/reglas.md) y lo compartido de la hoja del proyecto
# (00_BASE/compartido/) dentro de cada skill para que lo herede.
# Uso: bash tools/empaquetar.sh            → todas las skills
#      bash tools/empaquetar.sh desglose-arte
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/dist"
skills=("$@"); [ ${#skills[@]} -eq 0 ] && skills=($(ls "$ROOT/skills"))
for s in "${skills[@]}"; do
  dir="$ROOT/skills/$s"
  mkdir -p "$dir/references"
  mkdir -p "$dir/scripts"
  cp "$ROOT/00_BASE/reglas.md" "$dir/references/reglas.md"
  cp "$ROOT/00_BASE/compartido/hoja.md" "$dir/references/hoja.md"
  cp "$ROOT/00_BASE/compartido/hoja_proyecto.py" "$dir/scripts/hoja_proyecto.py"
  (cd "$ROOT/skills" && rm -f "$ROOT/dist/$s.zip" && zip -qr "$ROOT/dist/$s.zip" "$s" -x '*/__pycache__/*' '*.DS_Store')
  echo "✓ dist/$s.zip"
done
