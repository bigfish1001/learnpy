#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File Name     :bh3.py
@Description   :
@Date          :2022/02/09 03:51:32
@Author        :
"""


import os
from multiprocessing import Pool

import requests
from fake_useragent import UserAgent
from lxml import etree
from pyinstrument import Profiler


class Spider(object):
    # @done
    def __init__(self):
        self.index_url = "https://www.bh3.com/valkyries"
        self.title_urls = []  # 保存所有女武神详情页url

    def send_request(self, url):
        headers = {"User-Agent": UserAgent().random}  # 随机请求头
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content

    def parse(self):
        """[解析女武神的详情页地址]"""
        response = self.send_request(self.index_url)
        html = etree.HTML(response)
        title_urls = html.xpath(r'//div[@class="roles"]/a/@href')  # 解析每个女武神的详情页url
        for title_url in title_urls:
            title_url = "https://www.bh3.com" + title_url
            self.title_urls.append(title_url)

    def parse_detail(self, title_url):
        """[解析每个女武神的详情页信息]

        Args:
            title_url ([type]): [description]
        """
        r = self.send_request(title_url).decode()
        html = etree.HTML(r)
        img_url = html.xpath(r'//div[@class="big-img"]/img/@src')[0]  # 图片url
        name_1 = html.xpath(r'//div[@class="valkyries-detail-bd__title"]/text()')[
            0
        ].strip()
        name_2 = html.xpath(r'//div[@class="wrap"]/div[1]/text()')[0].strip()
        img_name = name_1 + "-" + name_2  # 图片名字
        self.download(img_url, img_name)

    def download(self, img_url, img_name):
        """[下载图片]

        Args:
            img_url ([type]): [description]
            img_name ([type]): [description]
        """
        img_path = "./崩坏3女武神"  # 图片保存目录
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        filename = "{}/{}.png".format(img_path, img_name)  # 图片文件名
        if not os.path.exists(filename):  # @tag避免重复下载
            content = self.send_request(img_url)
            print("正在下载：", filename)
            with open(filename, "wb") as f:
                f.write(content)

    def start_pool(self):
        """[执行进程池]"""
        pool = Pool()
        pool.map(self.parse_detail, self.title_urls)


def main():
    """主程序"""
    spider = Spider()
    spider.parse()
    spider.start_pool()


if __name__ == "__main__":
    profiler = Profiler()
    profiler.start()
    main()
    profiler.stop()
    profiler.output_text()
