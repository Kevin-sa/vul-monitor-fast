import os
import tarfile
import traceback
import requests

from utils import file_utils
from utils.logger import logger
from utils.spider_utils import SpiderUtils
from DrissionPage import ChromiumPage
from urllib.parse import urlparse, unquote


class ChromeExtendsCommon(object):
    def __init__(self):
        self.logger = logger
        self.spider = SpiderUtils()

    def get_new_extension(self, history_extensions: list, cache_path: str) -> dict:
        try:
            rank_list = self.get_rank_list_info(history_extensions=history_extensions)
            for key in rank_list.keys():
                try:
                    download_url = self.get_extends_download(rank_list.get(key))
                except Exception as e:
                    self.logger.error(f"get_new_extension get download_url error:{e} traceback:{traceback.format_exc()}")
                    continue
                self.logger.info(f"name:{key} download_url:{download_url}")
                if download_url is not None and download_url != "javascript:void(0);":
                    filename = ""
                    url_parse_param = urlparse(unquote(download_url)).query.split("&")
                    for param in url_parse_param:
                        if "filename=" in param:
                            filename = param.replace("filename=", "").strip()
                    file_utils.download_actuator(download_url=download_url.replace("&type=install", "&type=zip"),
                                                extension_name=filename,
                                                cache_path=cache_path)
                    break
            return rank_list
        except Exception as e:
            self.logger.error(f"error:{e} traceback:{traceback.format_exc()}")
            return {}


    def get_rank_list_info(self, history_extensions: list) -> dict:
        page = ChromiumPage(self.spider.get_drission_opt())
        page.get('https://www.crxsoso.com/')
        rank_list = {}
        history_exist = False
        for page_int in range(1, 10):
            if history_exist:
                break
            result = page.eles('t:div@class=rank-list')
            if len(result) < 2:
                continue
            for i in result[1].eles('t:div@class=item'):
                name = i('t:a').text
                if name in history_extensions:
                    history_exist = True
                    self.logger.info(f"{name} in history_extensions")
                    break
                dowload_url = i('t:a').attr('href')
                self.logger.info(f"get new extends {name}:{dowload_url}")
                rank_list[name] = dowload_url
            if history_exist is True:
                break
            for card_div in page.eles('t:div@class:sidebar'):
                if card_div('t:div@class=flex').text != '最近更新':
                    continue
                card_div.eles('t:button')[1].click()
                page.wait.load_start()
        page.close()
        return rank_list

    def get_extends_download(self, url: str) -> str:
        page = ChromiumPage(self.spider.get_drission_opt())
        page.get(url)
        page.set.load_mode.eager()
        page.ele('t:a@id=onlion')
        page.stop_loading()
        result = page.eles('t:div@class=addon-detail')
        right_div = result[0]('t:div@class=right')
        if right_div is not None:
            return right_div('t:a').attr('href')
        page.close()
        return None
