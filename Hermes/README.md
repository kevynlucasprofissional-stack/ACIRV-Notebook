# Hermes — área operacional

Esta pasta contém pacotes de execução preparados para o Hermes trabalhar sobre o ACIRV Notebook sem misturar estado operacional com as notas institucionais do cofre.

## Pacotes ativos

- [`Pesquisas-Q4-2026/`](./Pesquisas-Q4-2026/) — operação de pesquisas prioritárias, controle local de contatos/respostas e promoção de agregados para a camada canônica.

## Pacote ativo de Social Media

- [`Planejamento 4º Trimestre de 2026/`](./Planejamento%204%C2%BA%20Trimestre%20de%202026/) — Social Media da ACIRV, de 16/09/2026 a 31/12/2026.

## Convenção

Cada pacote trimestral deve ter:

- `00_README.md` como ponto de entrada;
- `01_RUNBOOK_HERMES.md` com regras de execução e auditoria;
- `02_TRELLO_CONFIG.json` com destinos externos validados;
- `03_EXECUTION_STATE.json` com estado mutável/checkpoint;
- `04_RECONCILIACAO_TRELLO_INICIAL.md` com riscos de duplicação e legado;
- `calendario/` com o plano versionado por mês;
- `moodboard/` com a projeção operacional das referências visuais e seu contrato de uso; a autoridade semântica de identidade permanece na camada canônica `01-Estrategia-e-Marca/Design-System-ACIRV.md`.

A regra arquitetural é: **plano versionado e estado de execução são coisas diferentes**. O Hermes não deve reescrever o plano silenciosamente ao atualizar o progresso.


## Regra para inteligência visual

Arquivos do Hermes podem projetar a inteligência visual para execução, mas não devem se tornar uma fonte concorrente. O `MOODBOARD.md` operacional deve permanecer compatível com `01-Estrategia-e-Marca/Design-System-ACIRV.md`. Decisões visuais permanentes nascidas no fluxo operacional devem ser promovidas ao canônico.
