#!/usr/bin/env python3
"""
MeshWeaver Example 4: DHT Node Discovery
=========================================

This example demonstrates Kademlia DHT in depth:
- Bootstrap node initialization
- New node joining process
- K-bucket management
- Peer lookup and routing
- XOR distance calculation
- Data storage and retrieval

Difficulty: ⭐⭐⭐ Advanced
Run time: ~10 seconds
"""

import asyncio
import sys
import os
import hashlib

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from meshweaver.dht.kademlia import KademliaNetwork


# =============================================================================
# Helper Functions
# =============================================================================

def generate_node_id(seed):
    """Generate a deterministic 160-bit node ID"""
    return hashlib.sha1(seed.encode()).hexdigest()


def xor_distance(id1, id2):
    """Calculate XOR distance between two node IDs"""
    return int(id1, 16) ^ int(id2, 16)


def format_distance(distance):
    """Format distance for display"""
    if distance == 0:
        return "0 (same node)"
    bit_length = distance.bit_length()
    return f"2^{bit_length-1} to 2^{bit_length}"


# =============================================================================
# Network Setup
# =============================================================================

async def setup_bootstrap_node():
    """Create the bootstrap (first) node"""
    print("🚀 Creating Bootstrap Node")
    print("-" * 70)
    
    node_id = generate_node_id("bootstrap-node")
    node = KademliaNetwork(node_id, "127.0.0.1", 8001)
    
    print(f"   Node ID: {node_id}")
    print(f"   Address: {node.host}:{node.port}")
    print(f"   Role: Bootstrap Node (Network Entry Point)")
    print(f"   K-Buckets: 160")
    print(f"   Max Peers/Bucket: 20")
    
    return node


async def join_new_nodes(bootstrap_node, num_nodes=5):
    """Create and join new nodes to the network"""
    print(f"\n📥 Joining {num_nodes} New Nodes")
    print("-" * 70)
    
    nodes = [bootstrap_node]
    
    for i in range(1, num_nodes + 1):
        print(f"\n   Node #{i}:")
        
        # Generate node ID
        node_id = generate_node_id(f"node-{i}")
        port = 8001 + i
        
        # Create node
        node = KademliaNetwork(node_id, "127.0.0.1", port)
        print(f"      ID: {node_id[:16]}...")
        print(f"      Address: {node.host}:{port}")
        
        # Join via bootstrap
        await node.join(bootstrap_node.host, bootstrap_node.port)
        
        # Add to bootstrap node's routing table
        bootstrap_node.add_peer(node.node_id, node.host, node.port)
        
        # Add bootstrap to new node's routing table
        node.add_peer(bootstrap_node.node_id, bootstrap_node.host, bootstrap_node.port)
        
        # Add previous nodes
        for existing_node in nodes[1:]:
            node.add_peer(existing_node.node_id, existing_node.host, existing_node.port)
            existing_node.add_peer(node.node_id, node.host, node.port)
        
        nodes.append(node)
        print(f"      ✓ Joined network")
    
    print(f"\n   ✓ Total nodes in network: {len(nodes)}")
    return nodes


# =============================================================================
# DHT Operations
# =============================================================================

def demonstrate_xor_distance(nodes):
    """Demonstrate XOR distance metric"""
    print("\n📏 XOR Distance Metric")
    print("-" * 70)
    
    target_node = nodes[0]
    print(f"\n   Reference Node: {target_node.node_id[:16]}...")
    print(f"\n   Distance to other nodes:")
    print(f"   {'Node ID':<18} {'Distance (decimal)':<20} {'Distance Range'}")
    print(f"   {'-'*18} {'-'*20} {'-'*30}")
    
    for node in nodes[1:4]:  # Show first 3 for clarity
        distance = xor_distance(target_node.node_id, node.node_id)
        dist_range = format_distance(distance)
        print(f"   {node.node_id[:16]:<18} {distance:<20} {dist_range}")
    
    print(f"\n   ℹ️  Closer nodes have smaller XOR distance")
    print(f"   ℹ️  Distance determines k-bucket placement")


def demonstrate_bucket_distribution(node):
    """Show how peers are distributed across k-buckets"""
    print("\n🗂️  K-Bucket Distribution")
    print("-" * 70)
    
    print(f"\n   Node: {node.node_id[:16]}...")
    
    # Count peers per bucket
    bucket_counts = {}
    for i, bucket in enumerate(node.buckets):
        if len(bucket.peers) > 0:
            bucket_counts[i] = len(bucket.peers)
    
    if bucket_counts:
        print(f"\n   Active K-Buckets:")
        print(f"   {'Bucket':<10} {'Peers':<10} {'Distance Range'}")
        print(f"   {'-'*10} {'-'*10} {'-'*30}")
        
        for bucket_id, count in sorted(bucket_counts.items()):
            dist_range = f"2^{bucket_id} to 2^{bucket_id+1}"
            print(f"   {bucket_id:<10} {count:<10} {dist_range}")
        
        total_peers = sum(bucket_counts.values())
        print(f"\n   Total peers stored: {total_peers}")
        print(f"   Empty buckets: {160 - len(bucket_counts)}")
    else:
        print(f"\n   No peers in routing table")


def demonstrate_peer_lookup(node, target_id=None):
    """Demonstrate finding closest peers to a target"""
    print("\n🔍 Peer Lookup (FIND_NODE)")
    print("-" * 70)
    
    if target_id is None:
        # Use a semi-random target
        target_id = generate_node_id("lookup-target")
    
    print(f"\n   Target ID: {target_id[:16]}...")
    print(f"   Searching for 3 closest nodes...")
    
    closest = node.find_node(target_id, k=3)
    
    if closest:
        print(f"\n   Found {len(closest)} nodes:")
        print(f"   {'Node ID':<18} {'Address':<20} {'XOR Distance'}")
        print(f"   {'-'*18} {'-'*20} {'-'*15}")
        
        for peer in closest:
            distance = xor_distance(peer['id'], target_id)
            address = f"{peer['host']}:{peer['port']}"
            print(f"   {peer['id'][:16]:<18} {address:<20} {distance}")
    else:
        print(f"   No nodes found")
    
    print(f"\n   ℹ️  Lookup complexity: O(log n)")


def demonstrate_data_storage(nodes):
    """Demonstrate distributed data storage"""
    print("\n💾 Distributed Data Storage")
    print("-" * 70)
    
    storage_node = nodes[0]
    
    # Store various types of data
    data_items = [
        ("task:ml_training", {"model": "resnet50", "epochs": 100}),
        ("config:network", {"timeout": 30, "retry": 3}),
        ("metrics:node_alpha", {"cpu": 45.2, "ram": 62.1}),
        ("route:task_123", {"target": "node-beta", "priority": 5}),
    ]
    
    print(f"\n   Storing {len(data_items)} items on node: {storage_node.node_id[:16]}...")
    print()
    
    stored_keys = []
    for key, value in data_items:
        hash_key = storage_node.store(key, value)
        stored_keys.append((key, hash_key))
        print(f"      '{key}'")
        print(f"         Hash: {hash_key[:16]}...")
        print(f"         Value: {value}")
    
    # Retrieve data
    print(f"\n   Retrieving stored data...")
    print()
    
    for key, hash_key in stored_keys[:2]:  # Show first 2
        data = storage_node.get(key)
        if data:
            print(f"      '{key}': {data['value']}")
    
    # Display storage stats
    print(f"\n   Storage Statistics:")
    storage_node.display()


def demonstrate_network_topology(nodes):
    """Show the network topology"""
    print("\n🕸️  Network Topology")
    print("-" * 70)
    
    print(f"\n   Total Nodes: {len(nodes)}")
    print(f"\n   Node Connections:")
    
    for i, node in enumerate(nodes[:4]):  # Show first 4
        peer_count = sum(len(bucket.peers) for bucket in node.buckets)
        print(f"\n   {i+1}. {node.node_id[:16]}... @ {node.host}:{node.port}")
        print(f"      Peers: {peer_count}")
        print(f"      Data items: {len(node.data)}")
    
    if len(nodes) > 4:
        print(f"\n   ... and {len(nodes) - 4} more nodes")


# =============================================================================
# Main Demonstration
# =============================================================================

async def main():
    print("=" * 70)
    print("MeshWeaver - DHT Node Discovery Example")
    print("=" * 70)
    print()
    
    # =========================================================================
    # Phase 1: Network Setup
    # =========================================================================
    print("Phase 1: Network Initialization")
    print("=" * 70)
    
    # Create bootstrap node
    bootstrap = await setup_bootstrap_node()
    
    # Join additional nodes
    all_nodes = await join_new_nodes(bootstrap, num_nodes=5)
    
    # =========================================================================
    # Phase 2: DHT Operations
    # =========================================================================
    print("\n\nPhase 2: DHT Operations")
    print("=" * 70)
    
    # Demonstrate XOR distance
    demonstrate_xor_distance(all_nodes)
    
    # Show k-bucket distribution
    demonstrate_bucket_distribution(all_nodes[0])
    
    # Demonstrate peer lookup
    demonstrate_peer_lookup(all_nodes[0])
    
    # Demonstrate data storage
    demonstrate_data_storage(all_nodes)
    
    # Show network topology
    demonstrate_network_topology(all_nodes)
    
    # =========================================================================
    # Summary
    # =========================================================================
    print("\n\n" + "=" * 70)
    print("✅ DHT Node Discovery Demo Complete!")
    print("=" * 70)
    
    print("\n🎓 Key Concepts Demonstrated:")
    print("   1. Bootstrap Node: Entry point for network joining")
    print("   2. XOR Distance: Metric for node proximity")
    print("   3. K-Buckets: Routing table organization (160 buckets)")
    print("   4. FIND_NODE: Locate closest peers (O(log n) complexity)")
    print("   5. STORE/GET: Distributed data storage")
    print("   6. Routing Table: Maintains knowledge of network peers")
    
    print("\n📚 Kademlia Properties:")
    print("   • Decentralized: No central coordinator")
    print("   • Scalable: O(log n) lookup time")
    print("   • Fault-Tolerant: Survives node failures")
    print("   • Self-Organizing: Automatic routing table updates")
    
    print("\n🔧 Configuration:")
    print(f"   • K-Bucket Size: 20 peers/bucket")
    print(f"   • Total Buckets: 160")
    print(f"   • Network Capacity: ~3200 peers")
    print(f"   • ID Space: 2^160 possible node IDs")
    
    print("\n🌐 Real-World Applications:")
    print("   • BitTorrent: Peer discovery")
    print("   • Ethereum: Network bootstrapping")
    print("   • IPFS: Content routing")
    print("   • MeshWeaver: Task broker node discovery")
    
    print()


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    print("\nStarting MeshWeaver DHT Node Discovery Example...")
    print("Press Ctrl+C to exit\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
