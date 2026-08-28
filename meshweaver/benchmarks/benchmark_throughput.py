# MeshWeaver - Throughput Benchmarks - Week 3
# Measure throughput and processing capacity

import asyncio
import time
import statistics
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from network.gossip import GossipNode
from network.task_router import TaskRouter
from serializer.task_queue import DistributedQueue
from serializer.ml_functions import logistic_regression_train, k_nearest_neighbors
import numpy as np
import json
from datetime import datetime


class ThroughputBenchmark:
    """Benchmark throughput of mesh network operations"""
    
    def __init__(self):
        self.results = {
            'tasks_per_second': [],
            'messages_per_second': [],
            'routing_throughput': [],
            'concurrent_tasks': [],
            'data_transfer_rate': []
        }
    
    async def benchmark_task_throughput(self, num_tasks=1000, duration=10):
        """Measure tasks processed per second"""
        print("\n" + "="*60)
        print("BENCHMARK 1: Task Processing Throughput")
        print("="*60)
        
        queue = DistributedQueue("throughput-node")
        
        def simple_task(x):
            return x * 2
        
        # Submit many tasks
        print(f"Submitting {num_tasks} tasks...")
        start_time = time.perf_counter()
        
        for i in range(num_tasks):
            await queue.submit(simple_task, i, priority=1)
        
        submission_time = time.perf_counter() - start_time
        
        # Execute all tasks
        print("Executing tasks...")
        execution_start = time.perf_counter()
        completed = 0
        
        while not queue.queue.empty():
            await queue.execute_next()
            completed += 1
        
        execution_time = time.perf_counter() - execution_start
        
        tasks_per_second = completed / execution_time
        self.results['tasks_per_second'].append(tasks_per_second)
        
        print(f"Tasks Submitted: {num_tasks}")
        print(f"Submission Time: {submission_time:.4f} s")
        print(f"Execution Time: {execution_time:.4f} s")
        print(f"Tasks Completed: {completed}")
        print(f"Throughput: {tasks_per_second:.2f} tasks/second")
        print(f"Avg Latency: {(execution_time/completed)*1000:.4f} ms/task")
        
        return tasks_per_second
    
    def benchmark_message_throughput(self, num_messages=10000):
        """Measure gossip message processing throughput"""
        print("\n" + "="*60)
        print("BENCHMARK 2: Message Processing Throughput")
        print("="*60)
        
        node1 = GossipNode("sender", "127.0.0.1", 8001)
        node2 = GossipNode("receiver", "127.0.0.1", 8002)
        
        # Generate messages
        messages = []
        for i in range(num_messages):
            msg = node1.create_gossip_message()
            messages.append(msg)
        
        # Process messages
        print(f"Processing {num_messages} messages...")
        start_time = time.perf_counter()
        
        for msg in messages:
            node2.receive_gossip(msg)
        
        elapsed = time.perf_counter() - start_time
        
        messages_per_second = num_messages / elapsed
        self.results['messages_per_second'].append(messages_per_second)
        
        print(f"Messages Processed: {num_messages}")
        print(f"Time Elapsed: {elapsed:.4f} s")
        print(f"Throughput: {messages_per_second:.2f} messages/second")
        print(f"Avg Processing Time: {(elapsed/num_messages)*1000:.4f} ms/message")
        
        return messages_per_second
    
    def benchmark_routing_throughput(self, num_routes=5000):
        """Measure routing decision throughput"""
        print("\n" + "="*60)
        print("BENCHMARK 3: Routing Decision Throughput")
        print("="*60)
        
        router = TaskRouter("coordinator")
        
        # Setup network
        router.update_load("node-1", cpu=45, ram=60)
        router.update_load("node-2", cpu=23, ram=45)
        router.update_load("node-3", cpu=78, ram=50)
        router.update_load("node-4", cpu=12, ram=30)
        router.update_load("node-5", cpu=56, ram=40)
        
        print(f"Making {num_routes} routing decisions...")
        start_time = time.perf_counter()
        
        for i in range(num_routes):
            router.route_task(f"task_{i}", {"data": "test"})
        
        elapsed = time.perf_counter() - start_time
        
        routes_per_second = num_routes / elapsed
        self.results['routing_throughput'].append(routes_per_second)
        
        print(f"Routing Decisions: {num_routes}")
        print(f"Time Elapsed: {elapsed:.4f} s")
        print(f"Throughput: {routes_per_second:.2f} routes/second")
        print(f"Avg Decision Time: {(elapsed/num_routes)*1000:.4f} ms/route")
        
        return routes_per_second
    
    async def benchmark_concurrent_tasks(self, num_concurrent=100):
        """Measure concurrent task execution capacity"""
        print("\n" + "="*60)
        print("BENCHMARK 4: Concurrent Task Execution")
        print("="*60)
        
        async def worker_task(task_id, duration=0.01):
            """Simulated worker task"""
            await asyncio.sleep(duration)
            return {'task_id': task_id, 'result': task_id * 2}
        
        # Create multiple concurrent workers
        print(f"Running {num_concurrent} concurrent tasks...")
        start_time = time.perf_counter()
        
        tasks = [worker_task(i) for i in range(num_concurrent)]
        results = await asyncio.gather(*tasks)
        
        elapsed = time.perf_counter() - start_time
        
        tasks_per_second = num_concurrent / elapsed
        self.results['concurrent_tasks'].append(tasks_per_second)
        
        print(f"Concurrent Tasks: {num_concurrent}")
        print(f"Total Time: {elapsed:.4f} s")
        print(f"Throughput: {tasks_per_second:.2f} tasks/second")
        print(f"Concurrency Factor: {num_concurrent / elapsed:.2f}x")
        
        return tasks_per_second
    
    async def benchmark_data_transfer(self, num_transfers=100, data_size_kb=100):
        """Measure data transfer throughput"""
        print("\n" + "="*60)
        print("BENCHMARK 5: Data Transfer Rate")
        print("="*60)
        
        import cloudpickle
        
        # Generate test data
        data = np.random.rand(data_size_kb * 128)  # ~100KB per transfer
        
        print(f"Transferring {num_transfers} x {data_size_kb}KB...")
        start_time = time.perf_counter()
        
        total_bytes = 0
        
        for i in range(num_transfers):
            # Simulate serialization and transmission
            serialized = cloudpickle.dumps(data)
            total_bytes += len(serialized)
            
            # Simulate network delay
            await asyncio.sleep(0.001)
            
            # Deserialize
            deserialized = cloudpickle.loads(serialized)
        
        elapsed = time.perf_counter() - start_time
        
        total_mb = total_bytes / (1024 * 1024)
        mb_per_second = total_mb / elapsed
        self.results['data_transfer_rate'].append(mb_per_second)
        
        print(f"Total Transfers: {num_transfers}")
        print(f"Total Data: {total_mb:.2f} MB")
        print(f"Time Elapsed: {elapsed:.4f} s")
        print(f"Transfer Rate: {mb_per_second:.2f} MB/s")
        print(f"Avg Transfer Time: {(elapsed/num_transfers)*1000:.2f} ms/transfer")
        
        return mb_per_second
    
    async def benchmark_ml_task_throughput(self, num_tasks=50):
        """Measure ML task processing throughput"""
        print("\n" + "="*60)
        print("BENCHMARK 6: ML Task Throughput")
        print("="*60)
        
        queue = DistributedQueue("ml-node")
        
        # Generate ML tasks
        np.random.seed(42)
        
        print(f"Submitting {num_tasks} ML tasks...")
        
        for i in range(num_tasks):
            X_train = np.random.rand(20, 3)
            y_train = (X_train[:, 0] + X_train[:, 1] > 1).astype(int)
            X_test = np.random.rand(5, 3)
            
            await queue.submit(k_nearest_neighbors, X_train, y_train, X_test, k=3, priority=1)
        
        print("Executing ML tasks...")
        start_time = time.perf_counter()
        
        completed = 0
        while not queue.queue.empty():
            await queue.execute_next()
            completed += 1
        
        elapsed = time.perf_counter() - start_time
        
        ml_tasks_per_second = completed / elapsed
        
        print(f"ML Tasks Completed: {completed}")
        print(f"Time Elapsed: {elapsed:.4f} s")
        print(f"Throughput: {ml_tasks_per_second:.2f} ML tasks/second")
        print(f"Avg ML Task Time: {(elapsed/completed)*1000:.2f} ms/task")
        
        return ml_tasks_per_second
    
    async def run_all_benchmarks(self):
        """Run all throughput benchmarks"""
        print("\n" + "="*70)
        print(" "*20 + "THROUGHPUT BENCHMARKS")
        print("="*70)
        
        await self.benchmark_task_throughput(num_tasks=1000)
        self.benchmark_message_throughput(num_messages=10000)
        self.benchmark_routing_throughput(num_routes=5000)
        await self.benchmark_concurrent_tasks(num_concurrent=100)
        await self.benchmark_data_transfer(num_transfers=100)
        await self.benchmark_ml_task_throughput(num_tasks=50)
        
        self._print_summary()
    
    def _print_summary(self):
        """Print summary of all benchmarks"""
        print("\n" + "="*70)
        print(" "*25 + "SUMMARY")
        print("="*70)
        
        metrics = {
            'tasks_per_second': 'Task Processing',
            'messages_per_second': 'Message Processing',
            'routing_throughput': 'Routing Decisions',
            'concurrent_tasks': 'Concurrent Execution',
            'data_transfer_rate': 'Data Transfer (MB/s)'
        }
        
        for key, label in metrics.items():
            if self.results[key]:
                values = self.results[key]
                print(f"\n{label}:")
                print(f"  Throughput: {statistics.mean(values):.2f}")
        
        print("\n" + "="*70)
        print("✅ All throughput benchmarks complete!")
        print("="*70)
    
    def export_results(self, filename='results/throughput_results.json'):
        """Export results to JSON file"""
        results_data = {
            'timestamp': datetime.now().isoformat(),
            'benchmarks': {}
        }
        
        for name, values in self.results.items():
            if values:
                results_data['benchmarks'][name] = {
                    'mean': statistics.mean(values),
                    'values': values
                }
        
        os.makedirs('results', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"\n📊 Results exported to {filename}")


async def main():
    """Run throughput benchmarks"""
    benchmark = ThroughputBenchmark()
    await benchmark.run_all_benchmarks()
    benchmark.export_results()


if __name__ == "__main__":
    asyncio.run(main())
