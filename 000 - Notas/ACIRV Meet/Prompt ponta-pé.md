---
Modificado:
  - segunda-feira 96 06/04/2026
  - sexta-feira 93 03/04/2026
Criado: sexta-feira 93 03/04/2026
---
Aja como um **Arquiteto de Produto + Desenvolvedor Full-Stack Sênior + Especialista em UX/UI**.  
Sua tarefa é **construir de verdade**, e não apenas prototipar visualmente, o MVP web funcional chamado **ACIRV MEET**.

O produto resolve um problema simples e recorrente: **conciliar horários entre duas ou mais pessoas sem depender de idas e vindas por mensagem**.

---

# 0) PRINCÍPIO CENTRAL DO PRODUTO

O ACIRV MEET tem dois papéis totalmente distintos:

## Organizador
- cria conta
- faz login
- cria reuniões
- acompanha respostas
- confirma o horário final

## Participante (convidado)
- **não cria conta**
- entra por link
- informa apenas o nome
- seleciona disponibilidade
- salva

### Regra máxima
A experiência do participante deve ser **fricção zero** e **mobile-first**.  
Se houver qualquer conflito entre “sofisticação técnica” e “simplicidade do convidado”, preserve a simplicidade do convidado.

---

# 1) GUARDRAILS OBRIGATÓRIOS

Siga estas regras sem improvisar:

1. **NÃO crie tabela pública `users` com `password_hash`.**
   - Use **Supabase Auth** para credenciais.
   - Use uma tabela pública `profiles` ligada a `auth.users`.

2. **NÃO implemente Google Calendar OAuth, Outlook OAuth, notificações complexas, reminders automáticos, times/departamentos, monetização, white-label, IA extra ou features enterprise.**
   - O MVP deve usar **arquivo `.ics`** para “Adicionar ao calendário”.

3. **NÃO force login para o participante.**
   - O participante entra por link e informa somente o nome.

4. **NÃO entregue mockup solto, demo fake ou páginas desconectadas.**
   - Quero CRUD real ligado ao Supabase.

5. **NÃO misture a área do organizador com a jornada do participante.**
   - São fluxos separados.

6. **NÃO deixe o grid do participante quebrar no mobile.**
   - Sem rolagem horizontal obrigatória para usar a tela.
   - Botões e células clicáveis devem ser grandes e táteis.
   - CTA principal do participante deve ficar fixo na base da tela.

7. **NÃO exponha para participantes os horários exatos dos outros participantes.**
   - O organizador pode ver o painel completo.
   - O participante só vê a própria jornada e, quando a reunião for fechada, o resultado final.

8. Se alguma parte do projeto atual já existir, **preserve o que está funcionando** e aplique as mudanças sem quebrar o restante.

---

# 2) ESCOPO REAL DO MVP

## Inclui
- landing page simples
- login/cadastro do organizador
- dashboard de reuniões
- criação de reunião
- geração de link único de convite
- entrada do participante via link, sem conta
- captura de nome do participante
- seleção de disponibilidade em grid visual
- salvamento de disponibilidade
- painel do organizador com:
  - participantes que já responderam
  - horários sugeridos por compatibilidade
  - destaque para 100% de match
  - melhor opção por quórum quando não houver 100%
- confirmação final do horário
- tela final com opção de adicionar ao calendário por `.ics`

## Fica fora do MVP
- integração OAuth com Google Calendar / Outlook
- lembretes automáticos sofisticados
- reagendamento inteligente
- múltiplas regras avançadas de prioridade
- dashboards corporativos
- times/departamentos
- monetização
- white-label

---

# 3) STACK TÉCNICA

Use esta stack:

- **Frontend:** React + Vite + TypeScript
- **UI:** Tailwind CSS + componentes limpos e modernos
- **Forms/validação:** React Hook Form + Zod
- **Datas:** date-fns + suporte a timezone
- **Backend/BaaS:** Supabase
- **Auth:** Supabase Auth
- **Database:** PostgreSQL
- **Calendar export:** biblioteca JS para gerar `.ics`

Se precisar escolher bibliotecas auxiliares:
- priorize simplicidade
- evite dependências pesadas
- evite abstrações desnecessárias

---

# 4) ARQUITETURA DE DOMÍNIO

## Entidades principais

### `profiles`
Dados públicos mínimos do organizador autenticado.

### `meetings`
A reunião criada pelo organizador.

### `participants`
Os convidados da reunião.
Não têm conta.
Entram por link e se identificam apenas pelo nome.

### `availabilities`
Blocos de tempo informados por cada participante.

---

# 5) DECISÕES DE PRODUTO QUE VOCÊ DEVE ASSUMIR COMO DEFINITIVAS

Para o grid funcionar de forma consistente, a reunião precisa definir:

- título
- descrição opcional
- duração da reunião em minutos
- **janela de votação**:
  - data inicial
  - data final
  - horário inicial diário
  - horário final diário
- granularidade dos slots (`slot_minutes`)

Sem isso, o calendário fica arbitrário. Portanto, **isso faz parte do MVP**.

## Comportamento esperado
Exemplo:
- duração da reunião: 60 min
- janela: 15/04 até 18/04
- faixa diária: 08:00 às 18:00
- granularidade: 30 min

A UI deve gerar os slots possíveis dentro dessa janela.

---

# 6) ROTAS DO APP

Implemente estas rotas:

- `/` → Landing page
- `/auth` → Login / Cadastro
- `/dashboard` → Lista de reuniões do organizador
- `/meetings/new` → Criar nova reunião
- `/meetings/:id` → Painel da reunião do organizador
- `/invite/:id` → Entrada do participante
- `/invite/:id/availability` → Grid de disponibilidade do participante
- `/invite/:id/success` → Tela de sucesso do participante

Se preferir consolidar as telas do participante em menos rotas, pode fazer, desde que a UX fique extremamente clara.

---

# 7) MODELO DE DADOS — SQL DEFINITIVO

Crie o schema abaixo.

```sql
create extension if not exists pgcrypto;

-- =========================================
-- PROFILES
-- =========================================
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

-- Trigger para criar profile automaticamente ao criar usuário no Auth
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, full_name)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'full_name', '')
  )
  on conflict (id) do nothing;

  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;

create trigger on_auth_user_created
after insert on auth.users
for each row execute procedure public.handle_new_user();

-- =========================================
-- MEETINGS
-- =========================================
create table if not exists public.meetings (
  id uuid primary key default gen_random_uuid(),
  organizer_id uuid not null references public.profiles(id) on delete cascade,
  title text not null,
  description text,
  timezone_name text not null default 'America/Sao_Paulo',
  duration_minutes integer not null default 60 check (duration_minutes > 0 and duration_minutes <= 480),
  slot_minutes integer not null default 30 check (slot_minutes in (15, 30, 60)),
  window_start_date date not null,
  window_end_date date not null,
  day_start_time time not null,
  day_end_time time not null,
  status text not null default 'open' check (status in ('open', 'closed')),
  final_start_time timestamptz,
  final_end_time timestamptz,
  created_at timestamptz not null default now(),
  constraint meetings_window_valid check (window_end_date >= window_start_date),
  constraint meetings_daytime_valid check (day_end_time > day_start_time)
);

create index if not exists idx_meetings_organizer_id on public.meetings(organizer_id);
create index if not exists idx_meetings_status on public.meetings(status);

alter table public.meetings enable row level security;

-- =========================================
-- PARTICIPANTS
-- =========================================
create table if not exists public.participants (
  id uuid primary key default gen_random_uuid(),
  meeting_id uuid not null references public.meetings(id) on delete cascade,
  name text not null check (char_length(trim(name)) between 2 and 120),
  edit_token uuid not null default gen_random_uuid(),
  created_at timestamptz not null default now()
);

create index if not exists idx_participants_meeting_id on public.participants(meeting_id);
create index if not exists idx_participants_edit_token on public.participants(edit_token);

alter table public.participants enable row level security;

-- =========================================
-- AVAILABILITIES
-- =========================================
create table if not exists public.availabilities (
  id uuid primary key default gen_random_uuid(),
  participant_id uuid not null references public.participants(id) on delete cascade,
  start_time timestamptz not null,
  end_time timestamptz not null,
  created_at timestamptz not null default now(),
  constraint availabilities_valid_range check (end_time > start_time),
  unique (participant_id, start_time, end_time)
);

create index if not exists idx_availabilities_participant_id on public.availabilities(participant_id);
create index if not exists idx_availabilities_start_time on public.availabilities(start_time);

alter table public.availabilities enable row level security;

-- =========================================
-- RLS: PROFILES
-- =========================================
drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_own"
on public.profiles
for select
to authenticated
using (id = auth.uid());

drop policy if exists "profiles_update_own" on public.profiles;
create policy "profiles_update_own"
on public.profiles
for update
to authenticated
using (id = auth.uid())
with check (id = auth.uid());

-- =========================================
-- RLS: MEETINGS
-- =========================================
drop policy if exists "meetings_select_own" on public.meetings;
create policy "meetings_select_own"
on public.meetings
for select
to authenticated
using (organizer_id = auth.uid());

drop policy if exists "meetings_insert_own" on public.meetings;
create policy "meetings_insert_own"
on public.meetings
for insert
to authenticated
with check (organizer_id = auth.uid());

drop policy if exists "meetings_update_own" on public.meetings;
create policy "meetings_update_own"
on public.meetings
for update
to authenticated
using (organizer_id = auth.uid())
with check (organizer_id = auth.uid());

drop policy if exists "meetings_delete_own" on public.meetings;
create policy "meetings_delete_own"
on public.meetings
for delete
to authenticated
using (organizer_id = auth.uid());

-- =========================================
-- RLS: PARTICIPANTS (somente organizador vê)
-- =========================================
drop policy if exists "participants_select_for_owner" on public.participants;
create policy "participants_select_for_owner"
on public.participants
for select
to authenticated
using (
  exists (
    select 1
    from public.meetings m
    where m.id = participants.meeting_id
      and m.organizer_id = auth.uid()
  )
);

-- =========================================
-- RLS: AVAILABILITIES (somente organizador vê)
-- =========================================
drop policy if exists "availabilities_select_for_owner" on public.availabilities;
create policy "availabilities_select_for_owner"
on public.availabilities
for select
to authenticated
using (
  exists (
    select 1
    from public.participants p
    join public.meetings m on m.id = p.meeting_id
    where p.id = availabilities.participant_id
      and m.organizer_id = auth.uid()
  )
);

-- =========================================
-- RPC PÚBLICA: buscar dados seguros da reunião
-- =========================================
create or replace function public.get_public_meeting(p_meeting_id uuid)
returns table (
  id uuid,
  title text,
  description text,
  timezone_name text,
  duration_minutes integer,
  slot_minutes integer,
  window_start_date date,
  window_end_date date,
  day_start_time time,
  day_end_time time,
  status text,
  final_start_time timestamptz,
  final_end_time timestamptz
)
language sql
security definer
set search_path = public
as $$
  select
    m.id,
    m.title,
    m.description,
    m.timezone_name,
    m.duration_minutes,
    m.slot_minutes,
    m.window_start_date,
    m.window_end_date,
    m.day_start_time,
    m.day_end_time,
    m.status,
    m.final_start_time,
    m.final_end_time
  from public.meetings m
  where m.id = p_meeting_id;
$$;

grant execute on function public.get_public_meeting(uuid) to anon, authenticated;

-- =========================================
-- RPC PÚBLICA: criar participante
-- =========================================
create or replace function public.create_participant_for_meeting(
  p_meeting_id uuid,
  p_name text
)
returns table (
  participant_id uuid,
  edit_token uuid
)
language plpgsql
security definer
set search_path = public
as $$
declare
  v_status text;
  v_participant_id uuid;
  v_edit_token uuid;
begin
  select status into v_status
  from public.meetings
  where id = p_meeting_id;

  if v_status is null then
    raise exception 'meeting_not_found';
  end if;

  if v_status <> 'open' then
    raise exception 'meeting_closed';
  end if;

  insert into public.participants (meeting_id, name)
  values (p_meeting_id, trim(p_name))
  returning id, edit_token into v_participant_id, v_edit_token;

  return query
  select v_participant_id, v_edit_token;
end;
$$;

grant execute on function public.create_participant_for_meeting(uuid, text) to anon, authenticated;

-- =========================================
-- RPC PÚBLICA: substituir disponibilidades do participante
-- =========================================
create or replace function public.replace_participant_availabilities(
  p_participant_id uuid,
  p_edit_token uuid,
  p_slots jsonb
)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  v_meeting_status text;
begin
  select m.status
  into v_meeting_status
  from public.participants p
  join public.meetings m on m.id = p.meeting_id
  where p.id = p_participant_id
    and p.edit_token = p_edit_token;

  if v_meeting_status is null then
    raise exception 'invalid_participant_or_token';
  end if;

  if v_meeting_status <> 'open' then
    raise exception 'meeting_closed';
  end if;

  delete from public.availabilities
  where participant_id = p_participant_id;

  insert into public.availabilities (participant_id, start_time, end_time)
  select
    p_participant_id,
    (slot ->> 'start_time')::timestamptz,
    (slot ->> 'end_time')::timestamptz
  from jsonb_array_elements(p_slots) as slot
  where (slot ->> 'start_time') is not null
    and (slot ->> 'end_time') is not null
    and (slot ->> 'end_time')::timestamptz > (slot ->> 'start_time')::timestamptz;
end;
$$;

grant execute on function public.replace_participant_availabilities(uuid, uuid, jsonb) to anon, authenticated;
````

---

# 8) REGRAS FUNCIONAIS

## Status da reunião

A reunião só pode ter dois status:

- `open`
    
- `closed`
    

## Quando `open`

- organizador acompanha respostas
    
- participante pode entrar
    
- participante pode enviar disponibilidade
    
- participante pode editar a própria disponibilidade usando `participant_id + edit_token` armazenados em `localStorage`
    

## Quando `closed`

- participante não pode mais alterar disponibilidade
    
- tela do participante deve mostrar o resultado final
    
- o organizador vê o horário escolhido como definitivo
    

## Exclusão

Se o organizador apagar a reunião, tudo vinculado deve ser removido em cascata.

---

# 9) ALGORITMO DE COMPATIBILIDADE

Implemente a lógica de cruzamento assim:

1. Gere todos os slots possíveis com base em:
    
    - `window_start_date`
        
    - `window_end_date`
        
    - `day_start_time`
        
    - `day_end_time`
        
    - `slot_minutes`
        
    - `duration_minutes`
        
2. Um participante conta como compatível com um slot quando tiver uma disponibilidade que cubra integralmente o intervalo necessário da reunião.
    
3. Para cada slot candidato, calcule:
    
    - `match_count`
        
    - `total_participants`
        
    - `match_percentage`
        
4. Ordene os slots por:
    
    - maior `match_count`
        
    - maior `match_percentage`
        
    - menor data/hora
        
5. No painel do organizador:
    
    - destaque slots com `100% de match`
        
    - se não houver 100%, mostre a “melhor opção” por quórum
        
    - mostre rótulos como:
        
        - `100% de match`
            
        - `3 de 4 participantes`
            
        - `Melhor opção disponível`
            
6. Ao confirmar o horário:
    
    - grave `final_start_time`
        
    - grave `final_end_time`
        
    - altere status para `closed`
        

---

# 10) UX E TELAS

## Landing Page `/`

Objetivo:

- explicar o produto em 1 tela
    
- CTA para organizador criar conta
    
- visual limpo, moderno, confiável
    

Seções mínimas:

- hero
    
- problema
    
- como funciona em 3 passos
    
- CTA principal
    
- CTA secundário para login
    

---

## `/auth`

Tela única com tabs ou alternância entre:

- Entrar
    
- Criar conta
    

Campos:

- email
    
- senha
    
- nome completo no cadastro
    

Ações:

- autenticar com Supabase Auth
    
- criar profile automaticamente
    
- redirecionar para `/dashboard`
    

---

## `/dashboard`

Elementos:

- título “Minhas Reuniões”
    
- botão primário “Nova Reunião”
    
- cards com:
    
    - título
        
    - data de criação
        
    - status
        
    - número de participantes que já responderam
        

Ações:

- abrir reunião
    
- criar nova reunião
    
- sair
    

---

## `/meetings/new`

Formulário com:

- título/pauta
    
- descrição opcional
    
- duração da reunião
    
- granularidade do slot
    
- data inicial da janela
    
- data final da janela
    
- horário inicial diário
    
- horário final diário
    
- timezone
    

Botões:

- Gerar Link de Convite
    
- Cancelar
    

Ao salvar:

- cria reunião no banco
    
- redireciona para `/meetings/:id`
    
- copia o link para área de transferência
    
- mostra feedback visual de “link copiado”
    

---

## `/meetings/:id`

Painel do organizador.

Mostrar:

- bloco com link da reunião
    
- botão copiar link
    
- status da reunião
    
- lista de participantes que já responderam
    
- contador total de respostas
    
- ranking de horários sugeridos
    
- destaque visual para melhores horários
    
- ação de confirmar horário
    
- ação destrutiva para excluir reunião
    

Botões:

- Copiar Link
    
- Confirmar este Horário
    
- Excluir Reunião
    

Importante:

- essa tela é o core do organizador
    
- deve parecer um painel real, não mockup
    

---

## `/invite/:id`

Entrada do participante.

Fluxo:

- buscar reunião via RPC `get_public_meeting`
    
- se a reunião não existir → estado de erro amigável
    
- se estiver `closed` e existir horário final → mostrar estado de reunião encerrada com resultado
    
- se estiver `open` → mostrar entrada normal
    

Elementos:

- card com título da reunião
    
- descrição curta
    
- duração
    
- faixa de datas
    
- instrução curta e pragmática
    
- input “Seu nome”
    

Botão:

- Ver horários
    

Ação:

- chama `create_participant_for_meeting`
    
- salva `participant_id` e `edit_token` em `localStorage`
    
- avança para `/invite/:id/availability`
    

---

## `/invite/:id/availability`

Tela mais importante do projeto.

### Requisitos críticos de UX

- mobile-first de verdade
    
- sem quebrar em smartphones
    
- sem exigir zoom
    
- sem depender de tabela larga horizontal
    

### Como desenhar o grid

No mobile:

- prefira **dias em blocos/abas/acordeões**
    
- dentro de cada dia, exiba slots grandes e clicáveis
    
- permita marcar/desmarcar com toque
    
- feedback visual claro de selecionado / não selecionado
    

No desktop/tablet:

- pode usar grade mais ampla, desde que continue clara
    

### Elementos

- título curto
    
- instrução: “Toque nos horários que você tem livres.”
    
- visual dos dias
    
- visual dos slots
    
- botão sticky na base
    

Botões:

- Voltar
    
- Salvar Disponibilidade
    

Ação:

- monta array de slots selecionados
    
- chama `replace_participant_availabilities(participant_id, edit_token, slots_jsonb)`
    
- redireciona para `/invite/:id/success`
    

---

## `/invite/:id/success`

Elementos:

- ícone de check
    
- texto principal: “Pronto! Seus horários foram enviados.”
    
- texto secundário curto
    
- botão para adicionar ao calendário **somente se a reunião já estiver fechada**
    
- botão secundário:
    
    - `Crie sua própria reunião grátis`
        

Se a reunião ainda estiver `open`, mostre apenas a confirmação do envio.  
Se estiver `closed`, mostre também o horário final definido.

---

# 11) MICROCOPY

Use linguagem:

- simples
    
- direta
    
- humana
    
- sem jargão técnico
    
- focada em ação
    

Exemplos bons:

- “Seu nome”
    
- “Ver horários”
    
- “Salvar disponibilidade”
    
- “Pronto! Seus horários foram enviados.”
    
- “Confirmar este horário”
    
- “Crie sua própria reunião grátis”
    

Evite textos longos e complexos.

---

# 12) DESIGN SYSTEM

Quero interface:

- limpa
    
- moderna
    
- confiável
    
- com bom uso de espaço em branco
    
- com hierarquia visual forte
    
- com microinterações leves
    
- com estados claros de hover, focus, loading e disabled
    

### Requisitos de usabilidade

- área clicável grande
    
- contraste adequado
    
- loading states reais
    
- empty states reais
    
- error states reais
    
- success states reais
    

### Requisito obrigatório da jornada do participante

- CTA principal sticky no mobile
    
- elementos táteis grandes
    
- nada de rolagem horizontal para usar a tela
    

---

# 13) EDGE CASES OBRIGATÓRIOS

Implemente corretamente:

- reunião inexistente
    
- reunião fechada
    
- participante tentando salvar sem selecionar slot
    
- participante tentando usar link já encerrado
    
- erro de rede
    
- organizador sem reuniões ainda
    
- organizador acessando reunião que não é dele
    
- participante retornando ao fluxo no mesmo navegador
    
- validação de nome vazio
    
- `end_time` sempre maior que `start_time`
    

---

# 14) IMPLEMENTAÇÃO EM ORDEM

Siga esta ordem exata:

## Etapa 1 — Banco e Auth

- configurar Supabase
    
- criar tabelas
    
- criar índices
    
- criar trigger do profile
    
- criar RLS
    
- criar RPCs públicas
    

## Etapa 2 — Base do Frontend

- configurar React + Vite + TypeScript
    
- layout base
    
- navegação
    
- cliente Supabase
    
- estados globais mínimos
    

## Etapa 3 — Área do Organizador

- auth
    
- dashboard
    
- criação de reunião
    
- painel da reunião
    

## Etapa 4 — Fluxo do Participante

- entrada por link
    
- nome
    
- grid
    
- salvar disponibilidade
    
- success screen
    

## Etapa 5 — Engine de Compatibilidade

- gerar slots
    
- calcular match
    
- ranquear sugestões
    
- confirmar horário final
    

## Etapa 6 — Polimento

- loading
    
- erro
    
- empty states
    
- responsividade
    
- `.ics`
    

---

# 15) FORMATO DE ENTREGA

Quero que você:

1. implemente o projeto real
    
2. conecte frontend e backend
    
3. gere o SQL corretamente
    
4. respeite o schema acima
    
5. respeite os guardrails
    
6. não pare em análise
    
7. vá até uma versão funcional coerente
    

Antes de alterar qualquer coisa, pense passo a passo **internamente**.  
Depois disso, **execute**.

Se houver qualquer ambiguidade, resolva assim:

- preserve o MVP
    
- preserve a simplicidade do participante
    
- preserve a segurança do organizador
    
- preserve a clareza do banco
    
- preserve a estabilidade do projeto
    

Comece agora pelo banco + auth + schema real e depois avance para as telas e fluxos conectados.