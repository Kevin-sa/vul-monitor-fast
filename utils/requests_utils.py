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
                    param.update({"timeout": 3})
                response = session.request(method="GET", url=url, **param)
                return response
            except Exception as e:
                logging.error(f"url:{url} error:{e}")
                return None
