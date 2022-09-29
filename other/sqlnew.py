import psycopg2
import os
import json

def sqlConnect():
    configFile = open(os.path.join(os.getcwd(),"config.json"),'r')
    config = json.load(configFile)
    conn = psycopg2.connect(
        host=config['host'],
        database=config['database'],
        user=config['user'],
        password=config['password'])
    return conn

sql = sqlConnect()
cur = sql.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS newtable (
   column1 INTEGER
);
""")
cur.execute("""
INSERT into newtable(column1)
VALUES (
    5
);
""")
cur.execute("""
INSERT into newtable(column1)
VALUES (
    5
);
""")
cur.execute("""
SELECT * from newtable
""")
rows = cur.fetchall()
print(rows)
for row in rows:
    print(row[0])
sql.commit()
sql.close()