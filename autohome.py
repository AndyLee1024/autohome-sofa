# -*- coding: utf-8 -*-

__author__ = 'AndyLee'
import requests
import urllib
import re
import random
import json


class AutoHome():
    def __init__(self):
        self.target = 'http://app.api.autohome.com.cn/autov4.6/club' \
                      '/topics-a2-pm1-v4.6.2-b3457-btc-r0-ss0-o2-p1-s50-qf0.html'
        self.post = 'http://club.autohome.com.cn/Detail/AddReply'

        self.headers = {
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'DNT': '1',
            'Referer': 'http://www.autohome.com.cn/',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4'
        }

    def get_forum(self):

        res = {}

        res['data'] = {
            'name': urllib.quote('我的洗发水'),
            'pwd': '7c6a180b36896a0a8c02787eeafb0e4c',
            'isauto': 'true',
            'type': 'json'
        }
        try:

            topics = requests.get(
                'http://app.api.autohome.com.cn/autov4.6/club/topics-a2-pm1-v4.6.2-b442-btc-r0-ss0-o2-p1-s50-qf0.html',
                headers=self.headers).json()
        except:
            pass

        try:
            for i in topics['result']['list']:
                if i['replycounts'] == 0:
                    print '发现新帖子，准备抢~~~'
                    res['info'] = i
                    self.do_reply(res)
                else:
                    print '暂无新帖子'
        except:
            self.get_forum()


    def do_reply(self, res):
        try:

            c_detail = {
                'item1': '沙发,恭喜楼主提车!!!',
                'item2': '[微笑]沙发，恭喜楼主[强]',
                'item3': '楼主好品味，沙发[微笑]',
                'item4': '沙发，落地多少钱啊楼主？',
                'item5': '沙发，恭喜楼主!!!',
                'item6': '车是好车，恭喜楼主啊，沙发',
                'item7': '这个车好大气，看起来很不错，恭喜楼主，沙发!',
                'item8': '沙发,帮楼主顶起来!!',
                'item9': '好，支持楼主，下一辆车就是它了!',
                'item10': '最年轻时尚的车了,恭喜楼主，怒占沙发',
                'item11': '严重关注，顶起来!!沙发［强］',
                'item12': '由于订单较多,很多地方缺货,沙发',
                'item13': '上海大众、奔驰回应：我们错了 马上整改[微笑]',
                'item14': '恭喜楼主啦~~~',
                'item15': '[玫瑰] 楼主淡定啊。。。 沙发',
                'item16': '持续关注中 沙发!!!',
                'item17': '速腾,质造新标准! 领先的德国造车工艺.. 沙发',
                'item18': '荣臻品质，无需炫耀，全新速腾,质造新标准! ',
                'item19': '全新速腾，是中国人的恩赐'
            }
            url = 'http://club.autohome.com.cn/bbs/thread-c-' + str(res['info']['bbsid']) + '-' + str(
                res['info']['topicid']) + '-1.html'

            r = requests.get(url, headers=self.headers).text

            unique_id = re.findall(r'tz.uniquePageId = \"(.+?)\"', r)

            bbs_id = str(res['info']['bbsid'])
            topics_id = str(res['info']['topicid'])
            content = {
                'bbs': 'c',
                'bbsid': res['info']['bbsid'],
                'topicId': res['info']['topicid'],
                'content': c_detail['item' + str(random.randint(1, 16))],

                'uniquepageid': unique_id,
                'domain': 'autohome.com.cn'
            }

            # login_cookie = requests.get('http://account.autohome.com.cn',
            #                             headers=self.headers)
            # res = requests.post('http://account.autohome.com.cn/Login/ValidIndex', headers=self.build_header(res['data']
            #                                                                                                  , bbs_id,
            #                                                                                                  topics_id),
            #                     data=res['data'])
            # cookies = requests.utils.dict_from_cookiejar(res.cookies)

            '''上面是模拟登陆获取cookie的代码 下面是把cookies存到1.txt 防止反复请求 '''

            file = open('1.txt', 'r+')

            a =  file.read()
           # cookies = json.load()

            cookies = eval(a)


            r = requests.post('http://club.autohome.com.cn/Detail/AddReply', cookies=cookies,
                              headers=self.build_header(content, bbs_id, topics_id), data=content)
            print r.text
            print '抢劫完毕'

        except Exception, e:
            print  e.message
            pass


    def build_header(self, content, bbs_id, topic_id):
        length = len(content)
        header = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://club.autohome.com.cn/bbs/thread-c-' + bbs_id + '-' + topic_id + '-2.html',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36',
            'Accept-Encoding': 'gzip,deflate', 'Connection': 'keep-alive', 'Content-Length': length}

        return header


if __name__ == '__main__':
    while True:
        r = AutoHome()
        r.get_forum()


