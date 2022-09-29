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
        try:
            self.cur.execute(f"""
                DROP TABLE IF EXISTS {name}
            """)
        except:
            return self.rollback()
        self.conn.commit()

    def createTable(self, name):
        text = []
        columns = tables[name]
        for n, val in columns.items():
            text.append(f'{n} {val}')
        text = ',\n'.join(text)
        try:
            self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {name} (
                {text});
            """)
        except:
            return self.rollback()
        self.conn.commit()
    
    def insert(self, table, columns: dict):
        # columns should be columnName: value
        colsList = ', '.join(list(columns))
        valsList = [f"'{i}'" if isinstance(i, str) else f"{i}" for i in columns.values()]
        valsText = ',\n'.join(valsList)
        try:
            self.cur.execute(f"""
            INSERT into {table} ({colsList})
            VALUES (
                {valsText}
            )
            """)
        except:
            return self.rollback()
        self.conn.commit()

    def select(self, table, where=None):
        try:
            if where:
                self.cur.execute(f"""
                    SELECT * from {table} where {where}
                """)
            else:
                self.cur.execute(f"""
                    SELECT * from {table}
                """)
        except:
            return self.rollback()
        retList = []
        for s in self.cur.fetchall():
            row = {}
            for (colname, cast), value in zip(tables[table].items(), s):
                row.update({colname: self.typeCast(value, cast)[0]})
            retList.append(row)
        return retList
    
    def selectColumns(self, table):
        try:
            self.cur.execute(f"""
                SELECT * from {table}
            """)
        except:
            return self.rollback()
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

    def rollback(self):
        self.cur.execute('ROLLBACK')
        self.conn.commit()
        return 'ERROR: Bad request'
        