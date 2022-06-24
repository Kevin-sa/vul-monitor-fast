import json
import logging
from lxml import etree

from impl.monitor import Monitor


class IntigritoBugBytes(Monitor):
    """
    监控blog.intigriti.com的bug bytes
    """

    def __init__(self):
        super().__init__()
        self.url = "https://blog.intigriti.com/"
        self.rule = "bug_bytes"
        self.history_result = []
        self.temp_file_path = "temp/intigriti_bug_bytes.json"

    def do_business(self):
        logging.info("bug bytes do_business start")
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
                json.dump(self.history_result + result, file)
                file.close()
        warn_result["rule"] = self.rule
        return warn_result

    def get_warn_param(self, temp):
        root = etree.HTML(temp)
        node = root.xpath("//article/figure/a")
        result = []
        for i in node:
            href = i.attrib.get("href", "")
            if href not in self.history_result:
                result.append(href)
        return result


if __name__ == "__main__":
    IntigritoBugBytes().execute()
