# AGENTS.md

## Arquitetura do repositório

Este repositório opera em três camadas principais:

1. `000-Arquivos-originais/` — camada livre de captura e fontes primárias.
2. `00-*` até `99-*` — camada estruturada, canônica e derivada.
3. Pastas orientadas a agentes e automações, como `Hermes/` — camada operacional de IA.

A pasta `.obsidian/` contém apenas configuração do ambiente Obsidian e não pertence às três camadas de conhecimento.

## Regra absoluta: `000-Arquivos-originais/` é imutável para IAs

Todo conteúdo dentro de `000-Arquivos-originais/` deve ser tratado como **fonte primária somente leitura**.

Agentes de IA, automações, scripts autônomos e processos de síntese **NUNCA** devem:

- alterar ou reescrever arquivos existentes;
- excluir arquivos ou pastas;
- renomear ou mover arquivos ou pastas;
- adicionar frontmatter, tags, links ou metadados aos arquivos originais;
- normalizar nomes, formatos ou estrutura interna;
- corrigir ortografia, conteúdo, datas ou formatação;
- substituir documentos por versões processadas;
- implementar mudanças diretamente dentro dessa pasta.

É permitido apenas:

- ler;
- comparar versões por meio do histórico do Git;
- calcular hashes e metadados externos;
- extrair conhecimento;
- citar a fonte original;
- produzir sínteses, derivações e atualizações **fora** de `000-Arquivos-originais/`.

Se uma tarefa pedir explicitamente para editar algo dentro de `000-Arquivos-originais/`, o agente deve interromper essa parte da operação e preservar o original. A mudança deve ser feita em uma camada derivada apropriada, salvo ação humana manual consciente fora da automação.

## Fluxo de promoção de conhecimento

O fluxo normal é unidirecional:

`000-Arquivos-originais/` → análise/síntese → `00-*` a `99-*` → consumo por humanos, Hermes e outras automações.

Nunca usar a camada estruturada para sobrescrever retroativamente a fonte original.

Ao promover conhecimento para a camada estruturada:

1. identificar se a informação já existe;
2. atualizar a nota canônica correta em vez de criar duplicatas;
3. preservar rastreabilidade até a fonte original;
4. separar claramente fato documentado, dado calculado, interpretação operacional e hipótese;
5. registrar conflitos ou incertezas sem apagá-los;
6. preferir síntese cumulativa e incremental;
7. não copiar conteúdo bruto em excesso quando uma síntese fiel for suficiente;
8. tratar informações mais recentes como atualização apenas quando houver evidência temporal ou documental clara.

## Camada estruturada (`00`–`99`)

A camada estruturada é a fonte canônica de conhecimento operacional do ACIRV Notebook.

Ela deve:

- conter informação organizada por domínio;
- evitar duplicação desnecessária;
- manter links e relações semânticas coerentes;
- consolidar conhecimento extraído de múltiplas fontes;
- permanecer legível por humanos e deterministicamente consumível por agentes;
- registrar origem, confiança, período e natureza da evidência quando relevante.

## Camada de agentes e automações

Pastas como `Hermes/` podem conter estado operacional, runbooks, configurações, pacotes de execução, artefatos temporários e outros materiais específicos de agentes.

Essa camada pode consumir a camada estruturada e as fontes primárias em modo somente leitura, mas não deve transformar seus próprios estados operacionais em verdade institucional automaticamente.

Quando um resultado produzido por um agente merecer virar conhecimento canônico, ele deve passar pelo mesmo processo de promoção e validação aplicado às demais fontes.

## Rotina diária de ingestão

Uma automação de triagem pode revisar diariamente `000-Arquivos-originais/` para detectar arquivos novos ou alterados. Essa rotina deve operar em modo somente leitura e produzir, no mínimo:

- arquivos novos;
- arquivos alterados desde a última triagem;
- conhecimento novo detectado;
- destino canônico recomendado na camada `00`–`99`;
- conflitos com conhecimento existente;
- informações possivelmente obsoletas;
- lacunas e decisões que exigem validação humana.

A ausência de novidade relevante não deve gerar alterações artificiais na camada estruturada.
