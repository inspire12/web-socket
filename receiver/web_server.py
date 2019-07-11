import socket
import argparse, sys
import threading, time
import codecs
# https://www.tutorialspoint.com/python/python_http_headers.htm
# 차후에 struct 로 http header 수정
# https://www.binarytides.com/raw-socket-programming-in-python-linux
# https://btyy.tistory.com/93
import struct


class Web:
    BUF_SIZE = 1024

    def __init__(self, args):
        self.options = str(args.options).upper() # 대문자여야한다.
        try:
            self.home_dir = args.home_dir
        except:
            self.home_dir = "template/welcome.html"

    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (('127.0.0.1', 8080))
        print (server_address)
        server_socket.bind(server_address)
        server_socket.listen(5)

        while True:
            (client, address) = server_socket.accept()
            client.settimeout(60)
            print("Recieved connection from {addr}".format(addr=address))
            threading.Thread(target=self._handle_client, args=(client, address)).start()

    def _handle_client(self, client, address):

        PACKET_SIZE = 1024
        while True:
            print("CLIENT",client)
            data = client.recv(PACKET_SIZE).decode()

            if not data: break

            request_method = data.split(' ')[0]
            print("Method: {m}".format(m=request_method))
            print("Request Body: {b}".format(b=data))

            if request_method == "GET" or request_method == "HEAD":
                filepath_to_serve = self.home_dir
                print("Serving web page [{fp}]".format(fp=filepath_to_serve))

                response_data =''
                # Load and Serve files content
                try:
                    f = open(filepath_to_serve, 'rb')
                    if request_method == "GET": # Read only for GET
                        response_data = f.read()
                    f.close()
                    response_header = self._generate_headers(200)

                except Exception as e:
                    print("File not found. Serving 404 page.")
                    response_header = self._generate_headers(404)

                    if request_method == "GET": # Temporary 404 Response Page
                        response_data = b"<html><body>404 NOT FOUND</body></html>"

                response = response_header.encode()
                if request_method == "GET":
                    response += response_data

                client.send(response)
                client.close()
                break
            else:
                print("Unknown HTTP request method: {method}".format(method=request_method))

    def _generate_headers(self, response_code):
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Server: Simple-Python-Server\n'
        header += 'Connection: close\n\n' # Signal that connection will be closed after completing the request
        return header


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--options", type=str)
    parser.add_argument("--home_dir", type=str)

    args = parser.parse_args()
    web = Web(args=args)
    web.run_server()


    # method = str(args.method).upper() # 대문자여야한다.
    # headers = args.headers
    # url = args.url
    # request_header, host, port = make_header(url)
    # request_socket(host, port, request_header)


