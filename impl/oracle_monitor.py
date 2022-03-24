import logging
from lxml import etree
import re
import json

from impl.monitor import Monitor


class OracleMonitor(Monitor):
    """
    监控oracle security相关公告、补丁等
    """

    def __init__(self):
        super().__init__()
        self.url = "https://www.oracle.com/security-alerts/"
        self.rule = "oracle_monitor"
        self.history_result = []
        self.temp_file_path = "temp/oracle_monitor.json"
        self.host = "https://www.oracle.com"

    def do_business(self):
        logging.info("do_business start")
        with open(self.project_file + self.temp_file_path) as file:
            self.history_result = json.load(file)
            file.close()
        warn_result = {}
        resp = self.request.request(url=self.url, headers=self.headers)
        if resp.status_code != 200:
            logging.error("resp.status_code error:{}".format(resp.status_code))
            return

        result = self.get_warn_param(resp.text)
        if len(result) != 0:
            warn_result["data"] = result
            with open(self.project_file + self.temp_file_path, 'w') as file:
                json.dump(self.history_result, file)
                file.close()
        warn_result["rule"] = self.rule

        return warn_result

    def get_warn_param(self, temp):
        root = etree.HTML(temp)
        node = root.xpath("//table/tbody/tr/td/a")
        result = []
        for i in node:
            text = i.text
            if re.search("(Patch Update|Alert for)", text) is None:
                continue
            if text in self.history_result:
                continue
            self.history_result.append(text)
            href = i.attrib.get("href")
            result.append({"text": text, "href": self.host + href})
        return result


if __name__ == "__main__":
    OracleMonitor().execute()
