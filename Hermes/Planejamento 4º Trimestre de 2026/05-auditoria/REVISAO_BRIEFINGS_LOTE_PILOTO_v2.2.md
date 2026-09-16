# Auditoria editorial — briefings do lote piloto — v2.2

**Período:** 16/09/2026 a 05/10/2026  
**Total de posts:** 12  
**Objetivo:** elevar as pautas do nível editorial para ordens de produção completas antes da sincronização com o Trello.

## Resultado executivo

- 12/12 pautas receberam briefing canônico de produção.
- 12/12 possuem texto exato para todos os slides.
- 12/12 possuem direção visual por slide ou, no caso de peça única, direção visual específica da peça.
- 12/12 possuem legenda final pronta para copiar.
- 12/12 possuem assets/referências identificados.
- 12/12 possuem restrições `NÃO FAZER` quando relevantes.
- 11/12 estão `PRODUÇÃO_PRONTA`.
- 1/12 está `PRODUÇÃO_PRONTA_COM_ASSET_PENDENTE`: post 001, aguardando QR Code/link definitivo da pesquisa.
- 12 cards canônicos já existem no Trello.
- 1 card duplicado do post 005 foi identificado como arquivado e não deve ser reutilizado.
- A sincronização Trello dos briefings v2.2 permanece pendente; a autoria editorial está concluída.

## Mudança de responsabilidade

A partir da v2.2:

- o planejamento/GitHub é a fonte de autoria editorial;
- o Hermes não escreve ou melhora copy de posts já fechados;
- o Hermes apenas transfere o bloco `DESCRIÇÃO CANÔNICA PARA O TRELLO` para o card indicado no mapa de sincronização;
- pauta sem briefing fechado vira `BLOCKED_EDITORIAL_BRIEFING`, não texto improvisado pelo agente.

## Quality Gate — lote piloto

| Post | Copy exata | Direção visual | Legenda final | Assets | Status |
|---|---|---|---|---|---|
| ACIRV-SM-2026-001 | OK | OK | OK | QR pendente | PRODUÇÃO_PRONTA_COM_ASSET_PENDENTE |
| ACIRV-SM-2026-045 | OK | OK | OK | OK | PRODUÇÃO_PRONTA |
| ACIRV-SM-2026-002 | OK | OK | OK | OK | PRODUÇÃO_PRONTA |
| ACIRV-SM-2026-003 | OK | OK | OK | OK | PRODUÇÃO_PRONTA |
| ACIRV-SM-2026-004 | OK | OK | OK | OK | PRODUÇÃO_PRONTA |
| ACIRV-SM-2026-046 | OK | OK | OK | OK | PRODUÇÃO_PRONTA |
| ACIRV-SM-2026-005 | OK | OK | OK | OK | PRODUÇÃO_PRONTA |
| ACIRV-SM-2026-006 | OK | OK | OK | OK | PRODUÇÃO_PRONTA |
| ACIRV-SM-2026-007 | OK | OK | OK | OK | PRODUÇÃO_PRONTA |
| ACIRV-SM-2026-008 | OK | OK | OK | autorização se houver pessoa identificável | PRODUÇÃO_PRONTA |
| ACIRV-SM-2026-047 | OK | OK | OK | OK | PRODUÇÃO_PRONTA |
| ACIRV-SM-2026-009 | OK | OK | OK | OK | PRODUÇÃO_PRONTA |

## Principais problemas corrigidos

### 1. Estrutura sem copy

Antes, vários posts tinham instruções como:
- `mostrar pessoas, negócios, Conecta/Match/estande`;
- `uma situação por card`;
- `rede, representação, consultorias, certificado...`;
- `peça única com fotografia humana e frase principal`.

Agora cada slide possui texto final, função narrativa e hierarquia.

### 2. Direção visual genérica

Antes, uma única linha visual tentava orientar carrosséis de 4, 5 ou 6 slides.

Agora cada slide possui direção própria, definindo fotografia/composição, elemento dominante, destaque cromático e relação com `ACIRV-MOOD-v1`.

### 3. Assets indefinidos

Agora cada briefing explicita o tipo de foto, material, logo ou QR necessário e evita transferir pesquisa de conteúdo para a designer.

### 4. Legenda tratada como rascunho

As legendas do lote foram convertidas para `LEGENDA FINAL — PRONTA PARA COPIAR`, salvo pendências explicitamente registradas.

### 5. Hermes assumindo autoria editorial

O fluxo foi corrigido para impedir que o agente gere, resuma ou reescreva copy ao colocar o material no Trello.

## Exemplo antes × depois — carrossel 6 slides

### ACIRV-SM-2026-004 — Certificado Digital

**Antes:**

> Assinaturas, obrigações fiscais, procurações, NF-e/serviços digitais; validar exemplos e condições antes de publicar.

**Depois:**

O briefing define seis lâminas com copy final, incluindo:
- capa com gancho;
- assinatura digital;
- NF-e;
- serviços/obrigações digitais;
- procurações/identificação;
- fechamento e CTA;
- direção visual específica de cada slide;
- restrições para evitar afirmar obrigatoriedade universal ou condições comerciais não validadas.

A Samara não precisa mais transformar uma lista de temas em carrossel.

## Exemplo antes × depois — extra de 2 slides

### ACIRV-SM-2026-045 — SudoExpo acabou. E agora?

**Antes:**

> Slide 1: “SudoExpo acabou. E agora? 3 formas de continuar as conexões”. Slide 2: CTA curto. Peça leve com bastante respiro.

**Depois:**

Slide 1 recebeu copy exata:

> SUDOEXPO ACABOU.  
> E AGORA?  
> 3 formas de continuar as conexões.

Slide 2 recebeu fechamento e CTA exatos:

> Uma boa conexão não precisa terminar no evento.  
> Retome hoje uma conversa que fez sentido para você.

Os dois slides também possuem orientação visual própria e restrição explícita de não criar terceiro slide.

## Fontes operacionais resultantes

Briefings:
- `../01-planejamento/v2/2026-09.md`
- `../01-planejamento/v2/2026-10-1.md`

Padrão editorial:
- `../01-planejamento/v2/PADRAO_BRIEFING_PRODUCAO.md`

Mapa Trello:
- `../03-integracoes/LOTE_PILOTO_TRELLO_SYNC.md`

Estado:
- `../02-estado/execution_state_v2.json`

## Trabalho restante para o Hermes

Somente execução no Trello:
1. validar board/list;
2. abrir cada um dos 12 cards canônicos;
3. copiar o bloco canônico do GitHub;
4. substituir a descrição;
5. salvar e verificar;
6. tentar preencher o vencimento nativo com a data de entrega;
7. registrar o resultado no estado;
8. parar em 05/10.

O Hermes não possui tarefa editorial pendente neste lote.