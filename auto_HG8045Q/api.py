import re
from base64 import b64encode
from typing import Dict,  Optional

import requests


class Api:

    def __init__(self, username: str, password: str, host: str, language: Optional[str] = 'english'):
        self._username: str = username
        self._password: str = b64encode(password.encode()).decode()
        self._language = language
        self._base_addr: str = f'http://{host}'
        self._cookies: Optional[str] = None

    def get_session(self) -> bool:
        req_token = requests.post(self._base_addr + '/asp/GetRandCount.asp')
        req_token.encoding = 'UTF-8-SIG'
        token = req_token.text
        data = {
            'x.X_HW_Token': token
        }
        cookies = {
            'Cookie': f'UserName:{self._username}:PassWord:{self._password}:Language:{self._language}:id=-1'
        }
        req_login = requests.post(self._base_addr + '/login.cgi', data=data, cookies=cookies)
        response_cookies = req_login.cookies.get_dict()

        if 'Cookie' not in response_cookies:
            return False

        self._cookies = response_cookies
        return True

    def get_device_info(self) -> Dict[str, str]:
        requests.get(self._base_addr + '/frame.asp', cookies=self._cookies)
        req_info = requests.get(self._base_addr + '/html/ssmp/deviceinfo/deviceinfonomemcpu.asp', cookies=self._cookies)
        regex = r'"(\w*)",' \
                r'"(\d*\.\w*)",' \
                r'"(\w*)",' \
                r'"(\w*)",' \
                r'"(\w*)",' \
                r'"(\d*-\d*-\d*_\d*:\d*:\d*) ",' \
                r'"(\w*:\w*:\w*:\w*:\w*:\w*)",' \
                r'"(EchoLife HG8045Q GPON Terminal &#40;CLASS B\+/PRODUCT ID:\w*/CHIP:\w*&#41;)",' \
                r'"(\w*\.\w*)"'
        # SN
        # Hardware Version
        # Software Version
        # Device Type
        # SN (?)
        # Production Date (?)
        # Mac address
        # Description
        # Manufacture Info

        matched_data = re.search(regex, req_info.text).groups()
        data = {
            'serial_number': matched_data[0],
            'hardware_version': matched_data[1],
            'software_version': matched_data[2],
            'device_type': matched_data[3],
            '_unknown': matched_data[4],
            '_unknown2': matched_data[5],
            'mac_address': matched_data[6],
            'description': matched_data[7].replace('&#40;', '(').replace('&#41;', ')'),
            'manufacture_info': matched_data[8]
        }

        return data
