# MeshWeaver - Task Queue - Aug 19 - Noah
# Priority-based distributed task queue

import asyncio
import cloudpickle
import hashlib
from datetime import datetime
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"

class Task:
    def __init__(self, func, args=(), kwargs={}, priority=1):
        self.task_id = hashlib.md5(
            f"{func.__name__}{datetime.now()}".encode()
        ).hexdigest()[:8]
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.priority = priority
        self.status = Status.PENDING
        self.result = None
        self.func_name = func.__name__

class DistributedQueue:
    def __init__(self, node_id):
        self.node_id = node_id
        self.queue = asyncio.PriorityQueue()
        self.completed = []
        self.failed = []

    async def submit(self, func, *args, priority=1, **kwargs):
        task = Task(func, args, kwargs, priority)
        await self.queue.put((priority, task))
        print(f"[{self.node_id}] Submitted: "
              f"{task.func_name} (ID:{task.task_id})")
        return task.task_id

    async def execute_next(self):
        if self.queue.empty():
            return None
        _, task = await self.queue.get()
        task.status = Status.RUNNING
        print(f"[{self.node_id}] Running: {task.func_name}")
        try:
            task.result = task.func(*task.args, **task.kwargs)
            task.status = Status.COMPLETE
            self.completed.append(task)
            print(f"[{self.node_id}] ✅ Done: "
                  f"{task.func_name} → {task.result}")
        except Exception as e:
            task.status = Status.FAILED
            self.failed.append(task)
            print(f"[{self.node_id}] ❌ Failed: {e}")
        return task

    async def run_all(self):
        while not self.queue.empty():
            await self.execute_next()

    def display_stats(self):
        print(f"\n=== Queue Stats [{self.node_id}] ===")
        print(f"Completed: {len(self.completed)}")
        print(f"Failed:    {len(self.failed)}")
        for t in self.completed:
            print(f"  {t.task_id} | {t.func_name} → {t.result}")

def add(x, y): return x + y
def multiply(x, y): return x * y
def compute(data): return {'sum': sum(data), 'mean': sum(data)/len(data)}

async def demo():
    print("=== Distributed Task Queue Demo ===\n")
    q = DistributedQueue("node-alpha")
    await q.submit(add, 10, 20, priority=1)
    await q.submit(multiply, 5, 6, priority=2)
    await q.submit(compute, [1,2,3,4,5], priority=1)
    print("\nExecuting all tasks...")
    await q.run_all()
    q.display_stats()
    print("\n✅ Queue Demo Complete!")

if __name__ == "__main__":
    asyncio.run(demo())
# Aug 19 update
