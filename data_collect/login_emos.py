import requests
import hashlib
import time
import base64
import os


# base_url = 'http://10.46.0.1/'
base_url = 'http://10.53.160.65/'

def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


def login_check(user,pwd):
    userenc = base64.b64encode(user.encode('utf-8'))
    userenc = str(userenc, 'utf-8')
    pwdenc = base64.b64encode(pwd.encode('utf-8'))
    pwdenc = str(pwdenc, 'utf-8')
    url = base_url + 'was/portal_ldap/portalLogin/loginFromPortal?username_ad=%s&password_ad=%s&loginEntry=JZQX'%(userenc,pwdenc)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
    r = requests.get(url, headers=headers).json()
    return r['success']


def login_pp(user,pwd):
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Host': base_url[7:-1]}
    url = base_url + 'pkmslogin.form'
    pwd_md5 = md5(pwd)
    data = {}
    data['username'] = user
    data['password'] = pwd_md5
    data['ERROR'] = ''
    data['login-form-type'] = 'pwd'
    session.post(url, data=data, headers=headers, allow_redirects=True)
    session.cookies['login_user'] = user
    return session


def logout_pp(session,user):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Host': '10.53.160.65'}
    millis = int(round(time.time()*1000))
    url = 'http://10.53.160.65/was/portal_report/report/userLogout.do?timestamp=%s' % str(millis)
    #print(url)
    data = {}
    data['userid'] = user
    session.post(url, data=data, headers=headers)


def dir_pre_check():
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('result'):
        os.mkdir('result')


if __name__ == '__main__':
    login_pp('huangningcheng','Asdf.1908')