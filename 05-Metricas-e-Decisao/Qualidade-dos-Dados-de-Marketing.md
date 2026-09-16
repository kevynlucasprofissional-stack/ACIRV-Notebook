---
id: metrica-qualidade-dos-dados-de-marketing
titulo: Qualidade-dos-Dados-de-Marketing
aliases: []
tipo: metrica
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.1'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-06-18'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- auditoria
- dados
fontes_documentais:
- '[[Fonte - Dados Marketing]]'
- '[[Fonte - Relatorios Mensais de Marketing]]'
notas_relacionadas:
- '[[Fonte - Dados Marketing]]'
- '[[Dicionario-de-KPIs]]'
- '[[Pendencias-de-Dados]]'
confidencialidade: interno
subtipo: auditoria_dados
---

# Qualidade-dos-Dados-de-Marketing

> [!summary] Síntese
> Registro de inconsistências, lacunas e regras para impedir decisões baseadas em planilhas aparentemente precisas, mas semanticamente instáveis.

## Achados

A aba de visão geral menciona intervalo invertido e “último mês oficial” incompatível com linhas posteriores; abril e maio usam seriais de data; percentual de não seguidores mistura texto e número; qualidade de maio está vazia; algumas moedas têm formatação ambígua; relatórios podem divergir.

## Severidade

Nenhum achado impede preservar os dados, mas eles bloqueiam automação cega e comparação sem revisão.

## Correção recomendada

Criar tabela canônica com `mes` ISO, tipos numéricos, fonte, data de coleta, fórmula e status de validação. Manter coluna `valor_original` durante migração.

## Regra

Correção precisa ser versionada, aprovada e documentada; nunca sobrescrever o original.

## Teste

Validação de tipo, intervalo, duplicidade, lacuna, reconciliação e consistência entre relatório e planilha.

## Relações justificadas

- [[Fonte - Dados Marketing]] — é o arquivo auditado.
- [[Dicionario-de-KPIs]] — define schema.
- [[Pendencias-de-Dados]] — lista resolução.

## Fontes e rastreabilidade

- [[Fonte - Dados Marketing]]
- [[Fonte - Relatorios Mensais de Marketing]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.

## Dados disponíveis nas fontes

Esta nota possui informações complementares nos seguintes arquivos-fonte:

- `Dados ACIRV/Notas\Como fazer o relatório de março ser de alto nível.md`
- `Dados ACIRV/Notas\Como é realizado a reunião de apresentação de Métricas de todo dia 30 - Modelo da Vivi.md`
- `Dados ACIRV/Notas\Contraproposta para o relatório de abril.md`
- `Dados ACIRV/Notas\Dados sobre o Conecta Saúde 2º ed..md`
- `Dados ACIRV/Notas\Todos os dados para relatório de métricas.md`

> **Status da integração**: Dados identificados. Aguardando extração e incorporação dirigida.
