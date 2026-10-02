---
id: metrica-historico-de-kpis-mensais
titulo: Historico-de-KPIs-Mensais
aliases: []
tipo: metrica
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.2'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-09-22'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- dado_calculado
- interpretacao_operacional
tags:
- metricas
- serie
fontes_documentais:
- '[[Fonte - Dados Marketing]]'
- '000-Arquivos-originais/Relatório de Agosto.md'
notas_relacionadas:
- '[[Dicionario-de-KPIs]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
- '[[Painel-Executivo]]'
- '[[Diagnostico-Instagram-Agosto-Setembro-2026]]'
confidencialidade: interno
subtipo: serie_indicador
---

# Historico-de-KPIs-Mensais

> [!summary] Síntese
> Série mensal consolidada para leitura temporal. O dado de julho/agosto de 2026 mostra um ponto importante: **visualizações cresceram fortemente enquanto interações caíram**, portanto atenção, interação e crescimento de audiência precisam ser analisados separadamente. A série não autoriza atribuir causalidade a evento ou campanha sem cruzamento adicional.

## Série oficial observada

| Mês | Seguidores totais | Ganhos / métrica de seguidores¹ | Visualizações | Feed | Stories | Reels | Interações |
|---|---:|---:|---:|---:|---:|---:|---:|
| jun/2025 | 6.811 | — | — | — | — | — | — |
| ago/2025 | 7.424 | 305 | 141.000 | 45 | 182 | 9 | 3.700 |
| set/2025 | 7.729 | 291 | 310.000 | 56 | 218 | 7 | 4.991 |
| out/2025 | 8.002 | 325 | 330.000 | 68 | 296 | 5 | 4.817 |
| nov/2025 | 8.203 | 236 | 430.445 | 60 | 187 | 16 | 2.869 |
| dez/2025 | 8.314 | 126 | 238.492 | 31 | 162 | 16 | 2.484 |
| jan/2026 | 8.448 | 153 | 145.864 | 24 | 51 | 2 | 1.845 |
| fev/2026 | 8.603 | 158 | 200.193 | 25 | 206 | 7 | 2.822 |
| mar/2026 | 8.885 | 217 | 257.518 | 40 | 325 | 6 | 3.039 |
| abr/2026 | 9.039 | 218 | 1.466.852 | 41 | 230 | 4 | 3.600 |
| mai/2026 | 9.168 | 128 | 1.421.535 | 34 | 166 | 16 | 3.995 |
| jul/2026² | — | 366 | 1.465.844 | 41 | 109 | 9 | 9.882 |
| ago/2026² | — | 473 | 3.340.052 | 52 | 92 | 4 | 6.103 |

¹ A fonte mensal de julho/agosto usa o rótulo **“Seguidores”** para 366 e 473, mas não informa no próprio quadro se é total de base, ganho bruto ou saldo. Como esses números são incompatíveis com a base total histórica, a camada canônica os mantém como **métrica de seguidores reportada**, sem fingir semântica ainda não confirmada.

² Dados de julho/agosto de 2026 na versão atual de `000-Arquivos-originais/Relatório de Agosto.md`, blob `8a148b35af2b2990f99b4690ae707032c9db7da6`. A versão canônica anterior citava o blob `f029d200`; a mudança de SHA é tratada como nova versão da mesma fonte, preservando a proveniência.

## Comparação julho → agosto de 2026

| Métrica | Julho | Agosto | Variação registrada |
|---|---:|---:|---:|
| Feed | 41 | 52 | +26,83% |
| Stories | 109 | 92 | -15,60% |
| Reels | 9 | 4 | -55,56% |
| Vídeos produzidos | 2 | 9 | +350,00% |
| Visualizações | 1.465.844 | 3.340.052 | +127,86% |
| Interações | 9.882 | 6.103 | -38,24% |
| Métrica “Seguidores” da fonte | 366 | 473 | +29,23% |

## Leitura operacional

Agosto teve **mais que o dobro de visualizações de julho**, mas **menos interações**. Isso impede uma leitura simplista de “mais alcance = melhor desempenho em tudo”.

A reconciliação por publicação esclarece parte do salto de agosto: no MASTER, 10 dos 52 posts foram promovidos e concentraram 93,4% das visualizações somadas nas linhas. Ao mesmo tempo, os 42 posts não promovidos concentraram 85,5% das interações e 83,3% dos seguidores atribuídos no arquivo.

Isso é evidência descritiva do conjunto, não prova causal. O total mensal da conta continua distinto da soma das publicações.

## Reconciliação do grão de agosto

O MASTER auditado de agosto soma **1.912.836 visualizações** e **4.629 interações** nas 52 publicações. O relatório mensal registra **3.340.052 visualizações** e **6.103 interações**.

A diferença é preservada porque as fontes têm grãos diferentes. O MASTER é referência por publicação; o relatório mensal é referência para o agregado da conta. Não substituir nem somar os dois.

## Contexto operacional

O mesmo relatório mensal registra aumento de **4 para 12 eventos** e de **8 para 10 reuniões** entre julho e agosto, além de três eventos ACIRV em agosto. Esse aumento de intensidade operacional pode ser usado como contexto, mas não prova causalidade sobre o desempenho do Instagram.

## Estado de setembro/SudoExpo

A fonte disponível de setembro cobre **01–14/09/2026**, portanto ainda não fecha o mês. Ela contém 86 posts, 445.217 visualizações e 17.172 interações no próprio resumo do workbook.

O painel de setembro também mudou de schema e deixou de expor “Alcance/Contas alcançadas” de forma equivalente. Por isso:

- não adicionar setembro como mês fechado nesta série;
- não fabricar alcance para manter continuidade;
- manter pré-feira, 09–12/09 e pós-feira como recortes analíticos;
- tratar qualquer “efeito SudoExpo” como associação temporal.

Ver [[Diagnostico-Instagram-Agosto-Setembro-2026]].

## Limitações

- junho de 2025 tem cobertura parcial;
- a série mistura fontes mensais e janelas de plataforma;
- “ganhos” e “seguidores” podem ter semântica diferente por fonte;
- totais mensais não explicam distribuição por publicação;
- o salto de abril/maio exige revisão histórica de método;
- agosto já foi reconciliado no grão por publicação, mas não é semanticamente igual ao total da conta;
- setembro disponível é parcial (01–14/09) e apresenta quebra de schema.

## Uso

Antes de atualizar:

1. preservar a versão anterior;
2. registrar o blob da fonte;
3. confirmar período e unidade;
4. aplicar [[Dicionario-de-KPIs]];
5. registrar mudança de método;
6. cruzar com [[Qualidade-dos-Dados-de-Marketing]].

## Relações justificadas

- [[Dicionario-de-KPIs]] — define os campos.
- [[Qualidade-dos-Dados-de-Marketing]] — controla divergências.
- [[Painel-Executivo]] — resume sinais.

## Fontes e rastreabilidade

- `000-Arquivos-originais/Relatório de Agosto.md` — blob atual `8a148b35af2b2990f99b4690ae707032c9db7da6`.
- `.../instagram_acirvoficial_insights_agosto_2026_MASTER(1).xlsx` — blob `ccc1d627be0468abb41c650b18974161b6f741b1`.
- `.../instagram_acirvoficial_insights_setembro_2026.xlsx` — blob `993eb1eaab95589148903864c883937571951848`.
- [[Diagnostico-Instagram-Agosto-Setembro-2026]].
- [[Fonte - Dados Marketing]] — série histórica anterior.

## Limitações e revisão

A reconciliação por publicação de agosto foi concluída. Permanecem pendentes a semântica exata do rótulo mensal “Seguidores” (366/473) e o fechamento completo de setembro após 30/09.
