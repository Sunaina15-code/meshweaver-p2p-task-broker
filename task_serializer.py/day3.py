import cloudpickle
import uuid


class TaskSerializer:

    def serialize_task(self, func, args=(), kwargs=None):
        kwargs = kwargs or {}

        task_id = str(uuid.uuid4())

        payload = {
            "task_id": task_id,
            "func": cloudpickle.dumps(func),
            "args": cloudpickle.dumps(args),
            "kwargs": cloudpickle.dumps(kwargs)
        }

        return cloudpickle.dumps(payload)


# Example usage
def add(a, b):
    return a + b


serializer = TaskSerializer()

task = serializer.serialize_task(add, args=(10, 20))

print(task)