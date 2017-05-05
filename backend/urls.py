BASE            =   'swipemein'
VERSION         =   'v1'

                    #/swipemein/api/v1/
URL             =   f'/{BASE}/api/{VERSION}'

                    #/swipemein/api/v1/users
USERS           =   f'{URL}/users'

                    #/swipemein/api/v1/users/<ucinetid>
SPECIFIC_USER   =   f'{USERS}/<ucinetid>'