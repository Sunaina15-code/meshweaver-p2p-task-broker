# MeshWeaver - Task Router - Aug 15 - Athrva
# Routes tasks to node with lowest CPU load

from datetime import datetime

class TaskRouter:
    def __init__(self, node_id):
        self.node_id = node_id
        self.node_loads = {}
        self.routing_history = []

    def update_load(self, node_id, cpu, ram):
        self.node_loads[node_id] = {
            'cpu': cpu, 'ram': ram,
            'updated_at': datetime.now().isoformat()
        }

    def find_best_node(self):
        if not self.node_loads:
            return self.node_id
        best = min(
            self.node_loads.keys(),
            key=lambda n: self.node_loads[n]['cpu']
        )
        print(f"[{self.node_id}] Best node: {best} "
              f"(CPU: {self.node_loads[best]['cpu']}%)")
        return best

    def route_task(self, task_name, task_data):
        target = self.find_best_node()
        entry = {
            'task': task_name,
            'routed_to': target,
            'cpu': self.node_loads.get(target, {}).get('cpu', 0),
            'timestamp': datetime.now().isoformat()
        }
        self.routing_history.append(entry)
        print(f"[{self.node_id}] '{task_name}' → {target}")
        return target, entry

    def display_status(self):
        print(f"\n=== Network Status ===")
        for nid, load in self.node_loads.items():
            status = "✅ OK" if load['cpu'] < 70 else "⚠️ High"
            print(f"  {nid:<20} CPU:{load['cpu']}% {status}")

    def display_history(self):
        print(f"\n=== Routing History ===")
        for e in self.routing_history:
            print(f"  {e['task']:<20} → {e['routed_to']}")

if __name__ == "__main__":
    print("=== Task Router Demo ===\n")
    router = TaskRouter("coordinator")
    router.update_load("node-alpha", cpu=75, ram=60)
    router.update_load("node-beta", cpu=23, ram=45)
    router.update_load("node-gamma", cpu=45, ram=50)
    router.update_load("node-delta", cpu=12, ram=30)
    router.display_status()
    print("\nRouting tasks...")
    router.route_task("ml_inference", {"model": "bert"})
    router.route_task("data_process", {"rows": 50000})
    router.route_task("matrix_multiply", {"size": 1000})
    router.display_history()
    print("\n✅ Task routing complete!")