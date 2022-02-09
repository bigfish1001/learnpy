#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File Name     :pvphero.py
@Description   :
@Date          :2022/02/09 03:52:24
@Author        :
"""


import os
import re

import parsel
import requests
from fake_useragent import UserAgent


def get_response(html_url):
    # @done
    """[http响应]

    Args:
        html_url ([str]): [请求地址]

    Returns:
        [type]: [返回http响应]
    """
    headers = {"User-Agent": UserAgent().random}
    response = requests.get(url=html_url, headers=headers)
    # 万能转码方式
    response.encoding = response.apparent_encoding
    return response


def get_image_url(hero_id):
    """[保存格式 英雄ID-英雄名]

    Args:
        hero_id ([int]): [英雄ID]
    """
    # 英雄详情页URL
    # https://pvp.qq.com/web201605/herodetail/106.shtml
    hero_url = f"https://pvp.qq.com/web201605/herodetail/{hero_id}.shtml"
    response = get_response(hero_url)
    selector = parsel.Selector(response.text)
    # 提取英雄名字
    hero_name = selector.css(".cover-name::text").get()
    # 提取所有皮肤名字
    skin_name = re.findall(
        '<ul class="pic-pf-list pic-pf-list3" data-imgname="(.*?)">', response.text
    )[0].split("|")
    num = len(skin_name)
    for page in range(1, int(num) + 1):
        # 皮肤图片地址
        # https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/106/106-bigskin-2.jpg
        image_url = f"https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{hero_id}/{hero_id}-bigskin-{page}.jpg"
        # 请求皮肤 图片地址
        image_content = get_response(image_url).content
        # 相对路径
        path = f"./王者荣耀英雄皮肤/{hero_name}/"
        if not os.path.exists(path):
            os.makedirs(path)
        # @note皮肤图片保存的路径  文件夹 + skin_name[int(page) - 1].split('&')[0] 皮肤名字
        filename = path + skin_name[int(page) - 1].split("&")[0] + ".jpg"
        if not os.path.exists(filename):
            # @fixfilename 路径
            with open(filename, mode="wb") as f:
                f.write(image_content)
                print(f"正在保存：{hero_name}", skin_name[int(page) - 1].split("&")[0])
        else:
            print(f"{hero_name}", skin_name[int(page) - 1].split("&")[0], "已经存在")


if __name__ == "__main__":
    # @tag 
    url = "https://pvp.qq.com/web201605/js/herolist.json"
    json_data = get_response(url).json()
    for i in json_data:
        #  根据字典取值 提取每个英雄的ID
        hero_id = i["ename"]
        get_image_url(hero_id)
