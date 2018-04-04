import json
# 在其他.py文件中：
# import loadJson
# a = loadJson.loadTestIP

def loadTestIP():
    f = open("config.json", encoding='utf-8')
    setting = json.load(f)
    return setting["test"]["ip"]

def loadTestPort():
    f = open("config.json", encoding='utf-8')
    setting = json.load(f)
    return setting["test"]["port"]

def loadTest():
    f = open("config.json", encoding='utf-8')
    setting = json.load(f)
    return setting["test"]["ip"],setting["test"]["port"]

def loadLocalHostIP():
    f = open("config.json", encoding='utf-8')
    setting = json.load(f)
    return setting["srcIP"]

def loadDstIP():
    f = open("config.json", encoding='utf-8')
    setting = json.load(f)
    return setting["dstIP"]

def loadPort():
    f = open("config.json", encoding='utf-8')
    setting = json.load(f)
    return setting["port"]

def loadloss():
    f = open("config.json", encoding='utf-8')
    setting = json.load(f)
    return setting["loss"]

def loadDevice():
    f = open("config.json", encoding='utf-8')
    setting = json.load(f)
    return setting["device"]

def loadAll():
    f = open("config.json", encoding='utf-8')
    setting = json.load(f)
    return setting["test"]["ip"],setting["test"]["port"],setting["port"],setting["loss"],setting["device"]
