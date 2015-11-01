from Route.route import *


class Router(object):
    def __init__(self, routes):
        self.routes = routes

    def add_route(self, route):
        self.routes.append(route)

    def get_route_for_address(self, address):
        current_route = None

        for route in self.routes:
            if route.get_network().contains(address):
                current_route = route
                crm_length = current_route.get_network().get_mask_length()
                rm_length = route.get_network().get_mask_length()

                if crm_length < rm_length:
                    current_route = route
                elif current_route.get_metric() > route.get_metric():
                    current_route = route

        return current_route

    def get_routes(self):
        return self.routes

    def remove_route(self, route):
        self.routes.remove(route)
