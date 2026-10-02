---
id: auditoria-auditoria-de-links-e-metadados
titulo: Auditoria-de-Links-e-Metadados
aliases: []
tipo: auditoria
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
- auditoria
fontes_documentais:
- '[[Fonte - Briefing do projeto]]'
notas_relacionadas:
- '[[Relatorio-de-Auditoria-do-Vault]]'
- '[[Schema-de-Propriedades]]'
- '[[Ontologia-do-Vault]]'
confidencialidade: interno
subtipo: auditoria
---

# Auditoria-de-Links-e-Metadados

> [!summary] Síntese
> Contrato de integridade estrutural do vault.

## Bloqueantes

YAML inválido; ID duplicado; wikilink quebrado; Canvas inválido ou com arquivo ausente; JSON inválido; basename duplicado não intencional; ZIP corrompido.

## Testes

Parse de frontmatter; campos obrigatórios; vocabulários; normalização de caminhos; resolução de wikilinks; referências de Canvas; YAML de `.base`; JSON de `.obsidian`; hash de arquivos.

## Cabeçalhos e blocos

Links com subpath são auditados por verificação complementar. Este release evita depender de links frágeis para cabeçalhos críticos.

## Aceite

Zero falhas bloqueantes no diretório de produção e na cópia extraída do ZIP.

## Relações justificadas

- [[Relatorio-de-Auditoria-do-Vault]] — consolida resultado.
- [[Schema-de-Propriedades]] — define contrato.
- [[Ontologia-do-Vault]] — define vocabulário.

## Fontes e rastreabilidade

- [[Fonte - Briefing do projeto]]

## Limitações e revisão

Esta nota deve ser revisada quando a fonte, o responsável, a data, a metodologia ou o estado operacional mudar.
