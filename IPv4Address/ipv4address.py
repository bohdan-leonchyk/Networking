import socket
import struct


class IPv4Address(object):
    def __init__(self, address):
        self.string_ip = self.convert_to_string(address)
        self.long_ip = self.convert_to_long(address)

    def convert_to_long(self, address):
        if isinstance(address, (int, long)):
            return address
        return struct.unpack('!L', socket.inet_aton(address))[0]

    def convert_to_string(self, address):
        if isinstance(address, str):
            return address
        return socket.inet_ntoa(struct.pack('!L', address))

    def less_than(self, address):
        return self.long_ip < self.convert_to_long(address)

    def greater_than(self, address):
        return self.long_ip > self.convert_to_long(address)

    def equals(self, address):
        return self.long_ip == self.convert_to_long(address)

    def to_string(self):
        return self.string_ip

    def to_long(self):
        return self.long_ip

if __name__ == '__main__':
    ip = IPv4Address('127.12.45.22')

    print(ip.to_string())
    print(ip.to_long())

    ip = IPv4Address(2131504406)

    print(ip.to_string())
    print(ip.to_long())
    print(ip.equals("127.12.45.22"))
    print(ip.equals(2131504406L))
    print(ip.equals(0xF834AD02L))
    print(ip.equals("189.11.23.211"))
    print(ip.greater_than("131.16.34.66"))
    print(ip.less_than("131.16.34.66"))
