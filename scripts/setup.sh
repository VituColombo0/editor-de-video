#!/usr/bin/env bash
# Instala as ferramentas do Editor de Vídeos numa máquina nova (Linux ou macOS).
# Uso: bash scripts/setup.sh
set -euo pipefail

echo "==> FFmpeg"
if ! command -v ffmpeg >/dev/null; then
  if command -v apt >/dev/null; then sudo apt update && sudo apt install -y ffmpeg git curl
  elif command -v brew >/dev/null; then brew install ffmpeg
  else echo "Instale o FFmpeg manualmente: https://ffmpeg.org/download.html"; fi
fi

echo "==> uv (gerenciador Python)"
if ! command -v uv >/dev/null; then curl -LsSf https://astral.sh/uv/install.sh | sh; fi
export PATH="$HOME/.local/bin:$PATH"

echo "==> yt-dlp, Whisper, auto-editor, scenedetect"
uv tool install --force "yt-dlp[default]"
uv tool install --force whisper-ctranslate2
uv tool install --force auto-editor
uv tool install --force "scenedetect[opencv-headless]"

echo "==> Node 22 (nvm)"
export NVM_DIR="$HOME/.nvm"
if [ ! -s "$NVM_DIR/nvm.sh" ]; then
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
fi
# shellcheck disable=SC1091
. "$NVM_DIR/nvm.sh"
nvm install 22
nvm alias default 22

echo "==> HyperFrames + Chrome de renderização + skills do Claude"
npm install -g hyperframes
hyperframes browser ensure
hyperframes update -y

echo
hyperframes doctor || true
echo
echo "Pronto! Abra esta pasta no Claude Code."
