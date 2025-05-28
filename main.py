from configparser import ConfigParser
import psycopg2

# Função que pega as configurações do banco do arquivo database.ini
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
  

params = db_config()
conn = psycopg2.connect(**params)
aux = conn.cursor()
t_end = []
aux.execute("select transacao from log where operacao = 'end';")
transac_end = aux.fetchall()
for row in transac_end:
  t_end.append(row[0])
print(t_end)
#ler um por um das coisas da tabela log
aux.execute("select * from log;")
tudo_log = aux.fetchall()
for row in tudo_log:
  #comparar com o que ta na lista de transações finalizadas
  if tudo_log[0] in t_end:
    if tudo_log[1] == 'begin' or tudo_log[1] == 'end':
      continue
    #se tiver na lista, inserir na tabela de novo e imprimir
    elif tudo_log[1] == 'insert':
      aux.execute('insert into clientes_em_memoria (nome, saldo) values(' + tudo_log[3] + ',' + tudo_log[4] + ');')
    elif tudo_log[1] == 'update':
      aux.execute('update clientes_em_memoria set saldo = '+ tudo_log[4] + ', nome = '+ tudo_log[3] + 'where id ='+tudo_log[2]+';')
    elif tudo_log[1] == 'delete':
      aux.execute('delete from clientes_em_memoria where id= '+ tudo_log[2] +';')
