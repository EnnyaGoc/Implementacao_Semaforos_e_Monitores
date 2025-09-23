# Implementacao_Semaforos_e_Monitores

Você deve implementar duas soluções do problema Produtor-Consumidor visto em sala de aula. Uma implementação deve usar semáforos. Para testar esta implementação, crie várias threads em tempos aleatórios e verifique o comportamento da implementação respondendo às perguntas do slide da aula. Crie um relatório contendo as respostas e prints para essas perguntas. A outra implementação deve ser feita com monitores. Nesta, basta apresentar um vídeo curto mostrando a execução.


PERGUNTAS:

Por que precisamos do mutex?
    Porque o buffer é um recurso compartilhado. Sem ele, duas threads (produtor e consumidor, ou dois produtores) poderiam acessar/modificar o buffer ao mesmo tempo, causando condição de corrida (race condition).

Onde estão as regiões críticas?
    No acesso ao buffer:
    buffer.append(item) (inserção do produtor).
    item = buffer.pop(0) (remoção do consumidor).

    Essas operações precisam estar dentro do lock mutex.acquire() … mutex.release().


Podemos ter mais de N threads bloqueadas em wait(empty) ?
    Sim, pois quando o buffer está cheio, qualquer produtor que tentar inserir ficará bloqueado em empty.acquire().
    Então, se tivermos 10 produtores e N=5, pode acontecer de vários ficarem esperando até que consumidores liberem espaço.


Quanto vale empty + full (valor dos contadores)?
    Sempre vale N, que é o tamanho do buffer.

    Empty conta quantos espaços estão livres e full conta quantos espaços estão ocupados.

    Exemplo com N=5:
    Buffer vazio → empty=5, full=0.
    Buffer cheio → empty=0, full=5.
    Buffer com 3 itens → empty=2, full=3.
    A soma é sempre o tamanho do buffer.

Podemos trocar a ordem das chamadas de wait dos semáforos mutex e empty/full ?
    Não podemos trocar a ordem das chamadas de wait porque, no Produtor–Consumidor, primeiro precisamos verificar se há espaço ou item disponível (wait(empty) ou wait(full)) e só depois entrar na seção crítica com wait(mutex); se invertermos, uma thread pode segurar o mutex e ao mesmo tempo ficar bloqueada esperando espaço ou item, enquanto a outra também tenta pegar o mutex para liberar essa condição, o que gera um deadlock onde nenhum dos dois consegue prosseguir.
    A inversão da ordem só dá problema quando o buffer está totalmente cheio ou totalmente vazio, justamente os momentos em que precisamos que quem pode resolver a situação (consumidor no caso do cheio, produtor no caso do vazio) consiga agir livremente.