#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File Name     :lol_hero_async.py
@Description   :异步下载英雄联盟高清皮肤
@Date          :2022/02/09 23:27:30
@Author        :xingjun
"""
import asyncio
import os
from time import perf_counter

import aiohttp
import requests
from loguru import logger  # 日志

start = perf_counter()
# global variable
ROOT_DIR = os.path.dirname(__file__)
IMG_DIR = f"{ROOT_DIR}/英雄联盟皮肤-async"
RIGHT = 0  # counts of right image
ERROR = 0  # counts of error image
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
}
# target url
hero_url = "http://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
# skin's url, will completed with hero's id.
base_url = "http://game.gtimg.cn/images/lol/act/img/js/hero/"
loop = asyncio.get_event_loop()
tasks = []


def get_hero_id(url):
    """
    get hero's id, to complete base_url.

    :param url: target url
    :return: hero's id
    """
    response = requests.get(url=url, headers=headers)
    info = response.json()
    items = info.get("hero")
    for item in items:
        yield item.get("heroId")


async def fetch_hero_url(url):
    """
    fetch hero url, to get skin's info

    :param url: hero url
    :return: None
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            if response.status == 200:
                response = await response.json(content_type="application/x-javascript")
                # skin's list
                skins = response.get("skins")
                for skin in skins:
                    info = {}
                    info["hero_name"] = skin.get("heroId") + "_" + skin.get("heroName")
                    info["skin_name"] = skin.get("name")
                    info["skin_url"] = skin.get("mainImg")
                    await fetch_skin_url(info)


async def fetch_skin_url(info):
    """
    fetch image, save it to jpg.

    :param info: skin's info
    :return: None
    """
    global RIGHT, ERROR
    path = f'{IMG_DIR}/{info["hero_name"]}'
    make_dir(path)
    name = info["skin_name"]
    url = info["skin_url"]
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
                        logger.success(f"download {name} right {RIGHT}...")
                        file.write(chunk)
                else:
                    ERROR += 1
                    logger.error(f"{name},{url} status!=200")


def make_dir(path):
    """
    make dir with hero's name

    :param path: path
    :return: None
    """
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    for hero_id in get_hero_id(hero_url):
        url = base_url + str(hero_id) + ".js"
        tasks.append(fetch_hero_url(url))
    loop.run_until_complete(asyncio.wait(tasks))
    logger.info(f"count times {perf_counter() - start}s")
    logger.info(f"download RIGHT {RIGHT}, download ERROR {ERROR}")
