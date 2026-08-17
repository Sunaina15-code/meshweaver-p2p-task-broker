# MeshWeaver - Task Serializer
# Serialize Python functions with cloudpickle

import cloudpickle
import hashlib
from datetime import datetime

class TaskSerializer:
    def __init__(self):
        self.tasks = {}

    def serialize(self, func, *args, **kwargs):
        try:
            data = {
                'function': cloudpickle.dumps(func),
                'args': cloudpickle.dumps(args),
                'kwargs': cloudpickle.dumps(kwargs),
                'func_name': func.__name__,
                'timestamp': datetime.now().isoformat()
            }
            task_id = hashlib.md5(
                f"{func.__name__}{datetime.now()}".encode()
            ).hexdigest()[:8]
            self.tasks[task_id] = data
            print(f"✅ Serialized: {func.__name__} (ID: {task_id})")
            return task_id, cloudpickle.dumps(data)
        except Exception as e:
            print(f"❌ Error: {e}")
            return None, None

    def deserialize_and_run(self, serialized):
        try:
            data = cloudpickle.loads(serialized)
            func = cloudpickle.loads(data['function'])
            args = cloudpickle.loads(data['args'])
            kwargs = cloudpickle.loads(data['kwargs'])
            result = func(*args, **kwargs)
            print(f"✅ Executed: {data['func_name']} → {result}")
            return result
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

def add(x, y): return x + y
def multiply(x, y): return x * y
def stats(data): return {'sum': sum(data), 'mean': sum(data)/len(data)}

if __name__ == "__main__":
    print("=== Task Serializer Demo ===\n")
    s = TaskSerializer()
    _, ser1 = s.serialize(add, 10, 20)
    s.deserialize_and_run(ser1)
    _, ser2 = s.serialize(multiply, 5, 6)
    s.deserialize_and_run(ser2)
    _, ser3 = s.serialize(stats, [1,2,3,4,5])
    s.deserialize_and_run(ser3)
    print("\n✅ Serialization Complete!")