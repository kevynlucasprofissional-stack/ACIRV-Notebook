# Guia de Curadoria - Fontes do HD Externo da ACIRV

Regra principal: todo arquivo original trazido do HD externo permanece dentro de 000-Arquivos-originais. A curadoria futura cria derivados e conhecimento canonico em outras pastas sem substituir a fonte.

## Fontes do HD

- 000-Arquivos-originais\HD-ACIRV - HD-ACIRV - importacao selecionada 2026-09-22
- 000-Arquivos-originais\DADOS ACIRV - HD EXTERNO - DADOS ACIRV - HD EXTERNO - captura anterior

Total inventariado: 3020 arquivos / 1,21 GB.

## Privacidade do export do Instagram - politica V4

### Manter local e nao sincronizar

- security_and_login_information/**
- personal_information/device_information/**
- personal_information/information_about_you/possible_phone_numbers.json
- personal_information/information_about_you/locations_of_interest.json
- logged_information/link_history/**
- logged_information/recent_searches/**

Motivo: sao principalmente dados de seguranca, dispositivo, localizacao, pesquisas e telemetria administrativa. O valor para inteligencia institucional e baixo em relacao ao risco de exposicao.

### Elegiveis para sincronizacao

- instagram_profile_information.json
- professional_information.json
- profile_changes.json
- note_interactions.json

Motivo: podem registrar identidade institucional do perfil, configuracao profissional, mudancas historicas e interacoes relevantes para reconstruir a evolucao digital da ACIRV.

## Arquivos sensiveis locais definidos pelo usuario

Acessos site.md e Contas e Senhas.md permanecem fisicamente no clone local e protegidos pelo .gitignore. Este script nao le, imprime, remove nem altera o conteudo deles.

## Mapa de promocao futura

| Fonte original | Destino futuro sugerido | Tratamento |
|---|---|---|
| 01-Instagram | 04-Conteudo-Canais-e-Imprensa, 05-Metricas-e-Decisao, 85-Bases-e-Consultas | Preservar JSON; criar datasets normalizados e series historicas. |
| 02-WhatsApp-e-Conversas | 07-Reunioes-e-Decisoes, 06-Pessoas-e-Stakeholders, 08-Agenda-e-Execucao | Extrair decisoes, demandas, responsaveis, datas e proveniencia. |
| 03-Metricas-e-Relatorios | 05-Metricas-e-Decisao, 85-Bases-e-Consultas | Extrair tabelas, KPIs, calculos e metodologia. |
| 04-Pesquisas-e-Formularios | 05-Metricas-e-Decisao, 85-Bases-e-Consultas | Normalizar respostas e documentar contexto e amostra. |
| 05-Associados-e-Relacionamento | 06-Pessoas-e-Stakeholders, 85-Bases-e-Consultas | Criar dimensoes sanitizadas de empresas, segmentos e historico. |
| 06-Eventos | 03-Projetos-Campanhas-e-Eventos, 85-Bases-e-Consultas | Normalizar eventos, participantes, resultados e aprendizados. |
| 07-Notas-e-Diarios | 07-Reunioes-e-Decisoes, 08-Agenda-e-Execucao | Extrair fatos, decisoes, mudancas e contexto temporal. |
| 08-Reunioes-e-Decisoes | 07-Reunioes-e-Decisoes | Criar sinteses rastreaveis e atualizar decisoes canonicas. |
| 09-Planejamentos | 01-Estrategia-e-Marca, 03-Projetos-Campanhas-e-Eventos, 08-Agenda-e-Execucao | Separar estrategia, metas, calendario e execucao. |
| 10-Gestao-Historica-2014-2024 | varias camadas | Preservar periodo e gestao; construir memoria longitudinal. |
| 12-Fontes-Secundarias-IA | 97-Fontes-Brutas ou contexto auxiliar | Usar como apoio, nunca como substituto de evidencia primaria. |
| 13-Documentos-Institucionais | 01 a 08 conforme assunto | Classificar por natureza e promover somente derivados. |
| 90-AI-Friendly-Pendente | 85-Bases-e-Consultas e camadas canonicas | PDF/DOC/PPT para MD; XLS/XLSX para CSV e schema; DB para CSV/JSONL; SRT para MD. |

## Resumo dos lotes

| Lote | Arquivos | Volume MB |
|---|---:|---:|
| DADOS ACIRV - HD EXTERNO - captura anterior | 1135 | 32,3 |
| HD-ACIRV - importacao selecionada 2026-09-22 | 1885 | 1202,1 |

## Resumo do lote selecionado

| Secao | Arquivos | Volume MB |
|---|---:|---:|
| 01-Instagram | 1046 | 13,6 |
| 03-Metricas-e-Relatorios | 20 | 0,2 |
| 05-Associados-e-Relacionamento | 2 | 0,4 |
| 06-Eventos | 27 | 0,2 |
| 07-Notas-e-Diarios | 39 | 0,1 |
| 08-Reunioes-e-Decisoes | 3 | 0 |
| 09-Planejamentos | 35 | 0,3 |
| 10-Gestao-Historica-2014-2024 | 2 | 0 |
| 12-Fontes-Secundarias-IA | 4 | 1,4 |
| 13-Documentos-Institucionais | 130 | 4,7 |
| 90-AI-Friendly-Pendente | 577 | 1181,1 |

## Auditoria

Inventario: 00-Mapas-e-Manifestos-HD-Externo/inventario-fontes-HD-v4-20260922-220415.csv
Auditoria de privacidade: 00-Mapas-e-Manifestos-HD-Externo/auditoria-privacidade-instagram-v4-20260922-220415.csv
Arquivos grandes: 00-Mapas-e-Manifestos-HD-Externo/arquivos-grandes-HD-v4-20260922-220415.csv

Este script nao executa git add, commit ou push.
