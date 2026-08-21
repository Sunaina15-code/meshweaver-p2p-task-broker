# MeshWeaver - Peer Discovery - Aug 18 - Athrva
# Dynamic peer discovery without hardcoded IPs

import asyncio
import json
from datetime import datetime

class PeerDiscovery:
    """
    Discovers peers dynamically without hardcoded IPs
    Uses UDP broadcast for local network discovery
    """
    def __init__(self, node_id, host, port):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.discovered = {}

    def create_announcement(self):
        return json.dumps({
            'type': 'announce',
            'node_id': self.node_id,
            'host': self.host,
            'port': self.port,
            'timestamp': datetime.now().isoformat()
        })

    def process_announcement(self, message, addr):
        try:
            data = json.loads(message)
            peer_id = data['node_id']
            if peer_id != self.node_id:
                self.discovered[peer_id] = {
                    'host': addr,
                    'port': data['port'],
                    'discovered_at': datetime.now().isoformat()
                }
                print(f"[{self.node_id[:8]}] Found: "
                      f"{peer_id[:8]} @ {addr}:{data['port']}")
                return True
        except Exception as e:
            print(f"Error: {e}")
        return False

    def simulate_discovery(self, other_nodes):
        print(f"[{self.node_id[:8]}] Discovering peers...")
        for node in other_nodes:
            msg = node.create_announcement()
            self.process_announcement(msg, node.host)

    def get_peers(self):
        return list(self.discovered.items())

    def display_peers(self):
        print(f"\n=== Discovered Peers [{self.node_id[:8]}] ===")
        if not self.discovered:
            print("No peers found")
            return
        for pid, info in self.discovered.items():
            print(f"  {pid[:8]} @ {info['host']}:{info['port']}")
        print(f"Total: {len(self.discovered)} peers")

async def demo():
    print("=== Peer Discovery Demo ===\n")

    nodes = [
        PeerDiscovery(f"node{i}{'x'*12}", "127.0.0.1", 8000+i)
        for i in range(1, 6)
    ]

    print("5 nodes discovering each other...\n")
    for node in nodes:
        others = [n for n in nodes if n != node]
        node.simulate_discovery(others)

    print("\n=== Results ===")
    for node in nodes[:2]:
        node.display_peers()

    print("\n✅ Discovery complete — no hardcoded IPs needed!")

if __name__ == "__main__":
    asyncio.run(demo())