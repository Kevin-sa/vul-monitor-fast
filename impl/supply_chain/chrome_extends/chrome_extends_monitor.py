import json
import os
import traceback
from impl.monitor import Monitor
from utils import file_utils
from utils.llm_utils import LLMutils
from utils.logger import logger
from impl.supply_chain.chrome_extends.chrome_extends_common import ChromeExtendsCommon


class ChromeExtendsMonitor(Monitor):
    def __init__(self):
        super().__init__()
        self.chrome_extends_common = ChromeExtendsCommon()
        self.temp_file_path = "temp/supplyChina_chrome_extends.json"
        self.prompt = "当你是网络安全、供应链安全、chrome专家，擅长处理chrome插件包投毒事件，当前我有一个chrome插件包的相关文件，我提供的信息分别为：permissions是chrome插件申请的权限、content是js文件内容、matches和run_at是content_script的字段，请你根据以下信息来判断否是恶意投毒包，投毒的定义为：存在恶意http等请求、获取本地敏感信息及下载执行恶意文件等行为，请你分析是否存在恶意行为，请将你的回答以两部分输出：1）是否是存在恶意行为，需要布尔值回答：存在恶意行为或不存在恶意行为；2）判断原因说明"
        self.logger = logger
        self.history_result = []
        self.rule = "supplyChain_chrome_extends"
        self.cache_chrome_extends_path = "temp/cache/chrome"
        self.evil_cache_chrome_extends_path = "temp/cache/evil_chrome"
        self.sensitive_permission_list = ["sessions", "cookies"]

    def do_business(self):
        result = {}
        try:
            self.logger.info("chrome extends do_business start")
            with open(self.project_file + self.temp_file_path, "r") as file:
                content = file.read()
                if content.strip():
                    self.history_result = json.loads(content)
                else:
                    self.history_result = []
                file.close()
            new_extension_name_list = self.chrome_extends_common.get_new_extension(
                history_extensions=self.history_result,
                cache_path=self.project_file + self.cache_chrome_extends_path,
            )
            result['scope'] = new_extension_name_list
            self.logger.info(f"new_extension_name_list:{new_extension_name_list}")
            if len(new_extension_name_list) != 0:
                warn_result = self.get_warn_param(None)
                if len(warn_result) != 0:
                    result['data'] = warn_result
                    result['rule'] = self.rule

                with open(self.project_file + self.temp_file_path, 'w') as file:
                    combined_list = list(new_extension_name_list.keys())
                    json.dump(combined_list, file, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"error:{e} traceback:{traceback.format_exc()}")
        file_utils.remove_files_and_folders(self.project_file + self.cache_chrome_extends_path)
        return result

    def get_warn_param(self, temp) -> list:
        try:
            get_warn_param_result = []
            cache_path = self.project_file + self.cache_chrome_extends_path
            entries = os.listdir(cache_path)

            folders = [entry for entry in entries if
                       os.path.isdir(os.path.join(cache_path, entry))]
            for folder in folders:
                self.logger.info(f"folder:{folder} starting")
                manifest_path = f"{cache_path}/{folder}/manifest.json"
                if os.path.exists(manifest_path) is False:
                    continue
                with open(manifest_path, 'r') as file:
                    package_info = json.load(file)
                    permissions = package_info.get("permissions", "")
                    content_scripts = package_info.get("content_scripts", None)
                    file.close()
                if content_scripts is None:
                    self.logger.info(f"{folder} content_scripts is None")
                    continue
                for content_script in content_scripts:
                    script_path_list = content_script.get("js", None)
                    if script_path_list is None:
                        continue
                    for script_path in script_path_list:
                        if script_path.startswith('/'):
                            script_path = script_path.lstrip("/")
                        if os.path.exists(os.path.join(cache_path, folder, script_path)) is False:
                            continue
                        with open(os.path.join(cache_path, folder, script_path), 'r', encoding='utf-8') as f:
                            content_script_data = f.read()
                            f.close()
                        if content_script_data != "":
                            llm_content = {"permissions": permissions, "content": content_script_data[:5000],
                                        "matches": content_script.get("matches", ""),
                                        "run_at": content_script.get("run_at", "")}
                            result = LLMutils().dashscope_call_msg(content=json.dumps(llm_content), prompt=self.prompt)
                            if result is None:
                                continue
                            response_content = result.output.choices[0].message.content
                            check_strings = {"不存在恶意行为", "存在恶意行为：否", "存在恶意行为**：否", "没有直接的恶意行为", "存在恶意行为：`false`",
                                            "存在恶意行为: **否**", "存在恶意行为: 否"}
                            if not any(sub in response_content for sub in check_strings) or self.check_permissions(permissions):
                                get_warn_param_result.append({'pacakge_name': folder, 'permissions': permissions, 'matches': content_script.get('matches', ''), 'script_path': script_path, 'content': response_content})
                                file_utils.move_file(cache_path=cache_path, folder=folder,to_path=self.project_file + self.evil_cache_chrome_extends_path)
            return get_warn_param_result
        except Exception as e:
            self.logger.error(f"error:{e} traceback:{traceback.format_exc()}")
            return []

    # check_permissions 检查插件manifest中是否存在敏感权限
    def check_permissions(self, permissions: list) -> bool:
        if any(sub in permissions for sub in self.sensitive_permission_list):
            return True
        return False


if __name__ == "__main__":
    ChromeExtendsMonitor().do_business()
