from Network.network import *


class Route(object):
    def __init__(self, network, gateway, interface_name, metric):
        if (network is None) or (interface_name is None):
            raise Exception('Argument missed')

        if metric < 0:
            raise Exception('Wrong metric value')

        self.network = network
        self.gateway = gateway
        self.interface_name = interface_name
        self.metric = metric

    def get_gateway(self):
        return self.gateway

    def get_interface_name(self):
        return self.interface_name

    def get_metric(self):
        return self.metric

    def get_network(self):
        return self.network

    def to_string(self):
        if self.gateway is None:
            return 'net: {} interface: {} metric {}'.format(
                self.network.to_string(),
                self.interface_name,
                self.metric
            )
        return 'net: {} gateway: {} interface: {} metric {}'.format(
            self.network.to_string(),
            self.gateway.to_string(),
            self.interface_name,
            self.metric
        )
