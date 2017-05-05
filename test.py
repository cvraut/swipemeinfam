from flask import Flask

app = Flask(__name__)

def base():
    return 'LOL'

base = app.route(base, '/')

if __name__ == '__main__':
    app.run(debug=True)