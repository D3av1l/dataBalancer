class Server:
    def __init__(self, name, cpu_capacity):
        self.name = name
        self.cpu_capacity = cpu_capacity  # Capacidad total de CPU
        self.cpu_load = 0  # Carga actual de CPU
        self.total_cpu_processed = 0  # Total de CPU procesada
        self.cpu_processed_per_turn = 0  # CPU procesada por turno
        self.requests = []

    def handle_request(self, request, cpu_cost):
        if self.cpu_load + cpu_cost <= self.cpu_capacity:
            self.cpu_load += cpu_cost
            self.total_cpu_processed += cpu_cost
            self.cpu_processed_per_turn += cpu_cost
            self.requests.append(request)
        else:
            print(f"Server {self.name} cannot handle request {request} due to insufficient CPU capacity")

    def get_load(self):
        return self.cpu_load

    def reset_load(self):
        self.cpu_load = 0
        self.requests.clear()

    def reset_cpu_processed_per_turn(self):
        self.cpu_processed_per_turn = 0

    def can_handle(self, cpu_cost):
        return self.cpu_load + cpu_cost <= self.cpu_capacity

    def get_total_cpu_processed(self):
        return self.total_cpu_processed

    def get_cpu_processed_per_turn(self):
        return self.cpu_processed_per_turn