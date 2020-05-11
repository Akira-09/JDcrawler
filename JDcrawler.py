# -*- coding: utf-8 -*-
# 开发团队   ：漫游边界
# 开发人员   ：Akira
# 开发时间   ：2020/5/8  18:19
# 文件名称   ：JDcrawler.py
# 开发工具   ：PyCharm

import os
import csv
import time
import random
import pickle
from DecryptLogin import login


class JDCrawler():
    def __init__(self):
        if os.path.isfile('session.pkl'):
            self.session = pickle.load(open('session.pkl', 'rb'))
            self.session.headers.update({'Referer': ''})
        else:
            self.session = self.login()
            with open('session.pkl', 'wb') as session_file:
                pickle.dump(self.session, session_file)
                session_file.close()

    def login(self):
        lg = login.Login()
        infos_return, session = lg.jingdong()
        return session

    def run(self):
        url = 'https://search-x.jd.com/Search?'
        while True:
            good_name = input('请输入你想抓取的商品：')
            goods_info_list = []
            page = 1
            time_point = 1
            interval = random.randint(1, 5)
            while True:
                params = {
                    'area': '19',
                    'enc': 'utf-8',
                    'keyword': good_name,
                    'adType': '7',
                    'page': str(page),
                    'ad_ids': '291:25',
                    'xtest': 'new_search',
                    '_': str(int(time.time() * 1000))
                }
                respone = self.session.get(url, params=params)
                respone_json = respone.json()
                all_items = respone_json.get('291', [])
                if (respone.status_code != 200):
                    print('[INFO]: 发生了一些错误，无法正常！连接请重新检查参数')
                    # break
                if (len(all_items) == 0):
                    print(f'[INFO]: 关于{good_name}的商品数据抓取完毕, 共抓取到{len(goods_info_list)}条数据...')
                    break
                for item in all_items:
                    title = f"{item.get('ad_title', '')}".replace(r'<font class="skcolor_ljg">', '').replace('</font>',
                                                                                                             '').replace(
                        ' ', '')
                    goods_info_list.append(['https://img10.360buyimg.com/n7/' + item.get('image_url', ''),
                                            item.get('pc_price', ''),
                                            item.get('shop_link', {}).get('shop_name', ''),
                                            item.get('comment_num', ''),
                                            item.get('link_url', ''),
                                            title,
                                            item.get('good_rate', '')])
                page += 1
                time_point += 1
                if time_point == interval:
                    time.sleep(random.randint(50, 60) + random.random() * 10)
                    time_point = 0
                else:
                    time.sleep(random.random() + 1)
            self.save(goods_info_list, good_name + '.csv')

    def save(self, data, save_path):
        header = ['图片地址', '商品价格', '商店名称', '评论数量', '商品链接', '标题', '商品比重']
        save_file = open(save_path, 'w', encoding='utf-8', newline='')
        file_csv = csv.writer(save_file)
        file_csv.writerow(header)
        file_csv.writerows(data)
        save_file.close()


if __name__ == '__main__':
    crawler = JDCrawler()
    crawler.run()

