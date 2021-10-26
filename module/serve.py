from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
 
# 实例化DummyAuthorizer来创建ftp用户
authorizer = DummyAuthorizer()
# 参数：用户名，密码，目录，权限
authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
# 匿名登录
#authorizer.add_anonymous('.')
 
handler = FTPHandler
handler.authorizer = authorizer
 
# 参数：IP，端口，handler
server = FTPServer(('192.168.0.103', 21), handler)
server.serve_forever()