# /usr/bin/python3
'''
Author: whalefall
Date: 2021-03-05 22:29:50
LastEditTime: 2021-03-06 21:30:27
Description: OPQBot定时执行主程序
'''
import configparser
import os
import sys
import requests
import json
import datetime
import random
import time
from plugin import (
    yyz
)

# 初始化配置文件


def getConfig():
    config = configparser.ConfigParser()
    path_py = os.path.split(os.path.realpath(sys.argv[0]))[0]
    print("脚本目录:", path_py)
    path_config = os.path.join(path_py, "config.ini")
    if os.path.exists(path_config):
        config.read(path_config, encoding="utf-8")
        # 获取[OPQBot]配置
        host = config.get("OPQBot", "host")
        bot_qq = config.get("OPQBot", "bot_qq")
        print('''
#################config.ini#####################
#     请核对配置信息!首次试用请修改config.ini
################################################
Host:%s
bot_qq:%s
################################################
        ''' % (host, bot_qq)
              )
    else:
        config.add_section("OPQBot")
        config.set("OPQBot", "host", "http://127.0.0.1:8888")
        config.set("OPQBot", "bot_qq", "2734184475")
        print("首次使用 请修改config.ini内容")
        config.write(open(path_config, "w"))

    return host, bot_qq

# OPQ API部分 试用SendMsgV2版本 不完善


class OPQBot():
    def __init__(self, host, bot_qq):
        self.host = host
        self.bot_qq = int(bot_qq)
        self.api = "%s/v1/LuaApiCaller" % (host)

        self.params = {
            'qq': self.bot_qq,  # 机器人QQ号
            'funcname': "SendMsgV2",  # 调用方法类型
        }

        self.header = {
            "Accept": "application/json",
        }

    def postFun(self, data):

        try:
            resp = requests.post(self.api, params=self.params,
                                 data=json.dumps(data), headers=self.header)
            # print(resp)
            if resp.json()["Ret"] != 0:
                print("发送有异常 接口响应:{}".format(resp.text))
                return "101"
            else:
                print("发送成功~")
                return "200"
        except Exception as e:
            print("发送出现未知失败 错误:{}".format(e))
            return "0"

    def sendGoup(self, GoupID, ty, Content):
        if ty == "txt":
            data = {
                "ToUserUid": int(GoupID),
                "SendToType": 2,  # 1 为好友消息 2发送群消息  3发送私聊消息
                "SendMsgType": "TextMsg",
                "Content": Content
            }
        if ty == "pic":
            {
                "ToUserUid": 123456789,
                "SendToType": 2,
                "SendMsgType": "PicMsg",
                "PicUrl": "http://gchat.qpic.cn/gchatpic_new/304980169/636617867-2534335053-8E6B948D1E7A4F96DB5F9C4A6050FB02/0?vuin=123456789&term=255&pictype=0"
            }

        # 调用类的请求方法
        self.postFun(data)

    def sendFriendTxt(self, FriendID, Content):
        data = {
            "ToUserUid": int(FriendID),
            "SendToType": 1,  # 1 为好友消息 2发送群消息  3发送私聊消息
            "SendMsgType": "TextMsg",
            "Content": Content
        }

        # 调用类的请求方法
        self.postFun(data)

    # 发送群图片 Content为可选参数
    def sendGoupPic(self, GoupID, PicUrl, Content=""):
        data = {
            "ToUserUid": int(GoupID),
            "SendToType": 2,
            "SendMsgType": "PicMsg",
            "PicUrl": PicUrl,
            "Content": "[PICFLAG]"+Content
        }
        self.postFun(data)

    # 获取bot加入的群列表
    def getGroupList(self):
        param = {
            'qq': self.bot_qq,  # bot的QQ
            'funcname': 'GetGroupList'
        }
        datafrom = {
            "NextToken": ""
        }

        try:
            resp = requests.post(url=self.api, params=param,
                                 data=json.dumps(datafrom))
            TroopList = resp.json()["TroopList"]
            QQgroupList = []
            QQgroupList_all = []
            for QQgroup in TroopList:
                # print(QQgroup)
                groupID = QQgroup['GroupId']
                groupName = QQgroup['GroupName']
                group = {"groupID": groupID, "groupName": groupName}
                QQgroupList.append(groupID)
                QQgroupList_all.append(group)
            print("获取到的QQ群列表:", QQgroupList)
            print("详细信息:", QQgroupList_all)
            return QQgroupList
        except Exception as e:
            print("请求群列表出现未知失败 错误:{} 响应:{}".format(e, resp.status_code))
            return "0"

        '''       
        # 尝试通过旧版API 发送base64图片 (失败)
        # def sendGoupPic(self, groupID, base64):
        #     params = {
        #         'qq': self.bot_qq,  # bot的QQ
        #         'funcname': 'SendMsg'
        #     }
        #     data = {
        #         "toUser": groupID,  # 发到哪个QQ或者群号
        #         "sendToType": 2,  # 自己选择对应会话的数值
        #         "sendMsgType": "PicMsg",
        #         "content": "test",  # 文字消息
        #         "groupid": groupID,  # 群号
        #         "atUser": 0,
        #         "picUrl": "",  # 图片的url,iotqq会自动加Referer
        #         "picBase64Buf": base64,  # base64后的图片
        #         "fileMd5": "",  # 图片MD5,普通图片MD5貌似会过期,表情貌似不会
        #         "flashPic": "false"  # 闪照:仅群聊可用
        #     }

        #     resp = requests.post(self.api, params=params,
        #                          data=json.dumps(data), headers=self.header)

        #     print(resp.json())
        '''


# 主运行
if __name__ == "__main__":
    host, bot_qq = getConfig()
    bot = OPQBot(host, bot_qq)

    now = datetime.datetime.now()
    hour = now.strftime("%H")

    # 咕咕 临时用网易云
    '''
    # 如果在下面的时段
    if hour in ["00"]:
        pass
    '''
    
    minute = random.randint(1, 10)
    print("[YYZ]0点到 网抑云任务启动 随机等待%s分" % (minute))
    time.sleep(minute*60)
    GroupList = bot.getGroupList()
    # print("获取到的群列表:%s" % (GroupList))
    Group_Blask_List = ["173225643","512454918","930325107","1016977635","1142184904"]  # 不发送的群
    for groupID in GroupList:

        if str(groupID) in Group_Blask_List:
            continue

        con, picUrl = yyz.getYyz()
        bot.sendGoupPic(groupID, picUrl,con)
        time.sleep(5)
