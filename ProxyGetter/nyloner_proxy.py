import base64
import hashlib
import requests
import json
import time
from typing import List


def decode_str(data: str):
    key = "nyloner"
    key_len = len(key)
    code = ''
    for i in range(0, len(data)):
        coeFYlqUm2 = i % key_len
        code += chr(ord(data[i]) ^ ord(key[coeFYlqUm2]))
    return str(base64.b64decode(code), encoding="utf-8")


class GetNylonerProxy(object):

    @staticmethod
    def get_proxy_ip(proxies: List[str], page: int) -> bool:
        timestamp = time.time()
        token = hashlib.md5(bytes(str(page) + "15" + str(int(timestamp)), encoding="utf8"))
        resp = requests.get("https://www.nyloner.cn/proxy", params={
            "page": page,
            "num": 15,
            "token": token.hexdigest(),
            "t": int(timestamp)
        })
        if resp.status_code == 200:
            result = resp.json()
            encrypted_items = str(base64.b64decode(result['list']), encoding="utf-8")
            data = json.loads(decode_str(encrypted_items).replace("'", '"'))
            for server in data:
                proxies.append(server)
            return len(data) == 15
        else:
            print("request page %d error with %s" % (page, resp.text))
            return False
