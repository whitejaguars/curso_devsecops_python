from application.util.tools import Tools as Tools


class SimpleParser:
    """
    Porque nuestro propio parser ?
    R/ Jinja y otros han tenido vulnerabilidades, para nuestro caso solo se ocupa hacer parseo sencillo
    """
    @staticmethod
    def parse(text, mappings):
        includes = ["HEAD", "HEADER", "HEADER-SOLID", "HEADER-HOME", "FOOTER", "DEPENDENCIES", "SCRIPTS", "SERVICES"]
        response = text
        for key, value in mappings.items():
            response = response.replace("[[{}]]".format(key), value)
        for inc in includes:
            if "[[{}]]".format(inc) in response:
                txt = Tools.load_file("content/static/templates/{}.html".format(inc.lower()))
                txt = SimpleParser.parse(txt, mappings)
                response = response.replace("[[{}]]".format(inc), txt)
        return response

    @staticmethod
    def prepare_mappings(data):
        mappings = {}
        if "lang" in data and "country-code" in data and "country" in data:
            mappings["country-url"] = "{}-{}/{}".format(data["lang"].lower(),
                                                        data["country-code"].lower(),
                                                        str(data["country"]).replace(" ", "-").lower())
        for key, value in data.items():
            if key == "country":
                mappings["country"] = value
                mappings["country-encoded"] = str(data["country"]).replace(" ", "-").lower()
            elif key == "country-code":
                mappings["country-CODE"] = value.upper()
                mappings["country-code"] = value.lower()
            else:
                mappings[key] = value
        return mappings
