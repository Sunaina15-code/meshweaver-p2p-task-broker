# MeshWeaver - Dashboard
# Live CLI dashboard using Rich

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime

console = Console()

class MeshDashboard:
    def __init__(self):
        self.nodes = {}
        self.tasks = []

    def add_node(self, node_id, host, port, cpu=0, status="active"):
        self.nodes[node_id] = {
            'host': host, 'port': port,
            'cpu': cpu, 'status': status,
            'last_seen': datetime.now().strftime("%H:%M:%S")
        }

    def add_task(self, task_id, func_name, status, node_id):
        self.tasks.append({
            'id': task_id, 'function': func_name,
            'status': status, 'node': node_id,
            'time': datetime.now().strftime("%H:%M:%S")
        })

    def display(self):
        console.print(Panel(
            "[bold green]MeshWeaver - P2P Task Broker[/bold green]",
            style="green"
        ))
        node_table = Table(title="Active Nodes", box=box.ROUNDED)
        node_table.add_column("Node ID", style="cyan")
        node_table.add_column("Address", style="white")
        node_table.add_column("CPU%", style="yellow")
        node_table.add_column("Status", style="green")
        for nid, info in self.nodes.items():
            color = "green" if info['status'] == "active" else "red"
            node_table.add_row(
                nid[:12], f"{info['host']}:{info['port']}",
                f"{info['cpu']}%",
                f"[{color}]{info['status']}[/{color}]"
            )
        console.print(node_table)

        task_table = Table(title="Tasks", box=box.ROUNDED)
        task_table.add_column("ID", style="cyan")
        task_table.add_column("Function", style="white")
        task_table.add_column("Status", style="yellow")
        task_table.add_column("Node", style="white")
        for task in self.tasks:
            color = "green" if task['status'] == "complete" else "yellow"
            task_table.add_row(
                task['id'], task['function'],
                f"[{color}]{task['status']}[/{color}]",
                task['node'][:12]
            )
        console.print(task_table)

if __name__ == "__main__":
    d = MeshDashboard()
    d.add_node("node-alpha", "127.0.0.1", 8001, cpu=23)
    d.add_node("node-beta", "127.0.0.1", 8002, cpu=45)
    d.add_node("node-gamma", "127.0.0.1", 8003, cpu=12)
    d.add_task("t001", "add_numbers", "complete", "node-alpha")
    d.add_task("t002", "ml_compute", "running", "node-beta")
    d.display()