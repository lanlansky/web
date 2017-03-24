# web
Python3 实现一个简单的web服务器
# 教程
网址 https://zhuanlan.zhihu.com/p/21323273
# 注意
* BaseHTTPServer模块在Python3中已被合并到http.server。在引入的时候应该是</br>
```
from http.server import HTTPServer, BaseHTTPRequestHandler
```
* 在步骤一的do_GET函数中，发送Page内容时，应发送bytes,不应该是str。也就是需要对Page进行编码
```
self.wfile.write(self.Page.encode('ascii'))
``` 
* 在步骤三的send_content函数中，发送page内容时，应先判断page的数据类型。如果是str,应先进行编码
```python
if isinstance(page,str):
    page=page.encode('ascii')
```
* 在步骤三获取文件的完整路径的时候，os.getcwd() 得到的是类似于E:\python\web，self.path得到的是 /index.html.所以
```python
os.getcwd()+self.path
```
>> 得到的并不是正确的路径，我对self.path进行了处理，然后进行路径拼接
```
full_path=os.path.join(os.getcwd(),self.path.replace('/',''))
```
* 在步骤四中，设置的所有可能的情况Cases里面每个数据不应该带有()。</br>
  如果带有()，Cases[i]就是一个函数的实例化，后续的调用不能是  handler=case()
# 新接触的库
* `http.server` python3中内建的HTTP servers</br>
* `httpie` 是一个命令行下的HTTP客户端。可以在命令行提供与图形界面一样友好的网络服务交互，可用在HTTP服务器的测试、调试中。
* `subprocess` 进程库
