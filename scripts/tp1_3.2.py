import psycopg2

# Conexão Default Postgres Database
conn = psycopg2.connect(
    host="172.18.0.2",
    port=5432,
    database="postgres",
    user="postgres",
    password="postgres"
)

# Objeto de Cursor
cur = conn.cursor()
conn.autocommit = True

# Cria novo banco de dados
cur.execute("CREATE DATABASE tp1db;")

# Finaliza conexão e fecha cursor
cur.close()
conn.close()
