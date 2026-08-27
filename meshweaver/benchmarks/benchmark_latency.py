# MeshWeaver - Latency Benchmarks - Week 3
# Measure round-trip latency across mesh network components

import asyncio
import time
import statistics
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from network.gossip import GossipNode
from network.task_router import TaskRouter
from network.heartbeat import HeartbeatMonitor
from dht.kademlia import KademliaNetwork
from serializer.task_queue import DistributedQueue
import json
from datetime import datetime


class LatencyBenchmark:
    """Benchmark latency of mesh network operations"""
    
    def __init__(self):
        self.results = {
            'gossip_latency': [],
            'routing_latency': [],
            'heartbeat_latency': [],
            'dht_lookup_latency': [],
            'task_execution_latency': [],
            'serialization_latency': []
        }
    
    def benchmark_gossip_latency(self, num_trials=100):
        """Measure gossip message propagation latency"""
        print("\n" + "="*60)
        print("BENCHMARK 1: Gossip Protocol Latency")
        print("="*60)
        
        node1 = GossipNode("node-1", "127.0.0.1", 8001)
        node2 = GossipNode("node-2", "127.0.0.1", 8002)
        node1.add_neighbor("node-2", "127.0.0.1", 8002)
        
        latencies = []
        
        for i in range(num_trials):
            start = time.perf_counter()
            
            # Create and send gossip message
            msg = node1.create_gossip_message()
            node2.receive_gossip(msg)
            
            end = time.perf_counter()
            latency_ms = (end - start) * 1000
            latencies.append(latency_ms)
        
        self.results['gossip_latency'] = latencies
        
        print(f"Trials: {num_trials}")
        print(f"Mean Latency: {statistics.mean(latencies):.4f} ms")
        print(f"Median Latency: {statistics.median(latencies):.4f} ms")
        print(f"Min Latency: {min(latencies):.4f} ms")
        print(f"Max Latency: {max(latencies):.4f} ms")
        print(f"Std Dev: {statistics.stdev(latencies):.4f} ms")
        print(f"95th Percentile: {self._percentile(latencies, 95):.4f} ms")
        print(f"99th Percentile: {self._percentile(latencies, 99):.4f} ms")
        
        return latencies
    
    def benchmark_routing_latency(self, num_trials=100):
        """Measure task routing decision latency"""
        print("\n" + "="*60)
        print("BENCHMARK 2: Task Routing Latency")
        print("="*60)
        
        router = TaskRouter("coordinator")
        
        # Setup network state
        router.update_load("node-1", cpu=45, ram=60)
        router.update_load("node-2", cpu=23, ram=45)
        router.update_load("node-3", cpu=78, ram=50)
        router.update_load("node-4", cpu=12, ram=30)
        
        latencies = []
        
        for i in range(num_trials):
            start = time.perf_counter()
            
            # Route a task
            router.route_task(f"task_{i}", {"data": "test"})
            
            end = time.perf_counter()
            latency_ms = (end - start) * 1000
            latencies.append(latency_ms)
        
        self.results['routing_latency'] = latencies
        
        print(f"Trials: {num_trials}")
        print(f"Mean Latency: {statistics.mean(latencies):.4f} ms")
        print(f"Median Latency: {statistics.median(latencies):.4f} ms")
        print(f"Min Latency: {min(latencies):.4f} ms")
        print(f"Max Latency: {max(latencies):.4f} ms")
        print(f"Std Dev: {statistics.stdev(latencies):.4f} ms")
        print(f"95th Percentile: {self._percentile(latencies, 95):.4f} ms")
        
        return latencies
    
    async def benchmark_heartbeat_latency(self, num_trials=100):
        """Measure heartbeat round-trip latency"""
        print("\n" + "="*60)
        print("BENCHMARK 3: Heartbeat Monitor Latency")
        print("="*60)
        
        monitor = HeartbeatMonitor("coordinator", timeout=5)
        monitor.register_node("node-1")
        monitor.register_node("node-2")
        monitor.register_node("node-3")
        
        latencies = []
        
        for i in range(num_trials):
            start = time.perf_counter()
            
            # Simulate heartbeat exchange
            monitor.receive_heartbeat("node-1")
            monitor.receive_heartbeat("node-2")
            monitor.receive_heartbeat("node-3")
            
            end = time.perf_counter()
            latency_ms = (end - start) * 1000
            latencies.append(latency_ms)
            
            await asyncio.sleep(0.001)  # Small delay between trials
        
        self.results['heartbeat_latency'] = latencies
        
        print(f"Trials: {num_trials}")
        print(f"Mean Latency: {statistics.mean(latencies):.4f} ms")
        print(f"Median Latency: {statistics.median(latencies):.4f} ms")
        print(f"Min Latency: {min(latencies):.4f} ms")
        print(f"Max Latency: {max(latencies):.4f} ms")
        print(f"Std Dev: {statistics.stdev(latencies):.4f} ms")
        
        return latencies
    
    async def benchmark_dht_lookup_latency(self, num_trials=100):
        """Measure DHT key lookup latency"""
        print("\n" + "="*60)
        print("BENCHMARK 4: DHT Lookup Latency")
        print("="*60)
        
        dht = KademliaNetwork("node123456789abc", "127.0.0.1", 8001)
        
        # Add peers to DHT
        for i in range(20):
            peer_id = f"peer{i:04d}{'x'*12}"
            dht.add_peer(peer_id, "127.0.0.1", 8000+i)
        
        # Store some data
        for i in range(50):
            dht.store(f"key_{i}", {"value": f"data_{i}"})
        
        latencies = []
        
        for i in range(num_trials):
            start = time.perf_counter()
            
            # Perform DHT lookup
            key = f"key_{i % 50}"
            result = dht.get(key)
            
            end = time.perf_counter()
            latency_ms = (end - start) * 1000
            latencies.append(latency_ms)
        
        self.results['dht_lookup_latency'] = latencies
        
        print(f"Trials: {num_trials}")
        print(f"Mean Latency: {statistics.mean(latencies):.4f} ms")
        print(f"Median Latency: {statistics.median(latencies):.4f} ms")
        print(f"Min Latency: {min(latencies):.4f} ms")
        print(f"Max Latency: {max(latencies):.4f} ms")
        print(f"Std Dev: {statistics.stdev(latencies):.4f} ms")
        
        return latencies
    
    async def benchmark_task_execution_latency(self, num_trials=50):
        """Measure end-to-end task execution latency"""
        print("\n" + "="*60)
        print("BENCHMARK 5: Task Execution Latency")
        print("="*60)
        
        queue = DistributedQueue("benchmark-node")
        
        def simple_task(x, y):
            return x + y
        
        def compute_task(data):
            return {'sum': sum(data), 'mean': sum(data)/len(data)}
        
        latencies = []
        
        for i in range(num_trials):
            start = time.perf_counter()
            
            # Submit and execute task
            await queue.submit(simple_task, i, i*2, priority=1)
            await queue.execute_next()
            
            end = time.perf_counter()
            latency_ms = (end - start) * 1000
            latencies.append(latency_ms)
        
        self.results['task_execution_latency'] = latencies
        
        print(f"Trials: {num_trials}")
        print(f"Mean Latency: {statistics.mean(latencies):.4f} ms")
        print(f"Median Latency: {statistics.median(latencies):.4f} ms")
        print(f"Min Latency: {min(latencies):.4f} ms")
        print(f"Max Latency: {max(latencies):.4f} ms")
        print(f"Std Dev: {statistics.stdev(latencies):.4f} ms")
        
        return latencies
    
    def benchmark_serialization_latency(self, num_trials=100):
        """Measure function serialization latency"""
        print("\n" + "="*60)
        print("BENCHMARK 6: Serialization Latency")
        print("="*60)
        
        import cloudpickle
        
        def test_function(x, y, z):
            result = x * y + z
            return {'result': result, 'type': 'computation'}
        
        latencies = []
        
        for i in range(num_trials):
            start = time.perf_counter()
            
            # Serialize function
            serialized = cloudpickle.dumps(test_function)
            
            # Deserialize function
            deserialized = cloudpickle.loads(serialized)
            
            end = time.perf_counter()
            latency_ms = (end - start) * 1000
            latencies.append(latency_ms)
        
        self.results['serialization_latency'] = latencies
        
        print(f"Trials: {num_trials}")
        print(f"Mean Latency: {statistics.mean(latencies):.4f} ms")
        print(f"Median Latency: {statistics.median(latencies):.4f} ms")
        print(f"Min Latency: {min(latencies):.4f} ms")
        print(f"Max Latency: {max(latencies):.4f} ms")
        print(f"Std Dev: {statistics.stdev(latencies):.4f} ms")
        print(f"Serialized Size: {len(serialized)} bytes")
        
        return latencies
    
    def _percentile(self, data, percentile):
        """Calculate percentile of data"""
        size = len(data)
        return sorted(data)[int(size * percentile / 100)]
    
    async def run_all_benchmarks(self):
        """Run all latency benchmarks"""
        print("\n" + "="*70)
        print(" "*20 + "LATENCY BENCHMARKS")
        print("="*70)
        
        self.benchmark_gossip_latency()
        self.benchmark_routing_latency()
        await self.benchmark_heartbeat_latency()
        await self.benchmark_dht_lookup_latency()
        await self.benchmark_task_execution_latency()
        self.benchmark_serialization_latency()
        
        self._print_summary()
    
    def _print_summary(self):
        """Print summary of all benchmarks"""
        print("\n" + "="*70)
        print(" "*25 + "SUMMARY")
        print("="*70)
        
        for name, latencies in self.results.items():
            if latencies:
                print(f"\n{name.replace('_', ' ').title()}:")
                print(f"  Mean: {statistics.mean(latencies):.4f} ms")
                print(f"  Median: {statistics.median(latencies):.4f} ms")
                print(f"  95th percentile: {self._percentile(latencies, 95):.4f} ms")
        
        print("\n" + "="*70)
        print("✅ All latency benchmarks complete!")
        print("="*70)
    
    def export_results(self, filename='results/latency_results.json'):
        """Export results to JSON file"""
        results_data = {
            'timestamp': datetime.now().isoformat(),
            'benchmarks': {}
        }
        
        for name, latencies in self.results.items():
            if latencies:
                results_data['benchmarks'][name] = {
                    'mean': statistics.mean(latencies),
                    'median': statistics.median(latencies),
                    'min': min(latencies),
                    'max': max(latencies),
                    'std_dev': statistics.stdev(latencies),
                    'p95': self._percentile(latencies, 95),
                    'p99': self._percentile(latencies, 99),
                    'num_trials': len(latencies),
                    'raw_data': latencies[:100]  # Store first 100 samples
                }
        
        os.makedirs('results', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"\n📊 Results exported to {filename}")


async def main():
    """Run latency benchmarks"""
    benchmark = LatencyBenchmark()
    await benchmark.run_all_benchmarks()
    benchmark.export_results()


if __name__ == "__main__":
    asyncio.run(main())
