import requests
import zipfile
import os
import re

class NewIosDriver:
    def __init__(self, url: str, udid: str):
        self.url = url
        self.udid = udid
        self.device_url = f"{self.url}/api/ios/{self.udid}"
        self.timeout = 30
    def list_forwards(self):
        url = f"{self.device_url}/forwards"
        return requests.get(url, timeout=self.timeout).json()
    
    def retrieve_forwards(self, port: int) -> int:
        url = f"{self.device_url}/forwards/{port}"
        res =  requests.get(url, timeout=self.timeout)
        res.raise_for_status()
        data = res.json()
        return data['port']
    
    def install_app(self, file_or_url):
        url = f"{self.device_url}/apps"
        is_url = bool(re.match(r"^https?://", file_or_url))
        if is_url:
            res = requests.post(url, params={"pkg_url": file_or_url}, timeout=1200)
        else:
            # If the file_or_url is a local file, we need to upload it first.
            files = {'file': open(file_or_url, 'rb')}
            res = requests.post(url, files=files, timeout=1200)
        res.raise_for_status()
        return True
    
    def list_app(self)->list[tuple[str, str, str]]:
        url = f"{self.device_url}/apps"
        res = requests.get(url, timeout=self.timeout)
        res.raise_for_status()
        data = res.json()
        return [(app['CFBundleIdentifier'], app['CFBundleName'], app['CFBundleShortVersionString']) for app in data]
    
    def app_pull(self, remote_path: str, local_path: str, bundle_id: str, timeout=None) -> bool:
        url = f"{self.device_url}/apps/{bundle_id}/fsync/pull{remote_path}"
        download_and_handle_file(url, local_path, timeout=timeout)
        return True

    def device_pull(self, remote_path: str, local_path: str, timeout=None) -> bool:
        url = f"{self.device_url}/fsync/pull{remote_path}"
        download_and_handle_file(url, local_path, timeout=timeout)
        return True

def download_and_handle_file(url, local_dir, timeout=None, auto_unzip=True):
    """
    下载服务端 pullFile 文件，根据响应头自动区分普通文件与 zip 文件。
    支持自动解压 ZIP 文件。

    Args:
        url (str): 下载地址
        local_dir (str): 保存到本地的目录
        timeout (int|None): 超时秒数
        auto_unzip (bool): 是否自动解压 zip 文件
    Returns:
        local_path (str): 下载保存的文件路径
        is_zip (bool): 是否为 zip 文件
    """
    os.makedirs(local_dir, exist_ok=True)
    with requests.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        # 取得文件名以及类型
        content_type = response.headers.get('Content-Type', '')
        content_disposition = response.headers.get('Content-Disposition', '')
        # 提取文件名
        filename = "downloaded_file"
        if "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[-1].strip('"; ')
        elif content_type == "application/zip":
            filename = "downloaded.zip"
        local_path = os.path.join(local_dir, filename)

        # 下载文件
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    is_zip = content_type == "application/zip" or filename.lower().endswith(".zip")
    if is_zip and auto_unzip:
        # 解压到同级目录下的同名文件夹
        extract_dir = os.path.splitext(local_path)[0]
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(local_path, 'r') as zip_ref:
            zip_ref.extractall(local_dir)
        print(f"ZIP 文件已自动解压到：{local_dir}")
    else:
        print(f"文件已保存为：{local_path}")

    return local_path, is_zip