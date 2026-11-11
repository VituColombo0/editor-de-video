# Editor de Vídeos — instruções para o Claude

Este repositório é um **estúdio de edição de vídeo** operado pelo Claude.
O usuário passa referências e vídeos brutos; o Claude edita e entrega o vídeo pronto.
Sempre responda em **português do Brasil**.

## Estrutura de pastas

| Pasta | Conteúdo | Vai pro Git? |
|---|---|---|
| `Vídeos Brutos/` | Material gravado pelo usuário (entrada) | Não (pesado) |
| `Referencias/` | Vídeos de referência de estilo (baixados ou enviados) | Não (pesado) |
| `Videos Prontos/` | Vídeos finais renderizados (saída) | Não (pesado) |
| `projetos/<nome-do-video>/` | Um projeto HyperFrames por vídeo (HTML, roteiro, notas) | Sim |
| `transcricoes/` | Legendas/transcrições (.srt, .json) | Sim |
| `assets/` | Fontes, músicas, logos reutilizáveis | Sim (exceto arquivos > 50 MB) |
| `scripts/` | Scripts auxiliares (setup, utilitários) | Sim |
| `memoria/` | **Memória persistente do projeto** (ver abaixo) | Sim |

## Memória global (IMPORTANTE)

A memória precisa funcionar em qualquer máquina, então ela fica **dentro do repositório**, não na memória local do Claude:

- `memoria/preferencias.md` — estilo do usuário: cortes, ritmo, legendas, fontes, cores, música, formatos (9:16, 16:9…). Atualize sempre que o usuário aprovar ou corrigir algo.
- `memoria/historico.md` — uma linha por vídeo feito: data, nome, referência usada, decisões principais.
- `memoria/referencias.md` — análise de cada referência (ritmo, tipo de corte, legendas, transições, paleta).

Ao começar uma sessão: leia os três arquivos. Ao terminar um vídeo ou mudar uma preferência: atualize-os e faça
`git add -A && git commit -m "..." && git push` (vídeos ficam fora do Git pelo `.gitignore`).

## Ferramentas instaladas

- **HyperFrames** (`hyperframes`) — vídeo a partir de HTML/CSS/JS: títulos, legendas animadas, motion graphics, composição final. Precisa do Node 22 (`nvm use 22`). Skills do HyperFrames instaladas em `~/.claude/skills` (`hyperframes`, `hyperframes-cli`, `media-use`, `reverse-any-video`, `style-sampling`…) — use-as.
- **FFmpeg / ffprobe** — cortes, conversão, áudio, concatenação, normalização.
- **whisper-ctranslate2** — Whisper (faster-whisper) na CPU. Ex.: `whisper-ctranslate2 arquivo.mp4 --model small --language pt --output_format srt --output_dir transcricoes/ --word_timestamps True`. Esta máquina tem pouca RAM: prefira `small` ou `medium` com `--compute_type int8`.
- **yt-dlp** — baixar referências: `yt-dlp -o "Referencias/%(title)s.%(ext)s" URL`.
- **auto-editor** — remover silêncios automaticamente: `auto-editor bruto.mp4 --margin 0.2s`.
- **scenedetect** — detectar cortes de cena em referências: `scenedetect -i ref.mp4 detect-adaptive list-scenes`.

Em uma máquina nova: rode `bash scripts/setup.sh`.

## Fluxo de trabalho padrão

1. **Referência**: baixar para `Referencias/`, analisar (cortes com scenedetect, `hyperframes measure`, frames-chave, áudio) e registrar em `memoria/referencias.md`.
2. **Brutos**: transcrever com Whisper, cortar silêncios/erros, escolher os melhores trechos.
3. **Montagem**: criar `projetos/<nome>/` com HyperFrames (legendas, títulos, zooms, b-roll, música).
4. **Revisão**: `hyperframes snapshot`/`preview` para conferir antes de renderizar.
5. **Render**: saída final em `Videos Prontos/<nome>.mp4`.
6. **Memória**: atualizar `memoria/` e dar push.

## Limitações desta máquina (Linux Mint, 4 núcleos, 3,7 GB RAM, sem GPU)

Renders longos podem falhar por memória: renderizar com poucos workers, fechar outros apps, ou dividir em partes e concatenar com FFmpeg.
