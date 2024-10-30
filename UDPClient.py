#UDPClient.py
import socket as sk
import argparse
import os
# os提供了与操作系统交互的接口，用于文件操作、执行系统命令等

def UDPClient(server_ip, server_port, filepath, buffer_size=32768):
    client_socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

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

    print(f"File {file_name} sent successfully to {server_ip}:{server_port}")

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