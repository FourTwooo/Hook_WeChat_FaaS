# Hook_WeChat_FaaS
frida Hook 微信云函数脚本


## 环境

开发测试环境. 理论来说 安卓APP应该是不限版本 通用的

 - Android => 10

- frida => 14.2.18

- 微信安卓APP => 8.0.49



## 运行


在小程序界面时运行以下命令或使用进程ID去运行
```
    frida -UF -l .\Hook_WeChat_FaaS.js com.tencent.mm --no-pause
```

## 目前问题

主动调用那块 我是使用Java.choose 从内存中取的实例 但在内存中的实例有很多个  
所以每次主动调用 都会触发好几次. 但其实只会成功一个 其他的不会成功 这个暂时没弄清楚为什么
  
如果要Hook多个小程序, 会存在问题. 我自己机型来看 打开多个小程序 进程ID是完全一样的 除了包名不一样
更别谈涉及微信多开这个问题
  
这些问题 在上班时间 我会逐步修复. 这个项目也是因为公司业务有需求 临时开发. 开源了有自己想法的可以自己二次开发


## 参考文章

 - [看雪论坛 作者ID：Sharp_Wang](https://mp.weixin.qq.com/s/7yZzf4V-2fcn-jRwm4uO-w)

## 支持

实际上并没有多少技术含量. 其实就是HOOK了 请求和响应的代码位置. 没有什么技术含量
但是很多人都没有选择开源(至少我不知道有谁).

开源不易, 可以的话支持以下
![](https://github.com/FourTwooo/Hook_WeChat_FaaS/blob/main/wx.jpg?raw=true)
  
QQ交流群: 1021904342
