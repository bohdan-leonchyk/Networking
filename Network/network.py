from IPv4Address.ipv4address import *


class Network(object):
    def __init__(self, address, mask_length):
        if mask_length < 0 or mask_length > 32:
            raise Exception('Invalid mask length')

        self.mask_length = mask_length
        self.mask = ~((1L << 32 - self.mask_length) - 1) & 0xffffffffL
        self.inverted_mask = ~self.mask & 0xffffffffL
        self.nw_address = IPv4Address(address.to_long() & self.mask)
        self.bc_address = IPv4Address(address.to_long() | self.inverted_mask)
        self.private_networks = None

    def contains(self, address):
        return self.nw_address.to_long() == (address.to_long() & self.mask)

    def to_string(self):
        return '{}/{}'.format(self.nw_address.to_string(), self.mask_length)

    def get_address(self):
        return self.nw_address

    def get_broadcast_address(self):
        return self.bc_address

    def get_first_usable_address(self):
        if self.mask_length == 32:
            return self.nw_address
        elif self.mask_length == 31:
            return None
        return IPv4Address(self.nw_address.to_long() + 1)

    def get_last_usable_address(self):
        if self.mask_length == 32:
            return self.nw_address
        elif self.mask_length == 31:
            return None
        return IPv4Address(self.bc_address.to_long() - 1)

    def get_mask(self):
        return self.mask

    def get_mask_string(self):
        return (IPv4Address(self.mask)).to_string()

    def get_mask_length(self):
        return self.mask_length

    def get_subnets(self):
        new_mask_length = self.mask_length + 1

        subnets = (
            Network(self.nw_address, new_mask_length),
            Network(self.bc_address, new_mask_length)
        )
        return subnets

    def get_total_hosts(self):
        if self.mask_length == 32:
            return 1
        elif self.mask_length == 31:
            return 0
        return self.inverted_mask - 1

    def is_public(self):
        if self.private_networks is None:
            self.private_networks = (
                Network(IPv4Address('10.0.0.0'), 8),
                Network(IPv4Address('127.0.0.0'), 8),
                Network(IPv4Address('172.16.0.0'), 12),
                Network(IPv4Address('192.168.0.0'), 16)
            )

        for network in self.private_networks:
            if network.contains(self.nw_address):
                return False
        return True
