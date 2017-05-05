from db import *
from flask import request
import re

pattern = r'({valid_field})(__not)?__(ne|lt|gt|gte)'.format(valid_field="|".join(VALID_FIELDS))

def get_query_dict():
    query_dict = request.args.to_dict()
    query_dict = {field:query_dict.get(field) for field in query_dict if re.match(pattern, field) and query_dict.get(field, None) != None}
    return query_dict

def post_query_dict():
    query_dict = request.form.to_dict()
    query_dict = {field:query_dict.get(field) for field in VALID_FIELDS if query_dict.get(field, None) != None}
    return query_dict

def get_user_list():
    query_dict = get_query_dict()
    return db_get_user_list(**query_dict)

def get_user(ucinetid):
    return db_get_user(ucinetid)

def post_user(ucinetid):
    query_dict = post_query_dict()
    return db_post_user(ucinetid, **query_dict)

def put_user(ucinetid):
    query_dict = post_query_dict()
    return db_put_user(ucinetid, **query_dict)

def delete_user(ucinetid):
    return db_delete_user(ucinetid)