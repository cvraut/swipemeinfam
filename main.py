from flask import Flask, request
import sqlite3
import fmt

BASE = 'swipe'
VERSION = 'v1'

URL = f'/{BASE}/{VERSION}'

conn = sqlite3.connect('users.db', check_same_thread = False)
c = conn.cursor()

app = Flask(__name__)

@app.route(f'{URL}')
def base():
    return 'SWIPE ME IN'

@app.route(f'{URL}/users')
def users():
    all_ = request.args.get('all')
    if all_:
        search_result = [item for item in c.execute('SELECT * FROM USERS')]
        return fmt.all_to_json(search_result)
    user = request.args.get('user')
    if user:
        c.execute('SELECT * FROM USERS WHERE name=?', (user,))
        search_result = c.fetchone()
        if search_result:
            return fmt.search_to_json(search_result)
        else:
            return "No user found"
    else:
        return "ERROR"

@app.route(f'{URL}/users/adduser', methods=['POST'])
def adduser():
    user = tuple(request.form[item] for item in fmt.DB_ORGANIZATION)
    c.execute('INSERT INTO USERS VALUES (?, ?, ?, ?)', user)
    conn.commit()
    return '{"code": "success"}'

if __name__ == '__main__':
    app.run()