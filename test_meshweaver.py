# MeshWeaver - Complete Test Suite - Aug 21
import asyncio
from meshweaver.dht import KademliaNode
from meshweaver.serializer import TaskSerializer
from meshweaver.network.gossip import GossipNode
from meshweaver.network.task_router import TaskRouter
from meshweaver.network.security import MeshSecurity

def test_dht():
    print("[1/5] Testing DHT...")
    node = KademliaNode("aaaa1111bbbb2222", "127.0.0.1", 8001)
    node.store("test", {"value": 42})
    result = node.get("test")
    assert result is not None
    print("✅ DHT Passed!")

def test_serializer():
    print("[2/5] Testing Serializer...")
    s = TaskSerializer()
    def add(x, y): return x + y
    _, ser = s.serialize(add, 5, 10)
    result = s.deserialize_and_run(ser)
    assert result == 15
    print("✅ Serializer Passed!")

def test_gossip():
    print("[3/5] Testing Gossip...")
    n1 = GossipNode("node-a", "127.0.0.1", 8001)
    n2 = GossipNode("node-b", "127.0.0.1", 8002)
    msg = n2.create_gossip()
    n1.receive_gossip(msg)
    assert "node-b" in n1.node_loads
    print("✅ Gossip Passed!")

def test_router():
    print("[4/5] Testing Router...")
    r = TaskRouter("coordinator")
    r.update_load("node-a", cpu=80, ram=60)
    r.update_load("node-b", cpu=20, ram=40)
    best = r.find_best_node()
    assert best == "node-b"
    print("✅ Router Passed!")

def test_security():
    print("[5/5] Testing Security...")
    s = MeshSecurity("node-test")
    signed = s.create_signed_message("ping", {"data": "test"})
    assert 'signature' in signed
    assert 'message' in signed
    print("✅ Security Passed!")

if __name__ == "__main__":
    print("=" * 50)
    print("  MeshWeaver - Complete Test Suite")
    print("=" * 50 + "\n")
    test_dht()
    test_serializer()
    test_gossip()
    test_router()
    test_security()
    print("\n" + "=" * 50)
    print("  ALL 5 TESTS PASSED! MeshWeaver Ready! 🎉")
    print("=" * 50)