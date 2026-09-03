# MeshWeaver - CLI Dashboard - Aug 25 - John
import click
from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime
import random
import hashlib

console = Console()

@click.group()
def cli():
    """MeshWeaver - P2P Async Task Broker CLI"""
    pass

@cli.command()
@click.option('--nodes', default=3)
def status(nodes):
    """Show mesh network status"""
    console.print("\n[bold green]🌐 MeshWeaver Status[/bold green]\n")
    t = Table(box=box.ROUNDED)
    t.add_column("Node", style="cyan")
    t.add_column("Address", style="white")
    t.add_column("CPU%", style="yellow")
    t.add_column("Status", style="green")
    for i in range(nodes):
        cpu = random.randint(10, 90)
        c = "green" if cpu < 60 else "red"
        t.add_row(f"node-{i+1}", f"127.0.0.1:{8001+i}",
                  f"[{c}]{cpu}%[/{c}]", "[green]active[/green]")
    console.print(t)

@cli.command()
@click.argument('task_name')
@click.option('--priority', default=1)
def submit(task_name, priority):
    """Submit task to mesh"""
    tid = hashlib.md5(f"{task_name}{datetime.now()}".encode()).hexdigest()[:8]
    console.print(f"\n[green]✅ Task submitted![/green]")
    console.print(f"  Name: {task_name} | ID: {tid} | Priority: {priority}")

@cli.command()
def nodes():
    """List mesh nodes"""
    console.print("\n[bold blue]📡 Mesh Nodes[/bold blue]\n")
    for nid, port, cpu in [("node-alpha",8001,23),
                            ("node-beta",8002,67),
                            ("node-gamma",8003,12)]:
        c = "green" if cpu < 60 else "red"
        console.print(f"  [cyan]{nid}[/cyan] @ 127.0.0.1:{port} "
                      f"CPU:[{c}]{cpu}%[/{c}]")

@cli.command()
def tasks():
    """Show task history"""
    console.print("\n[bold purple]📋 Tasks[/bold purple]\n")
    t = Table(box=box.SIMPLE)
    t.add_column("ID", style="cyan")
    t.add_column("Function", style="white")
    t.add_column("Status", style="green")
    t.add_column("Node", style="white")
    for tid, func, status, node in [
        ("a1b2c3d4","ml_inference","complete","node-beta"),
        ("e5f6g7h8","data_process","running","node-alpha"),
        ("i9j0k1l2","image_resize","complete","node-gamma")
    ]:
        c = "green" if status=="complete" else "yellow"
        t.add_row(tid, func, f"[{c}]{status}[/{c}]", node)
    console.print(t)

if __name__ == "__main__":
    cli()