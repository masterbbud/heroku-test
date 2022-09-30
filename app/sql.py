import os
from datetime import datetime
from types import NoneType

import psycopg2

from urllib.parse import urlparse

import inspect

from app.utils import error, success

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
        query = f"""
            DROP TABLE IF EXISTS {name}
        """
        result = self.tryExecute(query)
        if result:
            return result
        self.conn.commit()
        return success(f'Dropped table {name}')

    def createTable(self, name):
        text = []
        columns = tables[name]
        for n, val in columns.items():
            text.append(f'{n} {val}')
        text = ',\n'.join(text)
        query = f"""
            CREATE TABLE IF NOT EXISTS {name} (
                {text});
        """
        result = self.tryExecute(query)
        if result:
            return result
        self.conn.commit()
        return success(f'Created table {name}')
    
    def insert(self, table, columns: dict):
        # columns should be columnName: value
        colsList = ', '.join(list(columns))
        valsList = [f"'{i}'" if isinstance(i, str) else f"{i}" for i in columns.values()]
        valsText = ',\n'.join(valsList)
        query = f"""
            INSERT into {table} ({colsList})
            VALUES (
                {valsText}
            )
        """
        result = self.tryExecute(query)
        if result:
            return result
        self.conn.commit()
        return success(f'Inserted into {table}')

    def select(self, table, where=None):
        if where:
            query = f"""
                SELECT * from {table} where {where}
            """
        else:
            query = f"""
                SELECT * from {table}
            """
        result = self.tryExecute(query)
        if result:
            return result
        retList = []
        for s in self.cur.fetchall():
            row = {}
            for (colname, cast), value in zip(tables[table].items(), s):
                row.update({colname: self.typeCast(value, cast)[0]})
            retList.append(row)
        return success(retList)
    
    def typeCast(self, val, typeString):
        # returns a value, typecast via typeString, and also the type
        if 'TEXT' in typeString:
            return str(val), str
        elif 'INTEGER' in typeString or 'SERIAL' in typeString:
            return int(val), int
        elif 'BOOLEAN' in typeString:
            return bool(val), bool
        elif 'TIMESTAMP' in typeString:
            return datetime.strptime(val, r"%Y-%m-%d %H:%M:%S.%f"), datetime
        return val, NoneType

    def rollback(self, data: str, e=None):
        self.cur.execute('ROLLBACK')
        self.conn.commit()
        return error('Bad Request', data, e)

    def tryExecute(self, query):
        try:
            self.cur.execute(query)
        except Exception as e:
            return self.rollback(f'{inspect.stack()[1].function}\n{query}', e)
