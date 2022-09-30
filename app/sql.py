import os
from datetime import datetime
from types import NoneType

import psycopg2

from urllib.parse import urlparse

tables = None

class SQL:
    def __init__(self):
        uri = os.environ['DATABASE_URL']
        result = urlparse(uri)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        port = result.port
        self.conn = psycopg2.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
            port=port)
        self.cur = self.conn.cursor()
        
    def dropTable(self, name):
        try:
            self.cur.execute(f"""
                DROP TABLE IF EXISTS {name}
            """)
        except:
            return self.rollback('drop '+name)
        self.conn.commit()
        return 'Dropped table '+name

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
        except Exception as e:
            return self.rollback(f"""
            CREATE TABLE IF NOT EXISTS {name} (
                {text});
            """, e)
        self.conn.commit()
        return 'Created table '+name
    
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
        except Exception as e:
            return self.rollback('insert '+table+' '+str(columns), e)
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
            return self.rollback('select '+table+' '+str(where))
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
            return self.rollback('column names '+table)
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

    def rollback(self, data: str, e=None):
        self.cur.execute('ROLLBACK')
        self.conn.commit()
        return 'ERROR: Bad request - ' + data + str(e)
