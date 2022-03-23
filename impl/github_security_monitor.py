import json
import logging
from lxml import etree

from impl.monitor import Monitor


class GithubSecurityMonitor(Monitor):
    def __init__(self):
        super().__init__()
        self.rule = "Github-security"
        self.url = "https://github.com/{user}/{repo}/security/advisories"
        self.temp_file_path = "temp/github_security_monitor.json"
        self.history_result = {}
        self.warn_flag = ""

    def do_business(self):
        """
        1、获取历史数据
        2、根据super的关注清单获取对应的security信息
        3、根据response返回的text解析为html并做信息匹配
        4、更新历史数据、新增告警数据
        :return:
        """
        logging.info("do_business start")

        with open(self.project_file + self.temp_file_path) as file:
            self.history_result = json.load(file)
            file.close()

        warn_result = {}
        for temp in self.github_repos:
            resp = self.request.request(url=self.url.format(user=temp.get('user', ''), repo=temp.get('repo', '')))
            if resp.status_code != 200:
                logging.error("resp.status_code error:{}, user:{}, repo:{}".format(
                    resp.status_code, temp.get('user', ''), temp.get('repo', '')))
                continue

            self.warn_flag = '{user}-{repo}'.format(user=temp.get('user'), repo=temp.get('repo'))

            result = self.get_warn_param(resp.text)

            if result is None or len(result) == 0:
                continue

            warn_result[self.warn_flag] = result

        with open(self.project_file + self.temp_file_path, 'w') as file:
            json.dump(self.history_result, file)
            file.close()

        warn_result["rule"] = self.rule

        return warn_result

    def get_warn_param(self, temp):
        """
        查看是否在历史数据中，并更新历史数据、新增告警数据
        :param temp:
        :return:
        """
        root = etree.HTML(temp)
        text = root.xpath('//a[@class="Link--primary v-align-middle no-underline h4"]/text()')
        href = root.xpath('//a[@class="Link--primary v-align-middle no-underline h4"]/@href')
        if len(text) == 0 or len(href) == 0:
            return None
        history_href = []
        for i in self.history_result.get(self.warn_flag, []):
            history_href.append(i.get('url', ''))
        if self.history_result.get(self.warn_flag, None) is None:
            self.history_result[self.warn_flag] = []

        result = []
        for i in range(0, len(href)):
            url = "https://github.com/" + href[i]
            if url not in history_href:
                temp_dict = {'text': text[i].strip(), 'url': url}
                result.append(temp_dict)
                self.history_result[self.warn_flag].append(temp_dict)
        return result


if __name__ == "__main__":
    GithubSecurityMonitor().execute()
