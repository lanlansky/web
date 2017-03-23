# -*- coding:utf-8 
_author_='lhw'
from http.server import HTTPServer, BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
	#处理请求并返回页面
	#页面模板
	Page='''\
		<html>
			<body>
				<p>Hello, web!</p>
			</body>
		</html>
	'''
	#处理一个get请求  重写的一个方法
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-Type", "text/html")
		#需要将Page编码成bytes,否则报错
		#bytes解码会得到str str编码会变成bytes
		self.send_header("Content-Length", str(len(self.Page)))
		#发送一个空白行，表明HTTP头响应结束
		self.end_headers()
		self.wfile.write(self.Page.encode('ascii'))
if __name__=='__main__':
	serverAddress=('',8080)
	server=HTTPServer(serverAddress,RequestHandler)
	print('Server started on 127.0.0.1,port 8080.....')
	server.serve_forever()