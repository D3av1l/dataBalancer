from queue import PriorityQueue

class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.pending_requests = PriorityQueue()

    def get_least_loaded_server(self, cpu_cost):
        suitable_servers = [server for server in self.servers if server.can_handle(cpu_cost)]
        if not suitable_servers:
            return None
        return min(suitable_servers, key=lambda server: server.get_load())

    def distribute_load(self, requests):
        for request, cpu_cost, priority in requests:
            self.pending_requests.put((priority, request, cpu_cost))

        self.process_pending_requests()

    def process_pending_requests(self):
        while not self.pending_requests.empty():
            priority, request, cpu_cost = self.pending_requests.get()
            server = self.get_least_loaded_server(cpu_cost)
            if server:
                server.handle_request(request, cpu_cost)
            else:
                self.pending_requests.put((priority, request, cpu_cost))
                break