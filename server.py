import socket
import threading

#创建服务器类
class HttpWebServer(object):
    def __init__(self,port):
        # 创建tcp服务端套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口号复用程序退出，端口号立即释放
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口号
        self.tcp_server_socket.bind(("", port))
        # 设置监听
        self.tcp_server_socket.listen(128)

    # 处理客户端请求
    @staticmethod
    def handle_client_request(new_socket):
        recv_data = new_socket.recv(4096)
        # 判断接受数据的长度是否为0
        if len(recv_data) == 0:
            new_socket.close()
            return
        # 对二进制数据进行解码
        recv_context = recv_data.decode("utf-8")
        # 对数据按照空格进行分割
        request_list = recv_context.split(" ", 2)
        # 获取请求资源的路径
        request_path = request_list[1]
        # print(request_path)

        # 判断请求的是否为根目录,如果是根目录设置返回的信息
        if request_path == '/':
            request_path = "/元宇宙/index.html"
        # 1、os.path.exits
        # os.path.exists("static/" + request_path)
        # 2、异常
        #print(request_path)
        try:
            # 打开文件读取数据
            with open("static" + request_path, 'rb') as f:
                file_data = f.read()
        except Exception as e:
            # 代码执行至此说明无此资源返回404
            # 响应行
            response_line = "HTTP/1.1 404 Not Found\r\n"
            # 响应头
            response_header = "Server: PWS/1.0\r\n"
            # 响应体
            with open("static/404.html", 'rb') as f:
                error_data = f.read()
            response_body = error_data
            # 把数据封装成HTTP响应报文
            response = (response_line + response_header + "\r\n").encode("utf-8") + response_body
            # 发送给浏览器的响应头报文数据
            new_socket.send(response)
        else:
            # 代码执行至此说明文件存在
            # 提示安全的打开文件
            # 响应行
            response_line = "HTTP/1.1 200 OK\r\n"
            # 响应头
            response_header = "Server: PWS/1.0\r\n"
            # 空行
            # 响应体
            response_body = file_data
            # 把数据封装成HTTP响应报文
            response = (response_line + response_header + "\r\n").encode("utf-8") + response_body
            # 发送给浏览器的响应头报文数据
            new_socket.send(response)
        finally:
            # 关闭服务于客户端的套接字
            new_socket.close()

    #启动服务器方法
    def start(self):
        # 循环等待接受客户端的请求
        while True:
            # 接受客户端的连接请求
            new_socket, ip_port = self.tcp_server_socket.accept()
            # 代码执行到此说明连接建立成功
            # 建立子线程
            sub_thread = threading.Thread(target=self.handle_client_request, args=(new_socket,))
            # 设置守护主线程
            sub_thread.setDaemon(True)
            # 启动子线程对应的任务
            sub_thread.start()
#函数主方法
def main():
    #获取终端命令行参数
    params = input("请输入端口号:")
    # print(params)
    #判断第二个参数是否都是由数字组成的字符串
    while True:
        if not params.isdigit():
            print("请输入正确的端口号!!!（纯数字）")
            params = input("请输入端口号:")
        else:
            break
    # 代码执行至此说明命令行参数的个数一定是两个,并且参数合理
    port = int(params)

    #服务器类实例化
    web_server = HttpWebServer(port)
    #启动服务器
    web_server.start()



#判断是否是主模块
if __name__ == '__main__':
    main()

