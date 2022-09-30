from app.utils import stripArgs

sql = None

def get_table():
    args = stripArgs('name')
    if not args[0]:
        return args[1]
    name = args[1]['name']
    return sql.select(name)

def drop_table():
    args = stripArgs('name')
    if not args[0]:
        return args[1]
    name = args[1]['name']
    return sql.dropTable(name)

def create_table():
    args = stripArgs('name')
    if not args[0]:
        return args[1]
    name = args[1]['name']
    return sql.createTable(name)