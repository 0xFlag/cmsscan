import os
import sys
import re
import math
import json
from function import function
from concurrent.futures import ThreadPoolExecutor

def run(url,data):
    try:
        responseArr = function.curl(url, "")
        for n in range(len(data['rules'])):
            if function.checkRule(data['rules'][n], responseArr["header"], responseArr["body"], url):
                print('\033[43;1m--cms是: ' + data["cms_name"] + '--\033[0m')
                for j in range(len(data['version'])):
                    version = function.checkVersion(data['version'][j], responseArr["body"], url)
                    if version:
                        print('\033[43;1m--版本是: ' + version[1] + '--\033[0m')
                        sys.exit("")
                sys.exit("")
    except Exception as e:
        print(e)

def main():
    url = input("请输入URL:")
    if not re.match(r'http[s]?://', url):
        sys.exit("输入的URL格式不正确,URL例子:https://www.example.com")
    
    with ThreadPoolExecutor(max_workers=100) as pool:
        website = function.matchWebsite(url)
        files = os.listdir("./rules")
        for x in range(len(files)):
            data = json.loads(open("./rules/" + files[x]).read().replace("{{http}}", website['scheme']).replace("{{host}}",website['host']))
            pool.submit(run, url,data)

if __name__ == "__main__":
    main()
