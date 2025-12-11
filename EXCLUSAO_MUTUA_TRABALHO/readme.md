# Exclusão Mútua Centralizada em Python

Trabalho da disciplina de Sistemas Concorrentes/Distribuídos.  
Objetivo: implementar um coordenador centralizado que controla o acesso de vários processos a um arquivo compartilhado, garantindo exclusão mútua.

## Arquivos principais

- `coordenador.py`: servidor central. Mantém a fila de pedidos, envia GRANT e registra tudo em `coordenador.log`.
- `processo.py`: processo cliente. Conecta no coordenador, pede acesso, escreve em `resultado.txt` e libera a região crítica.
- `mensagens.py`: funções para montar e interpretar mensagens fixas de 20 bytes (REQUEST, GRANT, RELEASE).
- `executar_processos.py`: script para iniciar vários processos de teste.
- `valida_resultado.py`: script que confere se o `resultado.txt` está correto (número de linhas, ordem de timestamps e quantidade de acessos por processo).

Arquivos gerados durante a execução:

- `coordenador.log`: log de mensagens recebidas/enviadas pelo coordenador.
- `resultado.txt`: linhas com o processo que entrou na região crítica e o horário.

## Como executar

Em um terminal, iniciar o coordenador:

```bash
python coordenador.py
```

Em outro terminal, iniciar os processos (exemplo com 5 processos, 3 repetições, 1 segundo na região crítica):

```bash
python executar_processos.py --n 5 --r 3 --k 1
```

Depois da execução, validar o arquivo de saída:

```bash
python valida_resultado.py --n 5 --r 3 --arquivo resultado.txt
```
