## Prompt para criar prompt para IA
Atualize no repositório o roadmap.md, o jornal de engenharia, o hermes work inteligence e qualquer outro documento necessário com essas descobertas que fizemos aqui.
Agora cria um prompt para eu mandar para a IA que vai realizar essas implementações/ajustes e ela realizar esses pontos de melhoria que identificamos nas análises anexadas. Me vê um prompt para eu mandar e ele resolver tudo isso. Cria um prompt que permita que a IA não precise pensar muito nem ficar lendo nada, que ele saiba de imediato o que ele tem que fazer. Para isso, leia todo o necessário direto no @GitHub

## Juntar tudo no main
Precisamos juntar essas alterações no main e sincronizar o main local com o main remoto (Main na nuvem do github).
Resolve conflitos, faz os commits, pull request, merge, sincroniza e junta tudo no main.

ou

Faça uma consolidação completa do repositório, deixando o `main` como a única fonte canônica, atualizada e sincronizada entre o ambiente local e o Git remoto.

Primeiro, inspecione o estado completo do repositório antes de alterar qualquer coisa: branches locais e remotas, Pull Requests abertos, Draft PRs, commits divergentes, alterações não commitadas, branches que estejam à frente ou atrás do `main`, merges pendentes e quaisquer outras divergências entre versões.

Em seguida:

1. Identifique todas as alterações válidas que ainda não chegaram ao `main`.
    
2. Compare branches e Pull Requests para evitar duplicar trabalho ou sobrescrever implementações mais recentes.
    
3. Resolva todos os conflitos de merge preservando a implementação mais completa, atual e compatível com a arquitetura existente.
    
4. Quando duas branches implementarem soluções diferentes para o mesmo problema, analise o código e consolide a melhor solução em vez de simplesmente escolher uma versão.
    
5. Integre ao `main` tudo o que estiver concluído e fizer sentido manter.
    
6. Resolva também Pull Requests e Draft PRs pendentes, incorporando ao `main` o trabalho aproveitável que ainda não esteja presente nele.
    
7. Verifique se existem commits órfãos, branches não incorporadas ou mudanças importantes que poderiam ser perdidas durante a consolidação.
    
8. Execute os testes, builds, linters ou demais validações existentes no projeto após os merges e corrija problemas introduzidos pela consolidação.
    
9. Só considere uma branch obsoleta ou descartável depois de confirmar que nenhuma alteração exclusiva e relevante dela será perdida.
    
10. Depois da consolidação, atualize o `main` remoto e sincronize novamente o `main` local com o remoto, garantindo que ambos apontem para o mesmo estado final.
    

Ao terminar, o repositório deve estar em um estado limpo e coerente:

- `main` local e `main` remoto sincronizados;
    
- nenhuma implementação válida perdida;
    
- nenhuma divergência relevante ainda presa em outra branch;
    
- conflitos resolvidos;
    
- Pull Requests e Draft PRs tratados;
    
- alterações importantes consolidadas;
    
- working tree limpa;
    
- projeto validado pelos testes disponíveis.
    

Não faça merges cegos, não use `force push` destrutivo e não descarte código apenas para eliminar conflitos. Preserve o histórico sempre que possível e priorize integridade do código e ausência de regressões.

Antes de finalizar, faça uma última auditoria comparando novamente `main`, branches locais, branches remotas e PRs para confirmar que nenhuma mudança relevante ficou para trás.

No final, apresente um resumo objetivo contendo:

- o que foi incorporado ao `main`;
    
- quais conflitos foram encontrados e como foram resolvidos;
    
- quais branches/PRs foram encerrados ou considerados obsoletos;
    
- quais validações foram executadas;
    
- o commit final do `main`;
    
- confirmação de que local e remoto estão sincronizados.

## Para analisar trabalho
Ok, ajustes feitos. Analisa a qualidade do trabalho no main, está disponível no @GitHub