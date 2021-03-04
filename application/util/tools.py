

class Tools:
    @staticmethod
    def hostname(request):
        hostnames = ["www.zirkul.com"]
        if request.headers['host'] in hostnames:
            return request.headers['host']
        else:
            return None

    @staticmethod
    def remote_ip(request):
        remote_ip = request.environ.get('HTTP_X_FORWARDED_FOR')
        if remote_ip is None:
            remote_ip = request.remote_addr
        return remote_ip

    @staticmethod
    def lang(request):
        supported = ["es", "en"]
        current_lang = request.cookies.get('lang')
        if current_lang is None:
            return None
        elif current_lang in supported:
            return current_lang
        else:
            return None

    @staticmethod
    def load_file(file_path):
        with open(file_path, 'r', encoding="utf-8") as the_file:
            return the_file.read()
