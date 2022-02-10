#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File Name     :pvp_hero_async.py
@Description   :异步爬取王者荣耀英雄高清皮肤
@Date          :2022/02/10 15:46:48
@Author        :xingjun
"""


import asyncio
import os
import re
from time import perf_counter

import aiohttp
import parsel
import requests
from loguru import logger

start = perf_counter()
# @note global variable
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
}
loop = asyncio.get_event_loop()
tasks = []
ROOT_DIR = os.path.dirname(__file__)
IMG_DIR = f"{ROOT_DIR}/wzry"
RIGHT, ERROR = 0, 0


def get_response(html_url):
    # @done
    """[http响应]

    Args:
        html_url ([str]): [请求地址]

    Returns:
        [type]: [返回http响应]
    """

    response = requests.get(url=html_url, headers=headers)
    # 万能转码方式
    response.encoding = response.apparent_encoding
    return response


async def get_image_url(hero_id):
    hero_url = f"https://pvp.qq.com/web201605/herodetail/{hero_id}.shtml"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=hero_url) as response:
            response = await response.text()
            selector = parsel.Selector(response)
            # @todo 提取英雄名字
            hero_name = selector.css(".cover-name::text").get()
            # @todo 提取所有皮肤名字
            skin_name = re.findall(
                '<ul class="pic-pf-list pic-pf-list3" data-imgname="(.*?)">',
                response,
            )[0].split("|")
            num = len(skin_name)
            for page in range(1, int(num) + 1):
                # @todo 皮肤图片地址
                image_url = f"https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{hero_id}/{hero_id}-bigskin-{page}.jpg"
                filename = skin_name[int(page) - 1].split("&")[0]
                info = {
                    "image_url": image_url,
                    "hero_name": hero_name,
                    "filename": filename,
                }
                await get_skin(info)


async def get_skin(info):
    global RIGHT, ERROR
    path = f'{IMG_DIR}/{info["hero_name"]}'
    if not os.path.exists(path):
        os.makedirs(path)
    name = info["filename"]
    url = info["image_url"]
    if name.count("/"):
        name.replace("/", "//")
    elif url == "":
        ERROR += 1
        logger.error(f"{name} url error {ERROR}")
    else:
        RIGHT += 1
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as response:
                if response.status == 200:
                    with open(f"{path}/{name}.jpg", "wb") as file:
                        chunk = await response.content.read()
                        logger.success(f"Downloading {name} right {RIGHT}...")
                        file.write(chunk)
                else:
                    ERROR += 1
                    logger.error(f"{name},{url} status!=200")


if __name__ == "__main__":
    # @todo
    url = "https://pvp.qq.com/web201605/js/herolist.json"
    json_data = get_response(url).json()
    for i in json_data:
        #  根据字典取值 提取每个英雄的ID
        hero_id = i["ename"]
        tasks.append(get_image_url(hero_id))
    loop.run_until_complete(asyncio.wait(tasks))
    logger.info(f"count times {perf_counter() - start}s")
    logger.info(f"download RIGHT {RIGHT}, download ERROR {ERROR}")
