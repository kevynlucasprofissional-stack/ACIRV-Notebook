# AGENTS.md

> **Convenção canônica do repositório:** `000-Arquivos-originais/` é a **fonte primária imutável**. As pastas `00-*` a `99-*` formam a **camada canônica** de conhecimento. Todo agente, automação ou processo de síntese deve preservar essa separação.

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

- ler fontes não sensíveis;
- comparar versões por meio do histórico do Git;
- calcular hashes e metadados externos sem modificar a origem;
- extrair conhecimento;
- citar a fonte original;
- produzir sínteses, derivações e atualizações **fora** de `000-Arquivos-originais/`.

Se uma tarefa pedir explicitamente para editar algo dentro de `000-Arquivos-originais/`, o agente deve interromper essa parte da operação e preservar o original. A mudança deve ser feita em uma camada derivada apropriada, salvo ação humana manual consciente fora da automação.

## Regra de segurança: segredos não devem ser lidos por automação

A permissão geral de leitura da pasta `000-Arquivos-originais/` não se aplica a arquivos que possam conter segredos ou material autenticador.

Se nome, caminho, extensão ou contexto sugerirem qualquer um dos itens abaixo, o agente deve **parar antes de abrir o conteúdo**:

- senha ou lista de senhas;
- token;
- API key/chave de API;
- chave privada, certificado privado ou seed;
- `.env` ou arquivo de credenciais;
- segredo de webhook;
- cookie ou sessão autenticada;
- qualquer material destinado a autenticação.

Sinais de risco incluem, sem se limitar a: `senha`, `password`, `token`, `secret`, `api key`, `apikey`, `chave`, `credentials`, `.env`, `private key`.

Nesses casos o agente deve:

1. não abrir, transcrever, resumir ou citar o valor do segredo;
2. registrar somente que existe um arquivo potencialmente sensível e seu caminho quando isso for seguro;
3. recomendar rotação/revogação caso exista possibilidade de credencial real versionada;
4. recomendar migração do segredo para um gerenciador apropriado;
5. nunca tentar “sanear” o arquivo original, pois `000-Arquivos-originais/` continua imutável para IAs;
6. não promover o segredo para nenhuma nota canônica.

A remoção de uma credencial real do repositório ou do histórico Git é uma ação de segurança humana deliberada e deve vir acompanhada de rotação/revogação; apagar apenas o arquivo não torna um segredo histórico seguro.

## Regra de auto-merge para curadoria e automações

Agentes e automações estão **autorizados a fazer merge automático no `main`** de PRs de curadoria, organização, análise, infraestrutura ou evolução do vault, desde que o diff da PR **não altere nenhum caminho dentro de `000-Arquivos-originais/`**.

Antes do merge automático, o agente deve verificar a lista real de arquivos alterados da PR. A regra é binária:

- se **nenhum** arquivo alterado estiver sob o prefixo `000-Arquivos-originais/`, o merge automático no `main` está autorizado;
- se **qualquer** arquivo alterado estiver sob `000-Arquivos-originais/`, o merge automático é proibido e a PR deve permanecer sem merge até revisão humana deliberada.

Essa autorização vale inclusive para mudanças produzidas por auditorias curatorias diárias. Branch e PR continuam preferíveis quando ajudam rastreabilidade, mas **aprovação humana não é requisito para o merge** quando a camada original permanece intocada.

Conflitos técnicos, proteções do GitHub ou impossibilidade material de merge devem ser reportados como bloqueios técnicos; eles não alteram a política acima.

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

Uma automação de triagem pode revisar diariamente `000-Arquivos-originais/` para detectar arquivos novos ou alterados. Essa rotina deve operar em modo somente leitura na camada original e produzir, no mínimo:

- arquivos novos;
- arquivos alterados desde a última triagem;
- conhecimento novo detectado;
- destino canônico recomendado na camada `00`–`99`;
- conflitos com conhecimento existente;
- informações possivelmente obsoletas;
- riscos de segurança detectáveis sem abrir segredos;
- lacunas e decisões que exigem validação humana.

Quando a informação for de alta confiança e o destino canônico for inequívoco, a automação pode propor ou executar a atualização **fora de `000-Arquivos-originais/`**, preferencialmente em branch/PR auditável. Ambiguidades e conflitos relevantes exigem validação humana.

A ausência de novidade relevante não deve gerar alterações artificiais na camada estruturada.
