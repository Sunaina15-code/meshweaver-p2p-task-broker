# MeshWeaver - Complete Network Benchmark Suite - Week 3
# Comprehensive performance benchmarking

import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from benchmark_latency import LatencyBenchmark
from benchmark_throughput import ThroughputBenchmark
from benchmark_reliability import ReliabilityBenchmark
import json
import statistics
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

class NetworkBenchmarkSuite:
    """Complete benchmark suite for MeshWeaver network"""

    def __init__(self):
        self.console = Console()
        self.latency_bench = LatencyBenchmark()
        self.throughput_bench = ThroughputBenchmark()
        self.reliability_bench = ReliabilityBenchmark()
        self.start_time = None
        self.end_time = None

    async def run_full_benchmark(self):
        """Run complete benchmark suite"""
        self.console.print("\n")
        self.console.print(Panel.fit(
            "[bold cyan]MeshWeaver Network Benchmark Suite[/bold cyan]\n"
            "[yellow]Week 3: Performance Benchmarking[/yellow]\n"
            "Measuring Latency, Throughput, and Reliability",
            border_style="cyan"
        ))

        self.start_time = datetime.now()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:

            # Latency Benchmarks
            task1 = progress.add_task("[cyan]Running latency benchmarks...", total=None)
            await self.latency_bench.run_all_benchmarks()
            progress.update(task1, completed=True)

            # Throughput Benchmarks
            task2 = progress.add_task("[green]Running throughput benchmarks...", total=None)
            await self.throughput_bench.run_all_benchmarks()
            progress.update(task2, completed=True)

            # Reliability Benchmarks
            task3 = progress.add_task("[yellow]Running reliability benchmarks...", total=None)
            await self.reliability_bench.run_all_benchmarks()
            progress.update(task3, completed=True)

        self.end_time = datetime.now()

        # Generate reports
        self._print_summary_report()
        self._export_all_results()

    def _print_summary_report(self):
        """Print comprehensive summary report"""
        self.console.print("\n")
        self.console.print("="*80)
        self.console.print("[bold cyan]COMPREHENSIVE BENCHMARK REPORT[/bold cyan]".center(80))
        self.console.print("="*80)

        # Latency Summary
        self.console.print("\n[bold]📊 LATENCY METRICS[/bold]")
        latency_table = Table(show_header=True, header_style="bold magenta")
        latency_table.add_column("Component", style="cyan")
        latency_table.add_column("Mean (ms)", justify="right")
        latency_table.add_column("Median (ms)", justify="right")
        latency_table.add_column("P95 (ms)", justify="right")
        latency_table.add_column("P99 (ms)", justify="right")

        for name, values in self.latency_bench.results.items():
            if values:
                latency_table.add_row(
                    name.replace('_', ' ').title(),
                    f"{statistics.mean(values):.4f}",
                    f"{statistics.median(values):.4f}",
                    f"{self._percentile(values, 95):.4f}",
                    f"{self._percentile(values, 99):.4f}"
                )

        self.console.print(latency_table)

        # Throughput Summary
        self.console.print("\n[bold]🚀 THROUGHPUT METRICS[/bold]")
        throughput_table = Table(show_header=True, header_style="bold green")
        throughput_table.add_column("Component", style="cyan")
        throughput_table.add_column("Throughput", justify="right")
        throughput_table.add_column("Unit", style="dim")

        throughput_metrics = {
            'tasks_per_second': ('Task Processing', 'tasks/s'),
            'messages_per_second': ('Message Processing', 'msgs/s'),
            'routing_throughput': ('Routing Decisions', 'routes/s'),
            'concurrent_tasks': ('Concurrent Execution', 'tasks/s'),
            'data_transfer_rate': ('Data Transfer', 'MB/s')
        }

        for key, (label, unit) in throughput_metrics.items():
            values = self.throughput_bench.results.get(key, [])
            if values:
                throughput_table.add_row(
                    label,
                    f"{statistics.mean(values):.2f}",
                    unit
                )

        self.console.print(throughput_table)

        # Reliability Summary
        self.console.print("\n[bold]🛡️ RELIABILITY METRICS[/bold]")
        reliability_table = Table(show_header=True, header_style="bold yellow")
        reliability_table.add_column("Component", style="cyan")
        reliability_table.add_column("Score", justify="right")
        reliability_table.add_column("Status", justify="center")

        reliability_metrics = {
            'failure_detection_time': ('Failure Detection', 'ms', 50),
            'task_rerouting_success': ('Task Re-routing', '%', 95),
            'network_partition_recovery': ('Partition Recovery', '%', 90),
            'heartbeat_accuracy': ('Heartbeat Accuracy', '%', 95),
            'data_consistency': ('Data Consistency', '%', 99)
        }

        for key, (label, unit, threshold) in reliability_metrics.items():
            values = self.reliability_bench.results.get(key, [])
            if values:
                mean_val = statistics.mean(values)

                if unit == 'ms':
                    status = "✅ Good" if mean_val < threshold else "⚠️ High"
                    score = f"{mean_val:.2f}"
                else:
                    status = "✅ Good" if mean_val >= threshold else "⚠️ Low"
                    score = f"{mean_val:.2f}"

                reliability_table.add_row(label, f"{score} {unit}", status)

        self.console.print(reliability_table)

        # Overall Summary
        duration = (self.end_time - self.start_time).total_seconds()

        self.console.print("\n[bold]📈 OVERALL SUMMARY[/bold]")
        summary_table = Table(show_header=False, box=None)
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="white")

        summary_table.add_row("Total Benchmark Duration", f"{duration:.2f} seconds")
        summary_table.add_row("Benchmark Start Time", self.start_time.strftime("%Y-%m-%d %H:%M:%S"))
        summary_table.add_row("Benchmark End Time", self.end_time.strftime("%Y-%m-%d %H:%M:%S"))
        summary_table.add_row("Total Test Categories", "3 (Latency, Throughput, Reliability)")
        summary_table.add_row("Status", "[bold green]✅ All Tests Completed[/bold green]")

        self.console.print(summary_table)

        self.console.print("\n" + "="*80)
        self.console.print("[bold green]✅ BENCHMARK SUITE COMPLETE![/bold green]".center(80))
        self.console.print("="*80 + "\n")

    def _percentile(self, data, percentile):
        """Calculate percentile"""
        size = len(data)
        return sorted(data)[int(size * percentile / 100)]

    def _export_all_results(self):
        """Export all benchmark results"""
        # Create results directory
        os.makedirs('results', exist_ok=True)

        # Export individual results
        self.latency_bench.export_results('results/latency_results.json')
        self.throughput_bench.export_results('results/throughput_results.json')
        self.reliability_bench.export_results('results/reliability_results.json')

        # Create comprehensive summary
        summary = {
            'benchmark_suite': 'MeshWeaver Network Performance',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': (self.end_time - self.start_time).total_seconds(),
            'summary': {
                'latency': self._summarize_results(self.latency_bench.results),
                'throughput': self._summarize_results(self.throughput_bench.results),
                'reliability': self._summarize_results(self.reliability_bench.results)
            }
        }

        with open('results/benchmark_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)

        self.console.print(f"📊 Complete results exported to results/ directory")
        self.console.print(f"   - latency_results.json")
        self.console.print(f"   - throughput_results.json")
        self.console.print(f"   - reliability_results.json")
        self.console.print(f"   - benchmark_summary.json\n")

    def _summarize_results(self, results_dict):
        """Create summary statistics for results"""
        summary = {}

        for name, values in results_dict.items():
            if values:
                summary[name] = {
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'min': min(values),
                    'max': max(values),
                    'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
                    'count': len(values)
                }

        return summary

async def main():
    """Run complete benchmark suite"""
    suite = NetworkBenchmarkSuite()
    await suite.run_full_benchmark()

if __name__ == "__main__":
    asyncio.run(main())
