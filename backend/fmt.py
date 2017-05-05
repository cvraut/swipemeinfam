import json

DB_ORGANIZATION = ('name', 'ucinetid', 'swipes', 'cost')

def search_to_json(search_result):
    return json.dumps(dict(zip(DB_ORGANIZATION, search_result)))

def all_to_json(db_list: [tuple]):
    return json.dumps({'users': [dict(zip(DB_ORGANIZATION, search_result)) for search_result in db_list]})