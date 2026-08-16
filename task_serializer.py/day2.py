import cloudpickle
def _pickle_test():
 fn = lambda x: x * 2
 blob = cloudpickle.dumps(fn)
 restored = cloudpickle.loads(blob)
 assert restored(4) == 8
 return True