import json
import logging
from lxml import etree

from impl.monitor import Monitor


class BugBountyWriteups(Monitor):
    """
    监控pentester.land咨询
    """

    def __init__(self):
        super().__init__()
        self.url = "https://pentester.land/list-of-bug-bounty-writeups.html"
        self.rule = "list_of_bug_bounty_writeups"
        self.history_result = []
        self.temp_file_path = "temp/list_of_bug_bounty_writeups.json"

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
        node = root.xpath("//td/a")
        result = []
        for i in node:
            if i.text not in self.history_result:
                data = {"text": i.text, "href": i.attrib.get("href", "")}
                self.history_result.append(i.text)
                result.append(data)

        return result


if __name__ == "__main__":
    BugBountyWriteups().execute()
