import requests
from requests.exceptions import RequestException
import time


def get_page(url, headers=None):
    """获得网页"""

    # 设置头
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
        }
    # 尝试获取
    flag = 10
    while flag > 0:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flag = 0
                return response
        except RequestException:
            flag -= 1
            print('retry')
            if flag <= 0:
                return None




def get_time():
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
