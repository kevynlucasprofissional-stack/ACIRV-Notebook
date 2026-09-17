---
id: hermes-ingestao-paridade
titulo: Hermes-Ingestao-e-Paridade
aliases: []
tipo: documentacao
status: ativo
profundidade: avancada
versao_schema: '2.0'
versao_conteudo: '2.0'
idioma: pt-BR
data_criacao: '2026-09-17'
ultima_revisao: '2026-09-17'
grau_confianca: alto
confidencialidade: interno
---

# Hermes — Integração com o Sistema de Ingestão e Paridade

> [!summary] Síntese
> Documentação para o Hermes atuar como **consumidor leitor** da camada canônica e validador de integridade do ACIRV Notebook.

## Papel Operacional do Hermes

A partir da transição arquitetural de setembro de 2026:

- **ChatGPT Agendado:** É o **executor cognitivo e editorial principal** da rotina de ingestão (ver [[ChatGPT-Protocolo-de-Ingestao-Agendada]]).
- **Hermes:** Atua como **agente operacional consumidor**, lendo o conhecimento canônico estabilizado para responder consultas, gerar copilotos, rodar automações secundárias e verificar a saúde do vault.

---

## Como o Hermes Consome a Ingestão

O Hermes consulta a camada canônica seguindo as regras de autoridade:

```text
000-Arquivos-originais/       (Somente leitura — consulta histórica)
        │
        ├─► 85-Bases-e-Consultas/ (Verifica Ledger-de-Ingestao e Claims-Canonicos)
        │
        └─► 00-* até 99-*         (Lê o CONHECIMENTO CANÔNICO NARRATIVO principal)
```

## Comandos de Auditoria Utilizados pelo Hermes

O Hermes pode executar os validadores determinísticos em tarefas de manutenção e auditoria:

```bash
# 1. Verificar inventário de fontes
python 98-Infraestrutura/ingestao/inventariar_fontes.py .

# 2. Validar claims e integridade referencial
python 98-Infraestrutura/ingestao/claims.py .

# 3. Validar invariantes e imutabilidade runtime
python 98-Infraestrutura/ingestao/validar_invariantes.py .

# 4. Gerar relatório de cobertura reproduzível
python 98-Infraestrutura/ingestao/relatorio_cobertura.py .
```

## Regras para o Hermes

1. **NUNCA** editar, mover ou deletar arquivos em `000-Arquivos-originais/`.
2. **NUNCA** abrir arquivos com `read_status = sensitive_do_not_read`.
3. **NUNCA** tomar o estado interno do agente ou execuções de testes como verdade institucional.
4. **SEMPRE** consumir o conhecimento canônico das notas narrativas (`00-*` a `99-*`) e citar suas fontes e evidências associadas.
