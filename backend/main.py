from flask import Flask
import routes

app = Flask(__name__)

for route in routes.ALL_ROUTES:
    app.add_url_rule(rule=route.url, view_func=route.func, methods=route.methods)

if __name__ == '__main__':
    app.run(debug=True, port=5000)