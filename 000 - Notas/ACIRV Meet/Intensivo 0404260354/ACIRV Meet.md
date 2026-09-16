---
id: stub-zip-acirv-meet
titulo: ACIRV Meet (QUARENTENADO - ZIP com .env)
aliases: []
tipo: pendencia
status: arquivado
profundidade: indice
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-06-18'
ultima_revisao: '2026-06-18'
grau_confianca: alto
tags:
- seguranca
- quarentena
- saas
fontes_documentais: []
notas_relacionadas:
- '[[Privacidade-e-Seguranca]]'
- '[[ACIRV-Meet]]'
confidencialidade: restrito
subtipo: stub
---

# ACIRV Meet (QUARENTENADO)

> [!warning] ZIP removido do vault por conter arquivo .env com chaves Supabase
> O arquivo ZIP original foi movido para `Quarentena-Sensivel/ACIRV Meet.zip`.

## Proveniencia da quarentena

- **Arquivo original**: `ACIRV Neo/000 - Notas/ACIRV Meet/Intensivo 0404260354/ACIRV Meet.zip`
- **SHA-256**: `58a8867cdea35ff2ce6c32259c65e33f8d0de39922c2a86e87d3041e1fa2f136`
- **Ciclo**: `RETOMADA-CORRETIVA`
- **Data da quarentena**: 2026-06-18
- **Motivo**: Arquivo ZIP contendo .env com chaves de API Supabase (VITE_SUPABASE_URL, VITE_SUPABASE_PUBLISHABLE_KEY, etc.)

## Acao recomendada

- Rotacionar as chaves Supabase imediatamente.
- Verificar se o projeto Supabase associado ainda esta ativo.
- Para recuperar o codigo-fonte, extrair em ambiente isolado e sanitizar.
- Consultar `Privacidade-e-Seguranca` para procedimento completo.

## Nota sobre o codigo-fonte

O codigo-fonte do SaaS permanece preservado na quarentena. Para trabalho de desenvolvimento, extrair temporariamente em ambiente controlado e remover credenciais antes de qualquer recompartilhamento.
