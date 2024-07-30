import tkinter as tk
from gui import ServerMonitorApp
from server import Server

def main():
    root = tk.Tk()
    servers = [Server(f"Server {i}", cpu_capacity=100) for i in range(3)]
    app = ServerMonitorApp(root, servers)
    root.mainloop()

if __name__ == "__main__":
    main()