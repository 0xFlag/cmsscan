import json
import re
import urllib.request
import hashlib


class function:

    @staticmethod
    def md5(str):
        hl = hashlib.md5()
        hl.update(str.encode("utf-8"))
        return hl.hexdigest()

    @staticmethod
    def checkMd5(condStr, md5Str):
        return function.md5(condStr) == md5Str

    @staticmethod
    def curl(domain, uri):
        url = domain + uri
        try:
            res = urllib.request.urlopen(url)
            header = json.dumps(res.getheaders())
            if function.match("image", header):
                return {"header": header, "body": res.read().hex()}
            else:
                return {"header": header, "body": res.read().decode()}
        except:
            return {"header": "", "body": ""}

    @staticmethod
    def checkVersion(rule, response, domain):
        if rule['key'] == "body":
            return function.match(rule['value'], response)
        elif rule['key'] == "uri":
            newResponse = function.curl(domain, rule['value'])
            return function.match(rule['function_value'], newResponse["body"])
        else:
            return False

    @staticmethod
    def checkRule(rule, header, response, domain):
        if rule['key'] == "body":
            return function.match(rule['value'], response)
        elif rule['key'] == "header":
            return function.match(rule['value'], header)
        else:
            newResponse = function.curl(domain, rule['value'])
            if rule['function'] == "body":
                return function.match(rule['function_value'], newResponse["body"])
            elif rule['function'] == "md5":
                return function.checkMd5(newResponse["body"], rule['function_value'])
            else:
                return False

    @staticmethod
    def match(pattern, value):
        return re.search(pattern, value, re.I)

    @staticmethod
    def matchWebsite(url):
        data = re.match(r'([https]+)://([\w.:]+)', url)
        return {"scheme": data[1], "host": data[2]}
