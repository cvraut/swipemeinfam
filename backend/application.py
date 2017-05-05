from flask import Flask
import routes

application = Flask(__name__)   

for route in routes.ALL_ROUTES:
    application.add_url_rule(rule=route.url, view_func=route.func, methods=route.methods)

@application.route('/')
def index():
    return "hello world!"

if __name__ == '__main__':
    application.run()