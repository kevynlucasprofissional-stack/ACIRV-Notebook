---
id: infraestrutura-contrato-de-nota-canonica-narrativa
titulo: Contrato-de-Nota-Canonica-Narrativa
aliases: [contrato-nota-canonica, padrão-editorial-notas]
tipo: infraestrutura
status: ativo
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-17'
ultima_revisao: '2026-09-17'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- infraestrutura
- padrao-editorial
- narrativa
- evidencia
fontes_documentais:
- '[[Politica-de-Fontes-e-Evidencia]]'
- '[[Decisao-Arquitetural-Ingestao-Narrativa]]'
notas_relacionadas:
- '[[Sistema-de-Ingestao]]'
- '[[Metodologia]]'
- '[[Schema-de-Propriedades]]'
confidencialidade: interno
subtipo: contrato_editorial
---

# Contrato da Nota Canônica Narrativa — ACIRV Notebook

> [!summary] Síntese
> Padrão editorial e estrutural da camada canônica (`00-*` a `99-*`). Define como o ChatGPT Agendado deve construir notas narrativas orientadas por dados, evidências e rastreabilidade temporal.

## 1. Princípio Fundamental

Uma nota canônica no ACIRV Notebook **não é** um dump de banco de dados, uma tabela isolada de fatos ou um resumo burocrático. Ela é uma **narrativa institucional orientada por evidências**.

Ela deve contar a história real do projeto, processo, evento, métrica ou decisão, integrando dados quantitativos no fluxo explicativo e permitindo que qualquer leitor (humano ou IA) compreenda o contexto completo.

---

## 2. As 10 Perguntas Orientadoras da Narrativa

Sempre que pertinente ao tipo de nota, o texto deve responder a:

1. **O que é isso?** — Contextualização síntese inteligível de abertura.
2. **O que aconteceu?** — Reconstrução narrativa clara dos fatos relevantes.
3. **Como isso evoluiu?** — Cronologia, fases e mudanças de estado ao longo do tempo.
4. **O que os dados mostram?** — Números e métricas inseridos onde explicam a história (storytelling orientado a dados).
5. **O que mudou?** — Alterações de estratégia, decisões formais, orçamento ou cronograma.
6. **Por que isso importa?** — Impacto, valor gerado ou consequências operacionais para a ACIRV e associados.
7. **O que sabemos com certeza?** — Fatos sustentados por fontes documentais ou registros primários.
8. **O que é interpretação?** — Análises e sínteses operacionais claramente distinguidas do fato bruto.
9. **O que ainda está incerto?** — Pendências de validação, lacunas de dados e divergências temporais.
10. **Qual é o estado atual?** — Síntese do status operacional presente.

---

## 3. Storytelling Orientado a Dados

Os números e métricas **não devem ser isolados em tabelas sem contexto** quando fizerem parte de uma narrativa explicativa.

### Exemplo Inadequado (Mecanicista):
```markdown
| Métrica | Valor |
| Visualizações | 3.340.052 |
| Interações | 6.103 |
| Seguidores | 473 |
```

### Exemplo Desejado (Narrativo Orientado a Dados):
```markdown
Em agosto de 2026, a escala da comunicação digital da ACIRV expandiu significativamente:
as visualizações no Instagram atingiram **3.340.052**, acompanhadas por **6.103 interações** e
um ganho de **473 novos seguidores**. Esse salto coincide com o período de intensificação
da divulgação da SudoExpo 2026 e do lançamento do Conecta SudoExpo, indicando alta tração
da pauta institucional durante a preparação do evento.
```

*Regra:* Nunca inventar causalidade não comprovada; integrar números onde eles explicam o efeito.

---

## 4. Distinção Temporal Obrigatória

A evolução de iniciativas exige diferenciar explicitamente os momentos do ciclo de vida:

- `planejado` (intenção / plano original);
- `aprovado` (decisão formal da diretoria);
- `agendado` (data/horário definidos em cronograma);
- `executado` (realização concreta);
- `observado` (dados capturados pós-execução);
- `resultado` (análise de efeito e alcance).

*Exemplo:* Um evento planejado para abril que começou em maio **não é uma contradição**, mas sim uma evolução temporal registrada.

---

## 5. Fatos × Interpretações × Incertezas

A nota deve manter separação transparente entre as camadas de evidência:

- **Fato Documentado:** Afirmação direta sustentada por documento primário em `000-Arquivos-originais/`.
- **Interpretação Operacional:** Análise da equipe ou do ChatGPT identificada como síntese/análise.
- **Incerteza / Pendência:** Registrada em callout `> [!warning]` ou `> [!note]` com indicação clara do que aguarda validação.

---

## 6. Rastreabilidade e Seção de Fontes

Toda nota canônica deve conter uma seção final de **Fontes e Rastreabilidade**:

```markdown
## Fontes e Rastreabilidade

- `000-Arquivos-originais/Relatório de Agosto.md` — blob `f029d200` (Métricas de agosto)
- `000-Arquivos-originais/310826 - Mudanças mais recentes do cronograma.md` — blob `e48fd481` (Cronograma)
- Validação humana registrada em `99-Pendencias/Validacoes-Humanas-Necessarias.md` (17/09/2026)
```

A nota não precisa ter marcação de metadata em cada frase da prosa; a seção final e os claims associados garantem a rastreabilidade auditável sem poluir a leitura humana.
