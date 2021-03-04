import sys
from flask import current_app as app

from application.resources.resources import Resources as Resources
from flask import request
import logging
from logging.handlers import RotatingFileHandler


@app.route('{0}/'.format(app.config['BASE_URL']), methods=["GET"])
def index():
    return Resources.index()


@app.route('{0}<path:resource>'.format(app.config['BASE_URL']))
def dynamic_page(resource):
    return Resources.dynamic_resource(resource)


@app.before_first_request
def before_first_request():
    if not app.debug:
        handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=2000, backupCount=10)
    else:
        handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    print("Logger loaded")


@app.after_request
def after_request(response):
    supported_languages = ["en", "es"]
    response.headers["Server"] = "WhiteJaguars"
    response.headers["X-Frame-Options"] = "deny"
    if app.config['HTTPS_ENABLED']:
        response.headers["Strict-Transport-Security"] = "max-age=31536000 ; includeSubDomains"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    # response.headers["Content-Security-Policy"] = "script-src 'self'"
    # response.headers["Content-Security-Policy"] = "strict - dynamic"
    response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
    response.headers["Referrer-Policy"] = "no-referrer"
    if "." in request.url:
        extension = request.url.rsplit('.', 1)[1].lower()
        if extension == "mp4":
            response.headers['Accept-Ranges'] = "bytes"
        if extension in app.config['ALLOWED_MIME']:
            response.headers["Cache-Control"] = "public, max-age=31536000"
    else:
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


@app.errorhandler(401)
def http_401_handler(error):
    app.logger.info("{0}".format(error))
    return Resources.return_error(401)


@app.errorhandler(404)
def http_404_handler(error):
    app.logger.info("{0}".format(error))
    return Resources.return_error(404)


@app.errorhandler(500)
def http_500_handler(error):
    app.logger.error("{0}".format(error))
    return Resources.return_error(500)
