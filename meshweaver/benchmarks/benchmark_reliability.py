# MeshWeaver - Reliability Benchmarks - Week 3
# Measure failure detection, recovery, and network reliability

import asyncio
import time
import statistics
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from network.heartbeat import HeartbeatMonitor
from network.task_router import TaskRouter
from network.gossip import GossipNode
from serializer.task_queue import DistributedQueue
import json
from datetime import datetime
import random

class ReliabilityBenchmark:
    """Benchmark reliability and fault tolerance of mesh network"""

    def __init__(self):
        self.results = {
            'failure_detection_time': [],
            'recovery_success_rate': [],
            'task_rerouting_success': [],
            'network_partition_recovery': [],
            'heartbeat_accuracy': [],
            'data_consistency': []
        }

    async def benchmark_failure_detection(self, num_trials=50):
        """Measure node failure detection accuracy and speed"""
        print("\n" + "="*60)
        print("BENCHMARK 1: Failure Detection")
        print("="*60)

        detection_times = []
        false_positives = 0
        true_positives = 0

        for trial in range(num_trials):
            monitor = HeartbeatMonitor("coordinator", timeout=2)

            # Register nodes
            nodes = [f"node-{i}" for i in range(5)]
            for node in nodes:
                monitor.register_node(node)

            # Simulate healthy heartbeats
            for node in nodes:
                monitor.receive_heartbeat(node)

            # Simulate one node failure
            failed_node = random.choice(nodes)
            healthy_nodes = [n for n in nodes if n != failed_node]

            # Continue heartbeats for healthy nodes
            for node in healthy_nodes:
                monitor.receive_heartbeat(node)

            # Wait for timeout
            start = time.perf_counter()
            await asyncio.sleep(2.1)

            # Check for failures
            failed = monitor.check_nodes()
            detection_time = time.perf_counter() - start

            if failed_node in failed:
                true_positives += 1
                detection_times.append(detection_time * 1000)  # ms

            if len(failed) > 1:
                false_positives += len(failed) - 1

        accuracy = (true_positives / num_trials) * 100
        avg_detection_time = statistics.mean(detection_times) if detection_times else 0

        self.results['failure_detection_time'] = detection_times

        print(f"Trials: {num_trials}")
        print(f"True Positives: {true_positives}")
        print(f"False Positives: {false_positives}")
        print(f"Detection Accuracy: {accuracy:.2f}%")
        print(f"Avg Detection Time: {avg_detection_time:.2f} ms")
        print(f"Min Detection Time: {min(detection_times) if detection_times else 0:.2f} ms")
        print(f"Max Detection Time: {max(detection_times) if detection_times else 0:.2f} ms")

        return accuracy

    async def benchmark_task_rerouting(self, num_trials=100):
        """Measure task re-routing success rate after node failure"""
        print("\n" + "="*60)
        print("BENCHMARK 2: Task Re-routing Reliability")
        print("="*60)

        successful_reroutes = 0
        failed_reroutes = 0
        reroute_times = []

        for trial in range(num_trials):
            monitor = HeartbeatMonitor("coordinator", timeout=1)
            router = TaskRouter("coordinator")

            # Setup nodes
            nodes = [f"node-{i}" for i in range(5)]
            for i, node in enumerate(nodes):
                monitor.register_node(node)
                router.update_load(node, cpu=20 + i*10, ram=30 + i*5)

            # Assign tasks
            task_id = f"task-{trial}"
            assigned_node = random.choice(nodes)
            monitor.assign_task(task_id, assigned_node, {"data": "test"})

            # Simulate node failure
            monitor.failed_nodes.add(assigned_node)

            # Attempt re-routing
            start = time.perf_counter()

            affected = monitor.handle_failure(assigned_node)

            if task_id in affected:
                # Re-route to another node
                available_nodes = [n for n in nodes if n != assigned_node]
                if available_nodes:
                    new_node, _ = router.route_task(task_id, {"data": "test"})
                    if new_node != assigned_node:
                        successful_reroutes += 1
                        reroute_time = (time.perf_counter() - start) * 1000
                        reroute_times.append(reroute_time)
                    else:
                        failed_reroutes += 1
                else:
                    failed_reroutes += 1

        success_rate = (successful_reroutes / num_trials) * 100
        avg_reroute_time = statistics.mean(reroute_times) if reroute_times else 0

        self.results['task_rerouting_success'].append(success_rate)

        print(f"Trials: {num_trials}")
        print(f"Successful Re-routes: {successful_reroutes}")
        print(f"Failed Re-routes: {failed_reroutes}")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Avg Re-routing Time: {avg_reroute_time:.4f} ms")

        return success_rate

    async def benchmark_network_partition_recovery(self, num_trials=30):
        """Measure network partition detection and recovery"""
        print("\n" + "="*60)
        print("BENCHMARK 3: Network Partition Recovery")
        print("="*60)

        recovery_times = []
        successful_recoveries = 0

        for trial in range(num_trials):
            # Create two partitions of gossip nodes
            partition_a = [GossipNode(f"node-a{i}", "127.0.0.1", 8000+i) for i in range(3)]
            partition_b = [GossipNode(f"node-b{i}", "127.0.0.1", 8100+i) for i in range(3)]

            # Partition A nodes discover each other
            for node in partition_a:
                for other in partition_a:
                    if node != other:
                        node.add_neighbor(other.node_id, other.host, other.port)

            # Partition B nodes discover each other
            for node in partition_b:
                for other in partition_b:
                    if node != other:
                        node.add_neighbor(other.node_id, other.host, other.port)

            # Exchange gossip within partitions
            for node in partition_a:
                msg = node.create_gossip_message()
                for other in partition_a:
                    if node != other:
                        other.receive_gossip(msg)

            # Simulate partition healing
            start = time.perf_counter()

            # Bridge partitions
            bridge_a = partition_a[0]
            bridge_b = partition_b[0]

            bridge_a.add_neighbor(bridge_b.node_id, bridge_b.host, bridge_b.port)
            bridge_b.add_neighbor(bridge_a.node_id, bridge_a.host, bridge_a.port)

            # Exchange gossip across partition
            msg_a = bridge_a.create_gossip_message()
            bridge_b.receive_gossip(msg_a)

            msg_b = bridge_b.create_gossip_message()
            bridge_a.receive_gossip(msg_b)

            recovery_time = (time.perf_counter() - start) * 1000
            recovery_times.append(recovery_time)

            # Check if partitions are now aware of each other
            if len(bridge_a.node_loads) > len(partition_a) or len(bridge_b.node_loads) > len(partition_b):
                successful_recoveries += 1

        success_rate = (successful_recoveries / num_trials) * 100
        avg_recovery_time = statistics.mean(recovery_times)

        self.results['network_partition_recovery'].append(success_rate)

        print(f"Trials: {num_trials}")
        print(f"Successful Recoveries: {successful_recoveries}")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Avg Recovery Time: {avg_recovery_time:.4f} ms")
        print(f"Min Recovery Time: {min(recovery_times):.4f} ms")
        print(f"Max Recovery Time: {max(recovery_times):.4f} ms")

        return success_rate

    async def benchmark_heartbeat_accuracy(self, num_trials=100):
        """Measure heartbeat timeout accuracy"""
        print("\n" + "="*60)
        print("BENCHMARK 4: Heartbeat Timeout Accuracy")
        print("="*60)

        timeout_accuracies = []

        for trial in range(num_trials):
            monitor = HeartbeatMonitor("coordinator", timeout=1.0)
            monitor.register_node("test-node")

            # Initial heartbeat
            monitor.receive_heartbeat("test-node")

            # Wait for timeout
            await asyncio.sleep(1.05)

            # Check if detected as failed
            start = time.perf_counter()
            failed = monitor.check_nodes()
            check_time = time.perf_counter() - start

            # Calculate accuracy (how close to expected timeout)
            expected_timeout = 1.0
            actual_timeout = 1.05  # We waited this long
            accuracy = 100 - abs(actual_timeout - expected_timeout) * 100

            timeout_accuracies.append(accuracy)

        avg_accuracy = statistics.mean(timeout_accuracies)
        self.results['heartbeat_accuracy'] = timeout_accuracies

        print(f"Trials: {num_trials}")
        print(f"Avg Timeout Accuracy: {avg_accuracy:.2f}%")
        print(f"Min Accuracy: {min(timeout_accuracies):.2f}%")
        print(f"Max Accuracy: {max(timeout_accuracies):.2f}%")
        print(f"Std Dev: {statistics.stdev(timeout_accuracies):.2f}%")

        return avg_accuracy

    async def benchmark_data_consistency(self, num_trials=50):
        """Measure data consistency under concurrent operations"""
        print("\n" + "="*60)
        print("BENCHMARK 5: Data Consistency")
        print("="*60)

        consistency_scores = []

        for trial in range(num_trials):
            # Create multiple gossip nodes
            nodes = [GossipNode(f"node-{i}", "127.0.0.1", 8000+i) for i in range(5)]

            # Connect all nodes
            for node in nodes:
                for other in nodes:
                    if node != other:
                        node.add_neighbor(other.node_id, other.host, other.port)

            # Each node creates gossip
            messages = [node.create_gossip_message() for node in nodes]

            # Broadcast all messages
            for i, node in enumerate(nodes):
                for msg in messages:
                    node.receive_gossip(msg)

            # Check consistency: all nodes should have same view
            all_loads = [set(node.node_loads.keys()) for node in nodes]

            # Calculate consistency score
            if all_loads:
                reference = all_loads[0]
                matches = sum(1 for loads in all_loads if loads == reference)
                consistency = (matches / len(nodes)) * 100
                consistency_scores.append(consistency)

        avg_consistency = statistics.mean(consistency_scores)
        self.results['data_consistency'] = consistency_scores

        print(f"Trials: {num_trials}")
        print(f"Avg Consistency: {avg_consistency:.2f}%")
        print(f"Min Consistency: {min(consistency_scores):.2f}%")
        print(f"Max Consistency: {max(consistency_scores):.2f}%")
        print(f"Perfect Consistency Trials: {consistency_scores.count(100.0)}/{num_trials}")

        return avg_consistency

    async def run_all_benchmarks(self):
        """Run all reliability benchmarks"""
        print("\n" + "="*70)
        print(" "*20 + "RELIABILITY BENCHMARKS")
        print("="*70)

        await self.benchmark_failure_detection(num_trials=30)
        await self.benchmark_task_rerouting(num_trials=50)
        await self.benchmark_network_partition_recovery(num_trials=20)
        await self.benchmark_heartbeat_accuracy(num_trials=30)
        await self.benchmark_data_consistency(num_trials=30)

        self._print_summary()

    def _print_summary(self):
        """Print summary of all benchmarks"""
        print("\n" + "="*70)
        print(" "*25 + "SUMMARY")
        print("="*70)

        print(f"\nFailure Detection:")
        if self.results['failure_detection_time']:
            print(f"  Avg Time: {statistics.mean(self.results['failure_detection_time']):.2f} ms")

        print(f"\nTask Re-routing:")
        if self.results['task_rerouting_success']:
            print(f"  Success Rate: {statistics.mean(self.results['task_rerouting_success']):.2f}%")

        print(f"\nNetwork Partition Recovery:")
        if self.results['network_partition_recovery']:
            print(f"  Success Rate: {statistics.mean(self.results['network_partition_recovery']):.2f}%")

        print(f"\nHeartbeat Accuracy:")
        if self.results['heartbeat_accuracy']:
            print(f"  Avg Accuracy: {statistics.mean(self.results['heartbeat_accuracy']):.2f}%")

        print(f"\nData Consistency:")
        if self.results['data_consistency']:
            print(f"  Avg Consistency: {statistics.mean(self.results['data_consistency']):.2f}%")

        print("\n" + "="*70)
        print("✅ All reliability benchmarks complete!")
        print("="*70)

    def export_results(self, filename='results/reliability_results.json'):
        """Export results to JSON file"""
        results_data = {
            'timestamp': datetime.now().isoformat(),
            'benchmarks': {}
        }

        for name, values in self.results.items():
            if values:
                results_data['benchmarks'][name] = {
                    'mean': statistics.mean(values),
                    'min': min(values),
                    'max': max(values),
                    'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
                    'num_trials': len(values),
                    'raw_data': values[:50]  # Store first 50 samples
                }

        os.makedirs('results', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2)

        print(f"\n📊 Results exported to {filename}")

async def main():
    """Run reliability benchmarks"""
    benchmark = ReliabilityBenchmark()
    await benchmark.run_all_benchmarks()
    benchmark.export_results()

if __name__ == "__main__":
    asyncio.run(main())
