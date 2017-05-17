import apirequest
from copy import copy
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import json
import math


DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DEFAULT_SORT = ['times', 'swipes', 'cost'] # credibility_index will always be sorted as second priority

def run_gui():

    time, day, sort_by, people_shown, filters = reset()
    
    print('''
    _______________
    |SWIPE ME IN FAM|
     ````````````````''')
    while True:
        print('''
        commands:
    ct Day-HH : change time
    vp        : view pippin menu
    va        : view anteatery menu
    sp <str>  : select person from list
    ca        : create account to DB
    ma        : modify a field in an existing account
    cs        : change sorting priority
    f         : filter DB for specific fields
    uf        : unfilter DB for specific fields (reset)
    <ENTER>   : display the next 5 users in search
    q         : quit (terminate)
    ''')

        display_people(day, time, people_shown, sort_by, filters)

        command = input('Enter a command -> ')

        if command.startswith('ct'):
            day = command[3:command.index('-')]
            time = command[command.index('-')+1:]
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
            filters = filter_table()
        elif command == 'uf':
            time, day, sort_by, people_shown,filters = reset()
        elif command == '':
            people_shown += 5
        elif command == 'q':
            break # GRADY IS TRIGGERED
    

def display_pippin_menu():
    print("https://uci.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=4832")    

def display_anteatery_menu():
    print("https://uci.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=3056")

def select_person(ucinetid: str):
    # Send an email to ucinetid@uci.edu, with a confirmation/declination of the invitation
    # This code should be easy to port to django using django's send_mail() and the same string
    # Documentation: https://docs.djangoproject.com/en/1.11/topics/email/
    # Still need a SMTP service though boys
    
    email = "{}@uci.edu".format(ucinetid)
        #name = apirequest.get_request({ucinetid: name}) # how the fuck does get_request work?
        # what are the params i have to input?
    html_string = """\
                <html>
                <head></head>
                <body>
                <p>
                Hello Student!<br>
                Thank you for signing up for Antfeeder!<br>
                <a href="http://www.google.com">Click here to confirm you registration</a>.
                </p>
                </body>
                </html>
                """#.format(name)
    test_server = "cdxu@uci.edu" #replace with whatever email we send from later
    test_email = "craut@uci.edu" #using chinmay's email as a guinea pig
    msg = MIMEText(html_string, 'html')
    server = smtplib.SMTP('localhost', 1025) #change the domain to our SMTP host eventually
    server.send_mail(test_server, test_email, msg.as_string())
    server.quit()

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
        locations = input('Enter the locations you are able to swipe into (Pippin or Anteatery): ')
        if 'pippin' not in locations.lower() and 'anteatery' not in locations.lower():
            print('Error: Invalid dining hall location(s)')
        else:
            break
        
    places_dict = {}
    places_dict['pippin'] = False
    places_dict['anteatery'] = False
    
    if 'pippin' in locations.lower():
        places_dict['pippin'] = True
        
    if 'anteatery' in locations.lower():
        places_dict['anteatery'] = True
    
    infodict['places'] = places_dict
        
    days = []
    while True:
        days = input('Enter the days you are available separated by only spaces: ').strip().split()
        valid_days = True
        for day in days:
            day = day.lower()
            if day not in DAYS:
                print('Error: Invalid day of the week')
                valid_days = False
        if valid_days:
            break
    times = {}
    for day in days:
        timerange = input('Enter an approximate time range in hours for {} separated by a - in 24 hour time(i.e. 7-13)'.format(day)).strip().split('-')
        timerange = [int(i) for i in timerange]
        if day not in ['saturday' , 'sunday']:
            if timerange[0] < 7 or timerange[1] > 20:
                print('Error: Invalid time range')
                while True:
                    timerange = input('Enter an approximate time range in hours for {} separated by a - in 24 hour time(i.e. 7-13)'.format(day)).strip().split('-')
                    timerange = [int(i) for i in timerange]
                    if timerange[0] < 7 or timerange[1] > 20:
                        print('Error: Invalid time range')
                    else:
                        break
        else:
            if timerange[0] < 11 or timerange[1] > 20 or (timerange[0] > 15 and timerange[0] < 17) or (timerange[1] > 15 and timerange[1] < 17):
                print('Error: Invalid time range')
                while True:
                    timerange = input('Enter an approximate time range in hours for {} separated by a - in 24 hour time(i.e. 7-13)'.format(day)).strip().split('-')
                    timerange = [int(i) for i in timerange]
                    if timerange[0] < 11 or timerange[1] > 20 or (timerange[0] > 15 and timerange[0] < 17) or (timerange[1] > 15 and timerange[1] < 17):
                        print('Error: Invalid time range')
                    else:
                        break
        timesstr = ''
        for i in range(timerange[0], timerange[1]+1):
            timesstr += str(i) + ' '
        times[day] = timesstr.strip()
        
    infodict['days'] = times

    for key, val in infodict.items():
        print(key, val)
    
    apirequest.post_request(ucinetid, infodict)

def change_sorting_priority():
    priority = input("Enter in the new field you would like to prioritize in the table -> ").lower()
    return _get_sorting_preferences([priority])

def filter_table():
    result = {}
    
    name = input("Enter the name to filter for [Enter for all names] -> ")
    time = input("Enter the time to filter for [Enter for all times] -> ")
    location = input("Enter the location to filter for [Blank for all places] -> ")
    cost = input("Enter the cost to filter for [Enter for all prices] -> ")

    if name != '':
        result['name'] = name
    if time != '':
        result['times'] = time
    if location != '':
        if location.lower() == 'pippin':
            result['pippin'] = True
        elif location.lower() == 'anteatery':
            result['anteatery'] = True
    if cost != '':
        result['cost'] = cost
    
    return result
    

def reset():
    return (str(int(str(datetime.now())[11:13])+1) + ':00', DAYS[datetime.today().weekday()], DEFAULT_SORT, 5, {})



def display_people(day:str, time:str, people_shown, sort_by=['times', 'swipes', 'cost'], filters={}):
    sort_by = _get_sorting_preferences(sort_by)
    print('                        Swipe Me In              ')
    print('               Listings for ' + day + ' at ' + time)
    print('Sorting by: ', str(sort_by))
    print('{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}'.format('Name', 'Time', 'Pippin?', 'Anteatery?', 'Cost', 'Swipes'))

    #json_text = apirequest.get_request({'times':time})
    json_data = open('dankbase.json')
    json_text = json.load(json_data)
    result = ''
    count = 0
    for person in sorted(json_text, key=(lambda x:(sort_functions(day, time, sort_by[0], json_text[x][sort_by[0]]),-1* _cred_ind(json_text[x]['success'], json_text[x]['failure'], json_text[x]['swipes'], json_text[x]['response_time']),sort_functions(day, time, sort_by[1], json_text[x][sort_by[1]]), sort_functions(day, time, sort_by[2], json_text[x][sort_by[2]])))):
        if len(filters) == 0:
            result += '{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}'.format(json_text[person]['name'], display_next_time(day, time, json_text[person]['times']), str(json_text[person]['pippin']), str(json_text[person]['anteatery']), str(json_text[person]['cost']), str(json_text[person]['swipes'])) + '\n'
            count += 1
        else:
            if all(json_text[person][key] == filters[key] for key in filters):                  
                result += '{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}'.format(json_text[person]['name'],display_next_time(day, time, json_text[person]['times']), str(json_text[person]['pippin']), str(json_text[person]['anteatery']), str(json_text[person]['cost']), str(json_text[person]['swipes'])) + '\n'
                count += 1

        if count == people_shown:
            break

    print(result)


def sort_functions(day, time, name, value):
    if name == 'times':
        return _time_sort(day, time, value)
    elif name == 'swipes':
        return -1 * int(value)
    elif name == 'cost':
        return int(value)
        

def _time_sort(day, time, all_times):
    for t in sorted(all_times[day]):
        if t - int(time[:time.index(':')]) >= 0:
            return t - int(time[:time.index(':')])
    return 24

def display_next_time(day, time, all_times):
    for t in sorted(all_times[day]):
        if t - int(time[:time.index(':')]) >= 0:
            return day + ', ' + str(t) + ':00'
    current_day = (DAYS.index(day)+1) % 7
    for i in range(6):
        if len(all_times[DAYS[current_day]]) == 0:
            current_day = (current_day+1)%7
        else:
            return DAYS[current_day] + ', ' + str(all_times[DAYS[current_day]][0]) + ':00'

def _cred_ind(successes, failures, swipes, resp_time):
    first_frac = (successes+1)/(failures+1)
    second_frac = (swipes/(math.sqrt(resp_time+1)))

    return first_frac * second_frac

def _get_sorting_preferences(sort_by):
    if len(sort_by) == 3:
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
