---
id: auditoria-curadoria-delta-hd-externo-2026-09-22
titulo: Curadoria-Delta-HD-Externo-2026-09-22
tipo: auditoria
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-22'
ultima_revisao: '2026-09-22'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- dado_calculado
- interpretacao_operacional
tags:
- auditoria
- ingestao
- hd-externo
confidencialidade: interno
subtipo: auditoria_ingestao
---

# Curadoria-Delta-HD-Externo-2026-09-22

> [!summary] Síntese
> Auditoria da curadoria semântica dos lotes adicionados ao repositório em 22/09/2026. O trabalho priorizou novidade real: deduplicação por blob SHA, comparação de versões pelo nome, Safety Gate por caminho e promoção apenas do que acrescenta inteligência operacional.

## Ponto de corte

O delta veio principalmente de:

- `c1eab0d30f01a60f84148ef344529b1be3e00345` — reunião de marketing e ajuste de catálogo;
- `4acad86aa18cca20f8f5b175a945806bcb75fbec` — recuperação do HD externo.

Esses lotes entraram no `main` depois do ponto de corte usado pela curadoria anterior.

## Escala

O guia do HD registra **3.020 arquivos / 1,21 GB** entre os dois lotes documentados.

Na triagem GitHub-First dos formatos textuais/estruturados de maior prioridade:

| Etapa | Arquivos |
|---|---:|
| candidatos iniciais | 238 |
| duplicatas exatas por blob SHA | 200 |
| candidatos com SHA novo | 38 |

Assim, cerca de **84%** dos candidatos de alta prioridade já existiam byte a byte em outro caminho.

## Controle de versões

Entre os 38 restantes, vários eram versões menores ou anteriores de fontes com o mesmo nome já presentes em `000-Arquivos-originais/`.

Quando isso ocorreu, a versão mais completa foi usada como referência principal. A cópia do HD permaneceu como evidência histórica, evitando regressão de conhecimento.

Esse controle foi especialmente relevante para:

- tom de voz;
- assessoria de imprensa;
- Fórum da Indústria;
- planejamento do Conecta;
- métricas históricas;
- notas de reunião.

## Safety Gate

As classes marcadas pelo guia como locais, pessoais, de segurança ou de acesso restrito não foram abertas para curadoria semântica. Grandes exports de conversa e bases de pessoas também não foram usados quando não eram necessários para a decisão.

Arquivos em formatos pendentes de conversão permanecem pendentes; não foram tratados como “revisados” apenas por estarem no repositório.

## Promoções materiais desta etapa

### Operação atual

A reunião de 21/09 e o ajuste de catálogo de 22/09 alimentaram:

- [[Plano-Operacional-21-22-09-2026]];
- [[SudoExpo-Match]];
- [[Cafe-Entre-Amigos]];
- [[Check-In-Inteligente-de-Eventos]];
- [[Oficina-Raphael-Criacao-de-Site-com-IA]];
- [[Governanca-de-Aprovacoes]];
- [[Pendencias-de-Dados]];
- [[Servicos-e-Beneficios-da-ACIRV]];
- [[Validacoes-Humanas-Necessarias]].

### Instagram de agosto

A análise executiva inédita foi promovida para [[Diagnostico-Instagram-Agosto-2026]], preservando a necessidade de reconciliação com a planilha MASTER antes de publicação externa.

### Priorização e capacidade

Duas transcrições de março documentam a origem do conflito entre múltiplos solicitantes e uma tentativa histórica de pontuar prioridade, esforço e tempo.

A fórmula experimental não foi promovida. O aprendizado foi incorporado a:

- [[Criterios-de-Priorizacao-de-Marketing]];
- [[Gestao-de-Capacidade-e-WIP]].

### Conhecimento histórico reaproveitável

Fontes recuperadas ajudaram a completar:

- [[Manual-Operacional-de-Tom-de-Voz]];
- [[Assessoria-de-Imprensa]];
- [[Forum-da-Industria]].

No Fórum da Indústria foi preservada uma divergência de data em vez de resolvê-la por suposição.

## Material não promovido

Não foram transformados em notas canônicas:

- relatórios técnicos de empacotamento de arquivos de design;
- licenças de assets sem decisão operacional associada;
- dumps de estrutura de pastas como se representassem o Drive atual;
- versões históricas menores que fontes já existentes;
- dados restritos ou pessoais;
- itens que exigem conversão antes de leitura confiável.

O planejamento histórico do Conecta também não reabre decisões já validadas sobre a Cota Diamante e o significado dos R$ 4 milhões.

## Ledger

O `Ledger-de-Ingestao.jsonl` do `main` ainda representa um inventário anterior. O inventariador v2 já suporta o novo fluxo, mas a execução determinística não foi simulada manualmente nesta curadoria.

Uma tentativa de obter um clone efêmero para executar os scripts não conseguiu resolver o host remoto nesse ambiente. Portanto:

- o ledger não foi fabricado;
- novos statuses de revisão não foram inventados;
- claims dependentes das novas entradas de ledger não foram criados.

A validação da camada canônica desta entrega será feita pelo CI da Pull Request, conforme o fluxo GitHub-First.

## Limite desta etapa

Esta auditoria significa que o **delta semanticamente acionável selecionado foi curado**. Não significa que os 3.020 arquivos foram integralmente lidos.

O restante exige uma combinação de:

- deduplicação;
- conversão;
- lotes temáticos;
- governança de privacidade;
- execução futura do inventário determinístico.

## Fontes

- `000-Arquivos-originais/00-GUIA-DE-CURADORIA-HD-EXTERNO.md`;
- commits `c1eab0d30f01a60f84148ef344529b1be3e00345` e `4acad86aa18cca20f8f5b175a945806bcb75fbec`;
- árvore Git de `main` consultada durante esta curadoria.
