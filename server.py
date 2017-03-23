# -*- coding:utf-8 
_author_='lhw'
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys,io,os
class ServerException(Exception):
	#服务器内部错误
	pass
class case_no_file(object):
	#文件不存在，返回True
	def test(self,handler):
		return not os.path.exists(handler.full_path)
	def act(self,handler):
		#抛出异常，文件未找到
		raise ServerException('{0} not found'.format(handler.path))
class case_existing_file(object):
	#文件存在
	def test(self,handler):
		return os.path.isfile(handler.full_path)
	def act(self,handler):
		#处理该文件
		handler.handle_file(handler.full_path)
class case_always_fail(object):
	#所有情况都不符合时的默认处理类
	def test(self,handler):
		return True
	def act(self,handler):
		raise ServerException('Unknown Object {0}'.format(handler.path))
class case_directory_index_file(object):
	#浏览器访问根url的时候能返回工作目录下index.html的内容
	def index_path(self,handler):
		return os.path.join(handler.full_path,'index.html')
	#判断目标路径是否是目录 & 目录下是否有index.html
	def test(self,handler):
		return os.path.isdir(handler.full_path) and os.path.isfile(self.index_path(handler))
	def act(self,handler):
		#响应index.html
		handler.handle_file(self.index_path(handler))
class RequestHandler(BaseHTTPRequestHandler):
	# 所有可能的情况
	Cases = [case_no_file,
			case_existing_file,
			case_directory_index_file,
			case_always_fail]
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
			self.full_path=os.path.join(os.getcwd(),self.path.replace('/',''))
			#遍历所有可能的情况
			for case in self.Cases:
				#实例化
				handler=case()
				#是否符合情况
				if handler.test(self):
					#符合情况，进行相应处理
					handler.act(self)
					break			
		#处理异常
		except Exception as msg:
			self.handle_error(msg)
		
if __name__=='__main__':
	serverAddress=('',8080)
	server=HTTPServer(serverAddress,RequestHandler)
	print('Server started on 127.0.0.1,port 8080.....')
	server.serve_forever()