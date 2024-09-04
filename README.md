# Hook_WeChat_FaaS
frida Hook 微信云函数脚本

![](https://raw.githubusercontent.com/FourTwooo/Hook_WeChat_FaaS/main/images/cesi.png)

![](https://raw.githubusercontent.com/FourTwooo/Hook_WeChat_FaaS/main/images/pycesi.png)

## 环境

~~开发测试环境. 理论来说 安卓APP应该是不限版本 通用的~~

(appid hook点并不是通用, 如果只是需要app抓包的需求只需要使用目录中的 Hook_WeChat_FaaS.js, 不要使用frida_js下的)

 - Android => 10

- frida => 14.2.18

- 微信安卓APP => 8.0.49

python开发环境详见 requirements.txt


## 运行


在小程序界面时运行以下命令或使用进程ID去运行
```
    frida -UF -l .\Hook_WeChat_FaaS.js com.tencent.mm --no-pause
```

## 目前问题

主动调用可能调用部分api会存在bug
  
涉及微信多开的hook 暂时未适配
  
这个项目也是因为公司业务有需求 临时开发. 开源了有自己想法的可以自己二次开发


## 参考文章

 - [看雪论坛 作者ID：Sharp_Wang](https://mp.weixin.qq.com/s/7yZzf4V-2fcn-jRwm4uO-w)

## 支持

实际上并没有多少技术含量. 其实就是HOOK了 请求和响应的代码位置. 没有什么技术含量

可以的话支持以下
![](https://github.com/FourTwooo/Hook_WeChat_FaaS/blob/main/images/wx.jpg?raw=true)
  
QQ交流群: 1021904342
