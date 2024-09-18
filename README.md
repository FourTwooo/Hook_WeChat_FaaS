# Hook_WeChat_FaaS
frida Hook 微信云函数脚本

![cesi](https://github.com/user-attachments/assets/99219d31-882f-4948-b124-09f7266c877c)
![pycesi](https://github.com/user-attachments/assets/2be95b69-2773-4165-a8c9-8b2cc23b32e6)


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
    frida -UF -l .\Hook_WeChat_FaaS.js --no-pause
```

## 目前问题

主动调用可能调用部分api会存在bug
  
涉及微信多开的hook 暂时未适配
  
这个项目也是因为公司业务有需求 临时开发. 开源了有自己想法的可以自己二次开发


## 参考文章

 - [看雪论坛 作者ID：Sharp_Wang](https://mp.weixin.qq.com/s/7yZzf4V-2fcn-jRwm4uO-w)

## 支持

实际上并没有多少技术含量. 其实就是HOOK了 请求和响应的代码位置. 没有什么技术含量

<a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=6JWWosRVV0rtISqQKNVU5QY8KT0sBQP8&jump_from=webapi&authKey=kvD0trmJvJiWSeFVv1+WTUYBpalYGKh+dF3zgfpLDuByEmZF2wT8XXwC8QuT/tzQ"><img border="0" src="//pub.idqqimg.com/wpa/images/group.png" alt="逆向交流学习" title="逆向交流学习"></a>    QQ交流群: 1021904342

