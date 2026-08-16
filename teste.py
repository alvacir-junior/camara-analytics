import duckdb

con = duckdb.connect("sources/camara_db/camara.duckdb")

print("Schemas:")
print(con.execute("SHOW SCHEMAS").fetchall())

print("\nTabelas:")
print(con.execute("""
SELECT table_schema, table_name
FROM information_schema.tables
ORDER BY table_schema, table_name
""").fetchall())