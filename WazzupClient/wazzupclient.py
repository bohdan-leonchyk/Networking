import socket


class WazzupClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print('Connected to {}:{}'.format(self.host, self.port))

        message = 'Wazzup!'

        self.socket.send(message)
        print('sent: {}'.format(message))
        data = self.socket.recv(1024)

        if data:
            print('received: {}'.format(data))
        else:
            print('no data received')
            self.socket.close()

if __name__ == '__main__':
    client = WazzupClient('localhost', 4242)

    try:
        client.connect()
    except socket.error:
        print('Invalid host or port')
