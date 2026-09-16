---
Modificado:
  - quinta-feira 106 16/04/2026
  - segunda-feira 103 13/04/2026
  - sexta-feira 93 03/04/2026
Criado: sexta-feira 93 03/04/2026
---
1º - Sincronizações automáticas ainda dão erro ao clicar no botão de cancelar sync. Provavelmente a questão da Sync com o sheets também esteja quebrada.
![[{1D184211-8C02-43D4-AC1C-33B1F52409C1}.png]]

2º - O botão que leva para o whatsapp do cliente está sendo bloqueado, tem que ver o motivo e resolver isso. E também o botão "Contatar via WhatsApp" está muito perto do texto "Você já demonstrou interesse", tem que ter um espaço entre ele e o botão ou arrumar outro lugar para o texto. 
![[{56C7E035-30A3-47BA-850C-1768FA89F8A7}.png]]
![[{801526E5-4100-4830-A485-E895D55AA1B4}.png]]

3º - Aqui na tela /perfil o bloco "termos de uso" está pendente de aceite sendo que no ato do login eu cliquei em aceitar os termos de uso, agora que estou pensando não sei se tenho 100% de certeza disso mas minha memória pode estar me enganando. O que sei é que caso eu não tenha aceitado devemos mudar esse fluxo para que a pessoa só possa fazer o cadastro se aceitar os termos de uso, isso deve ser obrigatório.
![[{EACE3411-0DD8-47DD-A97D-F42457F8908A}.png]]

4º - Devemos implementar uma forma de na tela /perfil o associado, ou seja, o usuário conseguir personalizar todos os campos que aparecem na tela /associado/:id
![[{BF1D38E7-5DDB-4B24-9F41-4177CFF2E48E}.png]]
![[{D464A1C9-4A51-4D45-8365-118D782E215C}.png]]



# Ajustes 05

Na aba de perfil depois do primeiro acesso tem que ter a opção de mudar o email de contato/login

Todas as contas aparentemente estão tendo acesso ao painel de admin, e o sync não está procurando linhas novas, eu adicionei uma nova linha como se eu tivesse colocando um novo associado na base de dados, eu fiz isso colocando uma nova linha no google sheets, mas quando cliquei no botão de sync o site apenas olhou novamente as linhas que já existiam e não olhou as linhas novas e por isso não colocou na base de dados interna do site os novos associados que adicionei e estes ficaram sem conseguir logar no site.