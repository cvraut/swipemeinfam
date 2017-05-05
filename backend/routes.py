import api
from collections import namedtuple
import urls

Route = namedtuple('Route', ['url', 'name', 'func', 'methods'])

GET_USER_LIST   =   Route(urls.USERS,           'get_user_list',    api.get_user_list,  ['GET'])
GET_USER        =   Route(urls.SPECIFIC_USER,   'get_user',         api.get_user,       ['GET'])
POST_USER       =   Route(urls.SPECIFIC_USER,   'post_user',        api.post_user,      ['POST'])
PUT_USER        =   Route(urls.SPECIFIC_USER,   'put_user',         api.put_user,       ['PUT'])
DELETE_USER     =   Route(urls.SPECIFIC_USER,   'delete_user',      api.delete_user,    ['DELETE'])

ALL_ROUTES = [GET_USER_LIST, GET_USER, POST_USER, PUT_USER, DELETE_USER]