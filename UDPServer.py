# github地址 https://github.com/Ji11/UDPProgramForHomework

# 运行环境：
# Python 3.11.4
# Server: Vmware Workstation 17 Pro, Ubuntu 20.04 LTS
# Client: Windows 11 Home 23H2

#UDPServer.py
import socket as sk
import argparse

def UDPServer(host, port, buffer_size=32768):
    server_socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    server_socket.bind((host, port))
    print("Server is listening on {}:{}".format(host, port))

    while True:
        # 接收文件名与大小
        data, client_addr = server_socket.recvfrom(buffer_size)
        # recvfrom()的参数是缓冲区大小，即一次最多接收多少字节的数据
        # recvfrom()的返回值是一个元组，第一个元素是接收到的数据，第二个元素是客户端的地址
        if data.decode() == "CONNECT":
            # 下面的一切建立在确认连接的基础上
            print(f"Connection request received from {client_addr}")
            server_socket.sendto("ACK".encode(), client_addr)
            print("Connection established")

            data, client_addr = server_socket.recvfrom(buffer_size)
            file_name = data.decode()

            data, client_addr = server_socket.recvfrom(buffer_size)
            file_size = int(data.decode())
            # decode()用于将二进制数据（bytes类型）转换为字符串（str类型）
            # 所以decode()的返回值是str类型，需要转换为int类型

            # with语句，是一种上下文管理器，可以自动关闭文件，避免忘记关闭文件
            # 不用写f.close()了
            # as f：将打开的文件对象赋给变量f
            with open(file_name, "wb") as f:
            # wb表示以二进制写入模式打开文件
                received_size = 0
                while received_size < file_size:
                    data, client_addr = server_socket.recvfrom(buffer_size)
                    f.write(data)
                    received_size += len(data)
                    print(f"Receiving {received_size}/{file_size} bytes...")
            
            print(f"File {file_name} received successfully from {client_addr}")

            # 关闭连接
            server_socket.sendto("DISCONNECT".encode(), client_addr)
            print("Connection closed")


# 主函数
# 这行if的作用：
# 在Python中，每个模块（文件）都有一个内置的变量__name__，表示模块的名称
# 如果本文件在命令行中被直接运行，那么__name__的值会被设置为"__main__"
# 如果本文件被其他文件导入，那么__name__的值会被设置为模块的名称，而不是"__main__"
# 所以在本次实验中这行if没有什么作用，但在日后的工程开发中会用到
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Server")
    parser.add_argument("host", type=str, help="Server host")
    parser.add_argument("port", type=int, help="Server port")
    args = parser.parse_args()

    UDPServer(args.host, args.port)
# parser的作用：
# 第34行是创建了一个参数解析器对象，会读取命令行输入的参数，然后将其解析成Python对象
# 第35行、36行是为解析器添加了两个参数，分别是host和port，类型都是字符串
# 第37行是解析命令行输入的参数，解析完后，这些参数就储存在args这个对象中
# 最后调用函数