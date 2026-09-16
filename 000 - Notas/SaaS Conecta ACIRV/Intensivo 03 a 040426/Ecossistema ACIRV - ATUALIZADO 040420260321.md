---
id: stub-zip-ecossistema-acirv---atualizado-040420260
titulo: Ecossistema ACIRV - ATUALIZADO 040420260321 (QUARENTENADO - ZIP com .env)
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

# Ecossistema ACIRV - ATUALIZADO 040420260321 (QUARENTENADO)

> [!warning] ZIP removido do vault por conter arquivo .env com chaves Supabase
> O arquivo ZIP original foi movido para `Quarentena-Sensivel/Ecossistema ACIRV - ATUALIZADO 040420260321.zip`.

## Proveniencia da quarentena

- **Arquivo original**: `ACIRV Neo/000 - Notas/SaaS Conecta ACIRV/Intensivo 03 a 040426/Ecossistema ACIRV - ATUALIZADO 040420260321.zip`
- **SHA-256**: `7d1e1f06197704b6b29a8771fdbcdbf007588b2a5554e4dc1fc619932a2be466`
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
