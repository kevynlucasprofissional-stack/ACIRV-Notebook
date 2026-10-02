---
id: auditoria-mapa-maturidade-curadoria
titulo: Mapa-de-Maturidade-da-Curadoria
tipo: auditoria
status: ativo
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.3'
idioma: pt-BR
data_criacao: '2026-09-22'
ultima_revisao: '2026-09-23'
grau_confianca: medio_alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
- hipotese_de_trabalho
tags:
- auditoria
- maturidade
- curadoria
- antirregressao
confidencialidade: interno
subtipo: controle_curatorial
---

# Mapa-de-Maturidade-da-Curadoria

> [!summary] Função
> Controle persistente para orientar as auditorias diárias do ACIRV Notebook. O mapa mede o valor marginal de nova curadoria, não volume ou estética textual. Áreas maduras ficam protegidas contra retrabalho cosmético até surgir evidência material.

## Escala

- **insuficiente** — fontes relevantes existem, mas a camada canônica ainda não representa adequadamente o domínio.
- **em_evolucao** — já existe estrutura útil, porém faltam cobertura, reconciliação, evidência ou narrativa importantes.
- **bom** — conhecimento organizado, rastreável e operacionalmente útil; ainda há melhorias materiais identificáveis.
- **excelente** — cobertura, semântica, narrativa, proveniência e limites estão maduros para o escopo atual; só reabrir com motivo concreto.

Uma área excelente não é definitiva: pode ser reaberta por fonte nova material, contradição, desatualização, erro factual/proveniência ou melhoria semanticamente superior e demonstrável.

## Critérios observados

A avaliação considera conjuntamente cobertura das fontes, qualidade semântica e narrativa, utilidade operacional, proveniência, separação entre fato, cálculo, interpretação e hipótese, tratamento de contradições, atualidade, conexão entre notas e risco de retrabalho.

## Baseline de 23/09/2026

| Domínio | Estado | Justificativa | Próximo gatilho legítimo |
|---|---|---|---|
| Estratégia e metas 2026 | **bom** | Norte estratégico e metas estão separados da execução; ainda faltam proprietários, linhas de base e fórmulas oficiais para parte das metas. | confirmar fórmulas e dados de associados |
| Pesquisa, feedback e aprendizado | **bom** | A camada canônica agora explicita pesquisa como capacidade de decisão, separa percepção, comportamento, exposição e resultado, formaliza triangulação/longitudinalidade e trata “determinante” por força de evidência. Ainda falta institucionalizar rotina, responsáveis e registro de pesquisas/decisões. | executar primeiros ciclos com pergunta→decisão→nova medição e registrar responsáveis/instrumentos |
| Identidade visual e direção de arte | **excelente** | A curadoria de 23/09 consolidou fonte primária, Design System, ACIRV-MOOD e projeção operacional do Hermes em uma autoridade canônica única, com precedência explícita, tokens, repertório, acessibilidade, legibilidade, fotografia, backgrounds e critérios de aprovação. | nova decisão humana material, nova versão formal da identidade ou evidência de contradição/regressão no uso operacional |
| Priorização, capacidade e SCRUM | **bom** | Há diagnóstico de origem, critérios de prioridade, limites de WIP, evidência de ritual semanal e narrativa longitudinal março→setembro. | reconciliar backlog canônico com a semântica real do SCRUM/Trello e validar limites/SLA |
| SudoExpo 2026 | **bom** | Planejamento, execução, evidência, percepção e resultado posterior formam uma narrativa consistente, preservando conflitos. | fechar matriz Planejado×Entregue e resultados das pesquisas |
| SudoExpo Match | **bom** | Projeto, trajetória, metodologia e próximo ciclo estão separados entre fato, hipótese e resultado. | recomputar bases, reconciliar pesquisas e registrar follow-up comercial |
| Instagram e analytics de agosto | **bom** | A curadoria agora conecta série mensal, diagnóstico executivo, bases por publicação e leitura Pago×Orgânico. | fechar setembro e regenerar qualquer gráfico inconsistente |
| Tom de voz | **excelente** | V4.5/V5 vigentes e V6 futura estão distinguidas; regras, limites e proveniência estão claros. | nova versão formal aprovada ou evidência de mudança real de uso |
| Assessoria de imprensa | **bom** | Processo, critério de notícia, distribuição e follow-up estão organizados; listas voláteis permanecem nas fontes. | mudança relevante de processo/canais ou evidência de desempenho |
| Serviços e benefícios | **bom** | Categorias, gratuidade validada das consultorias e governança básica estão curadas; dados de uso ainda são limitados. | dados de utilização, satisfação e conversão |
| Governança de ingestão e proveniência | **em_evolucao** | Políticas, Safety Gate e auditorias estão maduras, mas o ledger ainda precisa alcançar lotes recentes de originais. | nova execução determinística do inventário/ledger |
| Backlog e execução atual | **em_evolucao** | O backlog preserva memória histórica, mas os 405 itens ainda não foram reconciliados com os snapshots recentes do SCRUM. | parse, deduplicação e primeiro lote de reconciliação backlog×SCRUM |
| Dados de associados/captação | **em_evolucao** | Existe meta, mas falta definição e número canônico de novos associados de 2026. | fonte institucional confirmada e definição da métrica |
| Check-in inteligente | **em_evolucao** | Projeto e guardrails estão estruturados, mas ainda não há piloto executado. | primeiro Café com MVP e dados de operação |

## Proteção antirregressão

### Tom de voz — excelente

Foi usado como amostra antirregressão. A nota [[Manual-Operacional-de-Tom-de-Voz]] distingue V4.5, V5 e V6, regras vigentes, evolução ainda não concluída e a fonte principal mais completa. Não foi encontrada razão material para reescrevê-la nesta sessão.

### Identidade visual e direção de arte — excelente

Os commits `7cf8d57597f5c2741120cc0a827021b48c11a892` e `a5c6dff451d19f5213f53515481a2d3d33a3efd8` fecharam uma lacuna arquitetural importante: a inteligência visual deixou de competir entre `ACIRV-MOOD-v1.md`, Design System e moodboard operacional. `01-Estrategia-e-Marca/Design-System-ACIRV.md` passou a ser a autoridade semântica única; `000-Arquivos-originais/DESIGN SYSTEM.md` permanece evidência primária imutável; e o moodboard do Hermes funciona como projeção operacional sincronizada. A área fica protegida contra novas reorganizações ou reescritas cosméticas enquanto essa arquitetura continuar coerente.

Antes de editar qualquer área `bom` ou `excelente`, verificar: há fonte material nova? existe lacuna semântica concreta? a mudança adiciona entendimento? as distinções epistemológicas anteriores foram preservadas?

## Áreas promovidas nesta consolidação

### Operação, priorização e capacidade

O cruzamento entre transcrições de março, snapshots do SCRUM, reunião de 21/09 e notas canônicas sustenta a trajetória:

**prioridades concorrentes informais → quadro visível → ritual semanal → memória de execução → variação real de carga → regras de capacidade e escalonamento.**

Essa história foi promovida para [[Evolucao-da-Operacao-de-Marketing-2026]], [[Evolucao-do-Sistema-de-Priorizacao-e-Execucao]] e notas operacionais relacionadas. O número de cards não é tratado como produtividade.

### Auditoria curatorial do SCRUM

O commit `9f3c9a55df6cb268035d5b60ae497a21750601ee` adicionou sete exports JSON em `000-Arquivos-originais/SCRUM da ACIRV + Vcom/`. Eles são uma fonte material para reconciliação do backlog, mas ainda devem ser tratados como snapshots: não se promoveu nenhum status operacional de aberto ou concluído sem deduplicação e interpretação segura.

### Inteligência visual

A sequência de curadoria de 23/09 conta uma história clara: **fonte original + decisões visuais recentes + moodboard operacional → consolidação temporária em ACIRV-MOOD → eliminação da duplicidade canônica → Design System único com projeção operacional sincronizada**. A mudança não altera a fonte original; ela resolve autoridade, precedência e manutenção futura da inteligência visual.

### Pesquisa, feedback e aprendizado

O novo estudo de 23/09 não foi promovido como verdade por si só. Ele funcionou como mapa para reler os três briefings primários e revelou uma arquitetura que estava parcialmente comprimida na nota canônica: **incerteza → pergunta → hipótese → variável → coleta → análise → decisão → mudança → nova medição**.

A curadoria também tornou explícitas quatro distinções necessárias para evitar conclusões frágeis:

- percepção declarada ≠ comportamento observado;
- não exposição ≠ insatisfação;
- associação ≠ causalidade;
- hipótese de determinante ≠ determinante comprovado.

O domínio sobe para **bom** porque a semântica e a proveniência ficaram sólidas, mas não para excelente: ainda falta provar que a ACIRV opera esse sistema de pesquisa de maneira recorrente, com responsáveis, instrumentos, decisões registradas e medições posteriores.

## Regra para próximas auditorias

Escolher áreas pelo **valor marginal da revisão**, na ordem insuficiente → em_evolucao → bom → excelente apenas com gatilho concreto ou amostragem antirregressão. Se uma área continuar estável e não houver evidência nova, registrar a estabilidade e seguir adiante.

## Fontes desta avaliação

- camada canônica atual do ACIRV Notebook em 23/09/2026;
- `01-Estrategia-e-Marca/Design-System-ACIRV.md`;
- `01-Estrategia-e-Marca/Pesquisa-e-Aprendizado-de-Marketing.md`;
- `000-Arquivos-originais/#PESQUISA - Um estudo sobre a questão das pesquisas dentro da ACIRV.md` — síntese secundária usada como mapa de lacunas;
- três briefings em `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Briefing inicial/` — fontes primárias da curadoria de pesquisa;
- commits `7cf8d57597f5c2741120cc0a827021b48c11a892` e `a5c6dff451d19f5213f53515481a2d3d33a3efd8`;
- `000-Arquivos-originais/DESIGN SYSTEM.md` — referenciado apenas como fonte primária preservada;
- `000-Arquivos-originais/SCRUM da ACIRV + Vcom/` — snapshots do board ACIRV + VCOM: SCRUM;
- `000-Arquivos-originais/HD-ACIRV/03-Metricas-e-Relatorios/KEVYN-DADOS-ACIRV/Documentos/Relatório de métrica Março parte 1 de 2.txt`;
- `000-Arquivos-originais/HD-ACIRV/03-Metricas-e-Relatorios/KEVYN-DADOS-ACIRV/Documentos/Relatório de métrica Março parte 2 de 2.txt`;
- [[Curadoria-Delta-HD-Externo-2026-09-22]];
- [[SudoExpo-Match]] e [[SudoExpo-Match-Metodologia-de-Avaliacao]].

## Limitações

Este mapa é instrumento de governança curatorial. Não substitui validação factual de cada domínio e não significa que uma área madura contenha todas as fontes existentes.
