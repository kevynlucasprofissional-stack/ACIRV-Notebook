---
id: metrica-base-instagram-agosto-2026
titulo: Base-Instagram-Agosto-2026
aliases:
- Agosto 2026 no Instagram
tipo: metrica
subtipo: base_derivada
status: revisado
profundidade: avancada
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-10-02'
ultima_revisao: '2026-10-02'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
- interpretacao_operacional
tags:
- dominio/metricas
- dominio/canais
fontes_documentais:
- '85-Bases-e-Consultas/Instagram-Publicacoes-2026-08.csv'
- 'Hermes/instagram-insights/captura/agosto-2026-faltantes/'
- 'Hermes/instagram-insights/auditorias/AUDITORIA-2026-08.md'
notas_relacionadas:
- '[[Instagram]]'
- '[[Base-Instagram-Setembro-2026]]'
- '[[Metricas-Consolidadas-por-Fonte]]'
- '[[Qualidade-dos-Dados-de-Marketing]]'
- '[[LEIA-ME-Instagram-Insights]]'
confidencialidade: interno
---

# Base-Instagram-Agosto-2026

Base canônica das publicações de **agosto/2026** do `@acirvoficial`: **62 linhas**, uma por publicação que passou pelo feed no mês. Fecha o mês que até 02/10/2026 estava incompleto — o export da Meta cobria 48 e faltavam as 14 que foram capturadas **post a post no painel profissional**.

## Números do mês

| | |
|---|---|
| Publicações no feed | **62** |
| Da conta (`vinculo=proprio`) | 38 |
| De parceiros (`vinculo=colaboracao`) | 24 |
| Imagem (p) / carrossel / reel | 39 / 14 / 9 |
| Visualizações | **2.154.226** |
| Interações | 6.034 |
| Curtidas | 3.469 |
| Comentários | 882 |
| Compartilhamentos | 1.462 |
| Salvamentos | 80 |
| Dias com publicação | 18 (04/08 a 30/08) |
| Publicações promovidas | 11 |

Cinco maiores por visualizações: `DbtOoFrjpJv` (06/08, 556.138), `Db83W6xKhbg` (12/08, 309.185), `DcUEyDAgrbq` (21/08, 265.656), `DcbJmepx1nq` (24/08, 233.550), `DcbECTUAleR` (24/08, 184.536).

## O que este mês ensinou (correções registradas)

- **As 14 que faltavam** entraram capturadas uma a uma do painel do post (`/insights/media/<media_id>/`): oito da conta (lotes de 24 e 28/08) e seis de colaboração (`raphael_valongo` ×5, `aplausoaudiovisual` ×1). Os painéis de post promovido **não** trazem "Visualizadores" e mostram "Contas Meta alcançadas" no lugar — isso está em `metricas_ausentes` e em `notas`, nunca virou zero.
- **Cinco datas publicadas erradas** foram corrigidas pelo shortcode: quatro publicações de **31/07** estavam rotuladas como agosto (saíram da base e viraram `Hermes/instagram-insights/auditorias/julho-2026-31-do-export-master.csv`) e uma dizia **26/08** quando o shortcode diz **13/08** (`Db-7_-OOxRu`).
- **O portão passou a conferir o dia**, não só o mês: era por isso que a data errada de `Db-7_-OOxRu` passava (mesmo mês).
- O arquivo antigo `Instagram-Publicacoes-2026-08-09.csv` fica como **registro** (o split separou agosto e setembro); a base canônica de agosto é este arquivo.

## Como conferir

```
python Hermes/instagram-insights/ferramentas/publicacoes_feed.py auditar --periodo 2026-08
python Hermes/instagram-insights/ferramentas/publicacoes_feed.py autoteste
python Hermes/instagram-insights/ferramentas/test_publicacoes_feed.py
```

O portão responde **COMPLETO** para 2026-08 (62) e para 2026-09 (116). `base_08_09`, `brutos_ago` e `export_ago` aparecem como **subconjuntos** (cobrem 48 de 62) e as datas erradas deles saem como aviso, não como reprovação.

## Procedência

- `85-Bases-e-Consultas/Instagram-Publicacoes-2026-08.csv` (sha256 `e10e5d6e8929a4c979ea86bd61e84c69eb90391c14cc6595d1fccb2e78e74981`) + `.xlsx` espelhado.
- **Correção de 02/10/2026:** a coluna `media_id` saiu **em branco em 48 das 62 linhas** na primeira montagem (só as 14 capturadas no painel tinham o valor). O portão não pegava — ele confere mês, dia, rótulo e cobertura, não completude de coluna. Preenchida a partir do próprio `shortcode` (`sc2mid`), com `mid2sc(sc2mid(sc)) == sc` conferido nas 62; `test_29` passa a travar isso. Referência cruzada por `media_id` (como a base de legendas) quebrava silenciosamente para agosto.
- 48 linhas do export MASTER de agosto, com data e hora conferidas pelo shortcode; 14 linhas capturadas em 02/10/2026 (`captura/agosto-2026-faltantes/insights_<media_id>.txt`, `source_path` + `source_blob_sha` por linha).
- Nenhuma credencial foi preservada nos arquivos de captura.

## Legenda

`85-Bases-e-Consultas/Instagram-Legendas-2026-08.csv` (62 linhas × 16 colunas) — a legenda de cada publicação, capturada em 02/10/2026 pela rota `GET /api/v1/media/<media_id>/info/`. 61 linhas com texto (15 a 982 chars, média 412, 20 com hashtag, 1 com link); `DcCPbyLGzGd` não tem legenda por natureza.

Conferência contra as 47 legendas que já existiam nos brutos do painel (`captura/agosto-2026/*.json`), normalizando espaço: **44 idênticas, 3 divergentes**. As três estão em `Hermes/instagram-insights/auditorias/CONFERENCIA-API-LEGENDA-2026-08.md`, e a que importa é `Dcl1hMpDirN`: o painel perdeu a palavra `por` no meio da frase — o painel monta a legenda juntando vários nós de texto do DOM e a junção engole pedaços. **Por isso a legenda vem da API, que devolve o texto como campo único, e não do painel.**

Também cobre o que estava faltando: em agosto 15 das 62 publicações não tinham legenda em lugar nenhum (as capturadas pelo painel gravaram outro formato). Agora são 62/62 na base, e o portão reprova agosto se alguma faltar.
