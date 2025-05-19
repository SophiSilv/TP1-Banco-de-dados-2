-- Active: 1744144573581@@127.0.0.1@5432@trabalhotp1@public
CREATE UNLOGGED TABLE clientes_em_memoria (
    id SERIAL PRIMARY KEY,
    nome TEXT,
    saldo NUMERIC
);

CREATE TABLE log(
    transacao text,
    operacao TEXT,
    id_cliente INT,
    nome TEXT,
    saldo NUMERIC
);

create or replace function public.mudou_cliente()
returns trigger
language plpgsql
as $function$
DECLARE
tid text;
begin
    select txid_current() into tid;

    if TG_OP = 'INSERT' then
        insert into log (transacao, operacao, id_cliente, nome, saldo)
        values (tid, 'insert', new.id, new.nome, new.saldo);

    elseif TG_OP = 'UPDATE' then
        insert into log (transacao, operacao, id_cliente, nome, saldo)
        values (tid,'update', new.id, new.nome, new.saldo);

    elseif TG_OP = 'DELETE' then
        insert into log (transacao, operacao, id_cliente, nome, saldo)
        values (tid,'delete', old.id, old.nome, old.saldo);
    end if;

    return new;
end;
$function$;


create trigger mudou_cliente after insert or update or delete on clientes_em_memoria
    for each row execute procedure mudou_cliente();

INSERT INTO clientes_em_memoria (nome, saldo) VALUES ('Cliente 1', 100.00);
UPDATE clientes_em_memoria SET saldo = saldo + 50 WHERE id = 1;

