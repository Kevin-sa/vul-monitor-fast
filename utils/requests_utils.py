from requests import sessions
import cloudscraper
from utils.logger import logger


class Request(object):

    def __init__(self):
        self.logger = logger

    def request(self, url, **param):
        """
        requests工具类封装
        :return:
        """
        with sessions.Session() as session:
            try:
                if param.get("timeout", None) is None:
                    param.update({"timeout": 30})
                response = session.request(method="GET", url=url, **param)
                return response
            except Exception as e:
                self.logger.error(f"url:{url} error:{e}")
                return None

    def scraper_get_request(self, url):
        try:
            scraper = cloudscraper.create_scraper()
            return scraper.get(url)
        except Exception as e:
            self.logger.error(f"url:{url} error:{e}")
            return None
