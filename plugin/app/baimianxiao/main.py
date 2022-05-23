# -*- encoding=utf8 -*-


import numbers
import OlivOS
import baimianxiao

import os
import time
import json
import requests
import random
import re


class Event(object):
    def init(plugin_event, Proc):
        if not os.path.exists("plugin/data/baimianxiao"):
            os.mkdir("plugin/data/baimianxiao")
        if not os.path.exists("plugin/data/baimianxiao/user_data.json"):
            data = {
                "2432115441": {
                    "timeLatest": 20200101,
                    "hcyNumber": 100000,
                    "experiencePoint": 200,
                    "level": 10000
                }
            }
            write_json(data, r"plugin/data/baimianxiao/user_data.json")
        if not os.path.exists("plugin/data/baimianxiao/conf.json"):
            data = {
                "masterList": [
                    2432115441
                ]
            }
            write_json(data, r"plugin/data/baimianxiao/conf.json")
        if not os.path.exists("plugin/data/baimianxiao/msg_reply.json"):
            data = {
                "咕咕咕": [
                    "咕咕咕??"
                ],
                "早安": [
                    "哦哈哟，准备好迎接新的一天了吗？"
                ]
            }
            write_json(data, r"plugin/data/baimianxiao/conf.json")
        if not os.path.exists("plugin/data/baimianxiao/msg_str.json"):
            data = {}
            write_json(data, r"plugin/data/baimianxiao/msg_str.json")

    def init_after(plugin_event, Proc):
        pass

    def private_message(plugin_event, Proc):
        pass

    def group_message(plugin_event, Proc):
        message = plugin_event.data.message
        if(message == "签到"):
            sign(plugin_event, Proc)
        elif(message == "查询档案"):
            private_info(plugin_event, Proc)
        elif(message == "test"):
            plugin_event.reply("开始转移")
        elif(message == "方舟十连" or message == "寻访十次"):
            arknights_draw(plugin_event, Proc)
        elif():
            msg_reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
        loginInfo = plugin_event.get_login_info()
        if(plugin_event.data.target_id == loginInfo["data"]["id"]):
            plugin_event.reply("工口发生！")
        plugin_event.set_block()
        pass

    def save(plugin_event, Proc):
        pass

# 签到函数


def sign(plugin_event, Proc):
    userName = plugin_event.data.sender["name"]
    userID = str(plugin_event.data.sender["user_id"])
    timeNow = int(time.strftime("%Y%m%d"))
    userDataList = get_json(r"plugin\data\baimianxiao\user_data.json")
    if(userID in userDataList.keys()):
        userData = userDataList[userID]
        if(timeNow == userData["timeLatest"]):
            plugin_event.reply(
                "————————————\n▼ Warning:请勿重复签到! \n————————————")
        else:
            hcyAdd = random.randint(30, 100)*100
            userData["timeLatest"] = timeNow
            userData["hcyNumber"] = userData["hcyNumber"]+hcyAdd
            if(str(plugin_event.data.group_id) == "884512210"):
                plugin_event.reply("————————————\n▼ 签到成功！\n│ 特别记录点：鹿岛重工\n┣———————————\n│ Dr." + userName +
                                   "\n│ 获得合成玉："+str(hcyAdd)+"\n▲ 现有合成玉："+str(userData["hcyNumber"])+"\n————————————")
                userDataList[userID] = userData
                write_json(userDataList, r"plugin\data\baimianxiao\user_data.json")
                return True
            plugin_event.reply("————————————\n▼ 签到成功！\n│ Sign in successfully!\n┣———————————\n│ Dr." +
                               userName+"\n│ 获得合成玉："+str(hcyAdd)+"\n▲ 现有合成玉："+str(userData["hcyNumber"])+"\n————————————")

    else:
        userData = {
            "timeLatest": timeNow,
            "hcyNumber": 100000,
            "experiencePoint": 10,
            "level": 1
        }
        plugin_event.reply(
            "————————————\n▼ 检测到新的使用个体\n│ 权限已注册\n│ 获得初始合成玉1w\n▲ 你好，Dr."+userName+"\n————————————")

    userDataList[userID] = userData
    write_json(userDataList, r"plugin\data\baimianxiao\user_data.json")

# 查询个人资料


def private_info(plugin_event, Proc):
    userName = plugin_event.data.sender["name"]
    userID = str(plugin_event.data.sender["user_id"])
    userDataList = get_json(r"plugin\data\baimianxiao\user_data.json")
    if(not userID in userDataList.keys()):
        plugin_event.reply(
            "————————————\n▼ 正在检索数据库……\n│ 无个人存档记录！ \n│ 请使用签到指令初始化\n————————————")
        return True
    userData = userDataList[userID]
    plugin_event.reply("————————————\n▼ 正在检索数据库……\n│ Success!\n┣———————————\n│ Dr." +
                       userName+"\n▲ 现有合成玉："+str(userData["hcyNumber"])+"\n————————————")
    return True


def arknights_draw(plugin_event, Proc):
    userName = plugin_event.data.sender["name"]
    userID = str(plugin_event.data.sender["user_id"])
    userDataList = get_json(r"plugin\data\baimianxiao\user_data.json")
    if(not userID in userDataList.keys()):
        plugin_event.reply(
            "————————————\n▼ 正在检索数据库……\n│ Warning:无个人存档记录 \n│ 请使用签到指令初始化\n————————————")
        return True
    userData = userDataList[userID]
    if(userData["hcyNumber"] >= 6000):
        userData["hcyNumber"] = userData["hcyNumber"]-6000
        plugin_event.reply("————————————\n▼ 开始模拟寻访\n│ 剩余合成玉：" + str(userData["hcyNumber"])+"\n————————————"+"[CQ:image,file=http://api.baimianxiao.cn/arknights/arknightsdraw/main.php?]")
        write_json(userDataList, r"plugin\data\baimianxiao\user_data.json")
        return True
    else:
        plugin_event.reply("————————————\n▼ Warning:合成玉不足！\n│ 现有合成玉:" +
                           str(userData["hcyNumber"])+"\n————————————")
        return True


# 写json文件
def write_json(data, path):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            return True
    except:
        return False

# 读json文件


def get_json(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            file = file.read()
            return json.loads(file)

    except:
        return False


frepList = {
    2432115441: {
        "times": 4,
        "timeSlot": 10800
    }
}

def msg_reply(plugin_event, Proc):
    replyList= get_json(r"plugin/data/baimianxiao/conf.json")
    if(not plugin_event.data.message in replyList.keys()):
        return False
    
    return True

def monitor_frep(plugin_event, Proc):
    global frepList
    timeSlot = int(time.strftime("1%H%M"))
