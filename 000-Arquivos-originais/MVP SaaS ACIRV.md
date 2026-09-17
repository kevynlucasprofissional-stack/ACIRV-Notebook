---
Modificado:
  - quarta-feira 91 01/04/2026
  - terça-feira 90 31/03/2026
Criado: terça-feira 90 31/03/2026
---
# Ideia bruta
**Qual problema resolvemos?**  
Falta de visibilidade e conexão entre associados, que faz com que demandas internas não encontrem ofertas dentro do próprio ecossistema da ACIRV, gerando perda de oportunidades de negócio.

**Para quem?**  
Associados da ACIRV (empresários, prestadores de serviço e indústrias) que têm demandas ou oferecem soluções dentro do ecossistema.

**Como resolvem hoje?**  
De forma informal e ineficiente: indicações pontuais, networking manual, grupos de WhatsApp, eventos presenciais ou tentativa individual de busca sem uma base centralizada.

**O que torna nossa solução melhor?**  
Uma plataforma centralizada, simples e intuitiva que conecta demanda e oferta de forma direta, rápida e estruturada, aumentando a visibilidade dos associados, facilitando o matchmaking de negócios e potencializando o networking com foco em geração real de oportunidades dentro da ACIRV.

# Refinamento da ideia

Problema
Associados da ACIRV deixam de fechar negócios entre si por falta de visibilidade e conexão estruturada dentro do próprio ecossistema.

Solução
Marketplace interno que conecta demandas e ofertas entre associados, com busca simples e acesso rápido a contatos e informações dos negócios.

Valor
Gera mais negócios dentro da ACIRV de forma prática, rápida e organizada.

# Proposta de valor

> Para **os associados da ACIRV**, nosso produto é um **marketplace interno de negócios** que **conecta rapidamente demandas a fornecedores dentro do próprio ecossistema**, diferente de **grupos de WhatsApp, indicações informais ou buscas externas**, porque **centraliza informações, facilita a descoberta de parceiros e gera conexões com foco direto em fechamento de negócios**.

# Manifesto do produto

Acreditamos que negócios deveriam acontecer primeiro entre quem já está conectado.

Hoje, muitos associados da ACIRV deixam de fechar negócios entre si por falta de visibilidade, organização e um canal claro de conexão.

Isso importa porque cada oportunidade perdida enfraquece o ecossistema que poderia crescer junto.

Nossa visão é uma ACIRV onde cada demanda encontra rapidamente um fornecedor dentro da própria rede.

Acreditamos na força da conexão, na confiança entre associados e em um ambiente onde crescer é um movimento coletivo.

Por isso, estamos construindo uma plataforma simples, intuitiva e direta, onde oferta e demanda se encontram com facilidade e se transformam em negócios reais.

# Definição do MVP

**Menor produto que resolve o problema:**

### MVP inclui:

- cadastro de associado
    
- perfil da empresa com informações essenciais
    
- busca de associados por segmento, nome da empresa, porte e telefone comercial
    
- página de resultado com dados de contato do associado
    
- publicação simples de demanda
    
- visualização de demandas por outros associados
    
- canal direto de contato entre quem demanda e quem pode ofertar
    

### Fica fora no MVP:

- feed social completo
    
- chat interno robusto
    
- sistema de pagamento
    
- avaliações e reviews
    
- automações complexas de recomendação
    
- gamificação
    
- painel avançado de métricas
    
- app mobile nativo
    

### Resposta direta:

O menor produto que resolve o problema é uma **plataforma interna simples onde o associado consegue buscar outros associados ou publicar uma demanda e encontrar rapidamente quem pode atendê-la dentro da ACIRV**.

# Lista de funcionalidades

Auth
- login
- cadastro
- recuperação de senha

Associados
- cadastro de associado
- edição de perfil
- visualização de perfil da empresa

Perfil da Empresa
- nome da empresa
- segmento
- porte do negócio
- descrição
- telefone comercial
- contato principal

Busca
- buscar por nome do associado
- buscar por nome da empresa
- buscar por segmento
- buscar por porte do negócio
- visualizar resultados da busca

Demandas
- publicar demanda
- listar demandas publicadas
- visualizar detalhes da demanda

Conexão
- acessar contato do associado
- demonstrar interesse em uma demanda
- entrar em contato com quem publicou a demanda

Admin
- aprovar cadastros
- gerenciar associados
- gerenciar demandas
  
# Entidades do Sistema (Data Model)

```text
User
Associate
CompanyProfile
Demand
DemandInterest
Category
GoogleSheetSync
AdminAction
```

### Leitura prática de cada entidade

**User**  
Representa o usuário que acessa o sistema.

**Associate**  
Representa o associado vinculado à ACIRV.

**CompanyProfile**  
Armazena os dados da empresa/negócio do associado que serão usados na busca e exibição.

**Demand**  
Representa uma necessidade publicada por um associado.

**DemandInterest**  
Registra quando outro associado demonstra interesse em atender uma demanda.

**Category**  
Organiza segmento, nicho ou categoria de atuação.

**GoogleSheetSync**  
Controla ou registra a leitura/importação dos dados da lista de associados vinda do Google Sheets.

**AdminAction**  
Registra ações administrativas, como aprovação, edição ou remoção de dados.

### Versão mais enxuta para o MVP

```text
User
Associate
CompanyProfile
Demand
DemandInterest
GoogleSheetSync
```

### Observação estratégica

Como o SaaS deve pesquisar na lista de associados do **Google Sheets**, essa fonte precisa ser considerada já no data model, mesmo que depois o sistema apenas consulte a planilha ou espelhe esses dados em banco.

# Estrutura do Banco (SQL)

## Visão geral das tabelas

```text
auth.users (nativa do Supabase)

profiles
associates
demands
demand_interests
sheet_sync_logs
```

---

## 1. `profiles`

Complementa o `auth.users` do Supabase.

### Campos

```text
id uuid pk
auth_user_id uuid unique references auth.users(id)
full_name text
email text
role text
created_at timestamp
updated_at timestamp
```

### Função

Armazena os dados do usuário que acessa o sistema.

### Observações

- `role` pode ser: `associate`, `admin`
    
- o login fica no `auth.users`
    
- esta tabela guarda os dados públicos/complementares do usuário
    

---

## 2. `associates`

Tabela principal para os associados que serão buscados no marketplace.

### Campos

```text
id uuid pk
sheet_row_id text unique
company_name text
associate_name text
segment text
business_size text
market_niche text
commercial_phone text
contact_phone text
contact_name text
email text
city text
state text
is_active boolean
source text
raw_data jsonb
created_at timestamp
updated_at timestamp
```

### Função

Armazena os dados dos associados que vêm da planilha do Google Sheets.

### Observações

- `sheet_row_id` ajuda a identificar a linha original da planilha
    
- `source` pode ser algo como `google_sheets`
    
- `raw_data` guarda o dado bruto da planilha para evitar perda de informação
    
- essa é a tabela usada pela busca do sistema
    

---

## 3. `demands`

Tabela para publicação de demandas dos associados.

### Campos

```text
id uuid pk
created_by_profile_id uuid references profiles(id)
title text
description text
segment text
status text
visibility text
created_at timestamp
updated_at timestamp
```

### Função

Permite que um associado publique uma necessidade ou oportunidade.

### Observações

- `status` pode ser: `open`, `closed`, `cancelled`
    
- `visibility` pode começar apenas com `associates_only`
    

---

## 4. `demand_interests`

Registra quando alguém demonstra interesse em atender uma demanda.

### Campos

```text
id uuid pk
demand_id uuid references demands(id)
associate_id uuid references associates(id)
profile_id uuid references profiles(id)
message text
status text
created_at timestamp
updated_at timestamp
```

### Função

Liga a demanda publicada ao associado interessado em ofertar.

### Observações

- `status` pode ser: `new`, `contacted`, `negotiating`, `closed`
    

---

## 5. `sheet_sync_logs`

Controla importação ou sincronização da planilha.

### Campos

```text
id uuid pk
source_url text
sync_status text
rows_processed integer
rows_created integer
rows_updated integer
error_message text
started_at timestamp
finished_at timestamp
created_at timestamp
```

### Função

Registrar quando o sistema buscou ou atualizou dados do Google Sheets.

### Observações

- importante para auditoria e manutenção
    
- ajuda a saber se a sincronização funcionou ou falhou
    

---

## Relacionamentos

```text
auth.users 1:1 profiles
profiles 1:N demands
demands 1:N demand_interests
associates 1:N demand_interests
profiles 1:N demand_interests
```

---

## Leitura prática da lógica

## `auth.users` + `profiles`

Controlam autenticação e usuário do sistema.

## `associates`

É a base consultável do marketplace, alimentada pela planilha do Google Sheets.

## `demands`

É onde o associado publica o que precisa.

## `demand_interests`

É onde registramos quem quer atender a demanda.

## `sheet_sync_logs`

É onde controlamos a integração com a planilha.

---

## Estrutura enxuta do MVP

Se quiser manter o MVP no menor tamanho possível, a estrutura pode ficar assim:

```text
auth.users
profiles
associates
demands
demand_interests
sheet_sync_logs
```

---

## Observação estratégica importante

Como a busca será feita com base em um **Google Sheets**, o ideal **não é consultar a planilha diretamente a cada pesquisa do usuário**.  
O melhor para o MVP é:

```text
Google Sheets = fonte de dados
Supabase = espelho consultável para busca rápida
```

Ou seja:

- o sistema lê a planilha
    
- salva ou atualiza os dados em `associates`
    
- a busca acontece no banco do Supabase
    

Isso deixa a experiência:

- mais rápida
    
- mais estável
    
- mais escalável
    
- mais fácil de filtrar
    

---

## Versão ultra resumida

```text
profiles
- usuário do sistema

associates
- base de associados vinda do Google Sheets

demands
- demandas publicadas

demand_interests
- interessados em atender a demanda

sheet_sync_logs
- histórico de sincronização da planilha
```

# Mapa de Navegação

### 1. Camada Pública (Atração e Filtro)
*   **Landing Page** (Proposta de valor clara: "Negócios entre quem você confia")
    *   **Login** (Acesso restrito a associados)
    *   **Cadastro / Solicitação de Acesso** (Fluxo de onboarding)
    *   **Recuperação de Senha**

### 2. Dashboard Principal (O "Hub" de Oportunidades)
*   **Feed de Demandas Recentes** (Visão rápida do que o mercado precisa agora)
*   **Barra de Busca Global** (Atalho para buscar empresas ou segmentos)

### 3. Marketplace de Ofertas (Busca de Associados)
*   **Explorar Associados** (Lista/Grid de empresas vindas do Google Sheets)
    *   **Filtros Avançados** (Segmento, Porte, Niche)
    *   **Perfil Público da Empresa** (Dados detalhados)
        *   **CTA: Contato Direto** (WhatsApp/Telefone comercial)

### 4. Central de Demandas (Onde o negócio nasce)
*   **Mural de Demandas** (Lista de necessidades publicadas por outros)
    *   **Detalhe da Demanda** (O que é preciso, prazo, contexto)
        *   **CTA: Demonstrar Interesse** (Gera notificação/contato)
*   **Publicar Nova Demanda** (Formulário simplificado de 3-4 campos)

### 5. Área do Associado (Gestão e Identidade)
*   **Meu Perfil / Perfil da Empresa** (Edição de dados e visibilidade)
*   **Minhas Demandas** (Gerenciar o que eu publiquei: Editar/Finalizar)
*   **Interesses Recebidos** (Quem quer me atender)

### 6. Painel Administrativo (Controle e Sincronização)
*   **Gestão de Associados** (Aprovação e status)
*   **Moderação de Demandas**
*   **Configurações de Sincronização** (Status do Google Sheets Sync)

---

## 💡 Notas de UX Estratégico para a Implementação:

1.  **Regra dos 3 Cliques:** O usuário deve conseguir: 1. Abrir o app -> 2. Clicar em "Buscar" -> 3. Ver o WhatsApp do fornecedor. Menos etapas = mais negócios fechados.
2.  **Mobile-First Rigoroso:** Empresários da ACIRV estarão em trânsito. O botão de "Entrar em contato" deve ser grande (mínimo 44px) e abrir o WhatsApp nativo diretamente.
3.  **Frequência de Uso:** Como o MVP depende de rede, a tela de **"Publicar Demanda"** deve ser o elemento de maior destaque visual (CTA de cor contrastante) para manter o ecossistema vivo.
4.  **Feedback Imediato:** Ao clicar em "Demonstrar Interesse", use uma microinteração de sucesso. O usuário precisa saber que sua intenção foi registrada.
5.  **Hierarchy de Busca:** Na página de resultados, o **Segmento** e o **Cidade/Bairro** são mais importantes que o nome da empresa para quem está procurando um serviço novo. Dê peso visual a essas tags.
   
# User Flow

### Fluxo 1: O Associado buscando um Fornecedor (Busca Ativa)
*Objetivo: Resolver uma necessidade imediata encontrando uma empresa específica na base.*

**Associado (Comprador)**
```text
Login 
↓
Dashboard (Barra de busca em destaque)
↓
Digitar Segmento ou Nome (ex: "Contabilidade")
↓
Lista de Resultados (Filtro por porte/niche)
↓
Ver Perfil da Empresa
↓
Clicar em "Entrar em Contato via WhatsApp"
↓
Negócio Iniciado (Fora da plataforma)
```

---

### Fluxo 2: O Associado gerando Oportunidade (Publicar Demanda)
*Objetivo: Lançar uma necessidade para que o ecossistema venha até ele.*

**Associado (Demandante)**
```text
Login 
↓
Botão "Publicar Nova Demanda" (+)
↓
Preencher Título, Descrição e Segmento alvo
↓
Confirmar Publicação
↓
Visualizar "Minhas Demandas" (Status: Aberta)
↓
Receber Notificação/Interesse de outros associados
```

---

### Fluxo 3: O Associado captando Negócios (Mural de Demandas)
*Objetivo: Encontrar novas oportunidades de venda dentro da ACIRV.*

**Associado (Prestador/Fornecedor)**
```text
Login 
↓
Navegar pelo "Mural de Demandas"
↓
Filtrar por Segmento de atuação
↓
Selecionar Detalhes da Demanda
↓
Clicar em "Tenho Interesse / Ver Contato"
↓
Sistema registra o interesse (Lead gerado)
↓
Acessar dados de contato do demandante
```

---

### 🛡️ Notas de Consultoria (Rigor de UX):

1.  **O "Pulo do Gato" no Fluxo 1:** No MVP, não force o usuário a preencher um formulário de contato interno. O botão deve disparar o `api.whatsapp.com` direto. O atrito deve ser zero para o primeiro contato.
2.  **Validação de Dados no Fluxo 2:** O formulário de demanda deve ser curto (Lei de Hick). Se tiver mais de 5 campos, a taxa de abandono subirá.
3.  **Transparência no Fluxo 3:** Ao clicar em "Ver Contato", o sistema deve deixar claro para o prestador que o demandante será notificado do interesse dele. Isso cria um senso de responsabilidade e seriedade no networking.
   
# Fluxos críticos
### 1. Onboarding (Validação de Associado)
*O momento em que o usuário prova que pertence ao ecossistema ACIRV.*
1.  **Entrada:** Usuário insere E-mail ou CNPJ.
2.  **Validação:** Sistema consulta a tabela `associates` (espelhada do Google Sheets).
3.  **Match:** Se encontrado, o sistema pré-preenche os dados da empresa.
4.  **Criação de Perfil:** Usuário define senha e complementa "Nicho de Atuação" e "Descrição".
5.  **Sucesso:** Dashboard liberado com mensagem de boas-vindas personalizada.

### 2. Conexão e Matchmaking (Substitui a "Contratação")
*O core business do app: transformar uma necessidade em contato real.*
1.  **Acesso:** Associado visualiza uma Demanda aberta no Mural.
2.  **Interesse:** Clica em "Tenho Interesse em Atender".
3.  **Registro:** O sistema grava a intenção na tabela `demand_interests`.
4.  **Revelação:** O contato (WhatsApp/E-mail) do dono da demanda é liberado.
5.  **Ação:** Usuário é redirecionado para o WhatsApp com uma mensagem template: *"Olá [Nome], vi sua demanda de [Título] no Marketplace ACIRV e posso te ajudar."*

### 3. Fechamento Externo (Substitui o "Pagamento")
*Como o sistema não processa pagamentos no MVP, este fluxo serve para medir conversão.*
1.  **Notificação:** Após 7 dias, o sistema pergunta ao dono da demanda: *"Você fechou negócio com alguém?"*
2.  **Atualização de Status:** Usuário marca a demanda como "Fechada/Resolvida".
3.  **Indicação de Parceiro:** Usuário seleciona qual associado o atendeu (vínculo de dados para métricas futuras).
4.  **Finalização:** Demanda sai do mural público.

### 4. Validação de Utilidade (Substitui a "Avaliação")
*Coleta de feedback simplificada para provar o valor do MVP.*
1.  **Gatilho:** Ao marcar uma demanda como resolvida.
2.  **Input:** Pergunta única: *"Em uma escala de 1 a 5, quão fácil foi encontrar esse parceiro na plataforma?"*
3.  **Comentário (Opcional):** Espaço livre para melhorias.
4.  **Encerramento:** Dados enviados para o Admin para cálculo de NPS do ecossistema.

---

### 🛡️ Prudência de Consultor:
*   **Atenção ao Onboarding:** Como o dado vem de um Google Sheets, a busca por CNPJ/E-mail deve ser tolerante a erros (espaços extras, pontos, traços). 
*   **O "Ponto Cego" do Pagamento:** Já que o pagamento é externo, o fluxo de **"Fechamento Externo"** é sua única forma de provar para a diretoria da ACIRV que o sistema está gerando dinheiro para os associados. Não o ignore.
  
# Sprint de Produto

### Tela: Login / Onboarding
**Elementos**
- Logo ACIRV
- Título: "Marketplace de Negócios"
- Campos: E-mail e Senha
- Link: "Primeiro acesso? Verifique se sua empresa já está na base"

**Botões**
- Entrar
- Recuperar Senha

**Ação**
- Clicar em "Entrar" valida credenciais e direciona para a Home.

---

### Tela: Home (Dashboard de Oportunidades)
**Elementos**
- Barra de Busca Global (Placeholder: "O que sua empresa precisa hoje?")
- Seção "Demandas Recentes" (Cards com Título e Segmento)
- Atalhos de Categorias (Ícones: Indústria, Comércio, Serviços)
- Banner de Proposta de Valor: "Conecte-se com associados"

**Botões**
- Publicar Demanda (Botão flutuante ou destaque na barra superior)
- Ver Todas as Demandas
- Explorar Empresas

**Ação**
- Clicar em "Publicar" abre o formulário de demanda.
- Clicar em um Card de Demanda abre os detalhes.

---

### Tela: Marketplace (Resultados da Busca)
**Elementos**
- Lista de Empresas (Cards com: Nome, Segmento, Tag de Porte)
- Filtros Laterais/Topo: Segmento, Localização, Nicho.
- Contador de Resultados: "Exibindo 42 parceiros encontrados"

**Botões**
- Ver Perfil Completo
- Limpar Filtros

**Ação**
- Clicar no card direciona para o Perfil do Associado.

---

### Tela: Perfil do Associado (Vendedor/Fornecedor)
**Elementos**
- Cabeçalho: Nome da Empresa e Logo (se disponível)
- Badge: "Associado Verificado ACIRV"
- Descrição: "O que fazemos"
- Informações de Contato (Telefone, E-mail, Responsável)
- Lista de Serviços/Produtos

**Botões**
- **Botão de Ação Primário: "Chamar no WhatsApp" (Destaque visual)**
- Voltar para busca

**Ação**
- Clicar no WhatsApp abre o link externo para conversa direta.

---

### Tela: Mural de Demandas
**Elementos**
- Lista de necessidades (Cards com: "Procuro fornecedor de...", Prazo, Descrição curta)
- Tags de Segmento em cada demanda

**Botões**
- Tenho Interesse / Ver Detalhes
- Filtrar por Segmento

**Ação**
- Clicar em "Tenho Interesse" abre o fluxo de conexão (Fluxo Crítico 2).

---

### Tela: Publicar Demanda
**Elementos**
- Campo: Título (O que você precisa?)
- Campo: Descrição (Detalhe sua necessidade)
- Seleção: Qual segmento pode te atender?
- Checkbox: "Permitir que associados vejam meu telefone"

**Botões**
- Publicar Agora
- Cancelar

**Ação**
- Ao publicar, o sistema dispara o log para a tabela `demands` e volta para o Mural.

---

### Tela: Painel Admin (Sincronização)
**Elementos**
- Status da última sincronização com Google Sheets
- Contador de Novos Associados importados
- Lista de Demandas para Moderação

**Botões**
- Sincronizar Agora (Manual)
- Aprovar/Reprovar Cadastro

**Ação**
- Clicar em "Sincronizar" dispara a função de leitura do Sheets para o Supabase.

---

### 🛡️ Checklist de UI para o Desenvolvedor:
- [ ] **Botões:** Mínimo 44px de altura para touch mobile.
- [ ] **WhatsApp:** Use o ícone oficial da marca para gerar confiança imediata.
- [ ] **Vazio:** Se uma busca não trouxer resultados, exiba um botão "Publicar Demanda" para incentivar a proatividade.
- [ ] **Contraste:** Garanta que as tags de segmento (ex: "Indústria") tenham fundo claro e texto escuro para legibilidade.

# Regras do Sistema
*As diretrizes que governam o comportamento do marketplace.*

*   **Fonte da Verdade:** A base de empresas (`associates`) é alimentada exclusivamente via Google Sheets (espelhada no Supabase). Usuários comuns não criam empresas, apenas vinculam seus perfis a elas.
*   **Acesso Restrito:** Apenas associados logados e verificados podem visualizar dados de contato (Telefone/WhatsApp) e detalhes de demandas.
*   **Ciclo da Demanda:** Uma demanda pode estar nos estados: `Aberta`, `Em Atendimento` ou `Finalizada`.
*   **Conexão Direta:** O sistema não intermedia o pagamento; ele facilita o *handshake* (aperto de mão) inicial via WhatsApp.
*   **Unicidade:** Um perfil de usuário (`profile`) deve estar obrigatoriamente vinculado a um e-mail ou CNPJ presente na base de associados para ter permissões completas.

# Permissões
*Quem pode fazer o que no ecossistema.*

**Associado (Usuário Padrão)**
*   Visualizar lista e perfis de outros associados.
*   Publicar, editar e encerrar suas próprias demandas.
*   Demonstrar interesse em demandas de terceiros.
*   Editar seu próprio perfil de usuário (nome, cargo, senha).

**Admin (Gestor ACIRV)**
*   Gatilhar a sincronização manual com Google Sheets.
*   Moderar (editar/excluir) qualquer demanda ou comentário impróprio.
*   Aprovar ou bloquear acesso de novos perfis.
*   Visualizar logs de sincronização e métricas de interesse.

---

# Integrações
*As ferramentas que dão vida ao MVP.*

*   **Supabase:** Banco de dados (PostgreSQL), Autenticação e Storage.
*   **Google Sheets API:** Fonte primária de dados dos associados da ACIRV.
*   **WhatsApp Public API:** Para geração de links diretos de conversa (`wa.me`).
*   **Resend (Opcional):** Para envio de e-mails transacionais (boas-vindas e alertas de nova demanda).
*   **Lovable (Deployment):** Orquestração do front-end e lógica de borda.

---

# Segurança
*Proteção de dados e Row Level Security (RLS).*

*   **Autenticação:** Gerenciada pelo Supabase Auth (E-mail/Senha).
*   **Row Level Security (RLS):**
    *   `profiles`: O usuário só pode ler e editar seu próprio registro (`auth.uid() = id`).
    *   `associates`: Leitura permitida para todos os usuários autenticados; escrita permitida apenas para a `service_role` (sync do Admin).
    *   `demands`: Leitura para todos os autenticados; edição/exclusão apenas para o criador (`profile_id`).
    *   `demand_interests`: Visível apenas para o dono da demanda e para quem demonstrou interesse.
*   **Validação de Entrada:** Proteção contra injeção de scripts (XSS) nos campos de descrição de demanda e perfil da empresa.
*   **Sanitização de Dados:** Filtro automático para remover espaços e formatação especial de CNPJ e telefones vindos da planilha para garantir buscas precisas.

---

### 🛡️ Conselho de Implementação (Foco em Conversão):
Para o Lovable, certifique-se de que a **RLS do Supabase** esteja ativa desde o dia 1. No contexto de uma associação comercial (ACIRV), a **privacidade dos dados de contato** é o que mantém o valor da anuidade. Se os dados vazarem para não-associados, o marketplace perde sua principal vantagem competitiva: a exclusividade.