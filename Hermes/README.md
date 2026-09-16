# Hermes — área operacional

Esta pasta contém pacotes de execução preparados para o Hermes trabalhar sobre o ACIRV Notebook sem misturar estado operacional com as notas institucionais do cofre.

## Pacote ativo

- [`Planejamento 4º Trimestre de 2026/`](./Planejamento%204%C2%BA%20Trimestre%20de%202026/) — Social Media da ACIRV, de 16/09/2026 a 31/12/2026.

## Convenção

Cada pacote trimestral deve ter:

- `00_README.md` como ponto de entrada;
- `01_RUNBOOK_HERMES.md` com regras de execução e auditoria;
- `02_TRELLO_CONFIG.json` com destinos externos validados;
- `03_EXECUTION_STATE.json` com estado mutável/checkpoint;
- `04_RECONCILIACAO_TRELLO_INICIAL.md` com riscos de duplicação e legado;
- `calendario/` com o plano versionado por mês;
- `moodboard/` com referências visuais e seu contrato de uso.

A regra arquitetural é: **plano versionado e estado de execução são coisas diferentes**. O Hermes não deve reescrever o plano silenciosamente ao atualizar o progresso.
