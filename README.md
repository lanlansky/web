# web
Python3 实现一个简单的web服务器
# 教程
网址 https://zhuanlan.zhihu.com/p/21323273
# 注意
* BaseHTTPServer模块在Python3中已被合并到http.server。在引入的时候应该是</br>
```
from http.server import HTTPServer, BaseHTTPRequestHandler
```
* 在do_GET函数中，发送Page内容时，应发送bytes,不应该是str。也就是需要对Page进行编码
```
self.wfile.write(self.Page.encode('ascii'))
``` 
# 新接触的库
* `http.server` python3中内建的HTTP servers</br>
* `httpie` 是一个命令行下的HTTP客户端。可以在命令行提供与图形界面一样友好的网络服务交互，可用在HTTP服务器的测试、调试中。
