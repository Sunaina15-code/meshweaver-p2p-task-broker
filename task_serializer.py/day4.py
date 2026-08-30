MAX_PAYLOAD_BYTES = 5 * 1024 * 1024  # 5 MB safety cap

def deserialize_task(self, blob):
    if len(blob) > MAX_PAYLOAD_BYTES:
        raise ValueError("Task payload exceeds max allowed size")

    try:
        payload = cloudpickle.loads(blob)
    except Exception as exc:
        raise ValueError(f"Failed to deserialize task: {exc}")

    func = cloudpickle.loads(payload["func"])
    args = cloudpickle.loads(payload["args"])
    kwargs = cloudpickle.loads(payload["kwargs"])

    return payload["task_id"], func, args