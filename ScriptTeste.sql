-- Active: 1744144308559@@127.0.0.1@5432@trabalhotp1

BEGIN;

insert into
    log(transacao, operacao)
values (txid_current(), 'begin');

INSERT INTO
    clientes_em_memoria (nome, saldo)
VALUES ('Cliente 1', 100.00);

UPDATE clientes_em_memoria SET saldo = saldo + 50 WHERE id = 1;

insert into log(transacao, operacao) values (txid_current(), 'end');

END;

BEGIN;

insert into
    log(transacao, operacao)
values (txid_current(), 'begin');

INSERT INTO
    clientes_em_memoria (nome, saldo)
VALUES ('Cliente 2', 200.00);

UPDATE clientes_em_memoria SET saldo = saldo + 50 WHERE id = 2;

insert into log(transacao, operacao) values (txid_current(), 'end');

END;

BEGIN;

insert into
    log(transacao, operacao)
values (txid_current(), 'begin');

INSERT INTO
    clientes_em_memoria (nome, saldo)
VALUES ('Cliente 3', 300.00);

UPDATE clientes_em_memoria SET saldo = saldo + 50 WHERE id = 2;

insert into log(transacao, operacao) values (txid_current(), 'end');

END;

BEGIN;

insert into
    log(transacao, operacao)
values (txid_current(), 'begin');

INSERT INTO
    clientes_em_memoria (nome, saldo)
VALUES ('Cliente 4', 400.00);

UPDATE clientes_em_memoria SET saldo = saldo + 50 WHERE id = 3;

BEGIN;

insert into
    log(transacao, operacao)
values (txid_current(), 'begin');

INSERT INTO
    clientes_em_memoria (nome, saldo)
VALUES ('Cliente 6', 600.00);

END;

END;