import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import time
from load_balancer import LoadBalancer
from server import Server

class ServerMonitorApp:
    def __init__(self, root, servers):
        self.root = root
        self.servers = servers
        self.load_balancer = LoadBalancer(servers)
        self.root.title("Server Load Monitor")

        self.fig, self.axs = plt.subplots(len(servers) + 1, 1, figsize=(12, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.info_frame = tk.Frame(root)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        self.info_labels = [tk.Label(self.info_frame, text="", font=("Helvetica", 14)) for _ in servers]
        for label in self.info_labels:
            label.pack(pady=10)

        self.queue_info_label = tk.Label(self.info_frame, text="", font=("Helvetica", 14))
        self.queue_info_label.pack(pady=10)

        self.cpu_loads_history = {server.name: [] for server in servers}
        self.incoming_cpu_load_history = []

        self.update_graph()

    def generate_random_requests(self):
        num_requests = random.randint(1, 40)
        requests = [(f"req{random.randint(1, 1000)}", random.randint(1, 20), random.randint(1, 20)) for _ in range(num_requests)]
        return requests

    def update_graph(self):
        requests = self.generate_random_requests()
        total_cpu_cost = sum(cpu_cost for _, cpu_cost, _ in requests)
        self.incoming_cpu_load_history.append(total_cpu_cost)

        self.load_balancer.distribute_load(requests)
        self.load_balancer.process_pending_requests()

        for server in self.servers:
            self.cpu_loads_history[server.name].append(server.get_load())

        for i, server in enumerate(self.servers):
            self.axs[i].clear()
            self.axs[i].plot(self.cpu_loads_history[server.name], label=f"{server.name} CPU Load", linewidth=2)
            self.axs[i].set_ylim(0, server.cpu_capacity)
            self.axs[i].set_ylabel('CPU Load', fontsize=12)
            self.axs[i].legend(loc='upper right', fontsize=12)

            self.info_labels[i].config(text=f"{server.name}\nCurrent Load: {server.get_load()}\nTasks: {len(server.requests)}")

        self.axs[-1].clear()
        self.axs[-1].plot(self.incoming_cpu_load_history, label="Incoming CPU Load", linewidth=2)
        self.axs[-1].set_ylabel('CPU Load', fontsize=12)
        self.axs[-1].legend(loc='upper right', fontsize=12)

        pending_requests = list(self.load_balancer.pending_requests.queue)
        pending_count = len(pending_requests)
        pending_cpu_cost = sum(cpu_cost for _, _, cpu_cost in pending_requests)
        self.queue_info_label.config(text=f"Pending Requests: {pending_count}\nTotal CPU Cost: {pending_cpu_cost}")

        self.canvas.draw()

        for server in self.servers:
            server.reset_load()
            server.reset_cpu_processed_per_turn()

        self.root.after(1000, self.update_graph)

if __name__ == "__main__":
    root = tk.Tk()
    servers = [Server(f"Server {i}", cpu_capacity=100) for i in range(3)]
    app = ServerMonitorApp(root, servers)
    root.mainloop()