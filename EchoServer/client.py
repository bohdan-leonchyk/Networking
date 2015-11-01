import threading


class Client(threading.Thread):
    def __init__(self, (client, address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address

    def get_address(self):
        return self.address

    def run(self):
        running = True

        while running:
            data = self.client.recv(1024)
            print('{} received: {}'.format(self.address, data))
            if data:
                self.client.send(data)
                print('{} sent: {}'.format(self.address, data))
                if data.strip() == 'disconnect':
                    self.client.close()
                    print('{} client disconnected'.format(self.address))
                    running = False
            else:
                self.client.close()
                print('{} client disconnected'.format(self.address))
                running = False
