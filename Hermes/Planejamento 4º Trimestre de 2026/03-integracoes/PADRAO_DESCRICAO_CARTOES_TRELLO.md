# Padrão de descrição dos cartões Trello — Samara

Este documento define o **padrão canônico** das descrições dos cartões de Social Media da ACIRV destinados à designer Samara.

## Princípio

O Trello é a interface operacional da designer. Portanto, a descrição do cartão deve conter **somente informações necessárias para entender e produzir a peça**.

Metadados de rastreabilidade continuam importantes para o Hermes, mas ficam no estado/Git e **não** na descrição visível para a Samara.

## Não colocar na descrição do cartão

Não incluir:

- `POST ID`;
- `PRIORIDADE`;
- `PILAR ESTRATÉGICO`;
- `CAMPANHA/FRENTE`;
- `SERVIÇO/BENEFÍCIO RELACIONADO`;
- `MÉTRICA PRINCIPAL`;
- `RECONCILIAÇÃO TRELLO`;
- `REFERÊNCIAS HISTÓRICAS`;
- nomes de arquivos internos do repositório;
- justificativas técnicas sobre de qual arquivo uma informação foi extraída;
- frases como `não especificado no plano` ou `não definido no plano`.

Esses dados, quando úteis, devem continuar registrados no estado operacional, auditoria ou arquivos internos do Hermes.

## Template canônico

Usar esta estrutura:

```text
PUBLICAÇÃO: DD/MM/AAAA
DATA DE ENTREGA PARA SAMARA: DD/MM/AAAA

OBJETIVO/RACIONAL:
[Explicação curta, direta e útil para produção.]

FORMATO: [formato]
NÚMERO DE SLIDES: [quantidade] ([EXATO quando aplicável])

CONTEÚDO/ESTRUTURA DOS SLIDES:

Slide 1: [...]
Slide 2: [...]
Slide 3: [...]

CTA: [...]

DIREÇÃO VISUAL: [...]

LEGENDA SUGERIDA (completa):
[Legenda completa]

DADOS A VALIDAR:

- [...]

OBSERVAÇÕES:

- [...]
```

Se `DADOS A VALIDAR` ou `OBSERVAÇÕES` não tiverem conteúdo real, a seção pode ser omitida em vez de preencher com `nenhum`, `não definido` ou equivalente.

## Regras de redação

- Escrever para a Samara, não para o sistema de auditoria.
- Ser claro, humano, escaneável e orientado à execução.
- Não repetir a mesma informação em campos diferentes.
- Não colocar caminhos de arquivos, classificação interna ou explicações de reconciliação na descrição.
- Uma observação de reconciliação pode permanecer **somente quando altera diretamente a produção da designer** — por exemplo, alertar que outra peça em produção cobre mensagem semelhante e deve ser coordenada.
- Não remover da legenda informações que pertencem ao briefing editorial.
- Não inventar dados para preencher seções vazias.

## IDs 045–060

Para os posts `ACIRV-SM-2026-045` a `060`, a descrição deve deixar inequívoco que são **2 slides exatos**:

- Slide 1 = capa/gancho;
- Slide 2 = CTA;
- o aprofundamento fica na legenda;
- não criar slides intermediários.

## Metadados internos do Hermes

Registrar internamente, fora da descrição do Trello, quando aplicável:

- `post_id`;
- prioridade;
- pilar estratégico;
- campanha/frente;
- serviço/benefício;
- métrica;
- classificação de reconciliação;
- referências históricas;
- dedupe key;
- fontes internas;
- card ID/URL;
- estado de execução;
- referência visual e versão do moodboard;
- validações e bloqueios.

## Atualização de cartões já criados

Se um cartão deste planejamento já existir com a descrição antiga e verbosa:

1. **não recriar o cartão**;
2. preservar ID, URL, posição, anexos, comentários e histórico;
3. abrir o cartão existente;
4. substituir somente a descrição pelo novo padrão;
5. clicar explicitamente em **Salvar**;
6. verificar depois da gravação que o texto está persistido no Trello.

## Procedimento de escrita no Trello via navegador

Aprendizados validados no lote piloto:

1. No composer da lista, inserir **somente o título do cartão**.
2. Criar o cartão.
3. Abrir o cartão criado.
4. Entrar no campo de descrição.
5. Preencher o editor de descrição.
6. Clicar no botão `Salvar` (`description-save-button`).
7. Verificar que a descrição ficou persistida antes de seguir para o próximo cartão.

Atenção: não usar o primeiro `textarea` encontrado na lista. O campo `list-name-textarea` renomeia a lista e não é o composer do cartão.

## Exemplo aprovado — ACIRV-SM-2026-001

```text
PUBLICAÇÃO: 16/09/2026
DATA DE ENTREGA PARA SAMARA: 16/09/2026

OBJETIVO/RACIONAL:
Frente Pós-SudoExpo: transformar o evento em evidência, conexão, aprendizado e continuidade

FORMATO: Carrossel 2 slides — 2 slide(s)
NÚMERO DE SLIDES: 2 (EXATO)

CONTEÚDO/ESTRUTURA DOS SLIDES:

Slide 1: convite para avaliar o estande. Slide 2: por que a resposta importa + QR Code.
CTA: Responder à pesquisa de 1 minuto

DIREÇÃO VISUAL: Visual direto, pouco texto, QR em destaque e foto/ilustração real do estande.

LEGENDA SUGERIDA (completa):
A SudoExpo terminou, mas a nossa escuta continua. Se você passou pelo estande da ACIRV, sua percepção ajuda a entender o que funcionou e o que pode evoluir nas próximas experiências. A pesquisa leva cerca de 1 minuto e transforma opinião em melhoria prática.
Responder à pesquisa de 1 minuto.
#ACIRV #ConectarParaCrescer

DADOS A VALIDAR:

- Link/QR do formulário de avaliação (pesquisa de 1 minuto) precisa ser fornecido antes da arte final.

OBSERVAÇÕES:

- Nenhum cartão existente corresponde a esta pauta: o pedido é novo (pesquisa de avaliação do estande).
- Coordenação obrigatória com '[ACIRV] Criativos de agradecimento' (EM PRODUÇÃO), que já cobre peças de fechamento da SudoExpo, para evitar encerramento redundante.
```
