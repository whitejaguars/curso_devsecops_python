from flask import current_app as app
from application.util.tools import Tools as Tools
from application.util.validations import InputValidation as InputValidation
from application.util.parser import SimpleParser as SimpleParser
from flask import send_from_directory, request, Response


class Resources:

    @staticmethod
    def index():
        """
        Return Index HTML content based on the region being accessed, e.g /en-us/
        """
        html_data = Tools.load_file("content/static/index.html")
        mappings = dict()
        mappings["resource"] = ""
        html_data = SimpleParser.parse(html_data, mappings)
        return html_data, 200

    @staticmethod
    def dynamic_resource(resource):
        """
        Return HTML content dynamically generated based on the region being accessed, e.g /en-us/some-content
        """
        country_data = dict()
        html_data = None
        if InputValidation.is_valid_file('content/static/{0}'.format(resource), app.config['ALLOWED_MIME']) and \
                not resource.endswith(".html") and resource != "index":
            extension = resource.rsplit('.', 1)[1].lower()
            if extension == "js" or extension == "css":
                path = 'content/static/{}'.format(resource)
                html_data = Tools.load_file(path)
                html_data = SimpleParser.parse(html_data, country_data)
                content_type = {"js": "text/javascript", "css": "text/css"}
                return Response(html_data, mimetype=content_type[extension])
            return send_from_directory('../content/static', resource), 200
        elif resource.endswith(".html"):
            return Resources.return_error(404)
        else:
            path = 'content/static/{}.html'.format(resource)
            if InputValidation.is_valid_file(path, app.config['ALLOWED_MIME']):
                html_data = Tools.load_file(path)
            if html_data is None:
                return Resources.return_error(404)
            mappings = SimpleParser.prepare_mappings(country_data)
            mappings["resource"] = resource
            html_data = SimpleParser.parse(html_data, mappings)
        return html_data, 200

    @staticmethod
    def return_error(code):
        supported_languages = ["en", "es"]
        lang_cookie = Tools.lang(request)
        if lang_cookie is None:
            lang_cookie = request.accept_languages.best_match(supported_languages)
            if lang_cookie is None:
                lang_cookie = "en"
        return send_from_directory('../content/error_pages', '{}_{}.html'.format(code, lang_cookie)), code
