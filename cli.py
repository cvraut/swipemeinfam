import apirequest
from copy import copy
DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
DEFAULT_SORT = ['times', 'credibility_index', 'swipes', 'cost']

def run_gui():
    print('''
    _______________
    |SWIPE ME IN FAM|
     ````````````````''')
    while True:
        print('''
        commands:
    ct D:HH:MM: change time
    vp        : view pippins menu
    va        : view anteatery menu
    sp <str>  : select person from list
    ca        : create account to DB
    ma        : modify a field in an existing account
    cs        : change sorting priority
    f         : filter DB for specific fields
    <ENTER>   : display the next 5 users in search
    q         : quit (terminate)
    ''')
        command = input('Enter a command -> ')

        if command.startswith('ct'):
            time = command[3:]
            display_people(time, DEFAULT_SORT)
        elif command == 'vp':
            display_pippin_menu()
        elif command == 'va':
            display_anteatery_menu()
        elif command.startswith('sp'):
            select_person(command[3:])
        elif command == 'ca':
            create_account()
        elif command == 'cs':
            change_sorting_priority()
        elif command == 'f':
            filter_table()
        elif command == '':
            display_next_five_users()
        elif command == 'q':
            break # GRADY IS TRIGGERED


def display_pippin_menu():
    #XXXXXX I'm too lazy to scrape the website for it right now
    pass

def display_anteatery_menu():
    #XXXXXX I'm too lazy to scrape the website for it right now
    pass

def select_person(ucinetid: str):
    # Send an email to ucinetid@uci.edu, with a confirmation/declination of the invitation
    pass

def create_account():
    ucinetid = input('Enter your ucinetid')
    swipes = int(input('Enter the number of swipes you have'))
    # .....
    # Create the account and put it in the DB

def change_sorting_priority():
    pass
    #send help, calling display_people(sort_by) with sort_by being a list of the attributes
    # that you want to prioritize. The code is pretty messy, you can change it if you want.

def filter_table():
    pass

def display_next_five_users():
    pass



def display_people(time:str, sort_by=['times', 'credibility_index', 'swipes', 'cost']):
    sort_by = _get_sorting_preferences(sort_by)
    print('                        Swipe Me In              ')
    print('               Listings for ' + DAYS[int(time[0])] + ' at ' + time[2:])

    print('{:<10}{:<10}{:<10}{:<15}{:<10}{:<10}'.format('Name', 'Time', 'Pippin?', 'Anteatery?', 'Cost', 'Swipes'))

    json_text = apirequest.get_request({'times':time})
    result = ''
    for user in sorted(json_text['users'], key=(lambda x:(x[sort_by[0]],x[sort_by[1]],x[sort_by[2]],x[sort_by[3]]))):
        result += '{:<10}{:<10}{:<10}{:<15}{:<10}{:<10}'.format(user['name'], str(user['times']['wd_times']), str(user['places']['pippin']), str(user['places']['anteatery']), str(user['cost']), str(user['swipes'])) + '\n'

    print(result)

def _get_sorting_preferences(sort_by):
    if len(sort_by) == 4:
        return sort_by

    if len(sort_by) == 1:
        index = DEFAULT_SORT.index(sort_by[0])
        sorter = copy(DEFAULT_SORT)
        priority = sorter.pop(index)
        sorter.insert(0, priority)
        return sorter

    return DEFAULT_SORT
        



if __name__ == '__main__':
    run_gui()
