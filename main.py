import config
import hashlib,base64,json,re
import urllib.request,http.cookiejar
import wechat_sdk

def getOpener():
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    return opener

def b64en (data):
    return base64.b64encode(data.encode("utf-8")).decode()

def sha1withSalt (data,salt):
    result=hashlib.sha1(data.encode()).hexdigest().upper()+salt
    result=hashlib.sha1(result.encode()).hexdigest().upper()
    return result

username=b64en(config.xxt_username)
logpre_url = "http://login.xxt.cn/login/ajax/loginpre.do?&username="+username
login_url = "http://login.xxt.cn/login/ajax/login.do?entry=xxt_web&clientVersion=V0.5.0&cryptType=A&callbackFn=XXTSSO.showResult"
get_url = "http://jxlx.xxt.cn/jxlx/teacher/msgReceive.action?receiveNum=0"
wx = wechat_sdk.WeChatEnterprise()
opener = getOpener()
logpre_req = opener.open(logpre_url)
logpre_res = logpre_req.read().decode()
jsonData = json.loads(logpre_res)
key = jsonData["key"]
password = sha1withSalt(config.xxt_password,key)
login_url += "&username=" + username + "&password="+password+"&key=" + key
login_req = opener.open(login_url)
received_res = opener.open(get_url)
received = received_res.read().decode("gbk")
msgs = re.findall("<span class=\"msgContent\">(.*?)</span>",received,re.S)
msgs.reverse()
fl = open('history.txt', 'r+')
history = fl.read()
history = history.split("|\n")[:-1]
new = set(msgs)^set(history)
for msg in new:
	wx.send_msg_to_user(msg,touser=["YifanLi"])
	fl.write(msg)
	fl.write("|\n")
