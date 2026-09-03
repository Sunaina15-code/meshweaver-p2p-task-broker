#!/usr/bin/env python3
"""
MeshWeaver Example 5: Custom Routing Strategy
==============================================

This example demonstrates advanced routing strategies:
- Custom routing algorithms
- Load balancing strategies
- Dynamic node selection
- Performance optimization
- Routing policies

Difficulty: ⭐⭐⭐ Advanced
Run time: ~15 seconds
"""

import asyncio
import sys
import os
import random
from datetime import datetime
from typing import List, Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from meshweaver.network.task_router import TaskRouter
from meshweaver.network.gossip import GossipNode


# =============================================================================
# Custom Router Classes
# =============================================================================

class RoundRobinRouter(TaskRouter):
    """Route tasks in round-robin fashion"""
    
    def __init__(self, node_id):
        super().__init__(node_id)
        self.current_index = 0
    
    def find_best_node(self):
        """Select next node in round-robin order"""
        if not self.node_loads:
            return self.node_id
        
        nodes = list(self.node_loads.keys())
        selected = nodes[self.current_index % len(nodes)]
        self.current_index += 1
        
        print(f"[RoundRobin] Selected: {selected} (index: {self.current_index - 1})")
        return selected


class WeightedRouter(TaskRouter):
    """Route based on combined CPU and RAM metrics"""
    
    def __init__(self, node_id, cpu_weight=0.7, ram_weight=0.3):
        super().__init__(node_id)
        self.cpu_weight = cpu_weight
        self.ram_weight = ram_weight
    
    def find_best_node(self):
        """Select node with lowest weighted score"""
        if not self.node_loads:
            return self.node_id
        
        scores = {}
        for node_id, load in self.node_loads.items():
            score = (load['cpu'] * self.cpu_weight + 
                    load['ram'] * self.ram_weight)
            scores[node_id] = score
        
        best = min(scores.keys(), key=lambda n: scores[n])
        print(f"[Weighted] Selected: {best} (score: {scores[best]:.2f})")
        return best


class ThresholdRouter(TaskRouter):
    """Only route to nodes below a threshold"""
    
    def __init__(self, node_id, cpu_threshold=70, ram_threshold=80):
        super().__init__(node_id)
        self.cpu_threshold = cpu_threshold
        self.ram_threshold = ram_threshold
    
    def find_best_node(self):
        """Select node below thresholds with lowest CPU"""
        if not self.node_loads:
            return self.node_id
        
        # Filter nodes below threshold
        eligible = {
            nid: load for nid, load in self.node_loads.items()
            if load['cpu'] < self.cpu_threshold and 
               load['ram'] < self.ram_threshold
        }
        
        if not eligible:
            print(f"[Threshold] ⚠️  No eligible nodes (using fallback)")
            return self.node_id
        
        best = min(eligible.keys(), key=lambda n: eligible[n]['cpu'])
        print(f"[Threshold] Selected: {best} "
              f"(CPU: {eligible[best]['cpu']}%, RAM: {eligible[best]['ram']}%)")
        return best


class PriorityAwareRouter(TaskRouter):
    """Route based on task priority and node capability"""
    
    def __init__(self, node_id):
        super().__init__(node_id)
        self.node_capabilities = {}
    
    def set_node_capability(self, node_id, capability_score):
        """Set capability score for a node (1-10, higher = more capable)"""
        self.node_capabilities[node_id] = capability_score
    
    def find_best_node_for_priority(self, priority=1):
        """Select node based on task priority"""
        if not self.node_loads:
            return self.node_id
        
        # High priority tasks go to high-capability nodes
        if priority >= 8:
            # Find most capable node with reasonable load
            eligible = {
                nid: (load, self.node_capabilities.get(nid, 5))
                for nid, load in self.node_loads.items()
                if load['cpu'] < 80
            }
            if eligible:
                best = max(eligible.keys(), 
                          key=lambda n: eligible[n][1])  # Max capability
                print(f"[Priority] High priority → high-capability: {best}")
                return best
        
        # Low priority tasks go to any available node
        best = min(self.node_loads.keys(), 
                  key=lambda n: self.node_loads[n]['cpu'])
        print(f"[Priority] Normal priority → lowest CPU: {best}")
        return best


class LocalityAwareRouter(TaskRouter):
    """Route based on data locality"""
    
    def __init__(self, node_id):
        super().__init__(node_id)
        self.data_locations = {}  # dataset_id -> [node_ids]
    
    def register_data_location(self, dataset_id, node_id):
        """Register that a node has a dataset"""
        if dataset_id not in self.data_locations:
            self.data_locations[dataset_id] = []
        if node_id not in self.data_locations[dataset_id]:
            self.data_locations[dataset_id].append(node_id)
    
    def find_best_node_for_data(self, dataset_id):
        """Find node with data and lowest load"""
        if dataset_id not in self.data_locations:
            print(f"[Locality] Dataset not found, using standard routing")
            return self.find_best_node()
        
        # Filter to nodes with the data
        nodes_with_data = self.data_locations[dataset_id]
        eligible = {
            nid: load for nid, load in self.node_loads.items()
            if nid in nodes_with_data
        }
        
        if not eligible:
            print(f"[Locality] No nodes with data available")
            return self.node_id
        
        best = min(eligible.keys(), key=lambda n: eligible[n]['cpu'])
        print(f"[Locality] Selected node with local data: {best}")
        return best


# =============================================================================
# Simulation Setup
# =============================================================================

def create_mock_nodes():
    """Create mock nodes with varying loads"""
    nodes = [
        {"id": "node-alpha", "cpu": 25, "ram": 40, "capability": 8},
        {"id": "node-beta", "cpu": 65, "ram": 70, "capability": 6},
        {"id": "node-gamma", "cpu": 45, "ram": 55, "capability": 7},
        {"id": "node-delta", "cpu": 15, "ram": 30, "capability": 9},
        {"id": "node-epsilon", "cpu": 85, "ram": 90, "capability": 5},
    ]
    return nodes


def update_router_with_loads(router, nodes):
    """Update router with node load information"""
    for node in nodes:
        router.update_load(node["id"], node["cpu"], node["ram"])


# =============================================================================
# Strategy Demonstrations
# =============================================================================

def demonstrate_round_robin():
    """Demonstrate round-robin routing"""
    print("\n🔄 Strategy 1: Round-Robin Routing")
    print("-" * 70)
    print("Routes tasks evenly across all nodes, ignoring load")
    print()
    
    router = RoundRobinRouter("coordinator")
    nodes = create_mock_nodes()
    update_router_with_loads(router, nodes)
    
    print("Routing 5 tasks:")
    for i in range(5):
        router.route_task(f"task_{i}", {})
    
    print("\n✓ All nodes used equally")


def demonstrate_weighted_routing():
    """Demonstrate weighted CPU+RAM routing"""
    print("\n⚖️  Strategy 2: Weighted Routing (CPU:70%, RAM:30%)")
    print("-" * 70)
    print("Considers both CPU and RAM with configurable weights")
    print()
    
    router = WeightedRouter("coordinator", cpu_weight=0.7, ram_weight=0.3)
    nodes = create_mock_nodes()
    update_router_with_loads(router, nodes)
    
    print("Node scores (lower is better):")
    for node in nodes:
        score = node['cpu'] * 0.7 + node['ram'] * 0.3
        print(f"   {node['id']:<15} CPU:{node['cpu']:>3}% RAM:{node['ram']:>3}% "
              f"→ Score: {score:>5.1f}")
    
    print("\nRouting 3 tasks:")
    for i in range(3):
        router.route_task(f"balanced_task_{i}", {})
    
    print("\n✓ Tasks routed to nodes with best combined metrics")


def demonstrate_threshold_routing():
    """Demonstrate threshold-based routing"""
    print("\n🚦 Strategy 3: Threshold Routing (CPU<70%, RAM<80%)")
    print("-" * 70)
    print("Only routes to nodes below resource thresholds")
    print()
    
    router = ThresholdRouter("coordinator", cpu_threshold=70, ram_threshold=80)
    nodes = create_mock_nodes()
    update_router_with_loads(router, nodes)
    
    print("Node eligibility:")
    for node in nodes:
        eligible = node['cpu'] < 70 and node['ram'] < 80
        status = "✓ Eligible" if eligible else "✗ Overloaded"
        print(f"   {node['id']:<15} CPU:{node['cpu']:>3}% RAM:{node['ram']:>3}% "
              f"→ {status}")
    
    print("\nRouting 3 tasks:")
    for i in range(3):
        router.route_task(f"threshold_task_{i}", {})
    
    print("\n✓ Only healthy nodes receive tasks")


def demonstrate_priority_routing():
    """Demonstrate priority-aware routing"""
    print("\n⭐ Strategy 4: Priority-Aware Routing")
    print("-" * 70)
    print("Routes high-priority tasks to high-capability nodes")
    print()
    
    router = PriorityAwareRouter("coordinator")
    nodes = create_mock_nodes()
    update_router_with_loads(router, nodes)
    
    # Set node capabilities
    for node in nodes:
        router.set_node_capability(node["id"], node["capability"])
    
    print("Node capabilities (1-10, higher = more capable):")
    for node in nodes:
        print(f"   {node['id']:<15} Capability: {node['capability']}/10")
    
    print("\nRouting tasks with different priorities:")
    
    # High priority task
    print("\n   Priority 10 (Critical):")
    target = router.find_best_node_for_priority(priority=10)
    router.route_task("critical_ml_training", {})
    
    # Normal priority tasks
    print("\n   Priority 5 (Normal):")
    target = router.find_best_node_for_priority(priority=5)
    router.route_task("regular_processing", {})
    
    print("\n   Priority 1 (Low):")
    target = router.find_best_node_for_priority(priority=1)
    router.route_task("background_task", {})
    
    print("\n✓ Task-node matching based on priority")


def demonstrate_locality_routing():
    """Demonstrate data locality-aware routing"""
    print("\n📍 Strategy 5: Locality-Aware Routing")
    print("-" * 70)
    print("Routes tasks to nodes where data already resides")
    print()
    
    router = LocalityAwareRouter("coordinator")
    nodes = create_mock_nodes()
    update_router_with_loads(router, nodes)
    
    # Register data locations
    router.register_data_location("dataset_images", "node-alpha")
    router.register_data_location("dataset_images", "node-gamma")
    router.register_data_location("dataset_text", "node-beta")
    router.register_data_location("dataset_text", "node-delta")
    
    print("Data distribution:")
    print("   dataset_images → node-alpha, node-gamma")
    print("   dataset_text   → node-beta, node-delta")
    
    print("\nRouting data-intensive tasks:")
    
    print("\n   Task requires 'dataset_images':")
    target = router.find_best_node_for_data("dataset_images")
    
    print("\n   Task requires 'dataset_text':")
    target = router.find_best_node_for_data("dataset_text")
    
    print("\n   Task with no data dependency:")
    target = router.find_best_node_for_data("dataset_unknown")
    
    print("\n✓ Minimizes data transfer by routing to local data")


# =============================================================================
# Comparison
# =============================================================================

def compare_strategies():
    """Compare all routing strategies side-by-side"""
    print("\n📊 Strategy Comparison")
    print("=" * 70)
    
    comparison = [
        {
            "strategy": "Round-Robin",
            "load_aware": "✗",
            "complexity": "O(1)",
            "use_case": "Uniform task distribution",
            "pros": "Simple, fair",
            "cons": "Ignores node capacity"
        },
        {
            "strategy": "Weighted",
            "load_aware": "✓",
            "complexity": "O(n)",
            "use_case": "Mixed resource optimization",
            "pros": "Balanced metrics",
            "cons": "Needs tuning"
        },
        {
            "strategy": "Threshold",
            "load_aware": "✓",
            "complexity": "O(n)",
            "use_case": "Prevent overload",
            "pros": "Protects nodes",
            "cons": "May reject tasks"
        },
        {
            "strategy": "Priority-Aware",
            "load_aware": "✓",
            "complexity": "O(n)",
            "use_case": "QoS differentiation",
            "pros": "Task-based routing",
            "cons": "Requires capabilities"
        },
        {
            "strategy": "Locality-Aware",
            "load_aware": "✓",
            "complexity": "O(n)",
            "use_case": "Data-intensive tasks",
            "pros": "Minimizes transfer",
            "cons": "Needs data tracking"
        },
    ]
    
    print(f"\n{'Strategy':<18} {'Load-Aware':<12} {'Complexity':<12} {'Best For':<25}")
    print("-" * 70)
    for item in comparison:
        print(f"{item['strategy']:<18} {item['load_aware']:<12} "
              f"{item['complexity']:<12} {item['use_case']:<25}")
    
    print("\n\nDetailed Analysis:")
    for item in comparison:
        print(f"\n{item['strategy']}:")
        print(f"   Pros: {item['pros']}")
        print(f"   Cons: {item['cons']}")


# =============================================================================
# Main Demonstration
# =============================================================================

async def main():
    print("=" * 70)
    print("MeshWeaver - Custom Routing Strategy Example")
    print("=" * 70)
    print()
    
    print("This example demonstrates 5 different routing strategies:")
    print("   1. Round-Robin")
    print("   2. Weighted (CPU + RAM)")
    print("   3. Threshold-Based")
    print("   4. Priority-Aware")
    print("   5. Locality-Aware")
    print()
    
    # Demonstrate each strategy
    demonstrate_round_robin()
    demonstrate_weighted_routing()
    demonstrate_threshold_routing()
    demonstrate_priority_routing()
    demonstrate_locality_routing()
    
    # Compare strategies
    compare_strategies()
    
    # Summary
    print("\n\n" + "=" * 70)
    print("✅ Custom Routing Strategy Demo Complete!")
    print("=" * 70)
    
    print("\n🎓 Key Takeaways:")
    print("   1. Different strategies suit different workloads")
    print("   2. Load-aware routing improves resource utilization")
    print("   3. Threshold routing prevents node overload")
    print("   4. Priority routing enables QoS differentiation")
    print("   5. Locality-aware routing minimizes data transfer")
    
    print("\n💡 Implementation Tips:")
    print("   • Combine strategies for hybrid approaches")
    print("   • Monitor and adjust based on metrics")
    print("   • Consider network topology and latency")
    print("   • Balance between optimality and complexity")
    
    print("\n🔧 Customization:")
    print("   • Extend TaskRouter base class")
    print("   • Override find_best_node() method")
    print("   • Add custom metrics and policies")
    print("   • Integrate with monitoring systems")
    
    print()


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    print("\nStarting MeshWeaver Custom Routing Strategy Example...")
    print("Press Ctrl+C to exit\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
