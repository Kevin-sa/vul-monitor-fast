import math
import os
import zipfile

import requests
from utils.logger import logger


class VscodeExtendsCommon(object):

    def __init__(self):
        self.headers = {"Content-Length": "application/json",
                        "Accept": "application/json;api-version=7.2-preview.1;excludeUrls=true"}
        self.logger = logger

    def extends_count(self):
        data = {"assetTypes": ["Microsoft.VisualStudio.Services.Icons.Default",
                               "Microsoft.VisualStudio.Services.Icons.Branding",
                               "Microsoft.VisualStudio.Services.Icons.Small"], "filters": [{"criteria": [
            {"filterType": 8, "value": "Microsoft.VisualStudio.Code"},
            {"filterType": 10, "value": "target:\"Microsoft.VisualStudio.Code\" "},
            {"filterType": 12, "value": "37888"}],
            "direction": 2, "pageSize": 54,
            "pageNumber": 1, "sortBy": 10,
            "sortOrder": 0,
            "pagingToken": None}],
                "flags": 870}
        resp = requests.post("https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery", json=data,
                             headers=self.headers).json()
        results = resp.get("results", {})
        result = results[0]
        count = result.get("resultMetadata", [])[0].get("metadataItems", [])[0].get("count", 0)
        return math.ceil(count / 54)

    def extends_list(self, history_extensions: list, page_min: int, page_max: int, cache_path: str,
                     is_download: bool) -> list:
        extension_name_list = []
        for i in range(page_min, page_max):
            self.logger.info(f"pageNumber:{i} page_min:{page_min} page_max:{page_max}")
            # https://marketplace.visualstudio.com/search?target=VSCode&category=All%20categories&sortBy=PublishedDate
            data = {"assetTypes": ["Microsoft.VisualStudio.Services.Icons.Default",
                                   "Microsoft.VisualStudio.Services.Icons.Branding",
                                   "Microsoft.VisualStudio.Services.Icons.Small"], "filters": [{"criteria": [
                {"filterType": 8, "value": "Microsoft.VisualStudio.Code"},
                {"filterType": 10, "value": "target:\"Microsoft.VisualStudio.Code\" "},
                {"filterType": 12, "value": "37888"}],
                "direction": 2, "pageSize": 54,
                "pageNumber": i, "sortBy": 10,
                "sortOrder": 0,
                "pagingToken": None}],
                    "flags": 870}
            resp = requests.post("https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery", json=data,
                                 headers=self.headers).json()
            results = resp.get("results", {})
            result = results[0]
            extensions = result.get("extensions", {})
            for extension in extensions:
                extension_name = extension.get("extensionName", "")
                if extension_name in history_extensions:
                    return extension_name_list
                extension_name_list.append(extension_name)
                publisher = extension.get("publisher", {})
                # https://marketplace.visualstudio.com/_apis/public/gallery/publishers/kEllie/vsextensions/vnscript/1.0.0/vspackage
                # https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery
                extension_info_value = f"{publisher.get('publisherName', '')}.{extension_name}"
                last_version = self.extension_info(extension_info_value)
                if last_version is None:
                    continue
                download_url = f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher.get('publisherName', '')}/vsextensions/{extension_name}/{last_version}/vspackage"
                if is_download:
                    self.download_actuator(download_url, extension_name, cache_path)
        return extension_name_list

    def extension_info(self, value: str):
        extension_info = requests.post("https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery",
                                       json={"assetTypes": None, "filters": [
                                           {"criteria": [{"filterType": 7, "value": value}],
                                            "direction": 2, "pageSize": 100, "pageNumber": 1, "sortBy": 0,
                                            "sortOrder": 0, "pagingToken": None}], "flags": 2151},
                                       headers=self.headers).json()
        results = extension_info.get("results", [])
        if results is None or len(results) == 0:
            self.logger.error(f"extension_info valuse:{value} results is None:{results}")
            return None
        result = results[0]
        extension = result.get("extensions")[0]
        version_info = extension.get("versions", [])[0]
        return version_info["version"]

    def download_actuator(self, download_url: str, extension_name: str, cache_path: str):
        try:
            # url = 'https://marketplace.visualstudio.com/_apis/public/gallery/publishers/IngotStudio1716410/vsextensions/ingotscript/1.0.0/vspackage'
            new_filename = f'{cache_path}/{extension_name}.zip'

            response = requests.get(download_url, stream=True)
            to_extension_name = f'{cache_path}/{extension_name}'
            if response.status_code == 200:
                with open(new_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                self.logger.info(f'file download success {new_filename}')
            else:
                self.logger.info(f'file download fail，response status code：{response.status_code}')
            if os.path.exists(new_filename):
                with zipfile.ZipFile(new_filename, 'r') as zip_ref:
                    zip_ref.extractall(to_extension_name)
                self.logger.info(f'ZIP success unzip  {to_extension_name}')
            else:
                self.logger.error(f'file {new_filename} not exits')
            response.close()
        except Exception as e:
            self.logger.error(f"{extension_name} download_actuator fail error:{e}")

    def main_content(self, main_file: str) -> str:
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()
            return content

    def found_active(self, folder: str, main_path: str) -> str:
        function_name = "function activate(context) {"
        try:
            with open(main_path, 'r') as file:
                lines = []
                left_parenthesis = 0
                right_parenthesis = 0
                capture = False
                for line in file:
                    if function_name in line:
                        capture = True
                        lines.append(line)
                        left_parenthesis += 1
                        continue
                    if capture:
                        lines.append(line)
                        if "{" in line:
                            left_parenthesis += 1
                        if "}" in line:
                            right_parenthesis += 1
                            if left_parenthesis == right_parenthesis:
                                break
                if len(line) != 1:
                    self.logger.info(f"{folder}:{main_path}:{len(lines)}")
                    return "\n".join(line)
                else:
                    return ""
        except Exception as e:
            self.logger.error(f"VscodeExtendsMonitor found_active error:{e}")
            return ""
