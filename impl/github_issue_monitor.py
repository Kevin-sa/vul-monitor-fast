import re
import requests
import logging

from impl.monitor import Monitor
from utils.date_utils import utc_date_compare_now_day


class GithubIssueMonitor(Monitor):
    """
    通过github的issue搜索安全相关问题
    """

    def __init__(self):
        super().__init__()
        self.rule = "Github-issue"
        self.url = 'https://api.github.com/repos/{user}/{repo}/issues?per_page=10'

    def do_business(self):
        logging.info("do_business start")

        warn_result = {'rule': self.rule}
        for temp in self.github_repos:
            resp = requests.get(url=self.url.format(user=temp.get('user'), repo=temp.get('repo')),
                                headers={'Authorization': self.github_authorization})
            if resp.status_code != 200:
                logging.error("resp.status_code error:{}, user:{}, repo:{}".format(
                    resp.status_code, temp.get('user', ''), temp.get('repo', '')))
                continue

            warn_flag = '{user}-{repo}'.format(user=temp.get('user'), repo=temp.get('repo'))
            warn_result[warn_flag] = []
            pattern = self.black_pattern.get('common') if self.black_pattern.get(
                temp.get('language')) is None else self.black_pattern.get(temp.get('language'))

            for result in resp.json():
                created_at = result.get('created_at', None)
                if utc_date_compare_now_day(created_at) is False:
                    continue
                title = result.get('title', '')
                if re.search(pattern, title, re.IGNORECASE):
                    warn_result[warn_flag].append(self.get_warn_param(result))
            if len(warn_result[warn_flag]) == 0:
                warn_result.pop(warn_flag)

        return warn_result

    def get_warn_param(self, temp):
        return {
            'title': temp.get('title'),
            'url': temp.get('html_url', '')
        }


if __name__ == "__main__":
    GithubIssueMonitor().execute()
