"""
@version:01.00.00
@Author:Shenglong
"""
import argparse, socket

from datetime import  datetime
MAX_BYTES = 65535

def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind('127.0.0.1',port)
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address,text))
        text = 'Your data was {} bytes long'.format(len(data))
        data = text.encode('ascii')
        sock.sendto(data,address)

def client(port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    text = 'The time is {}'.format(datetime.now())
    data = text.encode('ascii')
    sock.sendto('127.0.0.1',port)
    print('The OS assigned me the address {}'.format(sock.getsockname()))
    data,address = sock.recvfrom(MAX_BYTES)
    text = data.decode('ascii')
    print('The server {} replied {!r}'.format(address,text))

def main():
    choices = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role',choices = choices, help = 'which role to play')
    parser.add_argument('-p',metavar = 'PORT', type = int, default = 1060,
                        help = 'UDp port(default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)



if __name__ == '__main__':
    main()