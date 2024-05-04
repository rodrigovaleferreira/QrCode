import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Criar a tabela nomes no banco de dados se ainda não existir
c.execute('CREATE TABLE IF NOT EXISTS nomes (id INTEGER PRIMARY KEY, nome TEXT, status TEXT DEFAULT "ativo")')

# Commit e fechar a conexão com o banco de dados
conn.commit()
conn.close()
