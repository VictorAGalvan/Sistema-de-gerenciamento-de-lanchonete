import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="lanchoneteDB",
        user="postgres",
        password="1234567",
        client_encoding="utf8"
    )
    print("Conectou com sucesso!")
    conn.close()
except Exception as e:
    print("Erro:", repr(e))