# MeshWeaver - DHT Module
# Kademlia distributed hash table

import hashlib
from datetime import datetime

class KademliaNode:
    def __init__(self, node_id=None, host='127.0.0.1', port=8888):
        self.node_id = node_id or self._generate_id()
        self.host = host
        self.port = port
        self.routing_table = {}
        self.data_store = {}

    def _generate_id(self):
        import random
        return hashlib.sha1(
            str(random.randint(0, 999999)).encode()
        ).hexdigest()[:16]

    def distance(self, other_id):
        return int(self.node_id, 16) ^ int(other_id, 16)

    def add_peer(self, peer_id, host, port):
        self.routing_table[peer_id] = {
            'host': host,
            'port': port,
            'last_seen': datetime.now().isoformat(),
            'distance': self.distance(peer_id)
        }
        print(f"[{self.node_id[:8]}] Peer added: {peer_id[:8]}")

    def find_closest(self, target_id, k=3):
        peers = list(self.routing_table.items())
        peers.sort(key=lambda x: self.distance(x[0]))
        return peers[:k]

    def store(self, key, value):
        hkey = hashlib.sha1(key.encode()).hexdigest()[:16]
        self.data_store[hkey] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        print(f"[{self.node_id[:8]}] Stored: {key}")
        return hkey

    def get(self, key):
        hkey = hashlib.sha1(key.encode()).hexdigest()[:16]
        return self.data_store.get(hkey)

    def display_info(self):
        print(f"\n=== DHT Node [{self.node_id[:8]}] ===")
        print(f"Address: {self.host}:{self.port}")
        print(f"Peers:   {len(self.routing_table)}")
        print(f"Data:    {len(self.data_store)} items")

if __name__ == "__main__":
    print("=== Kademlia DHT Demo ===\n")
    node1 = KademliaNode("aaaa1111bbbb2222", "127.0.0.1", 8001)
    node2 = KademliaNode("cccc3333dddd4444", "127.0.0.1", 8002)
    node3 = KademliaNode("eeee5555ffff6666", "127.0.0.1", 8003)
    node1.add_peer(node2.node_id, node2.host, node2.port)
    node1.add_peer(node3.node_id, node3.host, node3.port)
    node1.store("task_1", {"function": "add", "args": [10, 20]})
    result = node1.get("task_1")
    print(f"Retrieved: {result['value']}")
    node1.display_info()
    print("\n✅ DHT Demo Complete!")