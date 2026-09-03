# MeshWeaver - Fault Tolerance - Aug 22 - Sunaina
from datetime import datetime

class FaultTolerance:
    def __init__(self, node_id):
        self.node_id = node_id
        self.node_status = {}
        self.task_assignments = {}
        self.retry_count = {}
        self.max_retries = 3

    def register_node(self, peer_id, host, port):
        self.node_status[peer_id] = {
            'host': host, 'port': port,
            'status': 'active', 'failures': 0,
            'last_check': datetime.now().isoformat()
        }
        print(f"[{self.node_id}] Registered: {peer_id}")

    def mark_failed(self, peer_id):
        if peer_id in self.node_status:
            self.node_status[peer_id]['status'] = 'failed'
            self.node_status[peer_id]['failures'] += 1
            print(f"[{self.node_id}] ❌ Failed: {peer_id}")

    def mark_recovered(self, peer_id):
        if peer_id in self.node_status:
            self.node_status[peer_id]['status'] = 'active'
            print(f"[{self.node_id}] ✅ Recovered: {peer_id}")

    def get_active_nodes(self):
        return [
            nid for nid, info in self.node_status.items()
            if info['status'] == 'active'
        ]

    def assign_task(self, task_id, node_id, data):
        self.task_assignments[task_id] = {
            'node': node_id, 'data': data,
            'status': 'running',
            'assigned_at': datetime.now().isoformat()
        }
        self.retry_count[task_id] = 0
        print(f"[{self.node_id}] Task {task_id} → {node_id}")

    def handle_failure(self, task_id):
        if task_id not in self.task_assignments:
            return None
        task = self.task_assignments[task_id]
        self.retry_count[task_id] += 1
        if self.retry_count[task_id] >= self.max_retries:
            task['status'] = 'permanently_failed'
            print(f"[{self.node_id}] ❌ {task_id} permanently failed")
            return None
        active = self.get_active_nodes()
        if not active:
            return None
        new_node = active[0]
        task['node'] = new_node
        task['status'] = 'running'
        print(f"[{self.node_id}] 🔄 {task_id} → {new_node} "
              f"(attempt {self.retry_count[task_id]})")
        return new_node

    def display_status(self):
        print(f"\n=== Fault Tolerance Status ===")
        for nid, info in self.node_status.items():
            icon = "✅" if info['status'] == 'active' else "❌"
            print(f"{icon} {nid:<20} {info['status']}")
        print("\nTasks:")
        for tid, task in self.task_assignments.items():
            print(f"  {tid} → {task['node']} ({task['status']})")

if __name__ == "__main__":
    print("=== Fault Tolerance Demo ===\n")
    ft = FaultTolerance("coordinator")
    ft.register_node("node-alpha", "127.0.0.1", 8001)
    ft.register_node("node-beta", "127.0.0.1", 8002)
    ft.register_node("node-gamma", "127.0.0.1", 8003)
    ft.assign_task("t001", "node-alpha", {"func": "ml"})
    ft.assign_task("t002", "node-beta", {"func": "data"})
    print("\nSimulating node-alpha failure...")
    ft.mark_failed("node-alpha")
    ft.handle_failure("t001")
    print("\nSimulating recovery...")
    ft.mark_recovered("node-alpha")
    ft.display_status()
    print("\n✅ Fault Tolerance Demo Complete!")