---
id: metrica-historico-de-kpis-mensais
titulo: Historico-de-KPIs-Mensais
aliases: []
tipo: metrica
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.1'
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

Hipóteses a investigar nas planilhas de Insights:

- maior distribuição de conteúdos com consumo passivo;
- peso de mídia promovida;
- diferença entre formatos;
- efeito de coautorias;
- concentração de visualizações em poucos posts;
- mudança na origem das visualizações;
- participação do período pré-SudoExpo no total de agosto.

Essas hipóteses não são resultados até serem testadas.

## Contexto operacional

O mesmo relatório mensal registra aumento de **4 para 12 eventos** e de **8 para 10 reuniões** entre julho e agosto, além de três eventos ACIRV em agosto. Esse aumento de intensidade operacional pode ser usado como contexto, mas não prova causalidade sobre o desempenho do Instagram.

## Regra para setembro/SudoExpo

As planilhas de setembro devem ser analisadas separando:

- pré-feira;
- 09–12/09;
- pós-feira;
- orgânico × promovido quando disponível;
- publicação × dia;
- coautoria quando disponível.

Qualquer efeito atribuído à SudoExpo precisa ser apresentado como associação temporal, salvo desenho causal adicional.

## Limitações

- junho de 2025 tem cobertura parcial;
- a série mistura fontes mensais e janelas de plataforma;
- “ganhos” e “seguidores” podem ter semântica diferente por fonte;
- totais mensais não explicam distribuição por publicação;
- o salto de abril/maio e o novo salto de agosto exigem reconciliação de metodologia.

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
- [[Fonte - Dados Marketing]] — série histórica anterior.

## Limitações e revisão

A próxima revisão deve reconciliar as planilhas de Insights de agosto e setembro com o relatório mensal antes de fechar definições de “seguidores”, orgânico/promovido e atribuição do pico de visualizações.
