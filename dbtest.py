import psycopg2

conn = psycopg2.connect("dbname=hophacks user=ubuntu password=0912")

cur = conn.cursor()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public'")
print(cur.fetchall())

