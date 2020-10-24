import json
import re
import urllib.request
import hashlib,requests


class function:

    @staticmethod
    def md5(str):
        hl = hashlib.md5()
        hl.update(str)
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
        headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0'
}

        if rule['key'] == "body":
            return function.match(rule['value'], response)
        elif rule['key'] == "header":
            return function.match(rule['value'], header)
        else:
            newResponse = function.curl(domain, rule['value'])
            if rule['function'] == "body":
                return function.match(rule['function_value'], newResponse["body"])
            elif rule['function'] == "md5":
                url = domain + rule['value']
                r = requests.get(url=url, headers=headers,verify=False)
                return function.checkMd5(r.content, rule['function_value'])
            else:
                return False

    @staticmethod
    def match(pattern, value):
        return re.search(pattern, value, re.I)

    @staticmethod
    def matchWebsite(url):
        data = re.match(r'([https]+)://([\w.:]+)', url)
        return {"scheme": data[1], "host": data[2]}
