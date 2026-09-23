---
id: metrica-qualidade-dos-dados-de-marketing
titulo: Qualidade-dos-Dados-de-Marketing
aliases: []
tipo: metrica
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.3'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-09-22'
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
- '[[Dicionario-de-KPIs]]'
- '[[Historico-de-KPIs-Mensais]]'
- '[[Pendencias-de-Dados]]'
- '[[SudoExpo-Match-Metodologia-de-Avaliacao]]'
- '[[Diagnostico-Instagram-Agosto-Setembro-2026]]'
- '[[Diagnostico-Longitudinal-Instagram-2025-2026]]'
confidencialidade: interno
subtipo: auditoria_dados
---

# Qualidade-dos-Dados-de-Marketing

> [!summary] Síntese
> A ACIRV possui dados suficientes para análises mais profundas, mas eles vêm de fontes com grãos, definições e janelas diferentes. A prioridade não é “juntar tudo”, e sim **reconciliar significado antes de comparar**. O pacote pós-SudoExpo aumenta a capacidade analítica e, ao mesmo tempo, aumenta o risco de precisão aparente sem equivalência semântica.

## Achados históricos

A base anterior já apresentava problemas como:

- intervalo invertido em visão geral;
- “último mês oficial” incompatível com linhas posteriores;
- datas em formato serial;
- percentuais misturando texto e número;
- lacunas;
- formatação monetária ambígua;
- divergência possível entre relatório e planilha.

Nenhum desses achados autoriza corrigir a fonte original. A correção deve existir apenas na camada derivada.

## Reconciliação do pacote de Instagram — concluída em 22/09/2026

As três fontes estruturadas foram abertas e reconciliadas:

1. `instagram_acirvoficial_insights_agosto_2026.xlsx`;
2. `instagram_acirvoficial_insights_agosto_2026_MASTER(1).xlsx`;
3. `instagram_acirvoficial_insights_setembro_2026.xlsx`.

### Agosto

O MASTER contém 52 posts, 1.089 linhas de métricas brutas e uma aba adicional de auditoria. A auditoria conclui que os 52 posts da lista mestre estão completos para agosto e explica os falsos positivos de setembro causados por data de upload/agendamento.

**Decisão:** usar o MASTER como fonte preferida no grão por publicação. O arquivo original continua preservado como proveniência.

### Diferença de grão em agosto

- relatório mensal da conta: 3.340.052 visualizações e 6.103 interações;
- soma do MASTER por publicação: 1.912.836 visualizações e 4.629 interações.

Não é uma divergência a “corrigir” por escolha de um número. São grãos diferentes e devem coexistir.

### Setembro

O workbook cobre somente **01–14/09/2026**, com 86 posts. O próprio `Controle` registra que o painel deixou de expor “Alcance/Contas alcançadas” da mesma forma e passou a mostrar `Visualizadores` e, em alguns casos, `Contas Meta alcançadas`.

**Decisão:** setembro permanece parcial; não fabricar alcance nem fechar o mês antecipadamente.

### Bases derivadas

- `85-Bases-e-Consultas/Instagram-Publicacoes-2026-08-09.csv` — 138 linhas, agosto MASTER + setembro parcial;
- `85-Bases-e-Consultas/Instagram-Publicacoes-Export-Meta-2025-2026.csv` — 200 linhas do export histórico `posts.json`.

## Regra de reconciliação

A camada derivada aplica as seguintes regras:

- identificar sempre período, grão, caminho e blob SHA;
- preservar o valor bruto ao lado do normalizado;
- normalizar somente valores numericamente seguros;
- não converter percentual, `9+`, `--` ou rótulo ambíguo em número exato;
- manter `promovido`, coautoria/vínculo e status de validação como dimensões;
- não substituir total da conta por soma de posts;
- registrar quebra de schema como quebra de série;
- manter fonte original imutável.

## Sinal concreto de divergência semântica

A versão atual de `Relatório de Agosto.md` usa a métrica **“Seguidores”** com valores 366 em julho e 473 em agosto. Esses números não parecem representar a base total de seguidores observada na série histórica, mas a fonte não explicita no quadro se são ganhos, saldo ou outra definição.

Por isso, [[Historico-de-KPIs-Mensais]] preserva o número e **não inventa a unidade**.

Esse é o padrão a seguir: quando o valor é conhecido, mas o significado exato não é, manter o dado e reduzir a confiança semântica.

## SudoExpo e causalidade

A presença da feira entre 09 e 12/09 permite um recorte temporal, mas não transforma automaticamente variações do Instagram em “efeito SudoExpo”.

A análise deve comparar:

- pré-feira;
- feira;
- pós-feira;
- conteúdo relacionado × não relacionado;
- orgânico × promovido;
- formatos;
- coautorias;
- posts outliers.

A linguagem correta é “houve aumento durante o período” ou “houve associação temporal”, salvo evidência causal mais forte.

## Pesquisas de satisfação

As duas planilhas de pesquisa são fontes de **percepção declarada** e devem ser mantidas separadas de telemetria.

Regras:

- preservar o número de respostas;
- documentar filtro;
- não descartar avaliação negativa só porque a pessoa não conheceu uma funcionalidade;
- quando conhecimento/uso alterar a interpretação, segmentar explicitamente;
- não expor resposta individual ou dado pessoal desnecessário;
- distinguir satisfação com estande, descoberta do Match e experiência efetiva de uso.

## SudoExpo Match

O JSON do Match é uma base comportamental distinta. As regras de score, origem estimada, funil e privacidade estão em [[SudoExpo-Match-Metodologia-de-Avaliacao]].

Não misturar:

- telemetria;
- decisão humana;
- conexão;
- pesquisa;
- negócio posterior.

## Escopo de privacidade do export Instagram

O export também contém DMs, buscas, histórico de links, dispositivos, login/logout, localização, possíveis telefones e outras telemetrias de conta.

Esses conjuntos **não são promovidos para a camada canônica por padrão**. A auditoria de privacidade já marca diversos caminhos como `LOCAL_NAO_SINCRONIZAR`. A existência de uma fonte não implica valor institucional suficiente para promoção.

Curtidas dadas pela conta, buscas e mensagens podem ser consultadas apenas em investigação específica com necessidade e tratamento de privacidade definidos.

## Severidade

Os dados são úteis, mas a heterogeneidade bloqueia:

- automação cega;
- soma entre fontes;
- comparação sem dicionário;
- causalidade automática;
- publicação de totais preliminares como resultado final.

## Processo de correção

1. identificar fonte e versão por blob SHA;
2. mapear schema e grão;
3. preservar valor original;
4. normalizar na camada derivada;
5. reconciliar divergências;
6. documentar fórmula;
7. validar amostra;
8. só então promover números para notas executivas.

## Relações justificadas

- [[Dicionario-de-KPIs]] — define semântica das métricas.
- [[Historico-de-KPIs-Mensais]] — recebe série validada.
- [[Pendencias-de-Dados]] — recebe lacunas.
- [[SudoExpo-Match-Metodologia-de-Avaliacao]] — governa dados do Match.
- [[Diagnostico-Instagram-Agosto-Setembro-2026]] — registra a reconciliação concluída.
- [[Diagnostico-Longitudinal-Instagram-2025-2026]] — governa a base histórica por publicação.

## Fontes e rastreabilidade

- `000-Arquivos-originais/Relatório de Agosto.md` — blob `8a148b35af2b2990f99b4690ae707032c9db7da6`.
- `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Redes sociais/instagram_acirvoficial_insights_agosto_2026.xlsx` — blob `c32a87ca22e0a640b6ac2ec83bb2c136bb632332`.
- `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Redes sociais/instagram_acirvoficial_insights_agosto_2026_MASTER(1).xlsx` — blob `ccc1d627be0468abb41c650b18974161b6f741b1`.
- `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Redes sociais/instagram_acirvoficial_insights_setembro_2026.xlsx` — blob `993eb1eaab95589148903864c883937571951848`.
- pesquisas pós-SudoExpo — blobs `c9331edee660716cecf43ca112f111398030a775` e `210c4fdbc4b4c35076bc1014e08ac8910dc4a13d`.

## Limitações e revisão

A extração/reconciliação por publicação foi concluída para agosto e para o recorte disponível de setembro. Permanecem como pendências: fechar 15–30/09, confirmar a semântica mensal de “Seguidores” (366/473) e manter vigilância sobre mudanças de schema da plataforma.
