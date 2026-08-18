# MeshWeaver - Heartbeat Monitor - Aug 16 - Noah
# Detects node failures and re-routes tasks

import asyncio
from datetime import datetime

class HeartbeatMonitor:
    def __init__(self, node_id, timeout=10):
        self.node_id = node_id
        self.timeout = timeout
        self.heartbeats = {}
        self.failed_nodes = set()
        self.pending_tasks = {}

    def register_node(self, peer_id):
        self.heartbeats[peer_id] = datetime.now()
        print(f"[{self.node_id}] Monitoring: {peer_id}")

    def receive_heartbeat(self, peer_id):
        self.heartbeats[peer_id] = datetime.now()
        if peer_id in self.failed_nodes:
            self.failed_nodes.remove(peer_id)
            print(f"[{self.node_id}] ✅ Recovered: {peer_id}")

    def check_nodes(self):
        now = datetime.now()
        failed = []
        for peer_id, last in self.heartbeats.items():
            elapsed = (now - last).seconds
            if elapsed > self.timeout:
                if peer_id not in self.failed_nodes:
                    self.failed_nodes.add(peer_id)
                    failed.append(peer_id)
                    print(f"[{self.node_id}] ❌ FAILED: {peer_id}")
        return failed

    def assign_task(self, task_id, node_id, data):
        self.pending_tasks[task_id] = {
            'node': node_id, 'data': data,
            'status': 'running',
            'assigned_at': datetime.now().isoformat()
        }
        print(f"[{self.node_id}] Task {task_id} → {node_id}")

    def handle_failure(self, failed_node):
        affected = {
            tid: t for tid, t in self.pending_tasks.items()
            if t['node'] == failed_node and t['status'] == 'running'
        }
        print(f"\n[{self.node_id}] Handling failure: {failed_node}")
        print(f"  Affected tasks: {len(affected)}")
        for tid, task in affected.items():
            task['status'] = 'failed'
            print(f"  ❌ {tid} → needs re-routing")
        return list(affected.keys())

    def get_active_nodes(self):
        return [n for n in self.heartbeats if n not in self.failed_nodes]

    def display_status(self):
        print(f"\n=== Heartbeat Status ===")
        now = datetime.now()
        for pid, last in self.heartbeats.items():
            elapsed = (now - last).seconds
            status = "❌ FAILED" if pid in self.failed_nodes else "✅ Active"
            print(f"  {pid:<20} {elapsed}s ago  {status}")
        print(f"\nActive: {len(self.get_active_nodes())} | "
              f"Failed: {len(self.failed_nodes)}")

async def demo():
    print("=== Heartbeat Monitor Demo ===\n")
    monitor = HeartbeatMonitor("coordinator", timeout=3)
    monitor.register_node("node-alpha")
    monitor.register_node("node-beta")
    monitor.register_node("node-gamma")
    monitor.assign_task("t001", "node-alpha", {"func": "ml"})
    monitor.assign_task("t002", "node-beta", {"func": "data"})
    monitor.receive_heartbeat("node-alpha")
    monitor.receive_heartbeat("node-beta")
    print("\nWaiting 4s (node-gamma will timeout)...")
    await asyncio.sleep(4)
    failed = monitor.check_nodes()
    for node in failed:
        monitor.handle_failure(node)
    monitor.display_status()
    print("\n✅ Heartbeat Demo Complete!")

if __name__ == "__main__":
    asyncio.run(demo())
# Aug 16 update
