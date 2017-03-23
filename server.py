# -*- coding:utf-8 
_author_='lhw'
from http.server import HTTPServer, BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
	#处理请求并返回页面
	#页面模板
	Page='''\
		<html>
			<body>
				<table>
					<tr>  <td>Header</td>         <td>Value</td>          </tr>
					<tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
					<tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
					<tr>  <td>Client port</td>    <td>{client_port}</td> </tr>
					<tr>  <td>Command</td>        <td>{command}</td>      </tr>
					<tr>  <td>Path</td>           <td>{path}</td>         </tr>
				</table>
			</body>
		</html>
	'''
	def create_page(self):
		values={
			'date_time'   : self.date_time_string(),
			'client_host' : self.client_address[0],
			'client_port' : self.client_address[1],
			'command'     : self.command,
			'path'        : self.path
		}
		#从format参数引入的变量名 类似于自动装填相同key值的数据
		page=self.Page.format(**values)
		return page

	def send_content(self,page):
		self.send_response(200)
		self.send_header("Content-Type", "text/html")
		#需要将Page编码成bytes,否则报错
		#bytes解码会得到str str编码会变成bytes
		self.send_header("Content-Length", str(len(page)))
		#发送一个空白行，表明HTTP头响应结束
		self.end_headers()
		self.wfile.write(page.encode('ascii'))

	#处理一个get请求  重写的一个方法
	def do_GET(self):
		page=self.create_page()
		self.send_content(page)
		
if __name__=='__main__':
	serverAddress=('',8080)
	server=HTTPServer(serverAddress,RequestHandler)
	print('Server started on 127.0.0.1,port 8080.....')
	server.serve_forever()