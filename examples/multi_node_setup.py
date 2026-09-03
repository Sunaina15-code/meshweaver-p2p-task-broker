#!/usr/bin/env python3
"""
MeshWeaver Example 3: Multi-Node Setup
=======================================

This example demonstrates setting up a complete mesh network:
- Create multiple nodes
- Configure gossip protocol
- Set up heartbeat monitoring
- Connect nodes with Kademlia DHT
- Simulate distributed task routing

Difficulty: ⭐⭐ Intermediate
Run time: ~20 seconds
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from meshweaver.network.gossip import GossipNode
from meshweaver.network.heartbeat import HeartbeatMonitor
from meshweaver.network.task_router import TaskRouter
from meshweaver.dht.kademlia import KademliaNetwork


# =============================================================================
# Node Configuration
# =============================================================================

NODE_CONFIGS = [
    {"id": "node-alpha", "host": "127.0.0.1", "port": 8001},
    {"id": "node-beta", "host": "127.0.0.1", "port": 8002},
    {"id": "node-gamma", "host": "127.0.0.1", "port": 8003},
    {"id": "node-delta", "host": "127.0.0.1", "port": 8004},
    {"id": "node-epsilon", "host": "127.0.0.1", "port": 8005},
]


# =============================================================================
# Network Setup Functions
# =============================================================================

def create_gossip_network():
    """Create a network of gossip nodes"""
    print("📡 Creating Gossip Protocol Network")
    print("-" * 70)
    
    nodes = []
    for config in NODE_CONFIGS:
        node = GossipNode(config["id"], config["host"], config["port"])
        nodes.append(node)
        print(f"   Created gossip node: {config['id']} @ {config['host']}:{config['port']}")
    
    # Connect nodes to each other
    print("\n   Connecting nodes...")
    for i, node in enumerate(nodes):
        for j, other_node in enumerate(nodes):
            if i != j:
                node.add_neighbor(
                    other_node.node_id,
                    other_node.host,
                    other_node.port
                )
    
    print(f"   ✓ {len(nodes)} nodes created and interconnected")
    return nodes


def create_heartbeat_monitors():
    """Create heartbeat monitors for each node"""
    print("\n💓 Creating Heartbeat Monitors")
    print("-" * 70)
    
    monitors = []
    for config in NODE_CONFIGS:
        monitor = HeartbeatMonitor(config["id"], timeout=10)
        monitors.append(monitor)
        print(f"   Monitor created for: {config['id']} (timeout: 10s)")
    
    # Register nodes with each other
    print("\n   Registering peer nodes...")
    for i, monitor in enumerate(monitors):
        for j, config in enumerate(NODE_CONFIGS):
            if i != j:
                monitor.register_node(config["id"])
    
    print(f"   ✓ {len(monitors)} monitors active")
    return monitors


def create_task_routers():
    """Create task routers for each node"""
    print("\n🎯 Creating Task Routers")
    print("-" * 70)
    
    routers = []
    for config in NODE_CONFIGS:
        router = TaskRouter(config["id"])
        routers.append(router)
        print(f"   Router created for: {config['id']}")
    
    print(f"   ✓ {len(routers)} routers initialized")
    return routers


async def create_kademlia_network():
    """Create Kademlia DHT network"""
    print("\n🔍 Creating Kademlia DHT Network")
    print("-" * 70)
    
    # Generate unique node IDs for Kademlia (160-bit hex strings)
    kad_ids = [
        "aaaa1111bbbb2222cccc3333dddd4444eeee5555",
        "1111aaaa2222bbbb3333cccc4444dddd5555eeee",
        "2222bbbb3333cccc4444dddd5555eeee6666ffff",
        "3333cccc4444dddd5555eeee6666ffff7777aaaa",
        "4444dddd5555eeee6666ffff7777aaaa8888bbbb",
    ]
    
    networks = []
    for i, config in enumerate(NODE_CONFIGS):
        network = KademliaNetwork(
            kad_ids[i],
            config["host"],
            config["port"]
        )
        networks.append(network)
        print(f"   DHT node: {config['id']} (ID: {kad_ids[i][:16]}...)")
    
    # Bootstrap network (nodes join via first node)
    print("\n   Bootstrapping network...")
    bootstrap_host = NODE_CONFIGS[0]["host"]
    bootstrap_port = NODE_CONFIGS[0]["port"]
    
    for i, network in enumerate(networks[1:], 1):
        await network.join(bootstrap_host, bootstrap_port)
        # Add peer connections
        for j, other_network in enumerate(networks):
            if i != j:
                network.add_peer(
                    other_network.node_id,
                    other_network.host,
                    other_network.port
                )
    
    print(f"   ✓ {len(networks)} DHT nodes connected")
    return networks


# =============================================================================
# Network Simulation
# =============================================================================

async def simulate_gossip_round(gossip_nodes):
    """Simulate one round of gossip protocol"""
    print("\n📢 Simulating Gossip Round")
    print("-" * 70)
    
    # Each node creates and shares gossip message
    for node in gossip_nodes:
        message = node.create_gossip_message()
        
        # Share with all neighbors
        for other_node in gossip_nodes:
            if other_node.node_id != node.node_id:
                other_node.receive_gossip(message)
    
    print("\n   Network Load Status:")
    gossip_nodes[0].display_network_load()


def simulate_heartbeat_round(monitors):
    """Simulate heartbeat monitoring"""
    print("\n💗 Simulating Heartbeat Round")
    print("-" * 70)
    
    # Simulate heartbeats from all nodes
    for monitor in monitors:
        for other_config in NODE_CONFIGS:
            if monitor.node_id != other_config["id"]:
                monitor.receive_heartbeat(other_config["id"])
    
    # Check node health
    print("\n   Node Health Check:")
    monitors[0].display_status()


def simulate_task_routing(routers, gossip_nodes):
    """Simulate task routing based on gossip state"""
    print("\n🚀 Simulating Task Routing")
    print("-" * 70)
    
    # Update routers with gossip state
    for router in routers:
        for node in gossip_nodes:
            load = node.get_local_load()
            router.update_load(node.node_id, load['cpu'], load['ram'])
    
    # Route some example tasks
    tasks = [
        ("ml_inference", {"model": "bert-large"}),
        ("data_processing", {"rows": 100000}),
        ("matrix_multiply", {"size": 1000}),
        ("video_encoding", {"format": "h264"}),
        ("batch_transform", {"records": 50000}),
    ]
    
    print("\n   Routing Tasks:")
    for task_name, task_data in tasks:
        target, entry = routers[0].route_task(task_name, task_data)
        print(f"      '{task_name}' → {target} (CPU: {entry['cpu']}%)")
    
    print("\n   Routing History:")
    routers[0].display_history()


async def store_and_retrieve_data(kad_networks):
    """Demonstrate DHT data storage and retrieval"""
    print("\n💾 Demonstrating DHT Storage & Retrieval")
    print("-" * 70)
    
    # Store data on first node
    node = kad_networks[0]
    
    print("\n   Storing data...")
    key1 = node.store("task_config_ml", {"lr": 0.01, "epochs": 100})
    print(f"      Stored 'task_config_ml'")
    
    key2 = node.store("node_capabilities", {"gpu": True, "ram": 32})
    print(f"      Stored 'node_capabilities'")
    
    key3 = node.store("service_endpoint", {"url": "http://api.mesh.local"})
    print(f"      Stored 'service_endpoint'")
    
    # Retrieve data
    print("\n   Retrieving data...")
    data1 = node.get("task_config_ml")
    print(f"      Retrieved 'task_config_ml': {data1['value']}")
    
    data2 = node.get("node_capabilities")
    print(f"      Retrieved 'node_capabilities': {data2['value']}")
    
    # Display DHT stats
    print()
    node.display()


# =============================================================================
# Main Demonstration
# =============================================================================

async def main():
    print("=" * 70)
    print("MeshWeaver - Multi-Node Setup Example")
    print("=" * 70)
    print()
    
    # Step 1: Create Gossip Network
    gossip_nodes = create_gossip_network()
    
    # Step 2: Create Heartbeat Monitors
    heartbeat_monitors = create_heartbeat_monitors()
    
    # Step 3: Create Task Routers
    task_routers = create_task_routers()
    
    # Step 4: Create Kademlia DHT
    kad_networks = await create_kademlia_network()
    
    # =========================================================================
    # Network Operation Simulation
    # =========================================================================
    print("\n" + "=" * 70)
    print("🌐 Network Operation Simulation")
    print("=" * 70)
    
    # Simulate gossip protocol
    await simulate_gossip_round(gossip_nodes)
    
    # Simulate heartbeat monitoring
    simulate_heartbeat_round(heartbeat_monitors)
    
    # Simulate task routing
    simulate_task_routing(task_routers, gossip_nodes)
    
    # Demonstrate DHT storage
    await store_and_retrieve_data(kad_networks)
    
    # =========================================================================
    # Network Statistics
    # =========================================================================
    print("\n" + "=" * 70)
    print("📊 Network Statistics")
    print("=" * 70)
    print(f"\n   Total Nodes: {len(NODE_CONFIGS)}")
    print(f"   Gossip Connections: {len(gossip_nodes) * (len(gossip_nodes) - 1)}")
    print(f"   Heartbeat Monitors: {len(heartbeat_monitors)}")
    print(f"   Active Routers: {len(task_routers)}")
    print(f"   DHT Nodes: {len(kad_networks)}")
    print(f"\n   Network Topology: Full Mesh")
    print(f"   Communication: Peer-to-Peer")
    print(f"   Consensus: Gossip Protocol")
    print(f"   Discovery: Kademlia DHT")
    
    # =========================================================================
    # Summary
    # =========================================================================
    print("\n" + "=" * 70)
    print("✅ Multi-Node Setup Complete!")
    print("=" * 70)
    
    print("\n🎓 Key Takeaways:")
    print("   1. Multiple nodes can be created and interconnected")
    print("   2. Gossip protocol shares resource state across network")
    print("   3. Heartbeat monitoring detects node failures")
    print("   4. Task routing selects optimal nodes based on CPU load")
    print("   5. Kademlia DHT enables decentralized data storage")
    print()
    
    print("Network Architecture:")
    print("""
           node-alpha ←→ node-beta
                ↕           ↕
           node-gamma ←→ node-delta
                    ↕
               node-epsilon
    
    • Full mesh connectivity
    • Gossip protocol for state propagation
    • DHT for peer discovery
    • Load-based task routing
    """)
    
    print("\nNext Steps:")
    print("   • Try dht_node_discovery.py for DHT deep dive")
    print("   • Explore custom_routing_strategy.py for advanced routing")
    print()


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    print("\nStarting MeshWeaver Multi-Node Setup Example...")
    print("Press Ctrl+C to exit\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
