---
id: auditoria-mapa-maturidade-curadoria
titulo: Mapa-de-Maturidade-da-Curadoria
tipo: auditoria
status: ativo
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-22'
ultima_revisao: '2026-09-22'
grau_confianca: medio_alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- auditoria
- maturidade
- curadoria
- antirregressao
confidencialidade: interno
subtipo: controle_curatorial
---

# Mapa-de-Maturidade-da-Curadoria

> [!summary] Finalidade
> Controle persistente para orientar a auditoria diária do ACIRV Notebook. O mapa não mede “quantidade de texto”: ele registra onde a camada curada já explica bem a realidade, onde ainda existem lacunas e quais áreas devem ser protegidas de retrabalho ou regressão.

## Escala

- **insuficiente** — fontes relevantes existem, mas a camada canônica ainda não representa adequadamente o domínio.
- **em_evolucao** — já existe estrutura útil, porém faltam reconciliação, evidência, narrativa ou fechamento importantes.
- **bom** — conhecimento bem organizado, rastreável e operacionalmente útil; ainda há melhorias materiais identificáveis.
- **excelente** — cobertura, semântica, narrativa, proveniência, limites e conexões estão suficientemente maduros para o uso atual. Só reabrir com motivo concreto.

Uma área excelente não é “final para sempre”. Ela fica protegida de mudanças cosméticas até surgir fonte nova material, contradição, desatualização, erro factual, problema de proveniência ou melhoria claramente superior e demonstrável.

## Critérios observados

A avaliação considera conjuntamente:

1. cobertura das fontes importantes;
2. qualidade semântica;
3. qualidade narrativa;
4. utilidade operacional;
5. proveniência e rastreabilidade;
6. separação entre fato, cálculo, interpretação e hipótese;
7. tratamento de contradições;
8. atualidade;
9. conexão com outras notas;
10. redundância e risco de retrabalho.

## Estado em 22/09/2026

| Domínio | Maturidade | Justificativa | Próximo gatilho de revisão |
|---|---|---|---|
| Estratégia e metas 2026 | **bom** | Norte estratégico e metas estão separados de execução; ainda faltam proprietários, linhas de base e fórmulas oficiais para parte das metas. | confirmação das fórmulas e dados de associados |
| Operação, priorização e capacidade | **bom** | O problema de múltiplos solicitantes, critérios de prioridade e limites de WIP já estão semanticamente separados. O novo SCRUM acrescenta evidência longitudinal da operação real. | integrar melhor histórico do board, esforço e bloqueios |
| SudoExpo 2026 | **bom** | A nota já conecta planejamento, execução, evidência, percepção e resultado posterior, preservando conflitos. O SCRUM agora reforça a trajetória operacional. | reconciliação estruturada de execução, pesquisas e Instagram |
| SudoExpo Match | **em_evolucao** | Produto, trajetória e metodologia estão bem definidos, mas os resultados quantitativos continuam pendentes de recomputação e follow-up. | recalcular JSON, pesquisas e continuidade das conexões |
| Instagram e analytics de agosto | **em_evolucao** | Já existe narrativa útil sobre descoberta, ressonância, intenção e aquisição, mas os números derivados ainda precisam ser reconciliados com a planilha MASTER. | reconciliação MASTER + setembro |
| Tom de voz | **excelente** | A nota distingue versões vigentes e futuras, incorpora a evolução histórica, explica regras e evita transformar propostas da V6 em regra atual. | nova validação humana ou nova versão efetivamente adotada |
| Assessoria de imprensa | **bom** | Processo, critério de notícia, distribuição e follow-up estão organizados; listas nominais voláteis permanecem nas fontes. | mudança relevante de processo/canais ou evidência de desempenho |
| Serviços e benefícios | **bom** | Categorias, gratuidade validada das consultorias e governança básica estão curadas; dados de uso/resultado ainda são limitados. | dados de utilização, satisfação e conversão |
| Governança de ingestão e proveniência | **em_evolucao** | Políticas, Safety Gate e auditorias estão maduras, mas o ledger ainda precisa alcançar o grande lote recente de originais. | nova execução determinística do inventário/ledger |
| Backlog e execução atual | **em_evolucao** | O backlog canônico preserva memória histórica, mas o SCRUM recém-adicionado ainda não foi totalmente reconciliado com tarefas abertas atuais. | reconciliação semântica SCRUM × backlog canônico |

## Área protegida nesta sessão

### Tom de voz — excelente

Foi usada como amostra antirregressão.

A nota [[Manual-Operacional-de-Tom-de-Voz]] já contém estado das versões V4.5, V5 e V6, regras vigentes, evolução ainda não concluída, fonte principal mais completa, distinção entre regra atual e proposta futura e limites de revisão.

Não foi encontrada razão material para reescrevê-la nesta sessão. Portanto, **nenhuma alteração foi feita apenas para melhorar o texto**.

## Área promovida nesta sessão

### Operação, priorização e capacidade

O novo conjunto de snapshots do SCRUM permite contar uma história antes fragmentada:

**problema de prioridades concorrentes → necessidade de tornar escolhas visíveis → operação semanal registrada → variação real de carga → concentração progressiva da SudoExpo → retorno ao fechamento e aprendizado pós-evento.**

Essa história foi promovida para [[Evolucao-da-Operacao-de-Marketing-2026]] e para notas operacionais relacionadas.

## Regra para próximas auditorias

A auditoria diária deve escolher áreas pelo **valor marginal da revisão**, não pela facilidade de editar.

Ordem preferencial: insuficiente → em_evolucao → bom → excelente apenas com gatilho concreto ou amostragem antirregressão.

Se uma área auditada continuar excelente e não houver nova evidência, registrar a estabilidade e seguir adiante.

## Fontes desta avaliação

- camada canônica atual do ACIRV Notebook em 22/09/2026;
- 000-Arquivos-originais/SCRUM da ACIRV + Vcom/ — snapshots do board ACIRV + VCOM: SCRUM;
- 000-Arquivos-originais/HD-ACIRV/03-Metricas-e-Relatorios/KEVYN-DADOS-ACIRV/Documentos/Relatório de métrica Março parte 1 de 2.txt;
- 000-Arquivos-originais/HD-ACIRV/03-Metricas-e-Relatorios/KEVYN-DADOS-ACIRV/Documentos/Relatório de métrica Março parte 2 de 2.txt;
- [[Curadoria-Delta-HD-Externo-2026-09-22]].

## Limitações

Este mapa é um instrumento de governança curatorial. Ele não substitui validação factual de cada domínio nem significa que uma área classificada como excelente contém todas as fontes existentes.
