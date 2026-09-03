# MeshWeaver - Task Executor - Aug 24 - Noah
import cloudpickle
from datetime import datetime

class TaskExecutor:
    def __init__(self, node_id):
        self.node_id = node_id
        self.executed = []
        self.failed = []
        self.total_time = 0

    def execute(self, serialized_task):
        start = datetime.now()
        try:
            data = cloudpickle.loads(serialized_task)
            func = cloudpickle.loads(data['function'])
            args = cloudpickle.loads(data['args'])
            kwargs = cloudpickle.loads(data['kwargs'])
            result = func(*args, **kwargs)
            elapsed = (datetime.now() - start).total_seconds()
            self.total_time += elapsed
            entry = {
                'func_name': data.get('func_name', func.__name__),
                'result': result, 'time': elapsed
            }
            self.executed.append(entry)
            print(f"[{self.node_id}] ✅ {entry['func_name']} "
                  f"→ {result} ({elapsed:.3f}s)")
            return result
        except Exception as e:
            self.failed.append({'error': str(e)})
            print(f"[{self.node_id}] ❌ Error: {e}")
            return None

    def display_stats(self):
        print(f"\n=== Executor Stats [{self.node_id}] ===")
        print(f"Executed: {len(self.executed)}")
        print(f"Failed:   {len(self.failed)}")
        if self.executed:
            avg = self.total_time / len(self.executed)
            print(f"Avg time: {avg:.3f}s")
        for e in self.executed:
            print(f"  {e['func_name']:<20} → {e['result']}")

def add(x, y): return x + y
def multiply(x, y): return x * y
def power(x, n): return x ** n
def stats(data): return {'sum': sum(data), 'mean': round(sum(data)/len(data), 2)}

if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from meshweaver.serializer import TaskSerializer
    print("=== Task Executor Demo ===\n")
    s = TaskSerializer()
    e = TaskExecutor("node-beta")
    for func, args in [(add,(10,20)), (multiply,(5,6)),
                       (power,(2,10)), (stats,([1,2,3,4,5],))]:
        _, ser = s.serialize(func, *args)
        e.execute(ser)
    e.display_stats()
    print("\n✅ Executor Demo Complete!")
# Aug 24 update
