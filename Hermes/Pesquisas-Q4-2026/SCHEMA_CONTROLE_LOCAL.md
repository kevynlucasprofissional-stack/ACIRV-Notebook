# Schema recomendado — controle local de pesquisas

> Este arquivo documenta a estrutura. **Não inserir contatos reais aqui.**

Arquivo operacional sugerido: `local/controle_pesquisas.csv`.

## Colunas mínimas

| Campo | Uso |
|---|---|
| `research_id` | identifica a pesquisa |
| `participant_local_id` | identificador local não publicado |
| `channel` | whatsapp, instagram, email, presencial, sympla |
| `contact_locator` | telefone/e-mail/handle — **somente local** |
| `display_name` | nome para operação — **somente local** |
| `segment` | associado, builder, prospect, ACIRVETE etc. |
| `association_status` | confirmado, não_associado, desconhecido |
| `source` | origem operacional do contato |
| `first_contact_at` | data/hora do primeiro contato |
| `last_contact_at` | última interação |
| `status` | PENDENTE, CONTATADO, RESPONDEU, FOLLOW_UP, RECUSOU, INVALIDO, ENCERRADO |
| `consent_or_context` | base/contexto da abordagem |
| `response_ref_local` | referência local à resposta |
| `notes_local` | observação operacional, sem promoção automática ao GitHub |

## Exportação para análise

Quando necessário, gerar uma segunda tabela sem identificadores diretos, com:
- `research_id`;
- `participant_hash_or_seq`;
- segmento;
- exposição;
- respostas codificadas;
- variáveis derivadas.

Somente agregados/anônimos e decisões podem ser promovidos para o ACIRV Notebook.
