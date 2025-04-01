import time
from threading import Thread
import json
from xmlrpc.server import SimpleXMLRPCServer
import tornado.websocket
import tornado.ioloop
from loguru import logger
import sys


# 捕获未处理的异常
def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error(f"[全局异常] 未捕获的异常: {exc_value}", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_uncaught_exception


class DataStore:
    def __init__(self, maxsize=100):
        self.data = {}
        self.maxsize = maxsize

    def put(self, key, value):
        if len(self.data) >= self.maxsize:
            logger.warning(f"[数据存储] 数据量超出限制，移除最早的数据")
            self.data.pop(next(iter(self.data)))  # 移除最早的键值对
        self.data[key] = value

    def get(self, key, timeout=3):
        end_time = time.time() + timeout
        while key not in self.data:
            remaining = end_time - time.time()
            if remaining <= 0.0:
                logger.warning(f"[数据获取] 超时未找到 key: {key}")
                return None
        return self.data.pop(key)


# 存储所有 WebSocket 连接
connections = {}
TaskId = 0
store = DataStore()


class WeChatSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.userid = None
        self.appid = None

    def data_received(self, chunk: bytes):
        pass

    def check_origin(self, origin):
        """
        允许所有的跨域请求。如果需要限制跨域访问，可以在这里添加校验逻辑。
        """
        return True

    def open(self):
        """
        处理新连接
        """
        try:
            self.userid = self.request.headers.get('userid', '').encode('ISO-8859-1').decode()
            self.appid = self.request.headers.get('appid', '')
            if not self.userid or not self.appid:
                self.close(code=400, reason="Missing userid or appid")
                logger.warning(f"[连接失败] 缺少 userid 或 appid")
                return

            connections[(self.appid, self.userid)] = self
            logger.debug(f"[新增连接] appid: {self.appid}, userid: {self.userid}")
        except Exception as e:
            logger.error(f"[连接异常] {e}")
            self.close(code=500, reason="Server error")

    def on_message(self, message):
        """
        处理收到的消息
        """
        try:
            message = json.loads(message)
            logger.success(message)
            if not message.get('data'):
                # logger.warning(f"[消息错误] 消息内容缺少 'data'")
                return

            logger.success(f"[接收消息] {message['data']}")
            key = f'{TaskId}-{self.userid}-{self.appid}'
            store.put(key=key, value=message['data'])
        except Exception as e:
            logger.error(f"[消息处理异常] {e}")

    def on_close(self):
        """
        处理连接断开
        """
        if connections.get((self.appid, self.userid)):
            del connections[(self.appid, self.userid)]
        logger.warning(f"[断开连接] appid: {self.appid}, userid: {self.userid}")

    @staticmethod
    def send_message(client, message, timeout: int = 20, params=None):
        """
        向客户端发送消息
        """
        if params is None:
            params = {}
        global TaskId
        try:
            userid = client.request.headers['userid'].encode('ISO-8859-1').decode()
            appid = client.request.headers['appid']
            logger.debug(f"[发送消息] appid: {appid}, userid: {userid} => {message}")

            if connections.get((appid, userid)):
                TaskId += 1
                client.write_message(json.dumps({"TaskId": TaskId, "function_name": message, "params": params}))
                key = f"{TaskId}-{userid}-{appid}"
                return store.get(key=key, timeout=timeout)
        except Exception as e:
            logger.error(f"[消息发送异常] {e}")
            return None


def get_connections():
    """
    获取当前所有连接信息
    """
    if len(connections.keys()) != 0:
        sockets_user = [{"appid": i[0], "username": i[1]} for i in connections.keys()]
        return json.dumps(sockets_user, ensure_ascii=False)
    else:
        return json.dumps({"error_msg": "未有连接"}, ensure_ascii=False)


def call(userid: str = "", appid: str = "wxc9c692c952025897", function_name: str = "wx.login()", timeout: int = 20,
         json_string=None):
    """
    调用指定客户端的函数
    """
    if json_string is None:
        params = {}
    else:
        params = json.loads(json_string)

    end_time = time.time() + timeout
    while connections.get((appid, userid)) is None:
        remaining = end_time - time.time()
        if remaining <= 0.0:
            logger.warning(f"[函数调用失败] {userid}-{appid} 未连接 => {connections}")
            return json.dumps({"error_msg": f'{appid} 未连接 => {connections}'}, ensure_ascii=False)

    result = WeChatSocketHandler.send_message(connections[(appid, userid)], function_name, timeout=timeout,
                                              params=params)
    return json.dumps(result, ensure_ascii=False)


# Tornado WebSocket 应用
application = tornado.web.Application([
    (r"/", WeChatSocketHandler),
])

# WebSocket 服务端启动
WEBSOCKET_PORT = 22115
application.listen(WEBSOCKET_PORT)
logger.success(f"[WebSocket 服务端启动] 端口 => {WEBSOCKET_PORT}")
Thread(target=tornado.ioloop.IOLoop.instance().start).start()

# RPC 服务端启动c
RPC_PORT = 22116


class SafeXMLRPCServer(SimpleXMLRPCServer):
    def _dispatch(self, method, params):
        try:
            return super()._dispatch(method, params)
        except Exception as e:
            logger.error(f"[XMLRPC 错误] 方法: {method}, 参数: {params}, 异常: {e}")
            return {"error_msg": str(e)}


server = SimpleXMLRPCServer(("0.0.0.0", RPC_PORT), allow_none=True)
logger.success(f"[RPC 服务端启动] 端口 => {RPC_PORT}")
server.register_multicall_functions()
server.register_function(call, "call")
server.register_function(get_connections, "get_connections")
server.serve_forever()
