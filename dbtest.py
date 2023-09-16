import psycopg2

conn = psycopg2.connect("dbname=hophacks user=ubuntu password=0912")

cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'prescription'")
print(cur.fetchall())
