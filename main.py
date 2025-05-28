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

aux.execute("select transacao from log where operacao = 'end';")
rows = aux.fetchall()
for row in rows:
    print(row)

#ler um por um das coisas da tabela log
#comparar com o que ta na lista de transações finalizadas
#se tiver na lista, inserir na tabela de novo e imprimir
