---
Modificado:
  - sexta-feira 93 03/04/2026
Criado: quarta-feira 91 01/04/2026
---
A solução principal é uma **aplicação para encontrar automaticamente um horário compatível entre duas ou mais pessoas que precisam se reunir**, evitando a troca interminável de mensagens até achar um horário comum.

## Fase 1 — Ideia e Fundamento

Objetivo: validar a lógica da solução antes de pensar em construção.

### 1. Ideia Bruta

```text
Problema:
Marcar reuniões entre duas ou mais pessoas é um processo lento, confuso e desgastante, porque depende de idas e vindas para descobrir quem pode em qual horário.

Público:
Pessoas, equipes, diretorias, empresas, faculdades, cursos e grupos que precisam conciliar agendas para reuniões.

Solução:
Uma aplicação em que uma pessoa cria um convite de reunião, informa a pauta, compartilha um link com os participantes, e cada convidado sugere os horários em que pode participar. A plataforma cruza essas disponibilidades e encontra automaticamente o horário compatível para todos.

Diferencial:
Elimina a necessidade de ficar conversando repetidamente para achar um horário em comum, tornando o processo mais rápido, organizado e prático.
```

Essa estrutura foi extraída do trecho em que Raphael descreve a dificuldade de “conciliar a agenda de duas ou mais pessoas”, dá o exemplo de tentativas frustradas de combinar horários e propõe um sistema com convite por link e sugestão de disponibilidade por cada participante até encontrar a compatibilidade.

---

### 2. Refinamento da Ideia

**Problema → Solução → Valor**

```text
Problema
Pessoas que precisam se reunir perdem tempo tentando conciliar horários manualmente, em conversas fragmentadas e pouco eficientes.

Solução
Uma plataforma de agendamento colaborativo em que cada participante informa seus horários disponíveis e o sistema identifica automaticamente a melhor opção em comum.

Valor
Reduz atrito, economiza tempo e organiza o processo de marcação de reuniões de forma simples e objetiva.
```

A lógica central da ideia está bem clara no áudio: o ganho não está apenas em “marcar reunião”, mas em **tirar o trabalho manual da conciliação de agenda**.

---

### 3. Value Proposition

```text
Para equipes, grupos e profissionais que precisam marcar reuniões com outras pessoas, nosso produto é uma plataforma de conciliação de agenda que coleta disponibilidades por link e encontra automaticamente o melhor horário em comum, diferente da combinação manual por mensagem, porque reduz conversa desnecessária, acelera a decisão e organiza o processo.
```

Isso reflete exatamente o mecanismo citado por Raphael: alguém cria a reunião, envia o link, cada um informa quando pode, e o sistema encontra o horário compatível para todos.

---

### 4. Manifesto do Produto

```text
Marcar uma reunião não deveria ser um problema.

Hoje, sempre que duas ou mais pessoas precisam se encontrar, o processo costuma virar uma troca cansativa de mensagens, tentativas e desencontros de horário.

Isso importa porque tempo, agilidade e organização são fundamentais para qualquer equipe, empresa ou grupo.

Acreditamos que a tecnologia deve eliminar atritos simples do dia a dia, especialmente aqueles que se repetem com frequência.

Nossa visão é tornar o agendamento de reuniões mais inteligente, direto e sem esforço.

Resolvemos isso com uma plataforma em que uma pessoa cria o convite, os participantes informam sua disponibilidade e o sistema encontra automaticamente o horário que funciona para todos.
```

---

# Fase 2 — Estrutura do Produto

Agora saímos da ideia e entramos no produto.

---

# 5 — Definição do MVP

A pergunta é:

> Qual é o menor produto que resolve esse problema de verdade?

### MVP inclui:

- criação de uma reunião com título ou pauta
    
- geração de link de convite
    
- envio do link para participantes
    
- campo para cada participante informar horários disponíveis
    
- cruzamento automático das disponibilidades
    
- exibição do melhor horário compatível
    
- confirmação final do horário escolhido
    

### Fica fora do MVP:

- integração com Google Calendar ou Outlook
    
- lembretes automáticos complexos
    
- reagendamento inteligente
    
- múltiplas regras avançadas de prioridade
    
- dashboards gerenciais
    
- versão corporativa com times/departamentos
    
- recursos de monetização ou white-label
    

### Definição objetiva do MVP

```text
Um usuário cria uma reunião, define a pauta, gera um link e compartilha com os convidados. Cada convidado informa os horários em que pode participar. O sistema cruza as respostas e aponta o horário compatível entre todos.
```

Aqui está a lista de funcionalidades adaptada para o escopo do **ACIRV MEET**, mantendo a estrutura solicitada e aplicando o rigor de UX para garantir baixa fricção no MVP:

# 6 — Lista de Funcionalidades (MVP ACIRV MEET)

**Auth (Fricção Reduzida)**
*   **Login / Cadastro (Organizador):** Acesso completo para gerenciar reuniões.
*   **Acesso de Convidado (Participante):** Entrada via link único sem necessidade de criar conta (Lei da Simplicidade), solicitando apenas nome para identificação.

**Gestão de Reuniões (Organizador)**
*   **Criar Reunião:** Definição de título, pauta e duração.
*   **Gerar Link de Convite:** URL única e compartilhável.
*   **Painel de Status:** Visualização de quem já respondeu e quem falta.

**Disponibilidade (Participante)**
*   **Grid de Horários:** Interface visual (padrão de calendário) para selecionar múltiplos slots de tempo disponíveis.
*   **Edição de Resposta:** Possibilidade de alterar os horários informados antes do fechamento da reunião.

**Inteligência de Cruzamento**
*   **Visualizador de Compatibilidade:** Exibição imediata para o organizador dos horários onde há 100% de convergência.
*   **Sugestão de "Melhor Opção":** Caso não haja 100%, o sistema sugere o horário com maior quórum.

**Confirmação**
*   **Fechamento de Agenda:** O organizador seleciona o horário final.
*   **Notificação de Resultado:** Tela de sucesso para todos os participantes com o horário definido e opção de "Adicionar ao Calendário" (ics file).

# Fase 3 — Arquitetura do Produto

# 7 — Entidades do Sistema (Data Model)

```text
User
Meeting
Participant
Availability
```

---

### 💡 Nota do Consultor:
A separação estrita entre `User` (quem cria a conta e organiza) e `Participant` (quem clica no link e apenas digita o nome) é o que garante a **Lei 2 (Simplicidade)**. Do ponto de vista de arquitetura de dados e UX, não forçar a criação de um `User` para cada `Participant` reduz a fricção de entrada a zero. A entidade `Availability` amarra o participante ao horário de forma atômica para permitir o cruzamento ágil.

---

# 8 — Estrutura do Banco (SQL)

```sql
-- 1. USERS: Apenas para quem organiza (Auth)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. MEETINGS: A reunião criada (O "id" é o próprio token do link de convite)
CREATE TABLE meetings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organizer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration_minutes INT DEFAULT 60,
    status VARCHAR(50) DEFAULT 'open', -- 'open' (coletando) ou 'closed' (decidido)
    final_start_time TIMESTAMP WITH TIME ZONE, -- Preenchido quando o organizador bate o martelo
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. PARTICIPANTS: Fricção zero (Não exige email ou senha, apenas o nome)
CREATE TABLE participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID REFERENCES meetings(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. AVAILABILITIES: Os blocos de tempo que cada participante marcou no Grid
CREATE TABLE availabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    participant_id UUID REFERENCES participants(id) ON DELETE CASCADE,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices recomendados para performance no cruzamento de dados
CREATE INDEX idx_availabilities_participant ON availabilities(participant_id);
CREATE INDEX idx_participants_meeting ON participants(meeting_id);
```

### 💡 Nota do Consultor:
*   **Segurança Silenciosa (UX):** Usamos `UUID` em todas as tabelas. Isso significa que o ID da `meeting` será algo como `f47ac10b-58cc-4372-a567-0e02b2c3d479`. Esse ID já serve como URL segura do convite (`acirvmeet.com/invite/f47a...`), eliminando a necessidade de criar tokens complexos ou senhas de acesso. O usuário clica e entra. Simples.
*   **Manutenção Pragmática:** O `ON DELETE CASCADE` garante que, se o organizador cancelar/deletar a reunião, todos os participantes e horários atrelados somem automaticamente, evitando "lixo" no banco de dados.

---

# Fase 4 — UX do Produto

# 9 — Mapa de Navegação

```text
Home (Landing Page)
 ├ Login
 ├ Cadastro
 │
 ├ Dashboard (Minhas Reuniões)
 │   ├ Criar Nova Reunião
 │   └ Detalhe da Reunião (Painel do Organizador)
 │       └ Confirmar Horário Final
 │
 └[URL do Convite] Tela de Entrada do Participante
     ├ Informar Nome
     ├ Selecionar Disponibilidade (Grid)
     └ Tela de Sucesso / Resultado Final
```

### 💡 Nota do Consultor:
Observe a aplicação estrita da **Lei dos 3 Cliques**. O participante que recebe o link de convite tem apenas três passos em uma jornada linear e isolada: abrir o link $\rightarrow$ digitar o nome $\rightarrow$ marcar na grade e salvar. Não há menus de topo, rodapés complexos ou distrações na rota do participante (redução de carga cognitiva de acordo com a **Lei 8 - White Space** e **Atenção** do Método SOMA).

---

# 10 — User Flow

**Organizador**
```text
Fazer Login / Cadastro
↓
Acessar Dashboard
↓
Criar Reunião (Definir pauta e duração)
↓
Gerar e Copiar Link de Convite
↓
Visualizar Painel (Acompanhar respostas e cruzamento)
↓
Confirmar Horário Final
```

**Participante (Convidado)**
```text
Acessar Link de Convite (URL única)
↓
Informar Nome (Sem criar conta)
↓
Selecionar Disponibilidade (Clicar nos blocos livres no Grid)
↓
Salvar
↓
Visualizar Confirmação (Sucesso)
```

### 💡 Nota do Consultor:
O fluxo do Participante representa a aplicação direta da **Microcopy Focada na Ação**. O usuário não "Agenda uma consulta", ele "Salva". Não há atalhos mentais complexos. Ao separar a jornada de quem cria (gestão) da jornada de quem responde (ação rápida), blindamos a experiência mobile contra a sobrecarga cognitiva e evitamos o abandono no meio do processo.

---

# 11 — Fluxos Críticos

*   **Onboarding & Criação (Time-to-Value):** O caminho desde o cadastro do organizador até a geração do primeiro link de convite copiável. Precisa durar menos de 60 segundos.
*   **Adesão do Convidado (Fricção Zero):** A experiência do participante ao abrir o link pelo celular, preencher apenas o nome e tocar nos blocos livres do calendário.
*   **Cruzamento Inteligente (O Core do Produto):** A engine processando as respostas e desenhando visualmente (Mapa de Calor) a sobreposição perfeita de horários para o organizador.
*   **Decisão e Fechamento:** A aprovação em "um clique" da melhor sugestão pelo organizador, mudando o status da reunião e gerando a visão de confirmação final para todos.

### 💡 Nota do Consultor:
Como especialista em alta conversão, reafirmo: o fluxo **Adesão do Convidado** é onde você ganha ou perde o jogo. Se a renderização do Grid de horários quebrar no mobile (violando a Lei do Mobile-First) ou os botões de seleção forem menores que 44x44px (violando a Anatomia Perfeita do Botão), o usuário vai fechar a aba e mandar um áudio no WhatsApp dizendo *"não consegui usar, que horas vocês podem?"*, matando a proposta de valor do sistema na hora. Atenção maníaca nesta tela.

---

# Fase 5 — Especificação de Telas

# 12 — Sprint de Produto

```text
Tela: Login / Cadastro
Elementos
- logo do ACIRV MEET
- campo de email
- campo de senha
- link "Esqueci minha senha"
Botões
- Entrar
- Criar Nova Conta
Ação
- autenticar e redirecionar para o Dashboard

Tela: Dashboard (Organizador)
Elementos
- título "Minhas Reuniões"
- lista de cards de reuniões (exibindo: Título, Data de Criação e Status [Aberta/Fechada])
- indicador de quórum (ex: "4 pessoas já responderam")
Botões
- Nova Reunião (CTA Primário - Alto Contraste)
- Sair
Ação
- clicar em "Nova Reunião" abre Tela de Criação
- clicar num card de reunião abre o Painel da Reunião

Tela: Criar Nova Reunião (Organizador)
Elementos
- campo de texto (Título/Pauta)
- campo de texto opcional (Descrição curta)
- seletor de duração (15min, 30min, 60min, customizado)
Botões
- Gerar Link Mágico
- Cancelar
Ação
- salvar no banco, gerar URL única e abrir o Painel da Reunião com o link já copiado para a área de transferência

Tela: Painel da Reunião (Organizador)
Elementos
- bloco de compartilhamento (exibindo o link mágico)
- lista de participantes (quem já votou)
- engine visual: "Mapa de Calor" ou lista de "Horários Sugeridos" ranqueados por compatibilidade (ex: "Quarta 14h - 100% de match")
Botões
- Copiar Link
- Confirmar este Horário (CTA Primário atrelado ao horário sugerido)
- Excluir Reunião (CTA Secundário/Destrutivo)
Ação
- clicar em "Confirmar" trava a reunião, altera o status para fechada e define o resultado final.

Tela: Entrada do Participante (Mobile-first)
Elementos
- card minimalista com Título da Reunião e Duração (Contexto)
- texto instrucional pragmático: "Identifique-se para escolher seu horário."
- campo de texto: "Seu Nome"
Botões
- Ver Horários
Ação
- salva o nome na sessão e avança para a grade de seleção

Tela: Seleção de Disponibilidade (O Grid)
Elementos
- instruções: "Toque nos horários que você tem livres."
- grade vertical de dias e horas (blocos grandes, no mínimo 44x44px)
- feedback visual tátil: bloco muda de cinza (vazio) para a cor primária (selecionado) ao toque
Botões
- Salvar Disponibilidade (Fixo na base da tela - Sticky Button)
- Voltar
Ação
- tocar em blocos marca/desmarca horários
- clicar em "Salvar" grava os dados e leva à tela de sucesso

Tela: Sucesso (Participante)
Elementos
- ícone de sucesso (Microinteração de check)
- texto: "Pronto! Seus horários foram enviados."
- texto secundário: "Avisaremos o organizador."
Botões
- Crie sua própria reunião grátis (Estratégia de Aquisição/Viralidade)
Ação
- fim da jornada do usuário
```

### 💡 Nota do Consultor:
Este Sprint obedece à **Lei 6 (Ancoragem no Grid)** e à **Microcopy Focada na Ação**. Note a tela de Sucesso do Participante: adicionamos um botão *"Crie sua própria reunião grátis"*. Essa é uma tática de **Growth Design (Ação de Aquisição)**. Como o usuário teve "Fricção Zero" para responder e achou o sistema incrível, aproveitamos o momento de alívio cognitivo (tarefa concluída) para convertê-lo em um novo Organizador (User). É assim que produtos digitais escalam sem gastar com marketing.

---

# Fase 6 — Modelagem Técnica

# 13 — Regras do Sistema

```text
- uma reunião só pode ter dois status: 'open' (coletando votos) ou 'closed' (horário definido).
- participantes não precisam de conta para interagir com uma reunião 'open'.
- um participante não pode adicionar horários a uma reunião 'closed'.
- a engine de cruzamento (mapa de calor) só processa os dados dos participantes vinculados ao ID específico daquela reunião.
- se uma reunião for apagada, todos os participantes e horários vinculados a ela são destruídos (Cascade).
```

---

# 14 — Permissões

```text
organizador (usuário autenticado)
- criar, editar e excluir as próprias reuniões.
- visualizar todos os participantes e horários das suas reuniões.
- alterar o status da sua reunião de 'open' para 'closed'.
- não pode ver reuniões de outros organizadores.

participante (visitante via link mágico)
- visualizar detalhes básicos da reunião (título, duração, organizador).
- criar um registro de participante (nome).
- enviar blocos de horários disponíveis.
- não pode excluir a reunião, nem visualizar os horários exatos votados por outras pessoas individualmente (evita viés).
```

---

# Fase 7 — Integrações

Como este é o MVP pragmático focado em Fricção Zero, a infraestrutura deve ser enxuta.

```text
Supabase
- Database (PostgreSQL para armazenar reuniões, participantes e grids).
- Auth (Gerenciamento de login do Organizador).

Biblioteca ICS (Frontend nativo)
- Em vez de integrar a API complexa do Google Calendar no MVP, usamos uma biblioteca JavaScript simples (ex: ics.js) para gerar um botão "Adicionar ao Calendário" na tela de sucesso.
```

---

# Fase 8 — Segurança

A segurança aqui deve proteger os dados do organizador sem criar barreiras (logins obrigatórios) para o participante. A chave é o **RLS (Row Level Security)** do Postgres/Supabase.

```text
autenticação
- necessária apenas para o Organizador (Email/Senha ou Magic Link do Supabase).

RLS (Políticas de Nível de Linha)
- tabela 'meetings': Organizadores só podem dar SELECT, UPDATE e DELETE onde organizer_id = auth.uid(). 
- tabela 'meetings': Visitantes anônimos podem dar SELECT em uma reunião específica usando apenas o ID (Link de Convite).
- tabela 'participants': Visitantes anônimos podem dar INSERT apenas se o status da reunião consultada for 'open'.
- tabela 'availabilities': Inserção pública permitida durante o fluxo do participante; SELECT restrito apenas ao organizador da reunião correspondente.

validação (Frontend e Backend)
- bloqueio de sobreposição matemática: garantir que a 'data_final' do bloco do participante seja sempre posterior à 'data_inicial'.
- sanitização: o campo 'nome' do participante deve aceitar apenas texto simples para evitar injeções XSS.
```

### 💡 Nota Final do Consultor Estratégico:
Com este documento de **Modelagem Técnica e Segurança**, você acaba de concluir o "Handoff Blindado" (Lei 10 do nosso Playbook). As regras de RLS descritas acima garantem que a **Lei 4 (Confiança)** não seja quebrada: dados de empresas não vazarão, e os participantes terão a agilidade prometida na **Lei 1 (Expectativa do Usuário)**. Seu MVP do **ACIRV MEET** está estruturado para ser construído em poucos dias com uma arquitetura de produto de padrão global. 