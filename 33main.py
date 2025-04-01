import json
import requests
import time
import hashlib
from log import log

def getParams(_time):  # 获取params
    params = {
        "_platform": "web",
        "_versioin": "0.2.5",
        "_ts": _time
    }
    return params


def getX_Signature(_time):  # 获取X-Signature
    tmp = "_platform=web,_ts=" + str(_time) + ",_versioin=0.2.5,"
    # tmp = "_platform=web,_ts=" + str(1688550004080) + ",_versioin=0.2.5,"
    x_str = hashlib.md5(tmp.encode('UTF-8')).hexdigest()
    # print(x_str)
    return x_str


def login():  # 登录
    userInfo = {
        "email": "你的邮箱",
        "password": "你的密码"
    }
    _time = int(round(time.time() * 1000) - 9999)
    params = getParams(_time)
    url = "https://ssv-api.agilestudio.cn/api/auth/email-login"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "X-Signature": getX_Signature(_time)
    }
    res = requests.post(url, params=params, json=userInfo, headers=header)
    token = json.loads(res.text)["data"]["token"]
    return token


def getIntegral(token):  # 获取当前积分
    _time = int(round(time.time() * 1000) - 9999)
    params = getParams(_time)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "X-Signature": getX_Signature(_time),
        "X-Token": token
    }
    res = requests.get(url="https://ssv-api.agilestudio.cn/api/user/my-info", params=params, headers=header)
    integral = json.loads(res.text)["data"]["integral"]
    return integral


def dailyCheck(token):
    _time = int(round(time.time() * 1000) - 9999)
    params = getParams(_time)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "X-Signature": getX_Signature(_time),
        "X-Token": token
    }
    res = requests.post(url="https://ssv-api.agilestudio.cn/api/integral/do-daily-check", params=params, headers=header)
    # print(json.loads(res.text)["data"])
    return json.loads(res.text)["data"]


def main():
    token = login()
    integral = getIntegral(token)
    # print("当前积分为:"+str(integral))
    dailyCheck(token)
    nowIntegral = getIntegral(token)
    print("签到前积分："+str(integral)+">>>>>>>>>>"+"签到后积分："+str(nowIntegral))
    if integral != nowIntegral:
        log.add_Log("33台词网签到成功")
        print("签到成功，当前积分为：" + str(integral) + "==>" + str(nowIntegral))
    if integral == nowIntegral:
        log.add_Log("33台词网重复签到")
        print("请勿重复签到，当前积分为:"+str(integral))


if __name__ == '__main__':
    main()
