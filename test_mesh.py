# MeshWeaver - Test Suite
from meshweaver.dht import KademliaNode
from meshweaver.serializer import TaskSerializer

def test_dht():
    print("[1/2] Testing DHT...")
    node = KademliaNode("aaaa1111bbbb2222", "127.0.0.1", 8001)
    node.store("test_key", {"value": 42})
    result = node.get("test_key")
    assert result is not None
    print("✅ DHT Test Passed!")

def test_serializer():
    print("[2/2] Testing Serializer...")
    s = TaskSerializer()
    def add(x, y): return x + y
    _, ser = s.serialize(add, 5, 10)
    result = s.deserialize_and_run(ser)
    assert result == 15
    print("✅ Serializer Test Passed!")

if __name__ == "__main__":
    print("=== MeshWeaver Test Suite ===\n")
    test_dht()
    test_serializer()
    print("\n✅ ALL TESTS PASSED!")