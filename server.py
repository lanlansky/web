# -*- coding:utf-8 
_author_='lhw'
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys,io,os
class ServerException(Exception):
	#服务器内部错误
	pass
class RequestHandler(BaseHTTPRequestHandler):
	#处理请求并返回页面
	Error_Page = '''\
		<html>
			<body>
				<h1>Error accessing {path}</h1>
				<p>{msg}</p>
			</body>
		</html>
	'''
	def send_content(self,page,status=200):
		self.send_response(status)
		self.send_header("Content-Type", "text/html")
		#需要将Page编码成bytes,否则报错
		#bytes解码会得到str str编码会变成bytes
		self.send_header("Content-Length", str(len(page)))
		#发送一个空白行，表明HTTP头响应结束
		self.end_headers()
		#以二进制进行读出的内容就是bytes，不用进行编码
		#判断page的类型，如果是str,需要进行编码
		if isinstance(page,str):
			page=page.encode('ascii')
		self.wfile.write(page)
	def handle_file(self,full_path):
		try:
			with open(full_path,'rb') as f:
				content=f.read()
			print(content)
			self.send_content(content)
		except Exception as msg:
			print(msg)
			msg='{0} cannot be read:{1}'.format(self.path,msg)
			self.handle_error(msg)
	def handle_error(self,msg):
		content=self.Error_Page.format(path=self.path,msg=msg)
		self.send_content(content,404)
	#处理一个get请求  重写的一个方法
	def do_GET(self):
		try:
			#文件的完整路径
			#full_path=os.getcwd()+self.path
			full_path=os.path.join(os.getcwd(),self.path.replace('/',''))
			#如果该路径不存在
			if not os.path.exists(full_path):
				#抛出异常，文件未找到
				raise ServerException('{0} not found'.format(self.path))
			#如果该路径是一个文件
			elif os.path.isfile(full_path):
				#处理该文件
				self.handle_file(full_path)
			else:
				#如果该路径不是一个文件		
				raise ServerException('Unknown Object {0}'.format(self.path))
		#处理异常
		except Exception as msg:
			print('存在异常')
			self.handle_error(msg)
		
if __name__=='__main__':
	serverAddress=('',8080)
	server=HTTPServer(serverAddress,RequestHandler)
	print('Server started on 127.0.0.1,port 8080.....')
	server.serve_forever()