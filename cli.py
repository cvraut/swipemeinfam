import apirequest
from copy import copy
from datetime import datetime
import smtplib
from email.mime.text import MIMEText


DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DEFAULT_SORT = ['times', 'credibility_index', 'swipes', 'cost']

def run_gui():

    time, day, sort_by, people_shown, filters = reset()
    
    print('''
    _______________
    |SWIPE ME IN FAM|
     ````````````````''')
    while True:
        print('''
        commands:
    ct Day:HH : change time
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
            filters = filter_table()
        elif command == 'uf':
            time, day, sort_by, people_shown = reset()
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
    priority = input("Enter in the new field you would like to prioritize in the table -> ")
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
        result['time'] = time
    if location != '':
        result['location'] = location
    if cost != '':
        result['cost'] = cost
    
    return result
    

def reset():
    return (str(int(str(datetime.now())[11:13])+1) + ':00', DAYS[datetime.today().weekday()], DEFAULT_SORT, 5, {})



def display_people(day:str, time:str, people_shown, sort_by=['times', 'credibility_index', 'swipes', 'cost'], filters={}):
    sort_by = _get_sorting_preferences(sort_by)
    print('                        Swipe Me In              ')
    print('               Listings for ' + day + ' at ' + time)

    print('{:<10}{:<10}{:<10}{:<15}{:<10}{:<10}'.format('Name', 'Time', 'Pippin?', 'Anteatery?', 'Cost', 'Swipes'))

    json_text = apirequest.get_request({'times':time})
    result = ''
    count = 0
    for user in sorted(json_text['users'], key=(lambda x:(x[sort_by[0]],x[sort_by[1]],x[sort_by[2]],x[sort_by[3]]))):
        if len(filters) == 0:
            result += '{:<10}{:<10}{:<10}{:<15}{:<10}{:<10}'.format(user['name'], str(user['times']['wd_times']), str(user['places']['pippin']), str(user['places']['anteatery']), str(user['cost']), str(user['swipes'])) + '\n'
            count += 1
        else:
            if all(user[key] == filters[key] for key in filters):                  
                result += '{:<10}{:<10}{:<10}{:<15}{:<10}{:<10}'.format(user['name'], str(user['times']['wd_times']), str(user['places']['pippin']), str(user['places']['anteatery']), str(user['cost']), str(user['swipes'])) + '\n'
                count += 1

        if count == people_shown:
            break

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
