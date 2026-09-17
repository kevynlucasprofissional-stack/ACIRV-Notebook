---
id: infraestrutura-privacidade-e-seguranca
titulo: Privacidade-e-Seguranca
aliases: []
tipo: infraestrutura
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '2.0'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-09-17'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- seguranca
- privacidade
fontes_documentais:
- '[[Fonte - Notas Operacionais]]'
- '[[Fonte - Conversas WhatsApp]]'
notas_relacionadas:
- '[[Riscos-Operacionais]]'
- '[[Manifesto-de-Preservacao-de-Fontes]]'
- '[[Fonte - Conversas WhatsApp]]'
- '[[Politica-de-Fontes-e-Evidencia]]'
confidencialidade: restrito
subtipo: politica
---

# Privacidade-e-Seguranca

> [!summary] Síntese
> Política de minimização e controle para um corpus que pode conter conversas, contatos, dossiês, acessos e credenciais. `000-Arquivos-originais/` é preservado, mas preservação não significa que todo conteúdo deva ser aberto por agentes.

## Classificação

Público; interno; restrito; segredo. O vault curado usa principalmente `interno` e `restrito`; credenciais e valores autenticadores nunca entram em Markdown curado.

## Princípio de minimização

Agentes devem acessar apenas o conteúdo necessário à tarefa. A existência de uma fonte dentro de `000-Arquivos-originais/` concede permissão de preservação e leitura contextual, mas não autoriza leitura indiscriminada de material sensível.

## Segredos: regra de não abertura

Se nome, caminho, extensão ou contexto sugerirem senha, token, chave de API, chave privada, `.env`, credencial, segredo de webhook, cookie/sessão autenticada ou outro material de autenticação, agentes e automações devem **não abrir o conteúdo**.

A detecção deve ocorrer por metadados externos sempre que possível. Sinais comuns incluem `senha`, `password`, `token`, `secret`, `api key`, `apikey`, `chave`, `credentials`, `.env` e `private key`.

Nesses casos:

1. registrar apenas a existência do risco e o caminho, quando apropriado;
2. não transcrever, resumir, indexar ou promover o segredo;
3. recomendar rotação/revogação se houver possibilidade de credencial real;
4. recomendar migração para gerenciador de segredos;
5. preservar `000-Arquivos-originais/` sem alteração automática;
6. tratar remoção do Git e reescrita de histórico como ação humana deliberada de segurança.

## Achados históricos

O corpus bruto já foi identificado como contendo notas de acessos/senhas/chaves de API e ZIPs de protótipo com `.env`. Esses valores não devem ser transcritos para a camada canônica e não devem ser lidos durante ingestões automáticas.

## Ações bloqueantes antes de compartilhar fontes originais

- rotacionar chaves e senhas potencialmente versionadas;
- revisar `.env` e artefatos de protótipos;
- remover segredos do histórico quando apropriado e após rotação;
- confirmar permissões do repositório e dos arquivos;
- migrar credenciais para gerenciador apropriado;
- registrar responsável pela remediação.

## Conversas e pessoas

Não reproduzir telefone, fala pessoal, avaliação profissional ou dossiê sem finalidade, autorização e acesso adequado. Durante síntese, preferir fatos institucionais necessários e minimizar dados pessoais.

## `000-Arquivos-originais/`

A pasta é imutável para IAs. Isso significa que um agente não pode apagar ou editar um segredo encontrado para “corrigir” o problema. Deve sinalizar o risco para ação humana, sem expor o valor.

A existência de um segredo em histórico Git exige rotação/revogação; apagar apenas o arquivo atual não invalida a credencial nem remove versões históricas.

## Compartilhamento

Não compartilhar a camada original com terceiros sem saneamento e revisão humana. Derivados destinados a circulação devem conter somente o mínimo necessário e jamais incorporar credenciais.

## Relações justificadas

- [[Riscos-Operacionais]] — registra risco.
- [[Manifesto-de-Preservacao-de-Fontes]] — explica preservação e imutabilidade.
- [[Politica-de-Fontes-e-Evidencia]] — define promoção sem vazamento da origem.
- [[Fonte - Conversas WhatsApp]] — representa material restrito.

## Fontes e rastreabilidade

- [[Fonte - Notas Operacionais]]
- [[Fonte - Conversas WhatsApp]]
- inventário de caminhos de `000-Arquivos-originais/`, sem abertura de arquivos suspeitos de conter segredos.

## Limitações e revisão

Esta nota deve ser revisada quando a arquitetura de fontes, as permissões, o processo de ingestão ou a postura de segurança mudar.
