import rpyc

class LoadBalancer():
    def __init__(self):
        self.services = self.get_slave_services()
        self.index = 0

    def get_slave_services(self):
        services = rpyc.list_services()
        services = [s for s in services if 'SLAVE' in s]
        return services

    def get_next_service(self):
        service = self.services[self.index]
        self.index = self.index + 1
        if self.index == len(self.services):
            self.index = 0
        return service

    def forward_request(self):
        service = self.get_next_service()
        slave_config = rpyc.discover(service)
        ip, port = slave_config[0]
        return service, ip, port

