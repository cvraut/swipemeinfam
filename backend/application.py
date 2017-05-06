from flask import Flask
import routes
from flask_cors import CORS, cross_origin

application = Flask(__name__)   
CORS(application)

for route in routes.ALL_ROUTES:
    application.add_url_rule(rule=route.url, view_func=route.func, methods=route.methods)

@application.route('/')
def index():
    return "hello world!"

if __name__ == '__main__':
    application.run()