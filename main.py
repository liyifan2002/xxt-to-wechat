import config
import urllib.request,re
get_url="http://jxlx.xxt.cn/jxlx/teacher/msgReceive.action?receiveNum=1"

xxt_head = {"Cookie" :config.xxt_cookies}
xxt_req = urllib.request.Request(get_url, headers=xxt_head)
xxt_res = urllib.request.urlopen(xxt_req)
msg = xxt_res.read().decode("gbk")
print(re.findall("<span class=\"msgContent\">(.*)</span>",msg))
