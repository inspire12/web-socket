import socket
import argparse, sys
# https://www.tutorialspoint.com/python/python_http_headers.htm
# 차후에 struct 로 http header 수정
# https://www.binarytides.com/raw-socket-programming-in-python-linux
# https://btyy.tistory.com/93
import struct


class Web:
    BUF_SIZE = 1024

    def __init__(self, args):
        self.method = str(args.method).upper()  # 대문자여야한다.
        self.headers = args.headers
        print(self.headers)
        self.url = args.url

    def run(self):
        request_header, host, port = self.make_header()
        self.request_socket(host, port, request_header)

    def __parse_url(self):
        url = self.url.split("://")[1]
        tmp = url.split(":")
        host = tmp[0]
        port = tmp[1].split("/")[0]
        path = tmp[1].split("/")[1]
        return host, int(port), path

    def request_socket(self, host, port, request_header):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ((socket.gethostbyname(host), port))
        client_socket.connect(server_address)
        client_socket.send(request_header)
        response = ''
        while True:
            recv = client_socket.recv(Web.BUF_SIZE)
            if not recv:
                break
            response += str(recv)

        print(response)
        client_socket.close()

    def make_header(self):
        # args = sys.argv[1:]
        host, port, path = self.__parse_url()
        print(host, port, path)
        request_header = ("{} / HTTP/1.0\nHost: {}\nPath:{}\n{}\n\n".format(self.method, host, path, self.headers))
        return request_header.encode(), host, port


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", type=str)
    parser.add_argument("--headers", type=str)
    parser.add_argument("--url", type=str)
    args = parser.parse_args()
    web = Web(args=args)
    web.run()

    # method = str(args.method).upper() # 대문자여야한다.
    # headers = args.headers
    # url = args.url
    # request_header, host, port = make_header(url)
    # request_socket(host, port, request_header)
