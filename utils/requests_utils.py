from requests import sessions
import logging


class Request(object):
    def request(self, url, **param):
        """
        requests工具类封装
        :return:
        """
        with sessions.Session() as session:
            try:
                if param.get("timeout", None) is None:
                    param.update({"timeout": 30})
                if param.get("User-Agent", None) is None:
                    param.update({
                        "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/94.0.4606.61 Safari/537.36 "
                    })
                response = session.request(method="GET", url=url, **param)
                return response
            except Exception as e:
                logging.error(f"url:{url} error:{e}")
                return None
