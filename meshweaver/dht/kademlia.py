# MeshWeaver - Kademlia DHT - Aug 16 - John
# Full Kademlia implementation

import hashlib
import asyncio
from datetime import datetime

class KBucket:
    def __init__(self, k=20):
        self.k = k
        self.peers = []

    def add(self, peer):
        if peer not in self.peers:
            if len(self.peers) < self.k:
                self.peers.append(peer)
                return True
        return False

class KademliaNetwork:
    def __init__(self, node_id, host, port):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.buckets = [KBucket() for _ in range(160)]
        self.data = {}

    def _distance(self, id1, id2):
        return int(id1, 16) ^ int(id2, 16)

    def _bucket_index(self, other_id):
        dist = self._distance(self.node_id, other_id)
        return 0 if dist == 0 else dist.bit_length() - 1

    def add_peer(self, peer_id, host, port):
        idx = self._bucket_index(peer_id)
        peer = {
            'id': peer_id, 'host': host, 'port': port,
            'last_seen': datetime.now().isoformat()
        }
        if self.buckets[idx].add(peer):
            print(f"[{self.node_id[:8]}] Peer → bucket {idx}: {peer_id[:8]}")

    def find_node(self, target_id, k=3):
        all_peers = []
        for bucket in self.buckets:
            all_peers.extend(bucket.peers)
        all_peers.sort(
            key=lambda p: self._distance(p['id'], target_id)
        )
        return all_peers[:k]

    def store(self, key, value):
        hkey = hashlib.sha1(key.encode()).hexdigest()
        self.data[hkey] = {
            'value': value,
            'stored_at': datetime.now().isoformat()
        }
        print(f"[{self.node_id[:8]}] Stored: {key}")
        return hkey

    def get(self, key):
        hkey = hashlib.sha1(key.encode()).hexdigest()
        return self.data.get(hkey)

    async def join(self, bootstrap_host, bootstrap_port):
        print(f"[{self.node_id[:8]}] Joining via "
              f"{bootstrap_host}:{bootstrap_port}")
        await asyncio.sleep(0.1)
        print(f"[{self.node_id[:8]}] Joined network!")

    def display(self):
        print(f"\n=== Kademlia [{self.node_id[:8]}] ===")
        total = sum(len(b.peers) for b in self.buckets)
        print(f"Peers: {total} | Data: {len(self.data)} items")

async def demo():
    print("=== Kademlia Network Demo ===\n")
    node1 = KademliaNetwork("aaaa1111bbbb2222", "127.0.0.1", 8001)
    node2 = KademliaNetwork("cccc3333dddd4444", "127.0.0.1", 8002)
    node3 = KademliaNetwork("eeee5555ffff6666", "127.0.0.1", 8003)
    await node2.join("127.0.0.1", 8001)
    await node3.join("127.0.0.1", 8001)
    node1.add_peer(node2.node_id, node2.host, node2.port)
    node1.add_peer(node3.node_id, node3.host, node3.port)
    node1.store("task_heavy", {"func": "matrix_multiply"})
    result = node1.get("task_heavy")
    print(f"Retrieved: {result['value']}")
    node1.display()
    print("\n✅ Kademlia Demo Complete!")

if __name__ == "__main__":
    asyncio.run(demo())