import config
import hashlib,base64,json,re
import urllib.request,http.cookiejar
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
logpre_url="http://login.xxt.cn/login/ajax/loginpre.do?&username="+username
login_url="http://login.xxt.cn/login/ajax/login.do?entry=xxt_web&clientVersion=V0.5.0&cryptType=A&callbackFn=XXTSSO.showResult"
get_url="http://jxlx.xxt.cn/jxlx/teacher/msgReceive.action?receiveNum=1"
opener = getOpener()
logpre_req=opener.open(logpre_url)
logpre_res=logpre_req.read().decode()
jsonData = json.loads(logpre_res)
key=jsonData["key"]
password=sha1withSalt(config.xxt_password,key)
login_url+="&username="+username+"&password="+password+"&key="+key
login_req=opener.open(login_url)
xxt_res = opener.open(get_url)
msg = xxt_res.read().decode("gbk")
print(re.findall("<span class=\"msgContent\">(.*)</span>",msg))
