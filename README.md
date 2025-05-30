# Trabalho Prático — Log REDO com PostgreSQL
Alunas: Ana Paula Hartmann (2311100039) e Sophia Silveira Marques (2311100008)

Este repositório contém a implementação de um mecanismo de **Log REDO**, desenvolvido como trabalho prático da disciplina de Banco de Dados II.

## Descrição
O projeto simula o funcionamento do mecanismo de log de um SGBD, permitindo que após uma falha (simulada através do `kill -9` e no nosso através do `taskkill /IM postgres.exe /F`), os dados sejam restaurados a partir da tabela de log. Foram implementadas:

- Tabela de dados em memória (`UNLOGGED TABLE`).
- Tabela de log persistente.
- Triggers para registrar automaticamente operações (`INSERT`, `UPDATE`, `DELETE`).
- Controle manual de transações (`BEGIN` e `END`) no log.
- Script de recuperação (REDO) que refaz operações de transações finalizadas.
- Simulação de falhas no PostgreSQL.


  ## Estrutura do Projeto
- ScriptCriacaoTabelas.sql // criação das tabelas e triggers
- ScriptTeste.sql // execução de transações com log
- main.py # script REDO para recuperação
- conexaobanco.ini // configurações de conexão com o banco
- README.md

 ## Como Executar
- Instale as dependências: 
pip install psycopg2

- Crie as tabelas e as triggers
psql -U postgres -d trabalhotp1 -f ScriptCriacaoTabelas.sql

- Execute as transações
psql -U postgres -d trabalhotp1 -f ScriptTeste.sql

- Simule a falha
`sudo kill -9 $(pidof postgres)`
`sudo service postgresql start`
OU se estiver no windows
`taskkill /IM postgres.exe /F`
`net start postgresql-x64-17` (conferir a sua versão do postgres)

- Execute o REDO
`python main.py`

## Observações
- As transações são controladas manualmente pelo log com 'begin' e 'end'.
- O REDO só aplica operações de transações que foram concluídas (end).
- O trigger mudou_cliente cuida do registro automático de operações INSERT, UPDATE e DELETE no log.
- Operações de controle de transação (begin e end) são feitas manualmente no script SQL.
