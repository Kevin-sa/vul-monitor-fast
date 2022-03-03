import logging
import re
import requests

from impl.monitor import Monitor
from utils.date_utils import utc_date_compare_now_day


class GithubCommitMonitor(Monitor):
    """
    通过github的commit搜索安全相关问题
    todo:如果如果时间内超过per_page=10数量限制怎么办
    """

    def __init__(self):
        super().__init__()
        self.rule = "Github-commit"
        self.url = 'https://api.github.com/repos/{user}/{repo}/commits?per_page=10'

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

            # 循环判断处理
            for result in resp.json():
                commit_date = result.get('commit', {}).get('committer', {}).get('date', None)
                if utc_date_compare_now_day(commit_date) is False:
                    continue
                msg = result.get('commit', {}).get('message', '')
                if re.search(pattern, msg, re.IGNORECASE):
                    warn_result[warn_flag].append(self.get_warn_param(result))
            if len(warn_result[warn_flag]) == 0:
                warn_result.pop(warn_flag)

        return warn_result

    def get_warn_param(self, temp):
        return {
            'message': temp.get('commit', {}).get('message', ''),
            'url': temp.get('html_url', '')
        }


if __name__ == "__main__":
    GithubCommitMonitor().execute()