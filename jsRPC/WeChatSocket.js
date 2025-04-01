function send_message(msg) {
    wx.sendSocketMessage({
        data: JSON.stringify(msg)
    })
}

function FaasSendMessage(func, _uuid) {
    func({
        success: function (e) {
            send_message({uuid: _uuid, type: "success", data: e})
        },
        fail: function (e) {
            send_message({uuid: _uuid, type: "fail", data: e})
        }
    });
}

class websocket {
    constructor(opt) {
        //多久重连一次
        this.reTime = opt.reTime || 5000;
        //重连延迟函数序列
        this.settime = "";
        //是否连接成功
        this.isconnect = false;
        //心跳发送数据
        this.heartdata = opt.heartdata || {};
        //多久发送一次心跳
        this.heartbeatsettime = opt.hearttime || 1000 * 50;
        //心跳延迟函数序列
        this.heartstime = 0;
        //url
        this.url = opt.url || "";
        //是否关闭心跳代码
        this.colse = false;
        //发送信息回调
        this.success = opt.success || function (e) {
            console.log("success", e);
        };

        this.InfoSync = wx.getAccountInfoSync().miniProgram;
        this.userid = opt.userid || "";

        this.call_function_names = {
            "wx.login()": function (uuid) {
                FaasSendMessage(wx.login, uuid);
            },
            "wx.getUserCryptoManager().getLatestUserKey()": function (uuid) {
                FaasSendMessage(wx.getUserCryptoManager().getLatestUserKey, uuid);
            },
            "wx.getUserInfo()": function (uuid) {
                FaasSendMessage(wx.getUserInfo, uuid);
            },
        };
    }

    addFunctionToCallFunction(key, value) {
        if (typeof key !== 'string') {
            throw new Error('Key must be a string');
        }
        if (typeof value !== 'function') {
            throw new Error('Value must be a function');
        }
        this.call_function_names[key] = value;
    }

    //连接
    connect_socket() {
        return new Promise((suc, err) => {
            if (this.url) {
                wx.connectSocket({
                    url: `${this.url}`,
                    header: {
                        "appid": this.InfoSync.appId,
                        "userid": this.userid
                    },
                    success: task => {
                        //将websocket任务返回出去
                        this.monitor();
                        suc();
                    },
                    fail: err => {
                        console.log(1, err);
                        this.fails();
                        err();
                    }
                });
            } else {
                console.log("未输入地址");
                err();
            }
        });
    };

    //错误连接发生重连
    reconnect() {
        //必须先清理之前的定时器
        let that = this;
        clearTimeout(this.settime);
        //判断是否连接成功，成功则不再进行重新连接
        if (!this.isconnect) {
            //延迟发送
            this.settime = setTimeout(() => {
                that.connect_socket();
            }, this.reTime);
        }
    };

    //心跳发送
    heartbeat() {
        let sock = this.socket;
        //console.log(this.heartdata);
        //先清理之前的心跳
        clearTimeout(this.heartstime);
        this.heartstime = setTimeout(() => {
            wx.sendSocketMessage({
                data: JSON.stringify(this.heartdata),
                success: e => {
                    //发送成功则代表服务器正常
                    this.success();
                },
                fail: e => {
                    //发送失败则代表服务器异常
                    this.fails();
                }
            });
            //注意心跳多久一次
        }, this.heartbeatsettime);
    }

    //监听事件
    monitor() {
        //检测异常关闭则执行重连
        wx.onSocketError((e) => {
            console.log(e);
            this.fails();
        });
        wx.onSocketClose((e) => {
            console.log(e);
            this.fails();
        });
        //连接成功则设置连接成功参数
        wx.onSocketOpen(() => {
            //成功则关闭重连函数
            this.success();
            //首次连接发送数据
            wx.sendSocketMessage({
                data: JSON.stringify(this.heartdata),
                success: () => {
                    //发送成功则代表服务器正常
                    this.success();
                },
                fail: e => {
                    //发送失败则代表服务器异常
                    this.fails();
                }
            });
            //回调函数
        });
        //接收发送信息
        this.send_success();
    }


    send_success() {
        //监听发送心跳之后数据是否正常返回，返回则再发一次心跳
        wx.onSocketMessage(res => {
            // this.success(res);
            console.log('WebSocket接收到消息：', res.data)
            let res_json = JSON.parse(res.data)
            let TaskId = res_json["TaskId"]
            let call_function_name = res_json["function_name"]
            let uuid = `${TaskId}-${this.userid}-${this.InfoSync.appId}`;

            if (this.call_function_names[call_function_name]) {
                this.call_function_names[call_function_name](uuid)
            } else {
                send_message({
                    uuid: uuid,
                    type: "error",
                    data: `${call_function_name} not in [${Object.keys(this.call_function_names)}]`
                })
            }

            this.success();
        });
    }

    //成功的处理
    success() {
        this.isconnect = true;
        this.heartbeat();
    }

    //失败的处理
    fails() {
        if (!this.colse) {
            this.isconnect = false;
            this.reconnect();
        }
    }

}
SASDX
let _ws = new websocket({
    url: 'ws://127.0.0.1:22115',
    // 用户昵称
    userid: "滔博1"
})
_ws.connect_socket().then(r => console.log(r))
// 注册方法
_ws.addFunctionToCallFunction("function_demo", function (uuid) {
    send_message({uuid: uuid, data: "demo"})
})

