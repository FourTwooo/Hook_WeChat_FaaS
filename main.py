import json
import time
import os

import frida
from loguru import logger

import tools
from tools.asyncRequestQueue import DataStore


class Frida_Server(DataStore):

    def __init__(self):
        super().__init__()

        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        with open(f'{current_dir_path}/frida_js/Hook_WeChat_FaaS.js', 'r') as f:
            hook_code = f.read()

        # 连接到设备
        self.device = frida.get_usb_device()  # 通过USB连接设备
        # device = frida.get_device_manager().add_remote_device('192.168.0.72:5555')
        AppBrandUI_pid = tools.get_pid(self.device.id, 'com.tencent.mm/.plugin.appbrand.ui.AppBrandUI')
        if not AppBrandUI_pid:
            raise Exception('微信小程序未打开? Pid未能搜索到')

        AppBrandUI_pid: int = int(AppBrandUI_pid)
        # 获取进程
        process = self.device.attach(AppBrandUI_pid)
        # 创建脚本
        self.script = process.create_script(hook_code)
        self.script.on('message', self.on_message)
        # 加载并运行脚本
        self.script.load()

    def get_tencent_appBrand_pid(self):
        for process in self.device.enumerate_processes():
            print(process)
            if "com.tencent.mm:appbrand" in process.name:
                return process.pid

        return None

    def on_message(self, message, data):
        if message['type'] == 'send':
            payload = json.loads(message['payload'])
            if payload['type'] == 'requests':
                logger.debug(f'{payload}')
            else:
                logger.success(f'{payload}')
                self.put(key=f'{payload["AppId"]}{payload["asyncRequestCounter"]}', value=payload)
        else:
            logger.error(f'{message}')

    def CallWX(self, appid, api_name, data):
        Appid_asyncRequestCounter = self.script.exports.call(appid, api_name, data)
        return self.get(Appid_asyncRequestCounter, timeout=3)

    def close(self):
        # 停止脚本
        self.script.unload()


class WeChatApi(Frida_Server):

    def __init__(self, appid):
        super().__init__()
        self.appid = appid

    @staticmethod
    def get_tid():
        return int(time.time() * 1000)

    @staticmethod
    def json_dumps_blank_space(json_data):
        return json.dumps(json_data, separators=(",", ":"))

    def login(self):
        return self.CallWX(self.appid, 'login', self.json_dumps_blank_space({"requestInQueue": False}))

    def getUserInfo(self):
        return self.CallWX(self.appid, 'operateWXData', self.json_dumps_blank_space({
            "data": {
                "api_name": "webapi_getuserinfo",
                "data": {
                    "lang": "en",
                    "version": "3.4.3"
                },
                "operate_directly": False,
                "with_credentials": True,
                "tid": self.get_tid()
            },
            "requestInQueue": True,
            "isImportant": True
        }))


if __name__ == '__main__':
    wx = WeChatApi(appid='wx3c12cdd0ae8b1a7b')
    print(wx.login())
    print(wx.login())
    print(wx.login())
    print(wx.getUserInfo())
    # import sys
    # sys.stdin.read()
    wx.close()
