import os
import sys
import time

from .api import Api
from .logger import log
from .setting import Setting


def main():
    Setting(filepath=os.path.join(__path__[0], "settings.json"))
    username = Setting().config['username'] = Setting().get('username') or input("username: ").strip()
    password = Setting().config['password'] = Setting().get('password') or input("password: ").strip()
    language = Setting().config['language'] = Setting().get('language')
    host = Setting().config['host'] = Setting().get('host') or input("host: ").strip()
    Setting().save()

    client = Api(username, password, host, language)
    if not client.get_session():
        log('warn', 'login failed. wait 60 seconds for cooldown.')
        time.sleep(61)
        if not client.get_session():
            log('error', 'a wrong username or password. please check your settings.')
            sys.exit(1)

    log('info', 'successful login to the router.')
    data = client.get_device_info()
    print(data)

