Viewed EventSelector.tsx:1-60

Aqui está o **passo a passo completo e prático** de como funciona a separação entre os participantes do **Café Entre Amigos** e da **SudoExpo 2026** pelo Painel do Admin, além de como trazer participantes do Café para a SudoExpo com segurança.

---

### Como a separação funciona na prática

A separação é **nativa e automática no banco de dados** por meio do campo `event_id`:
- **`cafe-entre-amigos-ago-2026`**: Guarda todo o histórico do evento piloto.
- **`sudoexpo-2026`**: É a base oficial e limpa da feira atual.
- **Regra de Ouro**: O motor de matching só cruza participantes que tenham **o mesmo `event_id`**. Quem estiver apenas no Café **jamais** receberá match com alguém cadastrado na SudoExpo 2026.

---

### Passo a Passo no Painel do Admin

#### 1. Selecionar qual evento você deseja gerenciar
No topo do painel administrativo (em `/admin`, `/admin/participantes` ou `/admin/matches`):
1. No canto superior direito do cabeçalho, localize o **Seletor de Evento** (ícone de calendário).
2. Clique no menu dropdown:
   - **SudoExpo 2026 (Ativo)**: Mostra apenas os participantes novos inscritos para a feira ou veteranos que já fizeram check-in.
   - **Café Entre Amigos — ACIRV (Agosto 2026) (Passado)**: Mostra os participantes históricos do evento piloto.
   - **Ambiente de Testes / Sandbox**: Para simulações.
3. Ao trocar o evento, **todas as métricas, lista de participantes e matches** são filtrados instantaneamente para aquele evento.

---

#### 2. Visualizar os participantes do Café Entre Amigos
1. Com o seletor em **"Café Entre Amigos"**, acesse a aba **Participantes** (`/admin/participantes`).
2. Você verá a lista de empresários que participaram do evento piloto.
3. Clique em qualquer participante para abrir a **gaveta lateral de detalhes** (`ParticipantDetailSheet`).

---

#### 3. Fazer o "Check-in" de um participante do Café na SudoExpo 2026
Quando um participante do Café comparecer presencialmente à SudoExpo 2026 e a equipe quiser ativá-lo para que ele comece a receber matches na feira:

* **Opção A — Pelo Painel do Admin (Equipe de Credenciamento)**:
  1. No painel, com o evento "Café Entre Amigos" selecionado, localize o participante.
  2. Na linha do participante ou dentro da gaveta de detalhes, clique no botão:
     👉 **"Fazer Check-in na SudoExpo 2026"**.
  3. O sistema irá:
     - Criar o cadastro dele na SudoExpo 2026.
     - Clonar automaticamente suas ofertas, necessidades e dados da empresa (sem ele ter que digitar nada).
     - Calcular na hora os matches dele com os outros participantes da SudoExpo 2026.
     - **Manter o histórico do Café 100% intacto**.

* **Opção B — O próprio participante faz sozinho pelo WhatsApp (Auto Check-in)**:
  1. O participante acessa o site do evento e clica em **"Acessar com WhatsApp"**.
  2. Ao digitar o número do WhatsApp:
     - O sistema identifica automaticamente: *"Olá, [Nome] da [Empresa]! Identificamos seu cadastro do Café Entre Amigos. Deseja fazer Check-in na SudoExpo 2026?"*.
  3. Ele clica em **"Confirmar Presença na SudoExpo 2026"** (1 clique) e já cai direto na tela com seus matches calculados para a feira!

---

#### 4. Como excluir ou reiniciar cadastros caso necessário
Se você precisar apagar um participante específico (por exemplo, um teste que fez com seu próprio número na SudoExpo para liberar o WhatsApp):
1. Vá em `/admin/participantes`.
2. Localize o participante e clique no botão vermelho **"Excluir"**.
3. Confirme na caixa de diálogo. O sistema apagará os dados em cascata e **liberará o número de WhatsApp imediatamente** para um novo cadastro.

---

> [!TIP]
> **Importante para o banco no Supabase**:
> Certifique-se de que a migration `supabase/migrations/20260909155500_multi_eventos_separacao_e_checkin.sql` e a `20260909171500_sandbox_e_delecao_participante.sql` foram executadas no SQL Editor do seu projeto Supabase. Elas criam os eventos `'cafe-entre-amigos-ago-2026'` e `'sandbox-sudoexpo'` e instalam as funções de check-in e exclusão.