from DrissionPage import ChromiumOptions


class SpiderUtils(object):

    # def get_drission_opt(self) -> object:
    #     co = ChromiumOptions()
    #     co.set_paths(browser_path=r'/usr/bin/chromium-browser')
    #     co.incognito()
    #     co.headless()
    #     co.set_argument('--no-sandbox')
    #     return co
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SpiderUtils, cls).__new__(cls)
            cls._instance._co = ChromiumOptions()
            cls._instance._co.set_paths(browser_path=r'/usr/bin/chromium-browser')
            cls._instance._co.incognito()
            cls._instance._co.headless()
            cls._instance._co.set_argument('--no-sandbox')
        return cls._instance

    def get_drission_opt(self) -> object:
        return self._co