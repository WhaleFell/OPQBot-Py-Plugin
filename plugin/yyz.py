# /usr/bin/python3
'''
Author: whalefall
Date: 2021-03-06 18:28:13
LastEditTime: 2021-03-06 20:58:43
Description: 每天合成发送抑郁语录 语录在目录的db文件中 现在不是太多 先用txt储存
###############
# 请关爱抑郁症群体....
###############
'''
import os
import sys
import random
import re

path_py = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
path_db = os.path.join(path_py, os.path.join("db", "yyz.txt"))


def getYyz():
    with open(path_db, encoding="utf8") as f:
        res = f.readlines()

        content = random.choice(res).replace(
            " ", "").replace("\r", "").replace("\n", "")
        # print(content)
        try:
            pat = re.compile(r"(.*?)[.](.*)")
            id = pat.findall(content)[0][0]  # id
            con = pat.findall(content)[0][1]  # 内容

            day = random.randint(100, 300)
            end = [
                "——落落的纸船 第%s天" % day,
                "——欣欣的日记 第%s天" % day,
                "——小娴的日记 第%s天" % day,
                "——遇境的纸船 第%s天" % day,
                "——云野的纸船 第%s天" % day,
                "——夏夏的日记 第%s天" % day,
            ]

            # 图片列表
            picUrl = [
                # 网抑云图片
                "https://i.loli.net/2021/03/06/rUyl7m48PiAp3G6.jpg",
                "https://i.loli.net/2021/03/06/dSuMLe3OJoh4RP9.jpg",
                "https://i.loli.net/2021/03/06/Kl3ntscpXoP72Ue.jpg",
                "https://i.loli.net/2021/03/06/1kvEpLbqiS94f57.jpg",
                "https://i.loli.net/2021/03/06/6dUxIATbCcpJ7yt.jpg",
                "https://i.loli.net/2021/03/06/RgtdwBKLEquAP3z.jpg",
                "https://i.loli.net/2021/03/06/yD431VZTEAWXP5j.gif",
                "https://i.loli.net/2021/03/06/cDO1IoqxivmNdsr.jpg",
                "https://i.loli.net/2021/03/06/nOS4smb5xVo6vpt.gif",
            ]

            result = "%s%s" % (con, random.choice(end))
            # print(result)

            return result,random.choice(picUrl)

        except Exception as e:
            print("[YYZ]匹配句子出错 %s" % e)

            return "0","0"


if __name__ == "__main__":
    print(getYyz())


