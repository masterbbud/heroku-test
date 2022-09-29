import os
from datetime import datetime
from types import NoneType

import psycopg2

tables = None

class SQL:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_DATABASE'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'])
        self.cur = self.conn.cursor()
        
    def dropTable(self, name):
        self.cur.execute(f"""
            ALTER TABLE {name}
                DROP CONSTRAINT {name}_id_seq
            DROP TABLE IF EXISTS {name}
        """)
        self.conn.commit()

    def createTable(self, name):
        text = []
        columns = tables[name]
        for n, val in columns.items():
            text.append(f'{n} {val}')
        text = ',\n'.join(text)
        self.cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {name} (
            {text});
        """)
        self.conn.commit()
    
    def insert(self, table, columns: dict):
        # columns should be columnName: value
        colsList = ', '.join(list(columns))
        valsList = [f"'{i}'" if isinstance(i, str) else f"{i}" for i in columns.values()]
        valsText = ',\n'.join(valsList)
        self.cur.execute(f"""
        INSERT into {table} ({colsList})
        VALUES (
            {valsText}
        )
        """)
        self.conn.commit()

    def select(self, table, where=None):
        if where:
            self.cur.execute(f"""
                SELECT * from {table} where {where}
            """)
        else:
            self.cur.execute(f"""
                SELECT * from {table}
            """)
        retList = []
        for s in self.cur.fetchall():
            row = {}
            for (colname, cast), value in zip(tables[table].items(), s):
                row.update({colname: self.typeCast(value, cast)[0]})
            retList.append(row)
        return retList
    
    def selectColumns(self, table):
        self.cur.execute(f"""
            SELECT * from {table}
        """)
        self.cur.fetchall()
        return [desc for desc in self.cur.description]

    def typeCast(self, val, typeString):
        # returns a value, typecast via typeString, and also the type
        if 'TEXT' in typeString:
            return str(val), str
        elif 'INTEGER' in typeString or 'SERIAL' in typeString:
            return int(val), int
        elif 'BOOLEAN' in typeString:
            return bool(val), bool
        elif 'TIMESTAMP' in typeString:
            return datetime(val), datetime
        return val, NoneType
        