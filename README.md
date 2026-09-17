# ACIRV Notebook

Este repositório organiza o conhecimento de comunicação, marketing, operação e execução da ACIRV em três camadas distintas.

## 1. Fontes originais — `000-Arquivos-originais/`

Área livre para captura humana: notas rápidas, ideias, diários, documentos, arquivos recebidos e materiais ainda não estruturados.

**Regra fundamental:** esta pasta é fonte primária e deve ser tratada como somente leitura por IAs e automações. Nenhuma IA deve alterar, excluir, mover, renomear, corrigir, normalizar ou reescrever qualquer conteúdo nela.

O papel dos agentes é ler essas fontes, identificar conhecimento novo e promover sínteses para a camada estruturada, preservando a rastreabilidade até o original.

## 2. Conhecimento estruturado — `00-*` a `99-*`

É a camada canônica do vault. Aqui ficam estratégia, processos, projetos, canais, métricas, stakeholders, reuniões, execução, MOCs, bases, auditorias, infraestrutura e pendências.

O conteúdo desta camada deve ser consolidado, deduplicado, semanticamente ligado e adequado tanto para leitura humana quanto para consumo por agentes.

## 3. Agentes e automações — `Hermes/` e futuras pastas específicas

Contém runbooks, estados operacionais, pacotes de execução, configurações e outros artefatos próprios de agentes e automações.

Esses materiais podem consumir as duas camadas anteriores, mas não se tornam automaticamente verdade institucional. Conhecimento produzido por agentes só deve entrar na camada canônica após promoção explícita e validação apropriada.

## `.obsidian/`

Contém somente configurações do Obsidian e fica fora das três camadas de conhecimento.

## Fluxo de conhecimento

```text
captura humana / documentos
        ↓
000-Arquivos-originais/       (imutável para IAs)
        ↓ leitura + análise + síntese
00-* ... 99-*                 (conhecimento canônico)
        ↓ consumo
Hermes/ + outras automações   (execução)
```

O fluxo de promoção é unidirecional. A camada estruturada nunca deve sobrescrever retroativamente as fontes originais.

As regras completas para agentes estão em `AGENTS.md`.
