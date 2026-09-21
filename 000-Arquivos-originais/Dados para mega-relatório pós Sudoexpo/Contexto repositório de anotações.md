# CONTEXTO UNIFICADO — APRESENTAÇÃO SUDOEXPO / MARKETING / IA — ACIRV

**Objetivo deste documento:** reunir, em um único contexto, todas as informações encontradas no repositório `kevynlucasprofissional-stack/ACIRV-Notebook` que ajudam a construir a apresentação descrita no briefing de SudoExpo, métricas, SudoExpo Match, Instagram, estratégia de marketing, Hermes Work e próximos passos.

**Repositório auditado:** `kevynlucasprofissional-stack/ACIRV-Notebook`  
**Branch:** `main`  
**HEAD auditado:** `c7a0c64b3776cc6ab09f5a09f9862f95250bc21e`  
**Data do HEAD:** 17/09/2026  
**Data de consolidação deste contexto:** 21/09/2026

---

# 1. COMO LER ESTE DOCUMENTO

O ACIRV-Notebook possui três camadas e essa distinção é importante para avaliar confiança:

1. `000-Arquivos-originais/` = fontes primárias humanas, preservadas e imutáveis para IAs.
2. `00-*` a `99-*` = camada canônica/estruturada, onde fatos e interpretações são consolidados com rastreabilidade.
3. `Hermes/` = camada operacional de agentes e automações; não vira automaticamente “verdade institucional”.

A própria política do repositório determina que fatos documentados, dados calculados, interpretações e hipóteses não devem ser misturados silenciosamente. Por isso, este contexto marca explicitamente lacunas e pontos que ainda exigem validação.

Fontes de governança:
- `README.md`
- `AGENTS.md`
- `98-Infraestrutura/Politica-de-Fontes-e-Evidencia.md`

---

# 2. RESUMO EXECUTIVO DA AUDITORIA DA CHECKLIST

## O que o repositório já resolve muito bem

O repositório já contém material suficiente para sustentar com boa segurança:

- o planejamento e o conceito do estande da ACIRV na SudoExpo;
- as principais decisões de comunicação e experiência do estande;
- a lógica e a arquitetura do SudoExpo Match;
- o significado técnico de match, score, interesse e conexão;
- um registro nominal das conexões realizadas na SudoExpo;
- o resultado mínimo registrado do piloto no Café Entre Amigos;
- o planejamento de conteúdo de agosto;
- os números agregados do Instagram em agosto;
- parte relevante do orçamento e dos KPIs da SudoExpo;
- a estratégia de comunicação da ACIRV;
- os pilares de marketing e critérios de priorização;
- a direção visual atual da ACIRV;
- o planejamento operacional do quarto trimestre;
- evidências de que o Hermes já está sendo usado como camada de execução/automação em fluxos editoriais;
- limitações técnicas reais do Hermes que devem impedir promessas exageradas.

## O que o repositório ainda NÃO resolve sozinho

Não foram encontrados, no estado auditado do repositório:

- base bruta/export completo do SudoExpo Match com todos os participantes, todos os matches, interesses e scores;
- total consolidado confiável de usuários cadastrados no SudoExpo Match;
- total consolidado de matches gerados;
- total de interesses unilaterais;
- total de interesses mútuos;
- distribuição completa de score;
- comprovação numérica da tese “15% permissivos geram >80% das conexões”;
- comprovação numérica da tese “usuários seletivos aceitaram 100% dos scores ≥8”;
- base bruta da pesquisa de satisfação do estande/SudoExpo Match;
- resultados consolidados da pesquisa de satisfação;
- base diária/post a post de Instagram de agosto/setembro;
- arquivo `instagram_acirvoficial_insights_agosto_2026.xlsx`;
- fotos finais do estande dentro do próprio repositório;
- vídeos finais da cobertura dentro do próprio repositório;
- material estruturado sobre a aula de Balestrin;
- evidência verificada de preço/capacidade de DGX Spark ou infraestrutura para centro de processamento;
- documentação específica sobre o evento do Rafael;
- documento da proposta de reorganização do Google Drive;
- benchmarks internos sobre BNI/Sebrae para o SudoExpo Match;
- formulário de avaliação slide a slide da apresentação.

---

# 3. STATUS DA CHECKLIST ORIGINAL

| Material necessário | Status no ACIRV-Notebook | O que foi encontrado | O que ainda falta |
|---|---|---|---|
| Planejamento original do estande | **ENCONTRADO / FORTE** | conceito, decisões, mapa de conexões, identidade, pins, folder, ativações, telão, cobertura | versão única “fechada” do escopo pré-feira, se existir |
| Fotos e vídeos do estande pronto | **PARCIAL** | briefings de captação + links para banco de imagens/Drive | arquivos finais/fotos finais no repo |
| Solicitações adicionais / alterações | **PARCIAL** | várias mudanças pré-feira e decisões de agosto/setembro | comprovação completa das solicitações feitas durante a feira |
| Base completa SudoExpo Match | **NÃO ENCONTRADA** | arquitetura, regras, logs de conexões | export CSV/XLSX/DB |
| Definição das métricas do Match | **ENCONTRADO / FORTE** | score, tipos de match, interesse, conexão, classificação | alinhar nomenclatura usada no deck |
| Metas do SudoExpo Match | **NÃO ENCONTRADA** | objetivos qualitativos | metas numéricas aprovadas |
| Pesquisa satisfação SudoExpo | **NÃO ENCONTRADA** | intenção/uso do QR aparece em roteiros | base e resultados |
| Dados Match Café Entre Amigos | **PARCIAL** | 17 conexões registradas | participantes, matches, interesses, scores |
| Dados completos Instagram | **PARCIAL** | agregados de agosto + dados históricos | série diária/post a post |
| Calendário de publicações | **ENCONTRADO / FORTE** | planejamento detalhado de agosto | execução real e links de cada peça |
| Investimento financeiro SudoExpo | **PARCIAL / BOM** | comunicação, estande, TV, palestrantes, outdoors, tecnologia | custo final realizado |
| Material atual Hermes Work | **ENCONTRADO / FORTE** | investigação, operação Q4, integração Trello, arquitetura | screenshots/demo final |
| Evidência de ganho do Hermes | **PARCIAL** | uso operacional e volume técnico | benchmark antes/depois de tempo/tokens/custo |
| Casos de uso internos de IA | **PARCIAL / BOM** | social media, Trello, planejamento, automação editorial | inventário completo por setor |
| Material Balestrin | **NÃO ENCONTRADO** | — | notas/aula/site/perguntas |
| Centro de processamento / DGX | **NÃO ENCONTRADO COMO EVIDÊNCIA** | — | pesquisa técnica e financeira atualizada |
| Evento Rafael | **NÃO ENCONTRADO** | — | data, público, proposta, formato |
| Estratégia de Marketing | **ENCONTRADO / FORTE** | estratégia, pilares, priorização, sistema operacional | material específico do professor citado no briefing |
| Pesquisas anteriores ACIRV | **PARCIAL** | referências a pesquisa e métricas | bases brutas e séries organizadas |
| Benchmarks networking BNI/Sebrae | **NÃO ENCONTRADO** | — | entrevistas/pesquisa comparativa |
| Jornada do associado/participante | **PARCIAL / BOM** | Café Entre Amigos, experiência, eventos e posicionamento | jornada única ponta a ponta formalizada |
| Google Drive atual/reorganização | **NÃO ENCONTRADO** | apenas links para pastas de assets | apresentação/proposta de reorganização |
| Identidade visual | **ENCONTRADO / FORTE** | `ACIRV-MOOD-v1`, paleta, regras de composição | manual oficial/tokens oficiais se houver |
| Limite e formato da apresentação | **NÃO ENCONTRADO** | — | tempo, público, decisão desejada |
| Formulário de avaliação dos slides | **NÃO ENCONTRADO** | — | criar formulário |

---

# 4. SUDOEXPO 2026 — DADOS INSTITUCIONAIS E OPERACIONAIS

## 4.1 Datas e programação

A nota canônica `03-Projetos-Campanhas-e-Eventos/SudoExpo-2026.md` registra:

- realização em **09, 10, 11 e 12 de setembro de 2026**;
- Rio Verde-GO;
- em 11/09:
  - Conecta: **07h30–12h00**, Arena;
  - Fórum de IA: **13h00–18h00**, Teatro;
  - ACIRV Mulher: **17h30–18h30**, Sala do Teatro;
  - Stand Up Paul Cabannes: **19h30–21h00**, Teatro;
- em 12/09:
  - Debate Político: **10h30–13h00**, Teatro.

Fonte principal da nota canônica:
`000-Arquivos-originais/310826 - Mudanças mais recentes do cronograma.md`

## 4.2 KPI principal

Na reunião de 13/07, José Carlos definiu como KPI principal da feira:

> **público / quantidade de visitantes na feira**

O pedido decorrente foi intensificar comunicação e divulgação da SudoExpo nas redes sociais.

Fonte:
`000-Arquivos-originais/130726 Reunião com a organização da SudoExpo.md`

## 4.3 Alegação “segunda maior feira multissetorial do Brasil”

A expressão aparece internamente em documentos do projeto, porém o próprio planejamento editorial determina:

> **não divulgar “segunda maior feira multissetorial do Brasil” sem guardar a fonte do ranking.**

Portanto, essa afirmação NÃO deve entrar como dado comprovado na apresentação até que exista fonte externa ou institucional verificável.

Fonte:
`000-Arquivos-originais/Planejamento de conteúdo da ACIRV - Agosto de 2026.md`

---

# 5. ESTANDE ACIRV — PLANEJAMENTO ENCONTRADO

## 5.1 Conceito central

Conceito aprovado em 03/08/2026:

> **“Estande ACIRV, a casa do empresário na SudoExpo”**

A campanha de agosto também desenvolve a ideia como:

> **Casa do Empreendedor**

Mensagem central planejada:

> **Entre com uma necessidade. Saia com uma conexão.**

Assinatura de campanha:

> **Casa do Empreendedor | ACIRV, realizadora da SudoExpo | Conectar para Crescer**

Fontes:
- `07-Reunioes-e-Decisoes/Reuniao-Marketing-03-08-2026.md`
- `000-Arquivos-originais/Planejamento de conteúdo da ACIRV - Agosto de 2026.md`

## 5.2 Objetivo estratégico do estande

O planejamento de agosto deixa claro que a comunicação deveria preparar o público para compreender quatro coisas:

1. a ACIRV é realizadora da SudoExpo;
2. o estande seria a Casa do Empreendedor, e não apenas um espaço institucional;
3. dentro da Casa, a ACIRV mostraria como gera conexões e apoia empresas;
4. a atuação da ACIRV continua durante o ano por meio de serviços e projetos.

## 5.3 Elementos planejados/documentados

Foram encontrados os seguintes elementos:

- layout em formato de casa;
- uso de amarelo, laranja e verde na campanha;
- slogan da ACIRV destacado;
- mapa físico de conexões;
- pins e cordões para materializar conexões;
- criação de pin “Me conectei na SudoExpo”;
- QR/landing page para SudoExpo Match;
- folder institucional;
- histórico da ACIRV em fotografias;
- telão em loop;
- serviços e projetos da entidade;
- bottons/pins “Sou ACIRV”;
- reconhecimento de parceiros;
- ativações de conteúdo e cobertura;
- estúdio/podcast disponível em períodos livres;
- forte sinalização de que a ACIRV realiza a SudoExpo.

Fontes principais:
- `000-Arquivos-originais/030826 Reunião com equipe de Marketing.md`
- `000-Arquivos-originais/140726 Reunião com equipe de Marketing da ACIRV sobre ações do estande da ACIRV na SudoExpo.md`
- `000-Arquivos-originais/Orçamentos e pedidos para a SudoExpo.md`
- `000-Arquivos-originais/BRIEFING TELÃO ACIRV SUDOEXPO 2026.md`
- `000-Arquivos-originais/Estratégia de cobertura estande ACIRV - 100926.md`
- `000-Arquivos-originais/Operacional cobertura estande ACIRV - 100926.md`

## 5.4 Itens explicitamente marcados como pedidos/orçados

O arquivo `Orçamentos e pedidos para a SudoExpo.md` registra como concluídos no checklist:

- cordinha;
- crachás;
- mapa em XPS;
- “Aqui todos crescem conectados” em LED;
- ACIRV e “A casa do empresário em Rio Verde” em PVC;
- logos ACIRV Mulher, Conecta, CAM-ACIRV e Fórum de RH.

Isso é evidência de pedido/planejamento, NÃO prova isoladamente de instalação final.

## 5.5 Mapa das Conexões

Em 14/07, foi definida uma ativação física:

> mapa de Rio Verde criando uma “Rede de Conexões”, com linhas entre profissionais/empresas que dessem match.

O painel seria físico, usando pins e cordões, e a própria pessoa poderia ligar um pin ao outro.

A comunicação de agosto descreveu a experiência:

1. cadastro por QR Code;
2. informar o que oferece;
3. informar o que procura;
4. sistema cruza oferta e demanda;
5. participante consulta novamente durante a feira;
6. ocorrendo conexão, os participantes se encontram;
7. pins são ligados por cordão no mapa;
8. a conexão passa a fazer parte da rede visível.

Fontes:
- `000-Arquivos-originais/140726 Reunião com equipe de Marketing da ACIRV sobre ações do estande da ACIRV na SudoExpo.md`
- `000-Arquivos-originais/Planejamento de conteúdo da ACIRV - Agosto de 2026.md`

## 5.6 Telão do estande

O briefing do telão define vídeo de aproximadamente **10 minutos**, em **4 blocos de ~2min30**:

1. presença — ACIRV hoje;
2. memória — linha do tempo;
3. atuação — o que a ACIRV faz;
4. movimento — preparação e escala da SudoExpo.

Ideia central:

> **Quem somos hoje → de onde viemos → o que fazemos → o que estamos construindo agora.**

O arquivo também contém links para:
- banco de imagens da ACIRV no Google Drive;
- logomarcas no Google Drive.

Fonte:
`000-Arquivos-originais/BRIEFING TELÃO ACIRV SUDOEXPO 2026.md`

## 5.7 Cobertura planejada do estande

Em 10/09 foi desenhada cobertura de **21 Stories**:

- 10 fotos + legenda;
- 7 one shots;
- 4 vídeos editados.

As maiores prioridades eram:
- SudoExpo Match funcionando;
- Mapa das Conexões;
- história da ACIRV;
- folder/projetos/serviços;
- Casa do Empresário;
- prova social do Match.

Isso é útil para localizar posteriormente as evidências visuais produzidas.

Fonte:
`000-Arquivos-originais/Estratégia de cobertura estande ACIRV - 100926.md`

---

# 6. ORÇAMENTO E INVESTIMENTOS DA SUDOEXPO ENCONTRADOS

Os documentos internos registram:

| Item | Valor registrado | Observação |
|---|---:|---|
| Verba inicial de comunicação | **R$ 243.000** | registro de 13/07 |
| Redirecionamento ao estande | **R$ 20.000** | autorizado por Diego Modolo |
| Corte de verba TV Globo | **-R$ 10.000** | concentração na semana da feira |
| Paul Cabannes + Andréa Vermont | **R$ 100.000** | R$ 25.000 pagos por parceira OCB |
| Tecnologia para Matchmaker | **R$ 2.500** | registrado em reunião de 14/07 |
| Outdoors Casa do Empreendedor | **4 × R$ 850** | papel incluso, total previsto R$ 3.400 |

Fontes:
- `000-Arquivos-originais/130726 Reunião com a organização da SudoExpo.md`
- `000-Arquivos-originais/140726 Reunião com equipe de Marketing da ACIRV sobre ações do estande da ACIRV na SudoExpo.md`
- `03-Projetos-Campanhas-e-Eventos/SudoExpo-2026.md`

**Cuidado:** esses valores são registros de planejamento/reunião e não equivalem automaticamente ao custo final realizado.

---

# 7. SUDOEXPO MATCH — DEFINIÇÃO TÉCNICA

A fonte mais importante é:

`000-Arquivos-originais/Como funciona o MatchMaker.md`

Ela descreve o motor v2.4.

## 7.1 Dados de entrada do perfil

O participante informa:

- porte;
- tipo de negócio;
- segmento;
- nicho;
- o que oferece;
- o que procura;
- necessidades prioritárias;
- perfil de empresa/pessoa que procura.

## 7.2 Regra básica

Ao salvar o perfil, o Postgres executa `recompute_own_matches`, comparando o usuário com os demais perfis do mesmo evento que consentiram com matchmaking.

## 7.3 Separação por evento

O sistema usa `event_id`.

Eventos explicitamente citados:
- `cafe-entre-amigos-ago-2026`;
- `sudoexpo-2026`;
- ambiente sandbox/testes.

Regra:

> o motor só cruza participantes que possuem o mesmo `event_id`.

Fonte:
`000-Arquivos-originais/Separação de matchs por evento.md`

## 7.4 Quando um par pode existir

A fonte descreve sinais como:

- encaixe oferta × necessidade;
- necessidade inversa;
- perfil desejado completo;
- relação complementar de taxonomia.

Sem sinal, a dupla não é criada.

## 7.5 Score por perspectiva

Cada dupla recebe duas notas independentes.

Pontuação documentada:

| Sinal | Pontos |
|---|---:|
| A outra empresa oferece o que você procura | +55 |
| A outra procura o que você oferece | +25 |
| Necessidade prioritária atendida | +10 |
| Complementaridade simples | +5 |
| Perfil atualizado recentemente | +3 |
| Mesma cidade | +2 |
| Relação complementar de taxonomia | até +30 |
| Perfil desejado | +20 / +30 / +40 |
| Perfil desejado mútuo | +10 |

## 7.6 Classificação exibida

A fonte documenta:

- **75+** = Alta compatibilidade;
- **40–74** = Boa oportunidade;
- **<40** = Conexão possível.

## 7.7 Tipos de match

A nomenclatura descrita inclui:

- direto;
- inverso;
- bidirecional;
- híbrido;
- complementar;
- perfil desejado.

## 7.8 Explicabilidade

Cada ponto ganho gera justificativa legível no card, como:

> “ele oferece o serviço que você procura”

A fonte afirma que a justificativa mantém rastreio da necessidade, oferta ou relação que gerou o ponto.

## 7.9 Interesse e conexão

Fluxo documentado:

1. cada lado recebe possíveis matches;
2. cada lado marca **“Tenho interesse”**;
3. com interesse mútuo, cria-se uma conexão na fila da equipe;
4. a equipe da ACIRV apresenta as duas pessoas presencialmente;
5. após o registro, contatos podem ser liberados;
6. o processo fica auditado.

Não havia notificação automática como parte central da experiência; o objetivo era estimular o retorno/presença e o trabalho da equipe.

## 7.10 Limitação técnica registrada

O documento de funcionamento informa que, no momento daquele registro, **não havia relações complementares cadastradas na taxonomia**.

Consequência:

> o sinal de taxonomia existia na arquitetura, mas valia zero na prática naquele estado.

Isso deve ser considerado ao explicar o motor.

---

# 8. SUDOEXPO MATCH — RESULTADOS REGISTRADOS NO REPOSITÓRIO

## 8.1 Conexões registradas na SudoExpo

Fonte:
`000-Arquivos-originais/Conexões Sudoexpo.md`

O arquivo lista conexões por dia:

| Data | Registros no arquivo |
|---|---:|
| 09/09/2026 | 7 |
| 10/09/2026 | 17 |
| 11/09/2026 | 13 |
| 12/09/2026 | 4 |
| **Total de linhas** | **41** |

Existe uma duplicação literal de:

> Raphael e Wallis

Portanto:
- **41 registros brutos**;
- **40 pares textuais únicos**, após deduplicação literal.

### Interpretação segura para slide

A formulação mais segura é:

> **“O registro operacional do repositório contém 41 lançamentos de conexão na SudoExpo, correspondentes a 40 pares únicos após remover uma duplicação literal.”**

Não chamar automaticamente de “40 negócios fechados”. O arquivo prova conexões registradas, não fechamento comercial.

## 8.2 Café Entre Amigos — piloto

Fonte:
`000-Arquivos-originais/Conexões geradas pelo SudoExpo Match no Café Entre Amigos do dia 270826.md`

Dado disponível:

> **17 conexões geradas**

Esse arquivo não fornece:
- total de cadastrados;
- total de matches;
- interesses;
- score;
- taxa de conversão.

## 8.3 Roteiro do Café Entre Amigos de 27/08

O roteiro comprova que o SudoExpo Match foi lançado/testado no encontro com:

- QR Code;
- cadastro;
- descrição “Tinder dos negócios”;
- cruzamento de ofertas e demandas;
- interesse mútuo;
- equipe fazendo apresentação presencial;
- pesquisa de satisfação no encerramento.

Fonte:
`000-Arquivos-originais/Café Entre Amigos (27 de Agosto) - Roteiro de Cerimonial.md`

---

# 9. O QUE NÃO ESTÁ PROVADO SOBRE O SUDOEXPO MATCH

As seguintes afirmações aparecem no briefing da apresentação, mas NÃO foram encontradas em base bruta no repositório auditado:

- “usuários permissivos representam cerca de 15% dos cadastrados”;
- “permissivos são responsáveis por mais de 80% das conexões concluídas”;
- “usuários seletivos marcaram interesse em 100% dos matches com score alto/≥8”;
- total de cadastrados;
- total de matches gerados;
- total de interesses;
- total de interesses mútuos;
- taxa de conversão;
- score médio;
- distribuição por tipo de match.

Esses pontos precisam vir de:
- banco/export do Supabase;
- CSV/XLSX;
- consulta SQL;
- relatório técnico do Match.

---

# 10. INSTAGRAM — DADOS DISPONÍVEIS

## 10.1 Agosto de 2026

Fonte:
`000-Arquivos-originais/Relatório de Agosto.md`

O arquivo registra:

| Métrica | Agosto |
|---|---:|
| Feed | **52** |
| Stories | **92** |
| Reels | **4** |
| Vídeos produzidos | **9** |
| Visualizações | **3.340.052** |
| Interações | **6.103** |

Esses são os dados de agosto mais diretamente utilizáveis encontrados no repositório.

## 10.2 Planejamento de agosto

Fonte:
`000-Arquivos-originais/Planejamento de conteúdo da ACIRV - Agosto de 2026.md`

Planejamento principal:

- **23 conteúdos principais**;
- 15 relacionados a SudoExpo/Casa do Empreendedor;
- 5 sobre serviços/benefícios;
- 3 sobre Rio Verde/datas/associativismo.

Distribuição:

| Pilar | Conteúdos | Participação |
|---|---:|---:|
| Casa do Empreendedor e SudoExpo | 15 | 65% |
| Serviços e benefícios | 5 | 22% |
| Rio Verde, datas e associativismo | 3 | 13% |
| **Total** | **23** | **100%** |

Diretrizes:
- priorizar pessoas, histórias, serviços e conexões;
- no máximo 20% de conteúdos baseados somente em dirigentes;
- todo post com próximo passo/CTA;
- uso forte do SudoExpo Match e do conceito Casa do Empreendedor;
- não prometer recursos que o sistema não possuía.

## 10.3 Série histórica de 90 dias — cuidado metodológico

Fonte:
`05-Metricas-e-Decisao/Resumo-Instagram-90-Dias.md`

Janela:
**10/01/2026 a 09/04/2026**

Dados:
- alcance: **211.235**;
- impressões: **657.084**;
- visitas ao perfil: **8.841**;
- toques em link externo: **328**;
- interações com conteúdo: **7.988**;
- contas engajadas: **2.888**;
- seguidores ganhos: **810**;
- seguidores perdidos: **261**;
- saldo: **+549**.

Esses números servem como contexto histórico, mas NÃO devem ser comparados diretamente com agosto sem equalizar:
- janela;
- definição de métrica;
- fonte;
- granularidade;
- sobreposição.

## 10.4 Qualidade dos dados

A auditoria canônica identifica inconsistências na base histórica, incluindo:

- intervalos de data problemáticos;
- datas como seriais;
- mistura de texto e número em percentuais;
- lacunas de qualidade;
- moedas ambíguas;
- divergências entre relatórios.

Fonte:
`05-Metricas-e-Decisao/Qualidade-dos-Dados-de-Marketing.md`

Regra para a apresentação:

> usar números atuais somente quando a origem e a unidade forem conhecidas; não fundir séries históricas diferentes apenas porque os nomes das métricas parecem iguais.

---

# 11. ESTRATÉGIA ACIRV 2026

## 11.1 Norte estratégico

Fonte:
`01-Estrategia-e-Marca/Estrategia-ACIRV-2026.md`

Direção:

> **Conectar para Crescer**

Objetivo:

> aumentar associados e valorizar quem já participa, consolidando a ACIRV como rede de apoio, representação e fortalecimento empresarial.

## 11.2 Regra de comunicação

Cada conteúdo, evento ou campanha deve mostrar função clara:

- demonstrar resultado;
- fortalecer pertencimento;
- ampliar autoridade;
- criar proximidade;
- converter interesse em associação/participação.

## 11.3 Critérios de decisão

A estratégia canônica usa:

- relevância;
- evidência;
- coerência com posicionamento;
- capacidade de execução;
- reaproveitamento;
- métrica definida antes da publicação.

---

# 12. PILARES DE COMUNICAÇÃO

Fonte:
`01-Estrategia-e-Marca/Pilares-Estrategicos-de-Comunicacao.md`

Pilares canônicos:

### Pertencimento
Fazer o associado se enxergar e entender por que vale participar.

### Resultados
Mostrar entregas, impacto, negócios, articulação e serviços.

### Autoridade
Posicionar a ACIRV como voz institucional e articuladora, sempre com contexto e fonte.

### Proximidade
Tornar a entidade acessível, útil e humana.

### Captação
Converter atenção em associação, inscrição, patrocínio, contato ou participação.

Regra:

> toda pauta deve ter um pilar principal e no máximo dois secundários.

---

# 13. METAS DE MARKETING DOCUMENTADAS

Fonte:
`01-Estrategia-e-Marca/Metas-de-Marketing-2026.md`

Metas registradas:

- **+30%** em novos associados;
- **80%** de retenção;
- **+50%** de crescimento digital;
- **15%** de conversão em landing pages;
- **30%** de abertura de e-mail.

Limitação canônica:

> várias metas ainda precisam de linha de base, período, população, fórmula e responsável para serem auditáveis.

Portanto, use-as como **metas institucionais documentadas**, não como indicadores automaticamente comprovados.

---

# 14. SISTEMA OPERACIONAL DE MARKETING

Fonte:
`02-Operacao-e-Processos/Sistema-Operacional-de-Marketing.md`

Fluxo canônico:

**Entrada → Triagem → Planejamento → Produção/Aprovação → Publicação/Execução → Fechamento/Aprendizado**

A lógica já existente no ACIRV-Notebook combina muito bem com a tese da apresentação de:

> medir → aprender → ajustar → reutilizar.

No fechamento de cada ação, o sistema prevê:
- arquivar fonte;
- registrar resultado;
- registrar decisão;
- registrar pendência;
- atualizar indicador;
- transformar aprendizado em checklist/nota.

---

# 15. CRITÉRIOS DE PRIORIZAÇÃO

Fonte:
`01-Estrategia-e-Marca/Criterios-de-Priorizacao-de-Marketing.md`

Classes:

- **P0:** crise/obrigação;
- **P1:** compromisso estratégico;
- **P2:** crescimento;
- **P3:** oportunidade;
- **P4:** estacionamento.

Dimensões avaliadas de 0 a 3:
- alinhamento estratégico;
- impacto;
- urgência real;
- evidência;
- capacidade;
- dependências;
- reaproveitamento.

Isso pode ser usado para defender que metas devem estar conectadas à capacidade real do sistema, em vez de funcionarem isoladamente.

---

# 16. IDENTIDADE VISUAL DISPONÍVEL

Fonte:
`Hermes/Planejamento 4º Trimestre de 2026/04-moodboard/MOODBOARD.md`

Versão ativa:

> **ACIRV-MOOD-v1 — READY**

## 16.1 Direção visual

Características principais:

- azul como âncora;
- contraste alto;
- tipografia sans-serif forte;
- mensagens curtas;
- palavras-chave destacadas;
- pessoas reais;
- linguagem contemporânea;
- sensação de conexão/movimento/rede.

## 16.2 Paleta percebida no moodboard

**Base aproximada**
- Azul real/elétrico: `#003DC5`
- Azul profundo: `#000EB4`
- Azul-marinho: `#080890`
- Azul escuro: `#000974`

**Acentos aproximados**
- verde neon;
- amarelo ácido;
- laranja `#DE733A`;
- ciano/azul claro `#027AB0` a `#129CDF`;
- roxo em gradientes;
- branco para leitura.

**Importante:** o próprio documento diz que são aproximações visuais e NÃO substituem tokens oficiais da marca.

## 16.3 Regra visual

> azul = âncora; verde/amarelo/laranja = acentos de hierarquia.

Evitar:
- template corporativo genérico;
- excesso de texto;
- fotografia genérica quando existe material real;
- neon sem função;
- mesma composição repetida.

---

# 17. HERMES WORK — O QUE O ACIRV-NOTEBOOK COMPROVA

## 17.1 Não apresentar como tecnologia “pronta e perfeita”

A investigação técnica armazenada no repo registra que o Hermes já possui:

- Task/Run;
- WorkPlan/WorkItem;
- Kanban;
- browser runtime;
- evidence store;
- journal;
- workers;
- artifacts;
- cron;
- Skills;
- mecanismos de recuperação.

Porém, a mesma investigação encontrou inconsistências de estado, como:

> WorkPlan terminal (`interrupted`) com WorkItems ainda `running` ou `pending`.

Conclusão do próprio relatório:

> estados terminais precisam ser invariantes de árvore, não apenas atributos locais.

Fonte:
`000-Arquivos-originais/170926 - Investigação Hermes Work por ChatGPT.md`

### Implicação para a apresentação

A narrativa segura é:

> **Hermes Work já tem uma arquitetura operacional relevante e já está sendo usado em fluxos reais, mas continua em hardening e validação.**

Evitar:

> “o sistema já está resolvido”, “100% confiável” ou equivalentes.

## 17.2 Evidência de escala técnica observada

No snapshot analisado pela investigação:

- 67 tasks;
- 358 task runs;
- 2.360 task events;
- 6 WorkPlans;
- aproximadamente 162 WorkItems no conjunto principal.

Nos bancos únicos do conjunto de dumps analisados:

- aproximadamente 139 WorkPlans;
- aproximadamente 8.124 WorkItems.

Isso comprova um corpus relevante de execução, mas NÃO é benchmark de ROI.

## 17.3 Hermes aplicado ao Social Media Q4

O repositório contém um pacote operacional de Q4 em:

`Hermes/Planejamento 4º Trimestre de 2026/`

Planejamento ativo:

- período: **16/09/2026 a 31/12/2026**;
- **60 publicações estáticas**;
- 0 Reels/vídeos atribuídos à designer;
- 16 peças extras com 2 slides;
- todas com legenda sugerida;
- fonte canônica versionada;
- cards canônicos no Trello;
- lote piloto de 12 briefings já fechado;
- estado operacional persistido;
- regras explícitas para o Hermes não improvisar copy.

Isso é uma evidência concreta de aplicação:

> o Hermes está sendo desenhado/operado como executor de um planejamento editorial canônico, e não simplesmente como chatbot gerando texto livre.

Fontes:
- `Hermes/Planejamento 4º Trimestre de 2026/00_README.md`
- `Hermes/Planejamento 4º Trimestre de 2026/01-planejamento/v2/PLANEJAMENTO_ESTRATEGICO.md`

## 17.4 O que ainda falta para transformar Hermes em business case executivo

O repositório não traz benchmark consolidado de:

- tempo antes × depois;
- custo antes × depois;
- tokens antes × depois;
- taxa de falhas;
- taxa de conclusão;
- custo por tarefa;
- horas humanas economizadas;
- automações reutilizadas;
- ROI financeiro.

Para a apresentação, o melhor enquadramento é:

> **prova de capacidade + piloto operacional + roadmap de medição**, e não “ROI já comprovado”.

---

# 18. PLANEJAMENTO SOCIAL MEDIA Q4 — EXEMPLO DE MATURIDADE OPERACIONAL

Fonte:
`Hermes/Planejamento 4º Trimestre de 2026/01-planejamento/v2/PLANEJAMENTO_ESTRATEGICO.md`

Norte:
**Conectar para Crescer**

Pilares:
- Pertencimento;
- Resultados;
- Autoridade;
- Proximidade;
- Captação.

Volume:
- 60 publicações;
- aproximadamente 3–4 peças estáticas por semana;
- 16 extras leves com exatamente 2 slides.

Princípio importante:

> a designer recebe copy, estrutura, CTA, direção visual e assets/referências; ela não precisa completar o raciocínio editorial.

Princípio do Hermes:

> quando o briefing estiver fechado, o Hermes sincroniza/executa; quando faltar informação, deve bloquear em vez de inventar.

Essa arquitetura pode ser usada como exemplo prático de como IA pode aumentar capacidade sem retirar governança humana.

---

# 19. FÓRUM DE IA DA SUDOEXPO

Fonte:
`000-Arquivos-originais/Dados Fórum de IA da SudoExpo.md`

Palestrantes registrados:

### André Maluf
Tema informado:

> **Do balcão ao algoritmo — Como negócios de qualquer tamanho estão usando IA para crescer**

Descrição interna:
- professor/coordenador na FIAP;
- administração e gestão de IA;
- consultoria e educação corporativa;
- experiência em estratégia, vendas e inovação.

### Rauhe Abdulhamid
Tema informado:

> **A IA não vai salvar sua empresa: a decisão com dados, sim**

Descrição interna:
- especialista em Dados e IA;
- mestre pelo ITA;
- atuação em IA/dados para crescimento e redução de custos;
- experiência com produtos e projetos empresariais.

O documento informa que ainda faltavam, naquele momento:
- painel de empresas;
- mesa redonda.

Esse material pode contextualizar a parte de IA, mas o documento não substitui validação das biografias/dados externos se forem entrar em versão pública.

---

# 20. JORNADA/EXPERIÊNCIA DE EVENTO JÁ DOCUMENTADA

O Café Entre Amigos possui uma estrutura canônica útil para pensar “protocolos de encantamento”:

Fonte:
`03-Projetos-Campanhas-e-Eventos/Cafe-Entre-Amigos.md`

Experiência recorrente:

> recepção → café → abertura → pitch de novos associados → conteúdo/palestra → networking → encerramento/próximos passos.

Métricas previstas:
- presença;
- novos públicos;
- associados apresentados;
- satisfação;
- conexões;
- conversões posteriores.

Isso oferece uma base para construir uma jornada mais formal de encantamento, mesmo que o fluxograma completo ainda não exista.

---

# 21. POSICIONAMENTO / PROPOSTA DE VALOR

Fonte:
`01-Estrategia-e-Marca/Posicionamento-e-Proposta-de-Valor.md`

Síntese:

> a ACIRV conecta empresas, representa interesses e transforma participação em acesso, informação, relacionamento e oportunidades.

Para associados:
- representação;
- serviços;
- consultorias;
- certificados;
- articulação;
- espaços;
- informação;
- rede.

Para não associados:
- entrada em ecossistema de negócios;
- prova social;
- próximo passo simples.

Para patrocinadores:
- acesso a rede empresarial;
- visibilidade contextualizada;
- participação em projetos com objetivos explícitos.

Regra crítica:

> proposta de valor deve ser sustentada por casos, números, depoimentos autorizados, entregas e registros; adjetivos institucionais sem evidência não bastam.

Essa regra é diretamente útil para a apresentação.

---

# 22. NARRATIVA DA APRESENTAÇÃO QUE O REPOSITÓRIO SUPORTA

Com o material existente, a narrativa mais bem sustentada é:

**1. Planejamos uma experiência para a SudoExpo**  
→ Casa do Empreendedor, mapa, Match, conteúdo, serviços, história.

**2. Criamos um mecanismo para transformar networking em processo**  
→ SudoExpo Match + score + interesse mútuo + equipe + mapa físico.

**3. Existem evidências de uso real**  
→ piloto do Café: 17 conexões; SudoExpo: 41 registros/40 pares textuais únicos.

**4. A comunicação foi estruturada ao redor dessa experiência**  
→ agosto com 23 pautas principais; dados agregados de 52 feeds, 92 stories, 4 reels, 9 vídeos, 3,34 milhões de visualizações e 6.103 interações.

**5. O aprendizado precisa virar sistema**  
→ estratégia “Conectar para Crescer”; pilares; sistema operacional de marketing; fechamento com dados.

**6. IA entra como alavanca do sistema, não como espetáculo**  
→ Hermes operando planejamento, estado e Trello; Q4 como piloto real.

**7. O próximo estágio é medir ROI e confiabilidade**  
→ business case com métricas antes/depois, pesquisas, funil e qualidade dos dados.

---

# 23. CLAIMS SEGUROS PARA USAR EM SLIDES

## Alta segurança / diretamente documentados

- SudoExpo 2026 ocorreu entre 09 e 12 de setembro.
- O conceito do estande foi “a casa do empresário/Casa do Empreendedor”.
- A campanha de agosto previa 23 conteúdos principais.
- O SudoExpo Match calcula score por perspectiva.
- 75+ é alta compatibilidade; 40–74 é boa oportunidade; abaixo de 40 é conexão possível, conforme a versão documentada.
- Interesse mútuo gera uma conexão operacional para a equipe.
- O piloto do Café Entre Amigos registra 17 conexões.
- O arquivo de SudoExpo contém 41 lançamentos de conexão e 40 pares textuais únicos após remover uma duplicação literal.
- O relatório de agosto registra 3.340.052 visualizações e 6.103 interações.
- O relatório de agosto registra 52 feed, 92 stories, 4 reels e 9 vídeos produzidos.
- O norte estratégico documentado é “Conectar para Crescer”.
- O planejamento Q4 possui 60 publicações estáticas.
- O Hermes está integrado a um fluxo editorial canônico/Trello no pacote de Q4.
- O próprio repositório registra limitações técnicas do Hermes e necessidade de hardening.

## Exigem cuidado ou fonte complementar

- “segunda maior feira multissetorial do Brasil”;
- “100% do planejamento entregue”;
- “15% dos usuários geraram >80% das conexões”;
- “100% de aceitação dos matches ≥8 pelos seletivos”;
- “40 conexões = 40 negócios”;
- impacto causal da SudoExpo nos números do Instagram;
- ROI do Hermes;
- economia exponencial de tokens;
- preço/capacidade de DGX Spark;
- viabilidade econômica do centro de processamento;
- resultados da pesquisa do estande;
- satisfação do público com o Match.

---

# 24. MATERIAIS QUE AINDA DEVEM SER REUNIDOS FORA DO REPOSITÓRIO

## Prioridade máxima

### SudoExpo Match
- export completo do banco;
- participantes;
- matches;
- scores;
- interesses;
- interesses mútuos;
- conexões concluídas;
- timestamp;
- perfil do usuário;
- status;
- identificador de evento.

### Pesquisa do estande
- CSV/XLSX/Google Sheets;
- perguntas;
- respostas;
- comentários;
- escala;
- data;
- número total de respondentes.

### Instagram
- `instagram_acirvoficial_insights_agosto_2026.xlsx`;
- série por dia;
- série por publicação;
- 01/08 até pelo menos 14/09;
- orgânico × pago;
- investimento;
- formatos;
- alcance;
- visualização;
- interação;
- compartilhamento;
- salvamento;
- comentário;
- visita ao perfil;
- seguidores.

### Evidência visual
- fotos finais do estande;
- mapa com pins e cordões;
- balcão;
- LEDs;
- logos;
- frase;
- fotos históricas;
- público;
- uso do Match;
- prints do painel Match;
- prints do Hermes.

## Prioridade alta

### Hermes
- benchmark antes/depois;
- tempo;
- tokens;
- custo;
- número de passos;
- falhas;
- recuperação;
- tarefas reutilizadas;
- demonstração simples.

### IA / estratégia
- material da aula do Balestrin;
- lista das 100 perguntas;
- fonte da frase sobre plano de dois anos;
- casos de uso por área da ACIRV;
- responsáveis e métricas.

### Centro de processamento
- hardware real;
- preço atualizado;
- memória;
- GPU;
- energia;
- rede;
- refrigeração;
- manutenção;
- capacidade;
- custo por token/uso;
- modelo de governança;
- segurança.

### Rafael
- data;
- local;
- lotação;
- conteúdo;
- proposta;
- público;
- parceria possível;
- espaço para pesquisa;
- patrocínio.

### Drive
- árvore atual;
- proposta de árvore futura;
- duplicidades;
- owners;
- regras de nomenclatura;
- apresentação já criada.

---

# 25. ARQUIVOS-CHAVE DO REPOSITÓRIO

## Fontes canônicas
- `03-Projetos-Campanhas-e-Eventos/SudoExpo-2026.md`
- `03-Projetos-Campanhas-e-Eventos/Cafe-Entre-Amigos.md`
- `04-Conteudo-Canais-e-Imprensa/Instagram.md`
- `05-Metricas-e-Decisao/Resumo-Instagram-90-Dias.md`
- `05-Metricas-e-Decisao/Qualidade-dos-Dados-de-Marketing.md`
- `01-Estrategia-e-Marca/Estrategia-ACIRV-2026.md`
- `01-Estrategia-e-Marca/Metas-de-Marketing-2026.md`
- `01-Estrategia-e-Marca/Pilares-Estrategicos-de-Comunicacao.md`
- `01-Estrategia-e-Marca/Criterios-de-Priorizacao-de-Marketing.md`
- `01-Estrategia-e-Marca/Posicionamento-e-Proposta-de-Valor.md`
- `02-Operacao-e-Processos/Sistema-Operacional-de-Marketing.md`
- `07-Reunioes-e-Decisoes/Reuniao-Marketing-03-08-2026.md`

## Fontes primárias mais relevantes
- `000-Arquivos-originais/Como funciona o MatchMaker.md`
- `000-Arquivos-originais/Conexões Sudoexpo.md`
- `000-Arquivos-originais/Conexões geradas pelo SudoExpo Match no Café Entre Amigos do dia 270826.md`
- `000-Arquivos-originais/Separação de matchs por evento.md`
- `000-Arquivos-originais/Relatório de Agosto.md`
- `000-Arquivos-originais/Planejamento de conteúdo da ACIRV - Agosto de 2026.md`
- `000-Arquivos-originais/Café Entre Amigos (27 de Agosto) - Roteiro de Cerimonial.md`
- `000-Arquivos-originais/030826 Reunião com equipe de Marketing.md`
- `000-Arquivos-originais/130726 Reunião com a organização da SudoExpo.md`
- `000-Arquivos-originais/140726 Reunião com equipe de Marketing da ACIRV sobre ações do estande da ACIRV na SudoExpo.md`
- `000-Arquivos-originais/Orçamentos e pedidos para a SudoExpo.md`
- `000-Arquivos-originais/BRIEFING TELÃO ACIRV SUDOEXPO 2026.md`
- `000-Arquivos-originais/Estratégia de cobertura estande ACIRV - 100926.md`
- `000-Arquivos-originais/Operacional cobertura estande ACIRV - 100926.md`
- `000-Arquivos-originais/Dados Fórum de IA da SudoExpo.md`
- `000-Arquivos-originais/170926 - Investigação Hermes Work por ChatGPT.md`

## Hermes / operação futura
- `Hermes/Planejamento 4º Trimestre de 2026/00_README.md`
- `Hermes/Planejamento 4º Trimestre de 2026/01-planejamento/v2/PLANEJAMENTO_ESTRATEGICO.md`
- `Hermes/Planejamento 4º Trimestre de 2026/04-moodboard/MOODBOARD.md`

---

# 26. CONCLUSÃO OPERACIONAL

O ACIRV-Notebook já fornece base forte para montar os blocos de:

**SudoExpo → Estante → SudoExpo Match → Instagram → Estratégia de Marketing → Hermes/IA.**

O maior gargalo não é mais “falta de contexto geral”. O gargalo agora é **dados brutos pós-evento**.

Para fechar a apresentação com rigor, os três materiais mais importantes que ainda precisam ser encontrados são:

1. **export completo do SudoExpo Match**;
2. **base da pesquisa de satisfação do estande/SudoExpo Match**;
3. **planilha completa de insights do Instagram agosto/setembro**.

Com esses três itens, a apresentação deixa de depender de hipóteses comportamentais e passa a conseguir provar:

- aquisição;
- uso;
- conversão;
- qualidade do Match;
- resposta do público;
- impacto da comunicação;
- oportunidades de melhoria.

Até que esses dados sejam incorporados, o deck deve separar visualmente:

**FATO DOCUMENTADO / DADO CALCULADO / INTERPRETAÇÃO / HIPÓTESE / PROPOSTA.**

Essa separação é coerente com a própria política de evidências do ACIRV-Notebook e reduz muito o risco de apresentar conclusões fortes demais para dados ainda incompletos.
