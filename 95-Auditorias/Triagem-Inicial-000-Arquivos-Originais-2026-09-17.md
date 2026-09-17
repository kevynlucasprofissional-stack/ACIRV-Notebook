---
id: auditoria-triagem-inicial-000-arquivos-originais-2026-09-17
titulo: Triagem-Inicial-000-Arquivos-Originais-2026-09-17
aliases: []
tipo: auditoria
status: em_revisao
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
- auditoria
- ingestao
- fontes
fontes_documentais:
- '[[Fonte - Planejamento Estrategico 2026]]'
- '[[Fonte - Notas Operacionais]]'
notas_relacionadas:
- '[[Metodologia]]'
- '[[Manifesto-de-Preservacao-de-Fontes]]'
- '[[Politica-de-Fontes-e-Evidencia]]'
- '[[Privacidade-e-Seguranca]]'
- '[[Validacoes-Humanas-Necessarias]]'
confidencialidade: interno
subtipo: triagem
---

# Triagem-Inicial-000-Arquivos-Originais-2026-09-17

> [!summary] Síntese
> Primeira triagem da camada `000-Arquivos-originais/` após sua formalização como fonte primária imutável para IAs. A análise confirmou que o corpus contém material institucional rico, versões históricas, documentos operacionais, conteúdo de projetos e também arquivos potencialmente sensíveis. Nenhum arquivo da pasta foi alterado.

## Linha de base

- pasta observada: `000-Arquivos-originais/`;
- tree SHA observado em `main` durante esta triagem: `4c95d74a2cb2546eff657452b1fe37dd650d58d7`;
- política aplicada: somente leitura;
- alterações realizadas dentro de `000-Arquivos-originais/`: **zero**.

O tree SHA serve apenas como referência histórica desta execução. A rotina diária deve usar histórico/diffs do Git para identificar arquivos novos ou modificados sem depender exclusivamente deste valor.

## Classes de material encontradas

A camada original contém, entre outros:

- planejamentos anuais e mensais;
- reuniões, transcrições e SCRUMs;
- dossiês de eventos e projetos;
- relatórios de métricas;
- manuais e versões de tom de voz;
- dados de serviços e produtos;
- materiais de SudoExpo, Conecta, ACIRV Mulher e campanhas;
- diários e notas livres;
- protótipos e documentação técnica;
- arquivos potencialmente sensíveis.

Isso confirma que a camada original funciona melhor como **corpus livre de captura**, enquanto `00-*` a `99-*` deve funcionar como conhecimento derivado e consolidado.

## Risco de segurança detectado sem abertura de conteúdo

Foram identificados, apenas pelo nome/caminho, arquivos potencialmente relacionados a credenciais, incluindo exemplos como:

- `000-Arquivos-originais/Contas e Senhas.md`;
- `000-Arquivos-originais/Minha Chave API Antropic.md`.

Esses arquivos **não foram abertos nem lidos** nesta triagem.

Também existem artefatos ZIP de protótipos cujo conteúdo histórico pode conter `.env`, conforme documentação de segurança já existente no vault.

### Ação humana recomendada

1. assumir que qualquer credencial real já versionada pode estar comprometida;
2. rotacionar/revogar a credencial antes de qualquer tentativa de limpeza;
3. migrar valores ativos para um gerenciador de segredos;
4. avaliar remoção segura do arquivo e, se necessário, reescrita do histórico Git;
5. não copiar valores para notas canônicas, issues, PRs ou logs de automação.

## Delta estratégico identificado

### Estratégia ACIRV 2026

O arquivo original `Dados sobre o novo tom de voz e planejamento de 2026.md` explicita três resultados institucionais que merecem permanecer visíveis na camada canônica:

- **Retenção**: aumentar orgulho de pertencer, percepção de retorno e participação em eventos;
- **Captação**: converter visibilidade e autoridade em novas adesões qualificadas;
- **Valor percebido**: comunicar benefícios tangíveis e entregas institucionais continuamente.

Também explicita os cinco pilares já representados no vault: Pertencimento, Resultados, Autoridade, Proximidade e Captação.

### Linhas recorrentes de conteúdo

A mesma fonte registra linhas editoriais recorrentes:

- `#SouAssociadoACIRV` — mensal;
- Empresário Inspirador — quinzenal;
- ACIRV em Ação — semanal;
- Benefícios do Associado — quinzenal;
- Notícias que Inspiram — quinzenal;
- Eventos & Convites — conforme calendário.

Essas frequências são planejamento documentado, não prova de execução real.

### Funil de captação e retenção

O planejamento também registra tráfego pago segmentado por setor e o uso de boletim mensal/WhatsApp como mecanismos de relacionamento e retenção. A camada canônica deve preservar a intenção estratégica separada da execução observada.

## Conflitos documentais detectados

### Campanha de pertencimento: abril × maio

O planejamento anual contém uma inconsistência interna: uma seção identifica a Campanha 2 como `abril`, enquanto o cronograma do próprio documento a coloca em `maio`. Um dossiê posterior, criado em 28/05/2026, define explicitamente **Maio de 2026** como período principal de `Eu Faço Parte do Movimento`.

**Tratamento recomendado:** manter maio como estado canônico de maior sustentação documental, registrando que a fonte anual continha divergência interna. Não modificar a fonte original.

### Conecta ACIRV: Cota Diamante R$ 20 mil × R$ 18 mil

O planejamento anual do Conecta registra a cota Diamante como **R$ 20.000** em uma tabela e **R$ 18.000** na descrição detalhada subsequente.

**Tratamento recomendado:** não promover nenhum dos dois valores como preço oficial sem validação humana ou documento comercial posterior. A estrutura de cotas pode permanecer canônica; o valor deve ser marcado como divergente.

### Conecta: R$ 4 milhões como histórico e meta

A mesma fonte usa R$ 4 milhões tanto como valor já movimentado em edições anteriores quanto como meta anual de geração de conexões/negócios. Isso exige separar claramente:

- resultado histórico alegado;
- meta futura;
- metodologia de atribuição/comprovação.

A nota canônica já sinaliza risco de evidência para essa cifra; uma futura ingestão deve procurar fontes mais recentes e metodologia antes de uso público.

## Conhecimento já bem representado

A comparação inicial indica que várias áreas estruturadas já absorveram corretamente parte do corpus original:

- `01-Estrategia-e-Marca/Estrategia-ACIRV-2026.md` representa o norte estratégico;
- `01-Estrategia-e-Marca/Pilares-Estrategicos-de-Comunicacao.md` representa os cinco pilares;
- `03-Projetos-Campanhas-e-Eventos/Campanha-Eu-Faco-Parte.md` já incorpora grande parte do dossiê de pertencimento;
- `03-Projetos-Campanhas-e-Eventos/Campanha-Quem-Indica-Fortalece.md` já consolida a mecânica básica da campanha de indicação;
- `03-Projetos-Campanhas-e-Eventos/Conecta-ACIRV.md` já consolida objetivo, calendário, estrutura, metas e riscos básicos do projeto.

Isso mostra que a prioridade não deve ser “reescrever tudo”, e sim **delta ingestion**: localizar informação ainda ausente, mais recente ou conflitante e integrá-la seletivamente.

## Ordem recomendada para a ingestão histórica

1. **Estratégia e marca** — planejamento anual, tom de voz, design system e posicionamento.
2. **Projetos ativos/recorrentes** — Conecta, Café Entre Amigos, ACIRV Mulher, SudoExpo e serviços.
3. **Métricas** — relatórios mensais, dados de mídia e definições de KPI.
4. **Processos** — relatórios, briefing, release, cerimonial, aprovação e comunidade.
5. **Stakeholders e decisões** — apenas fatos institucionais necessários, com minimização de dados pessoais.
6. **Diários e notas livres** — processados por delta e relevância, evitando transformar pensamentos transitórios em verdade institucional.
7. **Projetos técnicos/protótipos** — separados do conhecimento institucional quando forem experimentais.

## Regra operacional para automação diária

A automação deve priorizar **mudanças desde a última execução**, não reler integralmente o corpus todos os dias. Para cada arquivo novo ou alterado:

1. verificar risco de segredo antes de abrir;
2. localizar possíveis destinos canônicos;
3. comparar com o estado existente;
4. promover apenas novidade material de alta confiança;
5. usar branch/PR pequena quando houver alteração automática;
6. encaminhar conflito ou ambiguidade para validação humana;
7. nunca tocar no original.

## Próximas validações humanas

- confirmar o tratamento oficial da Campanha de Pertencimento como maio/2026;
- confirmar valor final da Cota Diamante do Conecta 2026;
- validar origem/metodologia da cifra de R$ 4 milhões do Conecta;
- revisar e rotacionar qualquer credencial real presente no histórico do repositório;
- decidir política humana de remoção de segredos históricos sem conceder permissão de alteração de `000` a agentes.

## Resultado desta triagem

A arquitetura proposta é viável: `000-Arquivos-originais/` pode permanecer livre e imutável, enquanto a camada `00-*` a `99-*` recebe conhecimento consolidado de forma incremental. O risco principal deixa de ser “bagunça de arquivos” e passa a ser um problema controlável de **proveniência, atualização, conflito e segurança**.
