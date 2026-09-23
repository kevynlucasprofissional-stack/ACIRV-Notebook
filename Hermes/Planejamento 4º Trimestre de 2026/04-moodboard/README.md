# Moodboard ACIRV — READY

Status: `READY`  
Perfil operacional: `ACIRV-MOOD-v1`  
Fonte canônica: `../../../01-Estrategia-e-Marca/Design-System-ACIRV.md`

A projeção operacional usada pelo Hermes está em:

`MOODBOARD.md`

## Arquitetura

- `01-Estrategia-e-Marca/Design-System-ACIRV.md` é a fonte canônica principal da inteligência visual.
- `MOODBOARD.md` existe por necessidade operacional do fluxo Hermes e deve permanecer semanticamente sincronizado ao canônico.
- `000-Arquivos-originais/DESIGN SYSTEM.md` é fonte primária imutável e serve como evidência/proveniência.
- O identificador `ACIRV-MOOD-v1` é preservado para compatibilidade com automações, briefings e prompts.

## Uso operacional

1. Ler `MOODBOARD.md` antes de gerar qualquer referência visual.
2. Usar referências âncora com peso maior que peças pequenas/complementares.
3. Adaptar a identidade ao briefing sem copiar literalmente composições existentes.
4. Gerar referências visuais apenas para orientar a designer; não tratá-las como arte final.
5. Registrar a referência gerada no estado do respectivo `post_id` e vinculá-la ao card correspondente quando o fluxo Trello estiver habilitado.
6. Se surgir dúvida ou conflito semântico, consultar o Design System canônico e fazer o `MOODBOARD.md` convergir para ele.

O moodboard não bloqueia mais o avanço para `REFERENCIA_VISUAL_CRIADA`.
