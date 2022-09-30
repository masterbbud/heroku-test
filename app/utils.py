from flask import jsonify, request

sql = None

def error(errortype, data=None, e=None):
    if data and e:
        return {'type': 'error', 'data': f'ERROR: {errortype}\n{data}\n{e}'}
    elif data:
        return {'type': 'error', 'data': f'ERROR: {errortype}\n{data}'}
    elif e:
        return {'type': 'error', 'data': f'ERROR: {errortype}\n{e}'}
    return {'type': 'error', 'data': f'ERROR: {errortype}'}

def success(data):
    return {'type': 'success', 'data': data}

def stripArgs(*names):
    kvpairs = {}
    args = request.json
    
    for arg in names:
        val = args.get(arg)
        if not val:
            return False, error(f'Request needs {arg}')
        if arg == 'auth' and not auth_token_used(val):
            return False, error(f'Invalid token')
        kvpairs[arg] = val
    
    return True, kvpairs

def auth_token_used(token):
    # check this
    res = sql.select('accounts', f"auth = '{token}'")
    if res['type'] == 'error' or not res['data']:
        return False
    return True

