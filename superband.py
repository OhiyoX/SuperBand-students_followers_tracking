from bs4 import BeautifulSoup
import os
import json
import re
import time

import function as fuck


class Superband():
    def __init__(self):
        self.stu_profiles = []
        if not os.path.exists('res/students.json'):
            self.get_students()

        with open('res/students.json', 'rb') as f:
            self.stu_list = json.load(f)

    # 获取粉丝数

    def get_followers(self):
        stu_f_path = 'res/stu_followers.json'
        # 建立快照
        datatime = fuck.get_time()
        stus_detail = []
        try:
            with open(stu_f_path, encoding='UTF-8') as f:
                stu_l = json.load(f)
        except:
            stu_l = []
            for stu_ in self.stu_list:
                a_stu = {}
                a_stu['id'] = stu_['id']
                a_stu['alias'] = stu_['alias']
                a_stu['uid'] = stu_['uid']
                a_stu['change'] = []
                stu_l.append(a_stu)

        for stu in self.stu_list:
            flagg = False
            while flagg is False: # 解决api可能出错的情况
                try:
                    detail = self.get_detail(stu['uid'])
                    detail_timestamp = time.time()
                    # 保存datail，相当于一个快照
                    temp_ = {'id': stu['id'],
                             'uid': stu['uid'],
                             'time': detail_timestamp,
                             'alias': stu['alias'],
                             'detail': detail['data']['userInfo']}
                    flagg = True
                except:
                    time.sleep(5)

            stus_detail.append(temp_)

            # 保存时间点上的fans
            fans = {'num': len(stu_l[stu['id']]['change']),
                    'time': detail_timestamp,
                    'status':detail['data']['userInfo']['statuses_count'],
                    'following':detail['data']['userInfo']['follow_count'],
                    'fan_counts': detail['data']['userInfo']['followers_count']}
            stu_l[stu['id']]['change'].append(fans)
            print(stu['alias'] + ', has ' + str(detail['data']['userInfo']['followers_count'])
                  + ' followers')

        date = time.time()

        print('starting save the data')
        if not os.path.exists('res/backup'):
            os.mkdir('res/backup')
        with open('res/backup/' + datatime + '_detail.json', 'w', encoding='UTF-8') as f_detail:
            json.dump(stus_detail, f_detail, ensure_ascii=False)

        with open(stu_f_path, 'w', encoding='UTF-8') as f_:
            json.dump(stu_l, f_, ensure_ascii=False)

    # 获取学生列表
    def get_students(self):

        stu_list = []
        prefix = "https://s.weibo.com/user?q=%E3%80%8A%E6%98%8E%E6%97%A5%E4%B9%8B%E5%AD%90" \
                 "%E4%B9%90%E5%9B%A2%E5%AD%A3%E3%80%8B%E5%AD%A6%E5%91%98&Refer=weibo_user&page="
        id_x = 0
        for n in range(1, 4):
            url = prefix + str(n)
            response = fuck.get_page(url)
            content = response.text
            soup = BeautifulSoup(content, "lxml")
            user_cards = soup.find_all(name='div', class_='card card-user-b s-pg16 s-brt1')

            for user_card in user_cards:
                u_ = {'id': id_x}
                id_x += 1

                # ref
                alias = user_card.find(name='a', class_='name')
                u_['ref'] = 'https:' + alias['href']

                # uid
                uid_check = re.search('[0-9]+', alias['href'])
                if uid_check is None:
                    uid = self.get_uid(u_['ref'])
                    u_['uid'] = uid
                else:
                    u_['uid'] = uid_check.group()
                time.sleep(1)
                detail = self.get_detail(u_['uid'])
                print(detail['data']['userInfo']['screen_name'] + ' is ok.')
                u_['alias'] = detail['data']['userInfo']['screen_name']
                u_['detail'] = detail

                stu_list.append(u_)

        path = 'res/' + 'students' + '.json'
        if not os.path.exists('res'):
            os.mkdir('res')
        with open(path, 'w', encoding="UTF-8") as f:
            json.dump(stu_list, f, ensure_ascii=False)

        print("列表保存成功")

    def get_detail(self, uid):
        """dict 形式"""
        prefix = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='
        url = prefix + uid
        content = fuck.get_page(url)
        return content.json()

    def get_uid(self, ref):
        # 当出现自定义域名时使用这个方法获取原始id
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OP'
                          'D3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chr'
                          'ome/84.0.4147.89 Mobile Safari/537.36 Edg/84.0.522.48'
        }
        content = fuck.get_page(ref, headers=headers)
        uid = re.search('[0-9]+', content.url)
        return uid.group()
