---
id: fonte-leia-me-quarentena
titulo: LEIA-ME-Quarentena
aliases: []
tipo: fonte
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-06-17'
ultima_revisao: '2026-06-17'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- seguranca
fontes_documentais:
- '[[Fonte - Notas Operacionais]]'
notas_relacionadas:
- '[[Privacidade-e-Seguranca]]'
- '[[Riscos-Operacionais]]'
confidencialidade: restrito
subtipo: alerta
---

# LEIA-ME-Quarentena

> [!summary] Síntese
> Área documental de alerta. Não contém credenciais; descreve onde há risco no material original e quais ações são necessárias.

## Riscos identificados

Notas de acessos, contas/senhas e chave de API; arquivos `.env` em três ZIPs de protótipos; conversas pessoais; listas e dossiês com dados identificáveis.

## Ação imediata

Rotacionar segredos, revisar histórico dos repositórios, confirmar permissões e usar gerenciador de senhas.

## Compartilhamento

Retire `00-Original/.preservados/Dados ACIRV.zip` antes de enviar o vault a terceiros, a menos que o acesso ao corpus bruto seja necessário e autorizado.

## Proibição

Não colar valores de segredo, tokens ou senhas em notas do Obsidian, cards, prompts ou relatórios.

## Relações justificadas

- [[Privacidade-e-Seguranca]] — define a política.
- [[Riscos-Operacionais]] — registra severidade.

## Fontes e rastreabilidade

- [[Fonte - Notas Operacionais]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
