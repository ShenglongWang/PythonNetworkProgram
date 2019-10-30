"""
@version:01.00.00
@Author:Shenglong
"""
import socket

def main():
    hostname = 'www.python.org'
    addr = socket.gethostbyname(hostname)
    print('The ip address of {} is {}'.format(hostname,addr))


if __name__ == '__main__':
    main()