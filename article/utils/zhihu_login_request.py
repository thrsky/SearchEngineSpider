# -*- coding: utf-8 -*-
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re

session = requests.session()
session.cookies=cookielib.LWPCookieJar(filename="zhihu_cookies.txt")
try:
    session.cookies.load(ingore_discard=True)
except:
    print("cookie未能加载")


agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
header={
    "POST":"www.zhihu.com",
    "referer":"https://www.zhihu.com",
    'User-Agent':agent
}


def is_login():
    #通过个人中心 返回状态码判断是否为登录状态
    inbox_url="https://www.zhihu.com/inbox"
    response = session.get(inbox_url,headers=header,allow_redirects=False)
    if response.status_code!=200:
        print("NO OK")
        return False
    else:
        print("OK")
        return True


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html",'wb') as f:
        f.write(response.txt.encode("utf8"))
    print("ok")

def get_captcha():
    import time
    t=str(int(time.time()*1000))
    captcha_url="https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t=session.get(captcha_url,headers=header)
    with open("captcha.jpg",'wb') as f:
        f.write(t.content)
        f.close()

    from PIL import Image
    try:
        im=Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        pass

    captcha = input("输入验证码\n")
    return captcha

def get_xsrf():
    #获取xsrf code
    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""


def zhihu_login(account,passwd):
    #知乎登录 用request
    if re.match("^1\d{10}",account):
        print("手机号登录")
        post_url="https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf":get_xsrf(),
            "phone_num":account,
            "password":passwd,
            "captcha":get_captcha()
        }
    else:
        if "@" in account:
            print("邮箱登录")
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": passwd,
                "captcha":get_captcha()
            }

    response_text = session.post(post_url, data=post_data, headers=header)
    # 保存cookie
    session.cookies.save()
#
# is_login()
zhihu_login("18858903314","19960411kang")
is_login()

