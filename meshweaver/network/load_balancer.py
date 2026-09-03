# MeshWeaver - Load Balancer - Aug 23 - Athrva
from datetime import datetime

class LoadBalancer:
    def __init__(self, node_id, strategy='score'):
        self.node_id = node_id
        self.strategy = strategy
        self.node_loads = {}
        self.routing_log = []

    def update_node(self, node_id, cpu, ram, tasks=0):
        self.node_loads[node_id] = {
            'cpu': cpu, 'ram': ram, 'tasks': tasks,
            'score': (cpu*0.5) + (ram*0.3) + (tasks*0.2),
            'updated': datetime.now().isoformat()
        }

    def get_best_node(self):
        if not self.node_loads:
            return None
        if self.strategy == 'cpu':
            return min(self.node_loads, key=lambda n: self.node_loads[n]['cpu'])
        elif self.strategy == 'ram':
            return min(self.node_loads, key=lambda n: self.node_loads[n]['ram'])
        elif self.strategy == 'tasks':
            return min(self.node_loads, key=lambda n: self.node_loads[n]['tasks'])
        return min(self.node_loads, key=lambda n: self.node_loads[n]['score'])

    def route(self, task_name):
        target = self.get_best_node()
        if not target:
            print(f"[{self.node_id}] ❌ No nodes!")
            return None
        self.routing_log.append({
            'task': task_name, 'target': target,
            'cpu': self.node_loads[target]['cpu'],
            'time': datetime.now().isoformat()
        })
        self.node_loads[target]['tasks'] += 1
        print(f"[{self.node_id}] '{task_name}' → {target} "
              f"(CPU:{self.node_loads[target]['cpu']}%)")
        return target

    def display_nodes(self):
        print(f"\n=== Load Balancer [{self.strategy.upper()}] ===")
        print(f"{'Node':<20} {'CPU%':<8} {'RAM%':<8} {'Tasks':<8} {'Score'}")
        print("-" * 55)
        for nid, load in self.node_loads.items():
            print(f"{nid:<20} {load['cpu']:<8} {load['ram']:<8} "
                  f"{load['tasks']:<8} {load['score']:.1f}")

    def display_log(self):
        print(f"\n=== Routing Log ===")
        for e in self.routing_log[-5:]:
            print(f"  {e['task']:<20} → {e['target']:<15} CPU:{e['cpu']}%")

if __name__ == "__main__":
    print("=== Load Balancer Demo ===\n")
    lb = LoadBalancer("coordinator", strategy='score')
    lb.update_node("node-alpha", cpu=75, ram=60, tasks=5)
    lb.update_node("node-beta",  cpu=23, ram=45, tasks=2)
    lb.update_node("node-gamma", cpu=45, ram=50, tasks=3)
    lb.update_node("node-delta", cpu=12, ram=30, tasks=1)
    lb.display_nodes()
    print("\nRouting tasks...")
    for task in ["ml_inference", "data_process", "image_resize", "train_model"]:
        lb.route(task)
    lb.display_log()
    print("\n✅ Load Balancer Demo Complete!")