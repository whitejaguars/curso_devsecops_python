import re
from pathlib import Path


class InputValidation:
    @staticmethod
    def no_xss(txt):
        attacks = ['<', '>', ' alert(', ');', '//']
        for attack in attacks:
            if attack in txt.lower():
                return False
        return True

    @staticmethod
    def is_valid_path(txt, allowed_ext=None):
        """Validates Safe values allowed for Linux paths.
        """
        if txt != "" and txt is not None and re.match(r'^[a-zA-Z0-9_\.\-\/\s]+$', txt):
            if isinstance(allowed_ext, list) and txt != "":
                extension = txt.rsplit('.', 1)[1].lower()
                if extension not in allowed_ext:
                    return False
            attack = '../'
            if attack not in txt:
                return True
        return False

    @staticmethod
    def is_valid_file(txt, allowed_ext=None):
        """Validates Safe values allowed for Linux paths.
        """
        if txt != "" and txt is not None and "." in txt and re.match(r'^[a-zA-Z0-9_\.\-\/\s]+$', txt):
            if isinstance(allowed_ext, list) and txt != "":
                extension = txt.rsplit('.', 1)[1].lower()
                if extension not in allowed_ext:
                    return False
            attack = '../'
            if attack not in txt:
                return Path(txt).is_file()
        return False

    @staticmethod
    def is_valid_file_landing(txt, allowed_ext=None):
        """Validates Safe values allowed for Linux paths.
        """
        if txt != "" and txt is not None and "." in txt and re.match(r'^[a-zA-Z0-9_\.\-\/\s]+$', txt):
            if isinstance(allowed_ext, list) and txt != "":
                extension = txt.rsplit('.', 1)[1].lower()
                if extension not in allowed_ext:
                    return False
            attack = '../'
            if attack not in txt:
                #return Path(txt).is_file()
                return True
        return False

    @staticmethod
    def is_valid_name(txt):
        """Validates Safe values allowed for Names.
        """
        if txt != "" and txt is not None and re.match(r'^[a-zA-Z0-9_\-\s]+$', txt):
            attack = '../'
            if attack not in txt:
                return True
        return False

    @staticmethod
    def is_valid_description(txt):
        """Validates Safe values allowed for Descriptions.
        """
        if txt != "" and txt is not None and re.match(r'^[a-zA-Z0-9_\.\-\(\)\[\]\{\}\:\;\s\n\,\'\&\@\#\$\%\*]+$', txt):
            attack = '../'
            if attack not in txt:
                return True
        return False


class NetworkValidations:
    @staticmethod
    def is_valid_ip(ip):
        """Validates IP addresses.
        """
        return NetworkValidations.is_valid_ipv4(ip) or NetworkValidations.is_valid_ipv6(ip)

    @staticmethod
    def is_valid_ipv6(ip):
        """Validates IPv6 addresses.
        """
        pattern = re.compile(r"""
            ^
            ^
            \s*                         # Leading whitespace
            (?!.*::.*::)                # Only a single whildcard allowed
            (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
            (?:                         # Repeat 6 times:
                [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
                (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
            ){6}                        #
            (?:                         # Either
                [0-9a-f]{0,4}           #   Another group
                (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
                [0-9a-f]{0,4}           #   Last group
                (?: (?<=::)             #   Colon iff preceeded by exacly one colon
                 |  (?<!:)              #
                 |  (?<=:) (?<!::) :    #
                 )                      # OR
             |                          #   A v4 address with NO leading zeros 
                (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
                (?: \.
                    (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
                ){3}
            )
            \s*                         # Trailing whitespace
            $
        """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
        return pattern.match(ip) is not None

    @staticmethod
    def is_valid_ipv4(ip):
        """Validates IPv4 addresses.
        """
        pattern = re.compile(r"""
            ^
            (?:
              # Dotted variants:
              (?:
                # Decimal 1-255 (no leading 0's)
                [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
              |
                0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
              |
                0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
              )
              (?:                  # Repeat 0-3 times, separated by a dot
                \.
                (?:
                  [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
                |
                  0x0*[0-9a-f]{1,2}
                |
                  0+[1-3]?[0-7]{0,2}
                )
              ){0,3}
            |
              0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
            |
              0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
            |
              # Decimal notation, 1-4294967295:
              429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
              42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
              4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
            )
            $
        """, re.VERBOSE | re.IGNORECASE)
        return pattern.match(ip) is not None

    @staticmethod
    def is_valid_domain(txt):
        """Validates Domain Names.
        """
        domain_labels = txt.lower().split(".")
        for domain in domain_labels:
            if not re.match(r'^[a-z0-9\-]+$', domain) or len(domain) < 2 or len(domain) > 63:
                return False
        return True

    @staticmethod
    def is_valid_port(port):
        try:
            iport = int(port)
            if iport > 0 and iport < 65535:
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def is_valid_url(url):
        t = NetworkValidations.parse_url(url)
        if t is None:
            return False
        else:
            return True

    @staticmethod
    def parse_url(url):
        res = {'protocol': '', 'port': 0, 'domain': '', 'location': '/', 'querystring': '', 'service': ''}
        if len(url) >= 2048:
            return None
        if url[:4] == 'http':
            # Seems to be a URL
            if url[:7] == 'http://':
                res['domain'] = url[7:]
                res['protocol'] = 'http'
                res['service'] = 'http'
            elif url[:8] == 'https://':
                res['domain'] = url[8:]
                res['protocol'] = 'https'
                res['service'] = 'https'
            if '/' in res['domain']:
                t = res['domain'].split('/', 1)
                res['location'] = t[1]
                res['domain'] = t[0]
            if '?' in res['location']:
                t = res['location'].split('?', 1)
                res['querystring'] = t[1]
                res['location'] = t[0]
            if ':' in res['domain']:
                t = res['domain'].split(':')
                res['port'] = t[1]
                if not NetworkValidations.is_valid_port(res['port']):
                    return None
                res['domain'] = t[0]
            if res['domain'] == '' or not (NetworkValidations.is_valid_ip(res['domain']) or
                                           NetworkValidations.is_valid_domain(res['domain'])):
                return None
            else:
                return res
        else:
            res = None
        return res
