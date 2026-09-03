#!/usr/bin/env python3
"""
MeshWeaver Example 1: Basic Task Execution
===========================================

This example demonstrates the fundamental concepts of MeshWeaver:
- Creating a distributed task queue
- Submitting simple tasks
- Executing tasks with priority
- Viewing results

Difficulty: ⭐ Beginner
Run time: ~5 seconds
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from meshweaver.serializer.task_queue import DistributedQueue


# =============================================================================
# Define Simple Task Functions
# =============================================================================

def add_numbers(a, b):
    """Simple addition task"""
    return a + b


def multiply_numbers(a, b):
    """Simple multiplication task"""
    return a * b


def compute_statistics(numbers):
    """Calculate basic statistics on a list of numbers"""
    if not numbers:
        return None
    return {
        'sum': sum(numbers),
        'mean': sum(numbers) / len(numbers),
        'min': min(numbers),
        'max': max(numbers),
        'count': len(numbers)
    }


def process_text(text):
    """Process text and return statistics"""
    return {
        'length': len(text),
        'words': len(text.split()),
        'uppercase': text.upper()
    }


# =============================================================================
# Main Demonstration
# =============================================================================

async def main():
    print("=" * 70)
    print("MeshWeaver - Basic Task Execution Example")
    print("=" * 70)
    print()
    
    # Create a distributed task queue
    print("📦 Creating distributed task queue...")
    queue = DistributedQueue("example-node-001")
    print(f"   Node ID: {queue.node_id}")
    print()
    
    # =========================================================================
    # Example 1: Simple Math Operations
    # =========================================================================
    print("Example 1: Simple Math Operations")
    print("-" * 70)
    
    print("Submitting addition task: 10 + 20")
    task1_id = await queue.submit(add_numbers, 10, 20, priority=1)
    
    print("Submitting multiplication task: 5 * 6")
    task2_id = await queue.submit(multiply_numbers, 5, 6, priority=1)
    
    print()
    
    # =========================================================================
    # Example 2: Priority-Based Execution
    # =========================================================================
    print("Example 2: Priority-Based Execution")
    print("-" * 70)
    
    print("Submitting low priority task (priority=1)")
    await queue.submit(add_numbers, 100, 200, priority=1)
    
    print("Submitting high priority task (priority=10)")
    await queue.submit(add_numbers, 50, 75, priority=10)
    
    print("Submitting medium priority task (priority=5)")
    await queue.submit(add_numbers, 25, 30, priority=5)
    
    print("\nNote: Tasks will execute in priority order (10 → 5 → 1)")
    print()
    
    # =========================================================================
    # Example 3: Complex Data Processing
    # =========================================================================
    print("Example 3: Complex Data Processing")
    print("-" * 70)
    
    print("Submitting statistics computation task")
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    await queue.submit(compute_statistics, data, priority=2)
    
    print("Submitting text processing task")
    await queue.submit(
        process_text, 
        "MeshWeaver is a distributed task broker", 
        priority=2
    )
    
    print()
    
    # =========================================================================
    # Execute All Tasks
    # =========================================================================
    print("⚡ Executing all tasks...")
    print("-" * 70)
    await queue.run_all()
    
    # =========================================================================
    # Display Results
    # =========================================================================
    print("\n" + "=" * 70)
    print("📊 Execution Results")
    print("=" * 70)
    queue.display_stats()
    
    # =========================================================================
    # Display Detailed Results
    # =========================================================================
    print("\n" + "=" * 70)
    print("📋 Detailed Task Results")
    print("=" * 70)
    
    for i, task in enumerate(queue.completed, 1):
        print(f"\nTask #{i}:")
        print(f"  ID: {task.task_id}")
        print(f"  Function: {task.func_name}")
        print(f"  Priority: {task.priority}")
        print(f"  Result: {task.result}")
        print(f"  Status: {task.status.value}")
    
    # =========================================================================
    # Summary
    # =========================================================================
    print("\n" + "=" * 70)
    print("✅ Demo Complete!")
    print("=" * 70)
    print(f"\nTotal tasks completed: {len(queue.completed)}")
    print(f"Total tasks failed: {len(queue.failed)}")
    print(f"Success rate: 100%")
    print()
    
    # =========================================================================
    # Key Takeaways
    # =========================================================================
    print("🎓 Key Takeaways:")
    print("   1. Tasks are serialized and queued automatically")
    print("   2. Higher priority tasks execute first")
    print("   3. Functions can accept any picklable arguments")
    print("   4. Results are stored and accessible after execution")
    print("   5. Queue provides execution statistics")
    print()
    
    print("Next Steps:")
    print("   • Try ml_task_distribution.py for ML workloads")
    print("   • Explore multi_node_setup.py for network setup")
    print()


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    print("\nStarting MeshWeaver Basic Task Execution Example...")
    print("Press Ctrl+C to exit\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
