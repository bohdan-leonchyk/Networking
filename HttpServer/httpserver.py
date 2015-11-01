from parse import parse
import socket
import time


class HttpServer(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.http_conf = None
        self.file_name = None
        self.content_text = None

    def start(self):
        self.http_conf = parse('http.conf')
        address = self.http_conf.get('address')
        port = self.http_conf.get('port')
        self.sock.bind((address, int(port)))
        self.sock.listen(1)

        print('Server started: {}:{}'.format(address, port))

        conn, addr = self.sock.accept()
        print('Connected client: {}:{}'.format(addr[0], addr[1]))

        try:
            while True:
                data = conn.recv(1024)
                print(data)
                self.content_text = data.split()

                if self.content_text[0] == 'GET':
                    if len(self.content_text) > 2:
                        http_version = self.content_text[2]
                        if http_version != 'HTTP/1.1':
                            conn.send(self.answer_id(405))
                        else:
                            print('Host: ' + addr[0])
                            conn.send(self.get_answer())
                    else:
                        conn.send(self.answer_id(405))
        except IndexError:
            print('Server closed')

    def answer_id(self, id):
        if id == 405:
            return '405 Method Not Allowed\n'
        if id == 404:
            return '404 Not Found\n'
        if id == 200:
            return '{} 200 OK\n'.format(self.content_text[2])

    def get_answer(self):
        try:
            file_name = self.content_text[1].rsplit('/', 1)[1]
            self.file_name = file_name
            file_extension = file_name.rsplit('.', 1)[1]
        except IndexError:
            return self.answer_id(404)

        try:
            with open(self.http_conf.get('root_dir') + file_name) as f:
                c_time = str(time.strftime('%a, %d %b %Y %H:%M:%S %Z'))
                header = (
                    '{}'
                    'Connection: close\n'
                    'Content-Length: {}\n'
                    'Content-Type: {}\n'
                    'Date: {}\n'.format(
                        self.answer_id(200),
                        str(len(f.read())),
                        self.mime_type(file_extension),
                        c_time
                    )
                )
                f.seek(0)
                send_data = header + f.read()
                return send_data
        except IOError:
            return self.answer_id(404)

    @staticmethod
    def mime_type(file_extension):
        mime = parse('mime.types')
        if file_extension in mime:
            return mime.get(file_extension)
        return 'application/octet-stream'


if __name__ == '__main__':
    server = HttpServer()

    try:
        server.start()
    except KeyboardInterrupt:
        print('Server closed')
