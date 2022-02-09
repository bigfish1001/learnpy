#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File Name     :lolhero.py
@Description   :
@Date          :2022/02/09 03:52:04
@Author        :
"""


import json
import os

import requests
from fake_useragent import UserAgent

# 设置头部信息，防止被检测出是爬虫
headers = {"User-Agent": UserAgent().random}
# 请求英雄列表的url地址
url = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
response = requests.get(url=url, headers=headers).text
loads = json.loads(response)
dic = loads["hero"]
for data in dic:
    id_ = data["heroId"]
    skinUrl = "https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js".format(id_)
    # 请求每个英雄皮肤的url地址
    skinResponse = requests.get(url=skinUrl, headers=headers).text
    json_loads = json.loads(skinResponse)
    hero_ = json_loads["hero"]
    save_path = "./英雄联盟皮肤/{}-{}".format(hero_["heroId"], hero_["name"])
    # 文件夹不存在，则创建文件夹
    folder = os.path.exists(save_path)
    if not folder:
        os.makedirs(save_path)
    skins_ = json_loads["skins"]
    for data in skins_:
        if data["chromas"] == "0":
            content = requests.get(url=data["mainImg"], headers=headers).content
            try:
                with open("{}/{}.jpg".format(save_path, data["name"]), "wb") as f:
                    print("正在下载英雄：{} 皮肤名称：{} ...".format(hero_["name"], data["name"]))
                    f.write(content)
            except Exception as e:
                print("下载失败")
                print(e)
# @todo 利用协程爬取
