"""
@version:01.00.00
@Author:Shenglong
该程序中的服务器并未始终响应客户端的请求，而是随机选择，只对收到的-半
客户端请求作出响应。

客户端会设置timeout参数，如果超时，会进入指数避让，重新赋值timeout的delay值
客户端会在接收服务器的数据时，等待delay时间。

运行方式：
服务器端： python 2_2_udp_remote.py server ""   # ""表示本机上的任何接口

客户端： python 2_2_udp_remote.py client "127.0.0.1"

"""
import argparse, random, socket, sys


MAX_BYTES = 65535
def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at ', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        if random.random() < 0.5:
            print('Pretending to drop packet from {}'.format(address))
            continue
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        message = 'Your data was {} bytes long'.format(len(data))
        sock.sendto(message.encode('ascii'),address)


def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = sys.argv[2]
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))

    delay = 0.1
    text = 'This is another message'
    data = text.encode('ascii')
    while True:
        sock.send(data)
        print('Waiting up to {} seconds for a repley'.format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout:
            delay *= 2 #wait even longer for the next request
            if delay > 2.0:
                raise RuntimeError('I think the server is down')
        else:
            break  # we are done, and can stop looping

    print('The server says {!r}'.format(data.decode('ascii')))



def main():

    choices = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description='send and receive UDP,'
                                                 ' pretending packets are often dropped')
    parser.add_argument('role',choices=choices,help='which role to take')
    parser.add_argument('host',help = 'interface the server listens at;'
                                      'host the client sends to')
    parser.add_argument('-p',metavar = 'PORT',type = int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host,args.p)



if __name__ == '__main__':
    main()


'''
套接字操作connect()
如果使用sendto()，那么每次向服务器发送消息时都必须显式的给出服务器IP和端口。
而如果使用connect()调用,那么操作系统事先就已经知道数据包要发送到的远程地址，
这样就可以简单地把要发送的数据作为参数传入send()调用，无需重复给出服务器地址。

另外，connect()还解决了客户端混杂性这一问题，一旦运行了connect()，那么只要
操作系统发现传入数据包的返回地址与已连接的地址不同，就会将该数据包丢弃。


编写对响应数据包地址进行仔细检查的UDP客户端，有两种方法：
（1）可以使用sendto()指定每个数据包的目标地址，然后使用recvfrom()接受响应，
并仔细检查响应数据包的返回地址，看看是否之前想该地址发过请求。
（2）可以在创建套接字后使用connect()将其与目标地址连接，然后使用send()和recv()
进行通信。操作系统会将不需要的数据包过滤掉。这种方法只支持同时与一台服务器交互
的情况，再次运行connect()，会把之前的目标地址覆盖掉。

'''

