from urllib import request, parse
import json

URL = 'http://backend-dev.us-west-1.elasticbeanstalk.com/swipemein/api/v1/users'

def _build_url_for_get(params: dict) -> str:
    '''Builds url for GET requests'''
    query_parameters = []

    for param, val in params.items():
        if param not in 'ucinetid name swipes cost times places':
            raise SyntaxError('A parameter that you passed is not a valid parameter name')
        query_parameters.append((param, val))

    return(URL + '?' + parse.urlencode(query_parameters))

def _build_url_with_ucinetid(ucinetid: str) -> str:
    '''Builds url for POST requests'''
    return(URL + '/' + ucinetid + '?')


def get_request(params: dict) -> str:
    ''' This function gets the information from the API as a JSON and returns it.
        params is a dictionary of query parameters (name, swipes, cost, etc.)'''

    url = _build_url_for_get(params)
    response = None

    try:
        response = request.urlopen(url)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)

    finally:
        if response != None:
            response.close()

def post_request(ucinetid:str, params: dict) -> str:
    ''' This function gets the information from the API as a JSON and returns it.
        params is a dictionary of query parameters (name, swipes, cost, etc.)'''

    url = _build_url_with_ucinetid(ucinetid)

    if 'name' not in params and 'swipes' not in params:
        raise SyntaxError('You need to specify at least a name and number of swipes in the paramters')
    
    data = parse.urlencode(params).encode()

    req = request.Request(url, data=data)
    response = None
    
    try:
        response = request.urlopen(req)
        resp = request.urlopen(req)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)
    finally:
        if response != None:
            response.close()

def put_request(ucinetid: str, params: dict) -> str:
    ''' This function gets the information from the API as a JSON and returns it
        params is a dictionary of query parameters (name, swipes, cost, etc.)'''

    url = _build_url_with_ucinetid(ucinetid)

    if len(params) == 0:
        raise SyntaxError('You need to specify the paramters than you want to update')

    data = parse.urlencode(params).encode()

    req = request.Request(url, data=data, method='PUT')
    response = None
    
    try:
        response = request.urlopen(req)
        resp = request.urlopen(req)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)
    finally:
        if response != None:
            response.close()

def delete_request(ucinetid: str) -> str:
    ''' This function gets the information from the API as a JSON and returns it'''

    url = _build_url_with_ucinetid(ucinetid)

    req = request.Request(url, method='DELETE')
    response = None
    
    try:
        response = request.urlopen(req)
        resp = request.urlopen(req)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)
    finally:
        if response != None:
            response.close()
