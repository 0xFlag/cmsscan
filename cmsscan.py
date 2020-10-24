import os, sys
import re
import threading
import math
import json
from function import function

# 定义线程数
threadCount = 10

url = input("请输入URL:")

if not re.match(r'http[s]?://', url):
    sys.exit("输入的URL格式不正确,URL例子:https://www.example.com")

# 请求URL获取主页数据
try:
    responseArr = function.curl(url, "")
except:
    sys.exit("获取不到网页数据")

# 解析URL scheme host
website = function.matchWebsite(url)

files = os.listdir("./rules")

# 判断数组长度,因为存储的是一个文件一个匹配规则,有多个文件 需要除以线程总数,让每个线程处理的文件数是一样的
fileArrLength = math.ceil(len(files) / threadCount)
tempNum = 0
tempArr = []
splitFileArr = []
for i in range(len(files)):
    tempNum += 1
    tempArr.append(files[i])
    if tempNum == fileArrLength or i == len(files) - 1:
        splitFileArr.append(tempArr)
        tempNum = 0
        tempArr = []


def run(fileList):
    for x in range(len(fileList)):
        # 加载对应的文件 获取匹配规则,把匹配规则里面{{http}} {{host}}为对应的协议和域名
        data = json.loads(
            open("./rules/" + fileList[x]).read().replace("{{http}}", website['scheme']).replace("{{host}}",
                                                                                                   website['host']))
        for n in range(len(data['rules'])):
            if function.checkRule(data['rules'][n], responseArr["header"], responseArr["body"], url):
                print('\033[43;1m--cms是: ' + data["cms_name"] + '--\033[0m')
                # 匹配对应的版本
                for j in range(len(data['version'])):
                    version = function.checkVersion(data['version'][j], responseArr["body"], url)
                    if version:
                        print('\033[43;1m--版本是: ' + version[1] + '--\033[0m')
                        sys.exit("")
                sys.exit("")


for i in range(threadCount):
    t = threading.Thread(target=run, args=(splitFileArr[i],))
    t.start()
