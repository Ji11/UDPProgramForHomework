# github地址 https://github.com/Ji11/UDPProgramForHomework

# 运行环境：
# Python 3.11.4
# Server: Vmware Workstation 17 Pro, Ubuntu 20.04 LTS
# Client: Windows 11 Home 23H2

# 使用方法：
# 命令行运行：python UDPClient.py server_ip server_port filepath
# 支持的文件传输格式：文本文件、二进制文件、压缩包等

# 已包含了UDP对TCP连接建立、释放的模拟实现，每个分组发送前都会进行ACK确认，避免丢包

#UDPClient.py
import socket as sk
import argparse
import time 
# 用于延迟执行
import os
# os提供了与操作系统交互的接口，用于文件操作、执行系统命令等

def UDPClient(server_ip, server_port, filepath, buffer_size=32768, delay=0.01):
    client_socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    ack_count = 0  # 初始化ACK计数器

    client_socket.sendto("CONNECT".encode(), (server_ip, server_port))
    data, server_addr = client_socket.recvfrom(buffer_size)
    # 确认连接 若未收到则不进行传输
    if data.decode()!= "ACK":
        print("Connection failed")
        return
    
    print("Connection established")

    # 获取文件名和文件大小
    # os.path.basename()用于获取路径中的文件名，返回路径中最后的部分（即文件名）
    # os.path.getsize()用于获取文件的大小，返回文件的字节数
    file_name = os.path.basename(filepath)
    file_size = os.path.getsize(filepath)

    client_socket.sendto(file_name.encode(), (server_ip, server_port))
    client_socket.sendto(str(file_size).encode(), (server_ip, server_port))

    with open(filepath, "rb") as f:
        sent_size = 0
        while sent_size < file_size:
            data = f.read(buffer_size)
            client_socket.sendto(data, (server_ip, server_port))
            sent_size += len(data)
            print(f"Sending {sent_size}/{file_size} bytes...")
            # time.sleep(delay)
            # 延迟执行，已经发现过快的client端传输，而server端接受速度不匹配导致丢包
            # 上网查询得到此种解决方法，在发送数据前加入延迟，使得server端有足够的时间来接受数据

            # 等待服务器确认
            ack, server_addr = client_socket.recvfrom(buffer_size)
            if ack.decode() != "ACK":
                print("Failed to receive ACK, resending packet...")
                client_socket.sendto(data, (server_ip, server_port))  # 重发数据包
            else:
                ack_count += 1  # 增加ACK计数
                print(f"ACK #{ack_count} received, sending next packet.")


    print(f"File {file_name} sent successfully to {server_ip}:{server_port}")
    print(f"Total ACKs received: {ack_count}")

    # 连接释放
    data, server_addr = client_socket.recvfrom(buffer_size)
    if data.decode() == "DISCONNECT":
        print("Connection closed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Client")
    parser.add_argument("server_ip", type=str, help="Server IP address")
    parser.add_argument("server_port", type=int, help="Server port")
    parser.add_argument("filepath", type=str, help="Path to the file to send")
    args = parser.parse_args()

    UDPClient(args.server_ip, args.server_port, args.filepath)