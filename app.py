from flask import Flask, render_template, request
from main.views import bp_main
app = Flask(__name__)

def create_and_config_app():
    app = Flask(__name__)
    app.register_blueprint(bp_main)
    return app

app = create_and_config_app()


if __name__ == '__main__':
    app.run()
