# Hermes Work — Pesquisas ACIRV Q4 2026

## Missão

Usar o Hermes Work como executor operacional das pesquisas prioritárias da reta final de 2026, mantendo a inteligência institucional no ACIRV Notebook e os dados identificáveis de contato/resposta em controle **local**.

Fonte metodológica canônica:
- `../../01-Estrategia-e-Marca/Pesquisa-e-Aprendizado-de-Marketing.md`
- `../../08-Agenda-e-Execucao/Roadmap-de-Pesquisas-Q4-2026.md`

## Frentes iniciais

1. comunidade Builders + IA;
2. pesquisa do Fórum de IA e modelos de financiamento;
3. pesquisa do evento de 08/10;
4. pesquisa estratégica com associados;
5. aquisição de novos associados;
6. pesquisa interna das ACIRVETES;
7. pesquisa pós-relatório diário;
8. apoio ao ciclo Sympla → check-in → pesquisa → análise → melhoria;
9. auditoria de telemetria do ASPMed.

## Capacidades esperadas do Hermes

- preparar questionários a partir de uma decisão explícita;
- organizar listas locais;
- apoiar contatos individuais por Instagram/WhatsApp/e-mail quando autorizado;
- registrar status de contato;
- controlar follow-up;
- importar/exportar respostas;
- deduplicar registros;
- segmentar públicos;
- calcular agregados;
- cruzar fontes compatíveis;
- gerar hipóteses e relatórios;
- promover somente conclusões sustentadas para a camada canônica.

## Controle local obrigatório

Arquivo recomendado:

`local/controle_pesquisas.csv`

ou formato equivalente (SQLite/Parquet) quando o volume justificar.

A pasta `local/` é ignorada pelo Git.

### Nunca versionar

- número de telefone;
- e-mail individual;
- @/handle de Instagram;
- lista nominal de WhatsApp;
- respostas identificáveis;
- consentimentos individualizados;
- observações pessoais;
- exports brutos de contatos.

O GitHub guarda schema, metodologia, questionários, agregados anônimos e decisões.

## Estados mínimos de contato

- `PENDENTE`
- `CONTATADO`
- `RESPONDEU`
- `FOLLOW_UP`
- `RECUSOU`
- `INVALIDO`
- `ENCERRADO`

## Regra para associados

Contatos existentes em grupos ou redes sociais **não provam** condição atual de associado. Quando a pesquisa exigir segmentação de associados, cruzar com uma base institucional atualizada.

## Fluxo padrão

**Pergunta de decisão → definição de público → instrumento → controle local → contato/coleta → validação → análise → decisão → ação → nova medição**

## Disparos

Preferir abordagem individualizada e rastreável. Evitar transformar automação em spam.

Antes de qualquer disparo:
1. confirmar finalidade;
2. confirmar público;
3. validar mensagem;
4. definir quem responderá retornos;
5. registrar o contato no controle local;
6. respeitar recusa e opt-out.

## Pesquisa pós-relatório diário

Pode ser executada como ritual recorrente após o relatório diário. O Hermes estrutura a coleta e consolida padrões; não produz score diário de desempenho pessoal.

Ver:
- `../../05-Metricas-e-Decisao/Pesquisa-Pos-Relatorio-Diario.md`
- `../../05-Metricas-e-Decisao/Telemetria-do-Trabalho-Humano.md`

## Relação com o pacote da Samara

A sincronização dos briefings do planejamento anual para a Samara continua no pacote:

`../Planejamento 4º Trimestre de 2026/`

Este pacote de pesquisas não altera o gate editorial daquele fluxo.
