import json
import xmlrpc.client

from loguru import logger

RPC = xmlrpc.client.ServerProxy("http://127.0.0.1:22116/")


def RpcCall(username: str = "测试", appid: str = "wxc9c692c952025897", function_name: str = "wx.login()",
            timeout: int = 5, **kwargs):
    result = RPC.call(username, appid, function_name, timeout, json.dumps(kwargs))
    try:
        return json.loads(result)
    except Exception as e:
        return {"data": result, "err_msg": e}


def GetSockets():
    return RPC.get_connections()


logger.debug(GetSockets())

result = RpcCall(username="滔博1", appid="wx887bf6ad752ca2f3", function_name="wx.login()")
logger.info(result)

# result = RpcCall(username="滔博1", appid="wx71a6af1f91734f18", function_name="wx.getUserCryptoManager().getLatestUserKey()")
# logger.info(result)

# result = RpcCall(
#     username="滔博1",
#     appid="wx96cbe8b2db62b578",
#     function_name="wx.cloud.callFunction()",
#     name="http",
#     data={
#         "url": 'http://10.10.0.21/api/key/fetch',
#         "method": 'POST',
#         "data": {"openid": '...'},
#         "headers": {
#             "openid": '...',
#             "traceId": '...'
#         },
#         "intStartTime": 1725866423981
#     }
# )
# logger.info(result)
