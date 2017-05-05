from flask import Flask
import routes

application = Flask(__name__)

for route in routes.ALL_ROUTES:
    application.add_url_rule(rule=route.url, view_func=route.func, methods=route.methods)

if __name__ == '__main__':
    application.run(port=80)