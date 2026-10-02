Faça o abaixo, resolve os conflitos e junta tudo no main.

Você está atuando como Engenheiro / Arquiteto do Hermes Workstation.

Foi criado recentemente um arquivo de inteligência centralizada no repositório: `workstation/context/HERMES_WORKSTATION_INTELLIGENCE.md`

Este arquivo é a fonte única de conhecimento duradouro sobre a arquitetura, o funcionamento real e a integração do **Hermes Work** (Hermes Workstation) entre todas as frentes (Electron Desktop, BrowserRuntime, Gateway, IPC, Workstation Controller, SessionDB, BrowserTask, etc.).

### Sua Tarefa:

1. **Leia** o conteúdo atual de `workstation/context/HERMES_WORKSTATION_INTELLIGENCE.md`.
2. **Complemente e enriqueça** esse documento trazendo **tudo o que você sabe, descobriu ou validou nesta sessão** sobre o Hermes Workstation. Não limite-se ao básico; inclua detalhes técnicos reais, tais como:
   - Como as partes do seu escopo conversam entre si (fluxos IPC, payloads, tokens, rotas, portas/loopback);
   - Invariantes críticos, armadilhas comuns e edge-cases descobertos;
   - Ciclo de vida de processos, isolamento de sessão e contratos de persistência;
   - Como os testes provam essas mecânicas e o que NÃO deve ser feito (anti-patterns);
   - Conexões com subsistemas existentes (Gateway, Kanban, Chat, etc.).

### Regras de Edição:

- **Não apague** os conceitos e seções já consolidados no documento; mescle, expanda ou adicione novas seções lógicas organizadas.
- Mantenha o formato limpo, direto e técnico em Markdown.
- Faça as modificações diretamente no arquivo e apresente um resumo das contribuições e melhorias adicionadas.