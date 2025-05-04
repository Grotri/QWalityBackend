import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_NAME = "aboba"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    connection = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
except psycopg2.OperationalError as e:
    print("❌ Failed to connect to PostgreSQL:")
    print(e)
    exit(1)

connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()

cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
exists = cursor.fetchone()

if not exists:
    print(f"📦 Creating database '{DB_NAME}'...")
    cursor.execute(f"CREATE DATABASE {DB_NAME};")
else:
    print(f"✅ Database '{DB_NAME}' already exists.")

cursor.close()
connection.close()
