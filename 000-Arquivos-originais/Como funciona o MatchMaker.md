# V2.3

### Explicação 01
Hoje o match funciona assim, do começo ao fim:

1. O perfil alimenta o motor
No wizard `/participar` a pessoa informa: quem ela é (porte, tipo de negócio, segmento, nicho), o que oferece, o que procura (necessidades, com opção de marcar prioridade) e quem procura (porte/tipo/segmento desejado — em branco = "Qualquer").

2. O cálculo roda no banco, na hora
Ao salvar o perfil, o Postgres executa o matcher v2.4 (`recompute_own_matches`) comparando você com todos os perfis do evento que consentiram com matchmaking. Matches que já viraram conexão são preservados; o resto é recalculado.

3. Um par só existe se houver sinal
- sinal comercial: o que eu procuro × o que o outro oferece (ou o inverso);
- relação complementar aprovada na taxonomia (peso ≥ 40);
- encaixe completo de "quem eu procuro × quem o outro é".

4. Pontuação — cada lado tem seu próprio score
| Sinal | Pontos |
|---|---|
| O outro oferece o que eu procuro | 55 |
| O outro procura o que eu ofereço | 25 |
| Cobre necessidade prioritária | 10 |
| Complementaridade | 5 |
| Perfil atualizado recentemente | 3 |
| Mesma cidade | 2 |
| Relação complementar de taxonomia | até 30 (peso × 0,30) |
| Perfil desejado (encaixe completo) | 20 / 30 / 40 (10 + 10 por critério) |
| Perfil desejado mútuo | +10 |

"Quem eu procuro" só pontua se todos os critérios preenchidos baterem, e nunca elimina ninguém — não é filtro, é bônus.

5. Tipo e rótulo
O tipo do match segue a precedência: comercial (bidirecional / híbrido / direto / inverso) → complementar → `perfil_desejado` (quando o par existe só pelo encaixe de perfil). O score de cada lado gera o rótulo — alta compatibilidade, boa oportunidade ou conexão possível — sempre por perspectiva, então as duas pessoas podem ver rótulos diferentes do mesmo par.

6. Explicação obrigatória
Cada ponto ganho gera um "motivo" em linguagem humana ("ele oferece o serviço de marketing que você procura"), com rastreio de qual necessidade, oferta e relação de taxonomia o produziram — é isso que aparece no card em `/participante`.

7. Do match à conexão
Cada lado marca "Tenho interesse". Com interesse mútuo, cria-se automaticamente uma conexão na fila em tempo real de `/equipe`. A equipe da ACIRV assume, apresenta as duas partes presencialmente e só depois desse registro o contato (WhatsApp/e-mail) é liberado — sempre com auditoria.

Nada é enviado por notificação: a descoberta acontece no painel e o fechamento no contato presencial da equipe.

Perfeito — é exatamente assim que funciona hoje. Qualquer ajuste, me chame.

### Explicação 02

Pergunta: Então por exemplo, se tem cadastrado um comércio de grande porte e eu me cadastro como alguém que está procurando um comércio de grande porte, essa empresa cadastrada vai aparecer nos meus possíveis "matchs"?

Sim — nesse caso ela aparece. Detalhando:

Seu exemplo
Você preenche "procuro": porte = grande, tipo = comércio, segmento = Qualquer.
A empresa cadastrada é: porte = grande, tipo = comércio.
→ 2 critérios especificados, 2 atendidos = encaixe completo. Isso por si só já cria o par, mesmo sem nenhum sinal comercial entre vocês.
→ Pontuação: 10 + (10 × 2) = 30 pontos, com o tipo `perfil_desejado` e o motivo explicando "o porte e o tipo de negócio que você procura".
→ Se ela também estiver procurando alguém com o seu perfil, entram +10 para cada lado (perfil desejado mútuo).

Quando NÃO apareceria só por isso
Se você preencher os três critérios (porte grande + comércio + segmento "Alimentação", por exemplo) e ela for comércio grande mas de outro segmento, o encaixe fica parcial — e encaixe parcial não pontua nem cria o par. Ela só apareceria se houvesse outro sinal: ela oferecer algo que você procura, você oferecer algo que ela procura, ou uma relação complementar da taxonomia.

Duas condições sempre valem
- A empresa precisa ter dado consentimento de matchmaking no evento (perfis sem consentimento ficam fora do cálculo).
- O cálculo roda ao salvar o perfil, então o par aparece imediatamente no seu painel.

Regra prática: quanto mais critérios você especifica, mais alto o bônus (20/30/40), mas mais exigente fica o encaixe. Deixar campos como "Qualquer" amplia o alcance.

### Explicação 03

Como o motor de match funciona hoje (versão 2.4, roda todo no banco):

1. Pontuação por perspectiva. Cada dupla recebe duas notas independentes — a sua nota sobre a outra empresa e a nota dela sobre você. Por isso a mesma dupla pode ser "alta compatibilidade" para um lado e só "conexão possível" para o outro.

2. Pesos somados:

| Sinal | Pontos |
|---|---|
| A outra empresa oferece o que você procura | 55 |
| A outra empresa procura o que você oferece | 25 |
| O encaixe atende uma necessidade marcada como prioritária | 10 |
| Complementaridade (segmentos diferentes, mas com encaixe) | 5 |
| Perfil da outra empresa atualizado nos últimos 7 dias | 3 |
| Mesma cidade | 2 |
| Perfil desejado ("quem eu procuro" × "quem o outro é") | 10 + 10 por critério informado → 20, 30 ou 40 |
| Perfil desejado mútuo (os dois se encaixam no alvo um do outro) | +10 |

No "perfil desejado", só pontua se todos os critérios que você informou baterem (porte, tipo de negócio, segmento). Critério deixado como "Qualquer" é simplesmente ignorado, nunca elimina ninguém. Encaixe parcial vale zero.

3. Quando a dupla é criada. Só existe match se houver pelo menos um sinal real: encaixe comercial (oferta × necessidade) ou encaixe completo de perfil desejado em qualquer direção. Sem sinal, a dupla não é gerada.

4. Tipo do match. Direto (ele oferece o que você precisa), inverso (ele precisa do que você oferece), bidirecional (os dois), híbrido (direto entre segmentos diferentes), complementar, ou perfil desejado — sinal comercial sempre tem precedência sobre o encaixe de perfil na hora de nomear.

5. Classificação exibida (pela sua nota, não pela nota geral): 75+ = Alta compatibilidade · 40–74 = Boa oportunidade · abaixo de 40 = Conexão possível.

6. Justificativas. Cada ponto ganho vira uma frase no card ("Oferece: marketing", "Corresponde ao porte e segmento que você procura"), então a explicação sempre reflete a conta real.

Exemplo prático: alguém que oferece exatamente o serviço que você busca, marcado como prioridade, em outro segmento, mesma cidade e perfil recém-atualizado = 55 + 10 + 5 + 3 + 2 = 75 → Alta compatibilidade.

Perfeito — o motor segue como está, sem alterações.

### Explicação 04 sobre as taxonomias

Como um match nasce
Cada participante é comparado com todos os outros do evento (só quem deu consentimento). Cada dupla recebe duas notas independentes — a sua nota sobre a outra empresa e a nota dela sobre você. Por isso a mesma dupla pode ser "alta compatibilidade" de um lado e só "conexão possível" do outro.

Pesos somados (por perspectiva)
| Sinal | Pontos |
|---|---|
| A outra empresa oferece o que você procura | 55 |
| A outra empresa procura o que você oferece | 25 |
| A necessidade atendida estava marcada como prioridade | 10 |
| Encaixe de "quem eu procuro" (porte/tipo/segmento) | 10 + 10 por critério informado |
| Atividades complementares (taxonomia) | até 30, conforme o peso da relação |
| Cadastro atualizado recentemente | 3 |
| Mesma cidade/região | 2 |

Classificação: 75+ = alta compatibilidade, 40+ = boa oportunidade, abaixo disso = conexão possível.

O papel da taxonomia
1. Casamento direto: oferta e necessidade não são comparadas por texto cru — cada item cadastrado aponta para um item do catálogo do evento, com apoio de sinônimos e similaridade textual. Assim "marketing digital" e "gestão de redes sociais" se encontram.
2. Relações complementares: no painel de taxonomia dá para ligar dois itens do catálogo dizendo "quem precisa de A combina com quem oferece B" (ex.: quem fabrica × quem embala), com peso e justificativa. O motor usa a melhor relação aplicável para cada lado (nunca soma várias). Hoje não há nenhuma relação cadastrada, então esse sinal está valendo zero na prática — é o único ponto do motor ocioso.

Cada ponto ganho vira uma frase explicativa no card, ligada ao item de oferta/necessidade ou à relação de taxonomia que o gerou.