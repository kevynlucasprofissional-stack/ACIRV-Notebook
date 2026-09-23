---
id: processo-governanca-do-acervo-digital
titulo: Governanca-do-Acervo-Digital
aliases: [Reorganizacao Segura do Drive, Governanca do Drive ACIRV]
tipo: processo
status: auditado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-22'
ultima_revisao: '2026-09-22'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- drive
- acervo
- governanca
- migracao
- seguranca
fontes_documentais:
- '000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Projeto de reorganização do Drive/acirv_reorganizador_seguro_v2_1.py'
- '[[Contexto-Mega-Relatorio-Pos-SudoExpo]]'
notas_relacionadas:
- '[[Sistema-Operacional-de-Marketing]]'
- '[[Politica-de-Fontes-e-Evidencia]]'
- '[[Riscos-Operacionais]]'
confidencialidade: interno
subtipo: governanca_acervo
---

# Governanca-do-Acervo-Digital

> [!summary] Síntese
> A reorganização do acervo da ACIRV deve ser tratada como **migração auditável de informação**, não como “arrumar pastas”. O script V2.1 materializa um princípio forte: primeiro inventariar e classificar sem tocar na origem; depois submeter ambiguidades à decisão humana; só então mover o que tiver regra suficientemente segura, preservando hash, journal, rollback e quarentena. A existência do script não prova que a migração já foi executada.

## Estado atual

O pacote pós-SudoExpo contém:

- uma apresentação de proposta para a diretoria;
- o script `acirv_reorganizador_seguro_v2_1.py`;
- contexto que posiciona a reorganização do acervo como melhoria operacional.

Nesta curadoria, a inteligência promovida vem do **design explícito do script**. A apresentação binária continua como fonte complementar e não é necessária para certificar a mecânica de segurança descrita abaixo.

## Princípio central

> **Organizar não pode significar perder, sobrescrever ou “adivinhar” o destino de informação.**

A migração segura separa:

1. auditoria;
2. classificação;
3. aprovação;
4. plano;
5. execução;
6. verificação;
7. possibilidade de rollback.

Isso transforma a reorganização em processo governado, e não em mutação manual difícil de auditar.

## Primeira execução: somente auditoria

O próprio script recomenda que a primeira execução seja apenas **NOVA AUDITORIA**.

Durante essa fase:

- as origens são lidas sem reorganização;
- o estado é gravado fora dos volumes auditados;
- arquivos recebem SHA-256;
- metadados e contexto de caminho são coletados;
- duplicatas por hash podem ser identificadas;
- classificação e destino proposto são produzidos sem execução automática.

O plano real só deve existir depois da revisão de regras e grupos.

## Níveis de confiança

O modelo distingue classes de decisão. O princípio operacional é mais importante que o nome da letra:

- regras humanas explícitas e aprovadas podem ser executáveis;
- itens sustentados por múltiplas evidências ainda podem exigir liberação explícita;
- classificações apenas prováveis não devem atravessar automaticamente para execução;
- itens ambíguos ficam bloqueados;
- legado aprovado pode seguir regras próprias.

No V2.1, itens **C** e **D** não podem chegar à execução; **B** exige liberação explícita; o padrão executável é restrito às classes aprovadas pelo desenho.

Isso impede que um classificador transforme “parece pertencer aqui” em movimento irreversível.

## Segurança de bytes

O script registra invariantes fortes:

### Sem overwrite

Se o destino aparecer depois que o plano foi gerado, a operação deve bloquear em vez de sobrescrever.

### Mesmo volume

A intenção é usar rename atômico depois de validar hash, metadados e lock de leitura.

### Entre volumes

O fluxo previsto é:

**cópia temporária → fsync → SHA-256 → publicação atômica → SHA-256 final → origem para quarentena**

A origem não é apagada imediatamente.

### Quarentena

A quarentena é parte do desenho de segurança. Ela mantém reversibilidade enquanto a migração ainda está sob validação.

## Journal e retomada

O estado é registrado em SQLite com journal configurado para persistência. O fluxo modela estados como:

- planejado;
- copiando;
- copiado;
- hash verificado;
- publicado;
- origem em quarentena;
- verificação remota;
- falha;
- rollback concluído ou bloqueado.

O objetivo é permitir retomada e investigação sem depender da memória de quem executou.

## Rollback

Rollback não deve “desfazer a qualquer custo”.

Se um arquivo mudou depois da migração, o mecanismo precisa bloquear uma reversão que sobrescreveria bytes novos. A preservação do conteúdo tem prioridade sobre voltar ao estado anterior visualmente.

## Verificação pós-migração

O desenho prevê comparar o **multiconjunto de hashes** antes e depois. A pergunta de controle é:

> **todo conteúdo esperado ainda existe em algum lugar válido?**

Há ainda verificação remota opcional via `rclone check --download`. Quando habilitada, a migração só pode ser considerada completa depois da validação remota.

## Classificação semântica

O script tenta organizar o acervo por função institucional, não apenas por extensão.

Entre os destinos propostos aparecem famílias como:

- marca e identidade;
- projetos e eventos;
- comunicação e conteúdo;
- banco de mídia;
- comercial e associados;
- dados e relatórios;
- histórico;
- legado a revisar.

Essa estrutura é útil porque aproxima armazenamento de uso e responsabilidade.

## Ambiguidade deve sobreviver

Quando mais de um evento é plausível, ou nenhuma regra semântica é suficiente, o item é encaminhado para estado ambíguo/revisão em vez de receber destino inventado.

Esse princípio deve permanecer mesmo que a implementação futura do script mude.

## Conteúdo restrito

O classificador contém tratamento explícito para materiais potencialmente privados ou restritos, evitando publicação automática no Drive compartilhado.

A regra canônica é:

- dado restrito não ganha distribuição mais ampla só porque foi encontrado;
- classificação de destino precisa considerar confidencialidade;
- reorganização não pode ampliar acesso silenciosamente.

## Sequência canônica recomendada

1. **Inventariar** — sem mutar origem.
2. **Hashar** — identificar conteúdo e duplicidade.
3. **Classificar** — com evidência e nível de confiança.
4. **Revisar ambiguidades** — decisão humana.
5. **Congelar plano** — origem, destino, hash e regra.
6. **Executar apenas o autorizado**.
7. **Verificar bytes e manifesto**.
8. **Quarentenar origem quando necessário**.
9. **Validar remoto**, se aplicável.
10. **Encerrar ou rollback** com journal preservado.

## O que esta nota não afirma

A existência do script **não prova** que:

- o Drive atual já foi reorganizado;
- todas as regras de destino estão aprovadas;
- a classificação automática está correta;
- a migração foi testada no acervo real;
- o plano foi autorizado pela diretoria;
- arquivos já foram movidos.

Esses são estados de execução que precisam de evidência própria.

## Critério de sucesso

Uma reorganização é bem-sucedida quando melhora encontrabilidade e governança **sem perder conteúdo, ampliar acesso indevidamente ou apagar a possibilidade de auditoria**.

O resultado esperado não é apenas uma árvore “bonita”, mas um acervo em que:

- a origem da decisão é recuperável;
- ambiguidade está explícita;
- bytes podem ser verificados;
- o histórico pode ser reconstruído;
- usuários sabem onde procurar;
- novos arquivos têm regra de entrada.

## Fontes e rastreabilidade

- `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Projeto de reorganização do Drive/acirv_reorganizador_seguro_v2_1.py` — blob `aa816a5eff54b7cb71113c2c706f8a28b26d9539`.
- `000-Arquivos-originais/Dados para mega-relatório pós Sudoexpo/Projeto de reorganização do Drive/ACIRV_Acervo_Digital_Diretoria_v2.pptx` — blob `6774a700a4e24cafbbec8a6d4b9bffc0b0556bbc`, fonte complementar.
- [[Contexto-Mega-Relatorio-Pos-SudoExpo]] — enquadramento da iniciativa.

## Limitações e revisão

A próxima revisão deve incorporar decisão humana sobre arquitetura de pastas, resultado de auditoria real e evidência de testes antes de declarar o processo pronto para execução institucional.
