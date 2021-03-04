from flask import Flask
from flask_restful import Api

app = Flask(__name__)

api = Api(app)


def create_app(debug=False):

    app.config['BASE_URL'] = "/"
    app.config['HTTPS_ENABLED'] = False
    app.config['LOG_FILE'] = "log.txt"
    app.config['ALLOWED_MIME'] = ["html","js", "css", "png", "jpg", "ico", "map", "xml", "json", "txt", "woff", "woff2", "eot", "ttf", "svg", "mp4", "pdf"]

    with app.app_context():
        from .views import views
        return app
