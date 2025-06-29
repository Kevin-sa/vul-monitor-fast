import os
import shutil
import zipfile

import requests

from utils.logger import logger


def remove_files_and_folders(cache_path: str):
    try:
        items = os.listdir(cache_path)
        for item in items:
            item_path = os.path.join(cache_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    except Exception as e:
        logger.exception(f"remove_files_and_folders error:{e}")


def move_file(folder: str, cache_path: str, to_path: str):
    try:
        items = os.listdir(cache_path)
        files = [item for item in items if os.path.isfile(os.path.join(cache_path, item))]
        for file in files:
            if folder in file:
                shutil.move(os.path.join(cache_path, file), to_path)
                break
    except Exception as e:
        logger.error(f"remove file error:{e}")


def download_actuator(download_url: str, extension_name: str, cache_path: str):
    try:
        # url = 'https://marketplace.visualstudio.com/_apis/public/gallery/publishers/IngotStudio1716410/vsextensions/ingotscript/1.0.0/vspackage'
        new_filename = f'{cache_path}/{extension_name}.zip'

        response = requests.get(download_url, stream=True)
        to_extension_name = f'{cache_path}/{extension_name}'
        if response.status_code == 200:
            with open(new_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f'file download success {new_filename}')
        else:
            logger.info(f'file download fail，response status code：{response.status_code}')
        if os.path.exists(new_filename):
            with zipfile.ZipFile(new_filename, 'r') as zip_ref:
                zip_ref.extractall(to_extension_name)
            logger.info(f'ZIP success unzip  {to_extension_name}')
        else:
            logger.error(f'file {new_filename} not exits')
        response.close()
    except Exception as e:
        logger.error(f"{extension_name} download_actuator fail error:{e}")


