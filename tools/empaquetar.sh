#!/usr/bin/env bash
# Empaqueta cada skill como .zip listo para subir a Claude.ai (Settings → Capabilities → Skills)
# y copia la base (00_BASE/reglas.md) dentro de cada skill para que la herede.
# Uso: bash tools/empaquetar.sh            → todas las skills
#      bash tools/empaquetar.sh desglose-arte
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/dist"
skills=("$@"); [ ${#skills[@]} -eq 0 ] && skills=($(ls "$ROOT/skills"))
for s in "${skills[@]}"; do
  dir="$ROOT/skills/$s"
  mkdir -p "$dir/references"
  cp "$ROOT/00_BASE/reglas.md" "$dir/references/reglas.md"
  (cd "$ROOT/skills" && rm -f "$ROOT/dist/$s.zip" && zip -qr "$ROOT/dist/$s.zip" "$s" -x '*/__pycache__/*' '*.DS_Store')
  echo "✓ dist/$s.zip"
done
