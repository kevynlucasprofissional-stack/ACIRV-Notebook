---
id: metrica-diagnostico-instagram-agosto-setembro-2026
titulo: Diagnostico-Instagram-Agosto-Setembro-2026
aliases: [Instagram agosto e setembro 2026]
tipo: metrica
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
- metricas
- instagram
- sudoexpo
fontes_documentais:
- '000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Redes sociais/instagram_acirvoficial_insights_agosto_2026.xlsx'
- '000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Redes sociais/instagram_acirvoficial_insights_agosto_2026_MASTER(1).xlsx'
- '000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Redes sociais/instagram_acirvoficial_insights_setembro_2026.xlsx'
- '85-Bases-e-Consultas/Instagram-Publicacoes-2026-08-09.csv'
notas_relacionadas:
- '[[Instagram]]'
- '[[Historico-de-KPIs-Mensais]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
confidencialidade: interno
subtipo: analise_periodo
---

# Diagnostico-Instagram-Agosto-Setembro-2026

> [!summary] Síntese
> A reconciliação separa **totais mensais da conta** de **métricas por publicação**. Agosto possui um MASTER auditado e completo para 52 posts. Setembro contém 86 posts apenas entre **01 e 14/09/2026**, com mudança de schema do Instagram; por isso é uma fotografia parcial, não um mês fechado.

## Agosto — escolha da fonte

Foram encontrados:

1. `instagram_acirvoficial_insights_agosto_2026.xlsx` — blob `c32a87ca22e0a640b6ac2ec83bb2c136bb632332`;
2. `instagram_acirvoficial_insights_agosto_2026_MASTER(1).xlsx` — blob `ccc1d627be0468abb41c650b18974161b6f741b1`.

A camada canônica passa a usar o **MASTER como fonte preferida por publicação**, porque ele contém os mesmos 52 itens/1.089 métricas brutas e adiciona uma aba de auditoria. A auditoria registra:

- 167 itens enumerados no grid;
- 52 itens da lista mestre encontrados;
- 0 itens da lista mestre fora do grid;
- fronteira validada de 01/08 a 30/08;
- falsos positivos de setembro reclassificados pela data do elemento `<time datetime>`;
- conclusão explícita de que o **MASTER de 52 posts está completo para agosto/2026**.

O arquivo original continua preservado como fonte e não é apagado.

## Agosto — resultados por publicação

No MASTER:

- 52 posts;
- 42 orgânicos;
- 10 promovidos;
- 22 colaborativos;
- 3 posts com alguma métrica ausente;
- 1.912.836 visualizações somadas nas linhas;
- 4.629 interações reportadas nas linhas;
- 216 novos seguidores atribuídos;
- 1.213 atividades do perfil;
- 451 visitas ao perfil;
- 546 toques em links externos.

### Orgânico × promovido

| Sinal | Orgânico | Promovido |
|---|---:|---:|
| Posts | 42 | 10 |
| Visualizações | 126.930 (6,6%) | 1.785.906 (93,4%) |
| Interações | 3.956 (85,5%) | 673 (14,5%) |
| Novos seguidores | 180 (83,3%) | 36 (16,7%) |
| Atividade do perfil | 672 (55,4%) | 541 (44,6%) |

Leitura descritiva: no conjunto de agosto, a promoção concentrou distribuição, enquanto os posts não promovidos concentraram a maior parte das interações e seguidores atribuídos. Isso **não prova** que orgânico seja causalmente superior: seleção de quais posts foram promovidos, objetivo de campanha, tema e público confundem a comparação.

## Por que 1,91 mi não substitui 3,34 mi

`[[Historico-de-KPIs-Mensais]]` registra **3.340.052 visualizações** e **6.103 interações** para agosto no relatório mensal.

O MASTER por publicação soma **1.912.836 visualizações** e **4.629 interações**.

Isso não é tratado como erro aritmético. São fontes com grãos diferentes:

- relatório mensal: visão agregada da conta/período;
- MASTER: soma de 52 publicações inventariadas;
- Stories e outras superfícies podem entrar na visão mensal sem existir na mesma forma na tabela de posts.

**Regra:** não substituir o total mensal pela soma das publicações e não somar os dois.

## Setembro — escopo real

O workbook `instagram_acirvoficial_insights_setembro_2026.xlsx` cobre somente **01–14/09/2026**.

Controle do arquivo:

- 86 posts;
- 42 próprios;
- 44 colaborações;
- 27 parceiros distintos;
- 1 post promovido reportado;
- 1.696 métricas brutas;
- 445.217 visualizações;
- 17.172 interações.

Componentes agregados no próprio workbook:

- 13.589 curtidas;
- 1.357 comentários;
- 1.670 compartilhamentos;
- 238 salvamentos.

### Próprio × colaboração

| Grupo | Posts | Visualizações | Interações |
|---|---:|---:|---:|
| Próprio | 42 | 239.991 (53,9%) | 6.004 (35,0%) |
| Colaboração | 44 | 205.226 (46,1%) | 11.168 (65,0%) |

Há associação entre colaborações e maior participação nas interações deste recorte, mas o período contém SudoExpo, parceiros, temas e um grande outlier. Não usar como efeito causal da coautoria.

## Concentração de setembro

O post de 12/09 com `sarahdaotica` registrou:

- 115.839 visualizações;
- 8.380 interações.

Ele responde sozinho por aproximadamente **48,8% das 17.172 interações** do arquivo parcial. Qualquer média de setembro deve ser apresentada com mediana/outliers ou com essa concentração explícita.

## Pré-feira × feira × pós-feira

Usando apenas métricas cuja coluna permaneceu consistente na base derivada:

| Recorte | Posts | Visualizações | Compartilhamentos |
|---|---:|---:|---:|
| 01–08/09 | 36 | 159.918 | 687 |
| 09–12/09 | 41 | 273.549 | 951 |
| 13–14/09 | 9 | 11.750 | 32 |

O intervalo da feira concentra **61,4% das visualizações** do arquivo parcial (273.549 / 445.217). Isso é **associação temporal**: o próprio volume de posts e a presença de colaborações/outliers mudam entre os recortes.

## Quebra de schema em setembro

O próprio `Controle` do workbook avisa que o painel de setembro **não expõe mais “Alcance/Contas alcançadas”** da mesma forma. Existem `Visualizadores` e, em alguns posts, `Contas Meta alcançadas`.

Também há campos em que o painel mostra percentuais/texto quando se esperaria um valor numérico. A base derivada preserva:

- valor bruto;
- valor normalizado somente quando é numericamente seguro;
- `metricas_ausentes`;
- notas de coleta;
- SHA e caminho da fonte.

Portanto, setembro não deve receber um “alcance” inventado para manter continuidade visual.

## Base derivada

`85-Bases-e-Consultas/Instagram-Publicacoes-2026-08-09.csv` contém 138 linhas:

- 52 de agosto;
- 86 de 01–14/09.

Ela inclui origem e status de validação por período. Agosto é marcado `master_validado_completo_agosto`; setembro, `parcial_setembro_com_quebra_de_schema`.

## Decisões de curação

- MASTER é a referência de agosto por publicação;
- relatório mensal continua referência para totais mensais da conta;
- setembro permanece parcial até haver fechamento de 01–30/09;
- não fabricar alcance em setembro;
- não atribuir à SudoExpo causalidade baseada apenas na coincidência 09–12/09;
- manter orgânico/promovido e próprio/colaboração como dimensões, não como explicações causais.

## Fontes e rastreabilidade

- agosto original — blob `c32a87ca22e0a640b6ac2ec83bb2c136bb632332`;
- agosto MASTER — blob `ccc1d627be0468abb41c650b18974161b6f741b1`;
- setembro parcial — blob `993eb1eaab95589148903864c883937571951848`.
