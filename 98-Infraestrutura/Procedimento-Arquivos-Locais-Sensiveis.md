---
id: infraestrutura-procedimento-arquivos-locais-sensiveis
titulo: Procedimento-Arquivos-Locais-Sensiveis
tipo: infraestrutura
status: ativo
versao_schema: '1.0'
versao_conteudo: '1.0'
idioma: pt-BR
data_criacao: '2026-09-17'
ultima_revisao: '2026-09-17'
grau_confianca: alto
camadas_evidencia:
- fato_documentado
tags:
- seguranca
- git
- credenciais
confidencialidade: interno
subtipo: procedimento
---

# Procedimento-Arquivos-Locais-Sensiveis

> [!warning] Regra
> Arquivos com credenciais reais não devem ser armazenados no GitHub. Quando precisarem continuar existindo no computador local, devem ser ignorados pelo Git e retirados apenas do **índice**, nunca apagados do disco durante essa operação.

## Arquivos atuais

- `000-Arquivos-originais/Contas e Senhas.md`
- `000-Arquivos-originais/Minha Chave API Antropic.md`

Esses caminhos estão listados no `.gitignore` do repositório.

## Sequência segura no computador local

A operação deve ser executada dentro do clone local do `ACIRV-Notebook`:

```bash
git pull

git rm --cached -- "000-Arquivos-originais/Contas e Senhas.md"
git rm --cached -- "000-Arquivos-originais/Minha Chave API Antropic.md"
```

`git rm --cached` remove somente o rastreamento pelo Git. Ele **não deve apagar o arquivo físico**.

Antes de qualquer commit ou remoção remota, confirmar explicitamente que os dois arquivos continuam existindo no filesystem local. Em PowerShell:

```powershell
Test-Path "000-Arquivos-originais/Contas e Senhas.md"
Test-Path "000-Arquivos-originais/Minha Chave API Antropic.md"
```

Os dois comandos devem retornar `True`.

Também verificar que os arquivos passaram a ser ignorados:

```bash
git check-ignore -v -- "000-Arquivos-originais/Contas e Senhas.md"
git check-ignore -v -- "000-Arquivos-originais/Minha Chave API Antropic.md"
```

E que aparecem como remoções apenas no índice:

```bash
git status --short
```

Somente depois dessas verificações é seguro confirmar a remoção da versão rastreada no GitHub.

## Limitação importante

O `.gitignore` não protege retroativamente arquivos já versionados. Por isso, adicionar os caminhos ao `.gitignore` é apenas a primeira etapa; `git rm --cached` no clone local é indispensável para preservar os arquivos fisicamente e deixar de sincronizá-los.

## Histórico e rotação

Remover os arquivos da branch atual não remove o conteúdo de commits antigos. Toda credencial real que tenha sido versionada deve ser considerada potencialmente exposta e deve ser rotacionada/revogada. Caso seja necessário eliminar os valores também do histórico Git, isso deve ser tratado separadamente após a rotação.
