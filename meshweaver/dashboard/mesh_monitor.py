# MeshWeaver - Mesh Monitor - Aug 20 - Sunaina
# Real-time mesh topology monitor

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich import box
from datetime import datetime
import time

console = Console()

class MeshMonitor:
    def __init__(self):
        self.nodes = {}
        self.connections = []
        self.tasks = []
        self.stats = {
            'total_tasks': 0,
            'completed': 0,
            'failed': 0,
            'active_nodes': 0
        }

    def add_node(self, node_id, host, port, cpu=0, ram=0):
        self.nodes[node_id] = {
            'host': host, 'port': port,
            'cpu': cpu, 'ram': ram,
            'status': 'active',
            'tasks_handled': 0,
            'joined_at': datetime.now().strftime("%H:%M:%S")
        }
        self.stats['active_nodes'] = len(self.nodes)

    def add_connection(self, node1, node2):
        self.connections.append((node1, node2))

    def add_task(self, task_id, func, status, node):
        self.tasks.append({
            'id': task_id, 'func': func,
            'status': status, 'node': node,
            'time': datetime.now().strftime("%H:%M:%S")
        })
        self.stats['total_tasks'] += 1
        if status == 'complete':
            self.stats['completed'] += 1
        elif status == 'failed':
            self.stats['failed'] += 1

    def render(self):
        console.print(Panel(
            f"[bold green]🌐 MeshWeaver Monitor[/bold green] | "
            f"Nodes: {self.stats['active_nodes']} | "
            f"Tasks: {self.stats['total_tasks']} | "
            f"Time: {datetime.now().strftime('%H:%M:%S')}",
            style="green"
        ))

        # Node table
        nt = Table(title="Mesh Nodes", box=box.ROUNDED, style="blue")
        nt.add_column("Node ID", style="cyan", width=15)
        nt.add_column("Address", style="white", width=18)
        nt.add_column("CPU%", style="yellow", width=8)
        nt.add_column("RAM%", style="magenta", width=8)
        nt.add_column("Status", style="green", width=10)

        for nid, info in self.nodes.items():
            cpu = info['cpu']
            color = "green" if cpu < 50 else "yellow" if cpu < 80 else "red"
            nt.add_row(
                nid[:14],
                f"{info['host']}:{info['port']}",
                f"[{color}]{cpu}%[/{color}]",
                f"{info['ram']}%",
                f"[green]{info['status']}[/green]"
            )
        console.print(nt)

        # Task table
        tt = Table(title="Recent Tasks", box=box.ROUNDED, style="purple")
        tt.add_column("ID", style="cyan", width=10)
        tt.add_column("Function", style="white", width=20)
        tt.add_column("Status", style="yellow", width=12)
        tt.add_column("Node", style="white", width=15)
        tt.add_column("Time", style="white", width=10)

        for task in self.tasks[-8:]:
            sc = "green" if task['status']=="complete" else "yellow"
            tt.add_row(
                task['id'], task['func'],
                f"[{sc}]{task['status']}[/{sc}]",
                task['node'][:14], task['time']
            )
        console.print(tt)

        # Stats
        st = Table(title="Network Stats", box=box.SIMPLE, style="white")
        st.add_column("Metric", style="cyan")
        st.add_column("Value", style="green")
        st.add_row("Total Tasks", str(self.stats['total_tasks']))
        st.add_row("Completed", str(self.stats['completed']))
        st.add_row("Failed", str(self.stats['failed']))
        st.add_row("Active Nodes", str(self.stats['active_nodes']))
        console.print(st)

if __name__ == "__main__":
    monitor = MeshMonitor()
    monitor.add_node("node-alpha", "127.0.0.1", 8001, cpu=23, ram=45)
    monitor.add_node("node-beta",  "127.0.0.1", 8002, cpu=67, ram=55)
    monitor.add_node("node-gamma", "127.0.0.1", 8003, cpu=12, ram=30)
    monitor.add_node("node-delta", "127.0.0.1", 8004, cpu=89, ram=70)
    monitor.add_task("t001", "ml_inference", "complete", "node-alpha")
    monitor.add_task("t002", "data_process", "running", "node-beta")
    monitor.add_task("t003", "image_resize", "complete", "node-gamma")
    monitor.add_task("t004", "train_model", "failed", "node-delta")
    monitor.render()
    print("\n✅ Monitor Demo Complete!")
# Aug 20 update
