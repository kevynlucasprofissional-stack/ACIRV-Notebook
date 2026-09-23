---
id: estrategia-design-system-acirv
titulo: Design-System-ACIRV
aliases:
- ACIRV Design System
- Sistema de Design ACIRV
tipo: estrategia
status: ativo
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-23'
ultima_revisao: '2026-09-23'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- marca
- design-system
- identidade-visual
- acessibilidade
- social-media
fontes_documentais:
- '000-Arquivos-originais/DESIGN SYSTEM.md'
- '[[ACIRV-MOOD-v1]]'
- 'Briefing visual Kevyn → Samara, 2026-09-23, fornecido por capturas de tela'
notas_relacionadas:
- '[[ACIRV-MOOD-v1]]'
- '[[Arquitetura-de-Marca-e-Nomenclatura]]'
- '[[Manual-Operacional-de-Tom-de-Voz]]'
confidencialidade: interno
subtipo: sistema_de_design
---

# Design-System-ACIRV

> [!summary] Síntese
> Sistema canônico de princípios, tokens e regras visuais da ACIRV. Parte do documento original `000-Arquivos-originais/DESIGN SYSTEM.md`, preservado como fonte imutável, e incorpora a direção visual atualizada em 23/09/2026. O sistema deve produzir comunicação institucional, humana, moderna, legível e reconhecível, sem engessar a variedade criativa.

## 1. Conceito de marca

Tema central: **Conectar para Crescer**.

A linguagem visual deve equilibrar:
- autoridade institucional;
- proximidade humana;
- conexão empresarial;
- movimento;
- crescimento local;
- clareza;
- energia contemporânea.

Princípios:
- institucional, sem burocracia;
- moderno, sem estética genérica de startup;
- vibrante, sem caos;
- humano, sem perder autoridade;
- local, sem limitar ambição;
- criativo, sem sacrificar legibilidade.

## 2. Relação entre Design System e ACIRV-MOOD

O [[ACIRV-MOOD-v1]] define a **direção visual aplicada** e o repertório criativo.

Este documento define o **sistema estável**:
- cores;
- tipografia;
- contraste;
- fundos;
- composição;
- fotografia;
- acessibilidade;
- componentes;
- critérios de aprovação.

Regra de precedência:
1. fatos e tokens oficiais documentados;
2. decisões canônicas mais recentes;
3. repertório do moodboard;
4. variações de campanha.

## 3. Tokens cromáticos de referência

Tokens herdados da fonte primária:

| Papel | Cor |
|---|---|
| Azul institucional / primary | `#0E1EB2` |
| Azul-claro / communication | `#039DE3` |
| Laranja / connection | `#FF7C31` |
| Verde / growth | `#27E300` |
| Amarelo / highlight | `#EAFF00` |
| Branco / surface | `#FFFFFF` |
| Branco suave / surface-soft | `#F6F8FC` |
| Texto primário | `#101828` |
| Texto secundário | `#475467` |
| Borda | `#D0D5DD` |

Valores percebidos em moodboards e campanhas podem variar visualmente, mas não substituem os tokens oficiais sem decisão explícita.

## 4. Papéis das cores

- **Azul:** estrutura, autoridade, confiança, identidade.
- **Azul-claro/ciano:** comunicação, digital, informação.
- **Laranja:** conexão, ação, eventos, contraste.
- **Verde:** crescimento, progresso, benefícios.
- **Amarelo:** destaque, conquista, atenção.
- **Roxo:** cor auxiliar permitida em transições/degradês, não token estrutural primário.

O azul deve continuar sendo a âncora geral do sistema, mesmo quando outra cor domina uma peça de campanha.

## 5. Sistema de backgrounds

A decisão de 23/09/2026 substitui a orientação antiga que desencorajava gradientes multicoloridos em termos gerais.

Quatro famílias passam a ser oficiais:

### A. Fundo sólido
Um único tom da paleta ACIRV.

Uso: peças diretas, gráficas, chamadas curtas, outdoors, campanhas com alta saturação.

### B. Degradê monocromático
Variações claras e escuras de uma mesma cor.

Uso: profundidade, sobriedade, peças institucionais e situações em que adicionar outra cor criaria ruído.

### C. Degradê fluido clássico
Principalmente azul + verde, com transição orgânica.

Uso: conexão, crescimento, institucional contemporâneo, carrosséis, campanhas de rede.

### D. Degradê linear experimental
Azul combinado com outras cores da paleta, incluindo laranja, ciano, verde, amarelo ou roxo auxiliar.

Uso: campanhas, capas, transições, peças de alto impacto.

Regras para D:
- não usar todas as cores ao mesmo tempo;
- manter um eixo cromático dominante;
- garantir área de contraste para texto;
- não sacrificar reconhecimento da marca;
- variar direção e incidência para evitar repetição mecânica.

## 6. Combinações complementares

A combinação **azul + laranja** está validada como repertório de contraste forte.

Ela funciona porque:
- cria separação visual imediata;
- ajuda a destacar áreas de ação;
- traz energia sem abandonar o azul;
- pode funcionar bem em gradientes quando a transição é controlada.

Não usar complementaridade como justificativa automática para qualquer combinação. A prioridade continua sendo legibilidade e coerência.

## 7. Tipografia

Fonte principal: **Campuni**.

Fallback:
1. Montserrat;
2. Arial;
3. sans-serif.

Evitar serifas decorativas, manuscritas e fontes futuristas que descaracterizem a marca.

### Hierarquia de referência

Da fonte original:
- `display-lg`: 3.5rem / 700 / 1.05
- `h1`: 3rem / 700 / 1.1
- `h2`: 2.25rem / 700 / 1.15
- `h3`: 1.5rem / 700 / 1.25
- `body-lg`: 1.125rem / 400 / 1.6
- `body-md`: 1rem / 400 / 1.6
- `body-sm`: 0.875rem / 400 / 1.5
- `label-lg`: 1rem / 700 / 1.2
- `label-md`: 0.875rem / 700 / 1.2
- `eyebrow`: 0.75rem / 700 / 1.2
- `metric-xl`: 3rem / 700 / 1

Esses tokens são referência digital. Em social media, a escala final deve ser adaptada ao formato e à leitura no celular.

## 8. Nova regra de tamanho mínimo perceptivo

A atualização de 23/09/2026 reforça:

> Contraste adequado não compensa fonte pequena demais.

Aplicação:
- aumentar títulos, subtítulos e corpo quando a leitura em feed estiver difícil;
- não comprimir texto para “caber”;
- reduzir copy antes de reduzir fonte;
- preservar informações críticas em tamanho confortável;
- tratar rodapés, data, local e CTA como conteúdo, não como decoração.

### QA obrigatório
A peça precisa ser testada em escala realista de celular. Se o usuário precisa ampliar a tela para ler informação necessária, a tipografia falhou.

## 9. Contraste e acessibilidade

Meta mínima:
- **4.5:1** para texto normal;
- **3:1** para texto grande e elementos gráficos essenciais;
- foco visível em interfaces;
- alvos de toque com pelo menos 44px quando aplicável.

Combinações seguras:
- branco sobre azul institucional;
- texto escuro sobre verde, amarelo, laranja e azul-claro.

Evitar:
- branco em texto normal sobre amarelo, verde, laranja ou azul-claro;
- texto pequeno sobre fotografia detalhada;
- depender apenas de cor para comunicar estado;
- contraste marginal compensado por sombra ou glow.

## 10. Regra de texto sobre fotografia

Quando o fundo for realista e tiver muitos detalhes, aplicar uma ou mais destas soluções:

1. caixa de texto sólida ou semitransparente;
2. faixa/bloco cromático;
3. overlay forte;
4. gradiente localizado;
5. desfoque seletivo;
6. reposicionamento para área negativa;
7. recorte da fotografia.

A referência positiva é manter a fotografia humana, mas garantir uma **superfície de leitura deliberada**.

Não aceitar texto corrido pequeno diretamente sobre área visualmente complexa.

## 11. Fotografia

Prioridade:
1. pessoas reais da ACIRV;
2. associados e empresários;
3. equipe e parceiros;
4. eventos e encontros reais;
5. comércio e cenas locais;
6. objetos/serviços quando tecnicamente necessário.

Tratamentos aceitos:
- overlay azul;
- duotone;
- recorte;
- colagem;
- fundo saturado;
- caixa de texto;
- gradiente sobre imagem.

Evitar banco de imagem genérico quando houver registro real disponível.

## 12. Layout e composição

Sistema espacial:
- múltiplos de 8px;
- 4px apenas para microajustes.

Web/interface:
- desktop: 12 colunas;
- tablet: 8;
- mobile: 4;
- margens mobile mínimas: 16px.

Princípios:
- hierarquia clara;
- respiro;
- composição escaneável;
- uma ação principal por seção;
- assimetria controlada;
- agrupamento lógico;
- densidade moderada;
- alinhamentos consistentes.

Social media:
- um gancho dominante;
- uma ideia visual central;
- CTA/assinatura secundária;
- evitar excesso de blocos;
- último slide de carrossel com ação inequívoca.

## 13. Shapes

- cantos moderadamente arredondados: 8–16px;
- 24px para painéis grandes;
- pills apenas em tags, filtros, selos e badges;
- linhas fluidas e conexões;
- nós e intersecções;
- formas ascendentes com parcimônia;
- elementos devem reforçar rede, movimento ou crescimento.

Evitar blobs e formas aleatórias sem função semântica.

## 14. Componentes digitais

### Botão primário
- fundo azul institucional;
- texto branco;
- ação central.

### Botão secundário
- fundo verde;
- texto escuro;
- benefícios/progresso.

### Botão acento
- fundo laranja;
- texto escuro;
- inscrições/eventos/contato.

### Cards
- claros: leitura e conteúdo recorrente;
- azuis: institucionalidade;
- verdes: métricas/evolução;
- laranja/amarelo: destaque pontual.

### Badges
- amarelo: conquista;
- laranja: evento/temporal;
- verde: benefício/confirmado.

## 15. Tokens de forma e espaçamento

### Border radius
- none: 0px
- xs: 4px
- sm: 8px
- md: 12px
- lg: 16px
- xl: 24px
- pill: 999px

### Spacing
- 0: 0px
- 1: 4px
- 2: 8px
- 3: 12px
- 4: 16px
- 5: 24px
- 6: 32px
- 7: 48px
- 8: 64px
- 9: 96px

## 16. Profundidade e efeitos

Preferir:
- contraste de superfícies;
- bordas sutis;
- overlays;
- sombras suaves;
- profundidade por cor.

Evitar:
- glassmorphism intenso;
- neon excessivo;
- reflexos metálicos;
- sombras pesadas;
- 3D gratuito;
- efeitos que prejudiquem a leitura.

## 17. Movimento

Em interfaces:
- transições geralmente entre 180ms e 240ms;
- entrada por opacidade;
- pequeno deslocamento;
- expansão controlada;
- linhas de conexão progressivas.

Respeitar redução de movimento.

Evitar parallax intenso, rotação decorativa e animação contínua.

## 18. Linguagem de conteúdo

A voz visual e textual deve combinar:
- clareza;
- proximidade;
- credibilidade;
- utilidade;
- orgulho da comunidade empresarial;
- pessoas e resultados reais.

A arte não deve carregar toda a profundidade do conteúdo. A legenda ou página completa a narrativa.

## 19. Do

- usar azul como âncora;
- mostrar pessoas reais;
- criar hierarquia forte;
- variar backgrounds entre A–D;
- usar foto com proteção de texto quando necessário;
- aumentar fontes quando a leitura pedir;
- usar cores com significado;
- preservar respiro;
- manter coerência entre canais;
- testar a peça em escala real de uso.

## 20. Don't

- não usar microtexto para informação importante;
- não colocar texto pequeno sobre fundo detalhado;
- não repetir sempre o mesmo degradê;
- não usar todas as cores com a mesma intensidade;
- não criar estética genérica de startup;
- não depender de efeito para corrigir contraste;
- não lotar a arte de copy;
- não distorcer o logo;
- não usar fotografia genérica quando houver material real;
- não sacrificar legibilidade em nome de estética.

## 21. Checklist final

- [ ] A peça é reconhecível como ACIRV?
- [ ] A mensagem principal é lida em segundos?
- [ ] Título, subtítulo e detalhes essenciais são legíveis no celular?
- [ ] O fundo pertence a uma família visual clara?
- [ ] A fotografia, se usada, não compete com o texto?
- [ ] As cores têm papel definido?
- [ ] O azul permanece como referência identitária?
- [ ] O contraste atende o conteúdo?
- [ ] O layout tem respiro?
- [ ] O logo está preservado?
- [ ] Há variação em relação às peças recentes?
- [ ] A peça evita microtexto e excesso de informação?

## 22. Histórico de decisão

### 2026-09-23 — revisão de legibilidade e backgrounds

Briefing Kevyn → Samara consolidado na camada canônica:

- aumentar fontes de títulos, subtítulos e texto corrido;
- reconhecer que contraste bom não resolve fonte pequena;
- usar caixa/faixa/overlay em fundos fotográficos detalhados;
- oficializar quatro famílias de background;
- aprovar degradês fluidos e experimentais como repertório;
- validar azul + laranja como combinação de alto contraste;
- preservar exemplos positivos recentes sem copiar literalmente suas composições.

Esta decisão atualiza a orientação da fonte primária que recomendava evitar gradientes multicoloridos de forma ampla.

## Fontes e rastreabilidade

Fonte primária imutável:
- `000-Arquivos-originais/DESIGN SYSTEM.md`

Direção visual operacional anterior:
- `Hermes/Planejamento 4º Trimestre de 2026/04-moodboard/MOODBOARD.md`

Atualização humana:
- briefing visual Kevyn → Samara, 23/09/2026, fornecido ao agente por capturas de tela.
