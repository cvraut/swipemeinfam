import apirequest
from copy import copy
from datetime import datetime
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DEFAULT_SORT = ['times', 'credibility_index', 'swipes', 'cost']

def run_gui():
    print('''
    _______________
    |SWIPE ME IN FAM|
     ````````````````''')
    while True:
        print('''
        commands:
    ct Day:HH : change time
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
        time = str(int(str(datetime.now())[11:13])+1) + ':00'
        day = DAYS[datetime.today().weekday()]
        sort_by = DEFAULT_SORT
        

        if command.startswith('ct'):
            time = command[3:] + ':00'
        elif command == 'vp':
            display_pippin_menu()
        elif command == 'va':
            display_anteatery_menu()
        elif command.startswith('sp'):
            select_person(command[3:])
        elif command == 'ca':
            create_account()
        elif command == 'cs':
            sort_by = change_sorting_priority()
        elif command == 'f':
            filter_table()
        elif command == '':
            display_next_five_users()
        elif command == 'q':
            break # GRADY IS TRIGGERED

        display_people(day, time, sort_by)


def display_pippin_menu():
    print("https://uci.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=4832")    

def display_anteatery_menu():
    print("https://uci.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=3056")

def select_person(ucinetid: str):
    # Send an email to ucinetid@uci.edu, with a confirmation/declination of the invitation
    pass

def create_account():
    # Create the account and put it in the DB
    infodict = {}
    name = input('Enter your name: ')
    infodict['name'] = name
    ucinetid = input('Enter your ucinetid: ')
    swipes = int(input('Enter the number of swipes you have: '))
    infodict['swipes'] = swipes
    fee = float(input('Enter your price per swipe: '))
    infodict['cost'] = fee
    locations = ''
    while True:
        locations = input('Enter the locations you are able to swipe into (Pippins or Anteatery): ')
        if 'pippins' not in locations.lower() and 'anteatery' not in locations.lower():
            print('Error: Invalid dining hall location(s)')
        else:
            break
    infodict['locations'] = locations
    days = []
    while True:
        days = input('Enter the days you are available separated by only spaces: ').strip().split('')
        valid_days = True
        for day in days:
            day = day.lower()
            if day not in DAYS:
                print('Error: Invalid day of the week')
                valid_days = False
        if valid_days:
            break
    times = []
    for day in days:
        timerange = map(int(), input('Enter an approximate time range in hours for {} separated by a - in 24 hour time(i.e. 7-13)'.format(day)).strip().split('-'))
        if day not in ['saturday' , 'sunday']:
            if timerange[0] < 7 or timerange[1] > 20:
                print('Error: Invalid time range')
                while True:
                    timerange = map(int(), input('Enter an approximate time range in hours for {} separated by a - in 24 hour time(i.e. 7-13)'.format(day)).strip().split('-'))
                    if timerange[0] < 7 or timerange[1] > 20:
                        print('Error: Invalid time range')
                    else:
                        break
        else:
            if timerange[0] < 11 or timerange[1] > 20 or (timerange[0] > 15 and timerange[0] < 17) or (timerange[1] > 15 and timerange[1] < 17):
                print('Error: Invalid time range')
                while True:
                    timerange = map(int(), input('Enter an approximate time range in hours for {} separated by a - in 24 hour time(i.e. 7-13)'.format(day)).strip().split('-'))
                    if timerange[0] < 11 or timerange[1] > 20 or (timerange[0] > 15 and timerange[0] < 17) or (timerange[1] > 15 and timerange[1] < 17):
                        print('Error: Invalid time range')
                    else:
                        break
        times.append(tuple(timerange))
    '''
     day and times will be added as a dictionary whose items are 2-tuples with the time range of availability
     we might need to update the api because im putting weekends and weekdays together and checking the times separately
     - Cody
    '''
    infodict['days'] = {day:time for day in days for time in times}
    apirequest.post_request(ucinetid, infodict)

def change_sorting_priority():
    priority = input("Enter in the new field you would like to prioritize in the table -> ")
    return _get_sorting_preferences([priority])

def filter_table():
    pass

def display_next_five_users():
    pass



def display_people(day:str, time:str, sort_by=['times', 'credibility_index', 'swipes', 'cost']):
    sort_by = _get_sorting_preferences(sort_by)
    print('                        Swipe Me In              ')
    print('               Listings for ' + day + ' at ' + time)

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
        credibility = sorter.pop(sorter.index('credibility_index'))
        sorter.insert(1, credibility)
        return sorter

    return DEFAULT_SORT
        



if __name__ == '__main__':
    run_gui()
