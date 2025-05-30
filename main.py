from configparser import ConfigParser
import psycopg2

# configura a conexão com o banco
def db_config(filename='conexaobanco.ini', section='postgresql'):
  parser = ConfigParser()
  parser.read(filename)

  db = {}
  if parser.has_section(section):
    params = parser.items(section)
    for param in params:
      db[param[0]] = param[1]
  else:
    raise Exception('Section {0} not found in the {1} file'.format(section, filename))

  return db

# imprime as transações
def printar(transacao, tipo, id, nome, saldo):
  print("<" + str(transacao) + ", " + tipo + ", " + str(id) + ", " + nome + ", " + str(saldo) + ">")


# main -> executa o código de fato
try:
  params = db_config()
  conn = psycopg2.connect(**params)
  aux = conn.cursor()

  t_end = []
  aux.execute("select transacao from log where operacao = 'end';")
  transac_end = aux.fetchall()
  print("Transações que devem realizar o REDO:")
  for row in transac_end:
    t_end.append(row[0])
  print(t_end, "\n")


  #ler um por um das coisas da tabela log
  aux.execute("select * from log;")
  tudo_log = aux.fetchall()
  aux.execute("insert into log(transacao, operacao) values (txid_current(), 'begin REDO');")
  print("Operações realizadas no REDO")
  for row in tudo_log:
    #comparar com o que ta na lista de transações finalizadas
    if row[0] in t_end:
      if row[1] == 'begin' or row[1] == 'end':
        continue
      #se tiver na lista, inserir na tabela de novo e imprimir
      elif row[1] == 'insert':
        aux.execute("insert into clientes_em_memoria (nome, saldo) values( '" + row[3] + "'," + str(row[4]) + ");")
      elif row[1] == 'update':
        aux.execute("update clientes_em_memoria set saldo = "+ str(row[4]) + ", nome = '"+ row[3] + "' where id = "+ str(row[2])+";")
      elif row[1] == 'delete':
        aux.execute("delete from clientes_em_memoria where id= "+ str(row[2]) +";")
      printar(row[0], row[1], row[2], row[3], row[4])
  aux.execute("insert into log(transacao, operacao) values (txid_current(), 'end REDO');")
  conn.commit()
  
  
except (Exception, psycopg2.DatabaseError) as error:
  print(error)
  
finally:
  if conn is not None:
    conn.close()