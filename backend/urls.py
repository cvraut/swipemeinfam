BASE            =   'swipemein'
VERSION         =   'v1'

                    #/swipemein/api/v1/
URL             =   '/' + BASE + '/api/' + VERSION

                    #/swipemein/api/v1/users
USERS           =   URL + '/users'

                    #/swipemein/api/v1/users/<ucinetid>
SPECIFIC_USER   =   USERS + '/<ucinetid>'