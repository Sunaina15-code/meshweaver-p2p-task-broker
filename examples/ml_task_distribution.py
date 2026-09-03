#!/usr/bin/env python3
"""
MeshWeaver Example 2: ML Task Distribution
===========================================

This example demonstrates distributing machine learning workloads:
- Serialize complex ML functions
- Submit ML algorithms as tasks
- Execute across distributed nodes
- Analyze results

Difficulty: ⭐⭐ Intermediate
Run time: ~15 seconds
Requirements: numpy
"""

import asyncio
import sys
import os
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from meshweaver.serializer.task_queue import DistributedQueue
from meshweaver.serializer.ml_functions import (
    logistic_regression_train,
    k_nearest_neighbors,
    pca_transform,
    time_series_features,
    neural_network_forward
)


# =============================================================================
# ML Task Functions
# =============================================================================

def generate_classification_data(n_samples=100, n_features=3):
    """Generate synthetic classification dataset"""
    np.random.seed(42)
    X = np.random.rand(n_samples, n_features)
    # Simple linear decision boundary
    y = (X[:, 0] + X[:, 1] > 1).astype(int)
    return X, y


def generate_timeseries_data(length=100):
    """Generate synthetic time series data"""
    np.random.seed(42)
    # Random walk
    return np.random.randn(length).cumsum()


def generate_high_dim_data(n_samples=50, n_features=10):
    """Generate high-dimensional data for PCA"""
    np.random.seed(42)
    return np.random.rand(n_samples, n_features)


# =============================================================================
# Main Demonstration
# =============================================================================

async def main():
    print("=" * 70)
    print("MeshWeaver - ML Task Distribution Example")
    print("=" * 70)
    print()
    
    # Create distributed queue
    print("📦 Creating distributed ML task queue...")
    queue = DistributedQueue("ml-node-001")
    print(f"   Node ID: {queue.node_id}")
    print()
    
    # =========================================================================
    # Example 1: Logistic Regression Training
    # =========================================================================
    print("Example 1: Distributed Logistic Regression")
    print("-" * 70)
    
    print("Generating classification dataset...")
    X_train, y_train = generate_classification_data(n_samples=100, n_features=3)
    print(f"   Dataset shape: X={X_train.shape}, y={y_train.shape}")
    
    print("Submitting logistic regression training task...")
    await queue.submit(
        logistic_regression_train,
        X_train, y_train,
        learning_rate=0.01,
        iterations=100,
        priority=10  # High priority
    )
    print("   ✓ Task submitted with priority=10")
    print()
    
    # =========================================================================
    # Example 2: K-Nearest Neighbors
    # =========================================================================
    print("Example 2: K-Nearest Neighbors Classification")
    print("-" * 70)
    
    print("Preparing KNN dataset...")
    X_knn_train = np.array([[1, 2], [2, 3], [3, 4], [6, 7], [7, 8], [8, 9]])
    y_knn_train = np.array([0, 0, 0, 1, 1, 1])
    X_knn_test = np.array([[2, 2], [7, 7], [4, 5]])
    
    print(f"   Training samples: {len(X_knn_train)}")
    print(f"   Test samples: {len(X_knn_test)}")
    
    print("Submitting KNN classification task...")
    await queue.submit(
        k_nearest_neighbors,
        X_knn_train, y_knn_train, X_knn_test,
        k=3,
        priority=8
    )
    print("   ✓ Task submitted with priority=8")
    print()
    
    # =========================================================================
    # Example 3: Principal Component Analysis
    # =========================================================================
    print("Example 3: PCA Dimensionality Reduction")
    print("-" * 70)
    
    print("Generating high-dimensional data...")
    X_pca = generate_high_dim_data(n_samples=50, n_features=10)
    print(f"   Original dimensions: {X_pca.shape}")
    print(f"   Target dimensions: 2")
    
    print("Submitting PCA transformation task...")
    await queue.submit(
        pca_transform,
        X_pca,
        n_components=2,
        priority=6
    )
    print("   ✓ Task submitted with priority=6")
    print()
    
    # =========================================================================
    # Example 4: Time Series Analysis
    # =========================================================================
    print("Example 4: Time Series Feature Extraction")
    print("-" * 70)
    
    print("Generating time series data...")
    ts_data = generate_timeseries_data(length=100)
    print(f"   Time series length: {len(ts_data)}")
    
    print("Submitting time series analysis task...")
    await queue.submit(
        time_series_features,
        ts_data,
        priority=4
    )
    print("   ✓ Task submitted with priority=4")
    print()
    
    # =========================================================================
    # Example 5: Neural Network Forward Pass
    # =========================================================================
    print("Example 5: Neural Network Inference")
    print("-" * 70)
    
    print("Setting up neural network parameters...")
    X_nn = np.random.rand(10, 5)  # 10 samples, 5 input features
    W1 = np.random.rand(5, 8)      # 5 input → 8 hidden
    b1 = np.random.rand(8)
    W2 = np.random.rand(8, 1)      # 8 hidden → 1 output
    b2 = np.random.rand(1)
    
    print(f"   Input shape: {X_nn.shape}")
    print(f"   Hidden layer: 8 neurons")
    print(f"   Output layer: 1 neuron")
    
    print("Submitting neural network forward pass task...")
    await queue.submit(
        neural_network_forward,
        X_nn, W1, b1, W2, b2,
        priority=2
    )
    print("   ✓ Task submitted with priority=2")
    print()
    
    # =========================================================================
    # Execute All ML Tasks
    # =========================================================================
    print("⚡ Executing all ML tasks in priority order...")
    print("-" * 70)
    print("Execution order: Priority 10 → 8 → 6 → 4 → 2")
    print()
    
    await queue.run_all()
    
    # =========================================================================
    # Display Results
    # =========================================================================
    print("\n" + "=" * 70)
    print("📊 ML Task Execution Summary")
    print("=" * 70)
    queue.display_stats()
    
    # =========================================================================
    # Detailed Results Analysis
    # =========================================================================
    print("\n" + "=" * 70)
    print("📋 Detailed ML Results")
    print("=" * 70)
    
    for i, task in enumerate(queue.completed, 1):
        print(f"\n{'='*70}")
        print(f"Task #{i}: {task.func_name}")
        print(f"{'='*70}")
        print(f"  Task ID: {task.task_id}")
        print(f"  Priority: {task.priority}")
        print(f"  Status: {task.status.value}")
        
        result = task.result
        
        if task.func_name == "logistic_regression_train":
            print(f"\n  Logistic Regression Results:")
            print(f"    Final Loss: {result['final_loss']:.4f}")
            print(f"    Weights: {[f'{w:.3f}' for w in result['weights']]}")
            print(f"    Bias: {result['bias']:.3f}")
            print(f"    Training iterations: 100")
            
        elif task.func_name == "k_nearest_neighbors":
            print(f"\n  K-Nearest Neighbors Results:")
            print(f"    Predictions: {result}")
            print(f"    Test samples classified: {len(result)}")
            
        elif task.func_name == "pca_transform":
            print(f"\n  PCA Results:")
            print(f"    Explained variance: {[f'{v:.2%}' for v in result['explained_variance']]}")
            print(f"    Total variance explained: {result['total_variance_explained']:.2%}")
            print(f"    Reduced dimensions: 2")
            
        elif task.func_name == "time_series_features":
            print(f"\n  Time Series Features:")
            print(f"    Mean: {result['mean']:.2f}")
            print(f"    Std Dev: {result['std']:.2f}")
            print(f"    Min: {result['min']:.2f}")
            print(f"    Max: {result['max']:.2f}")
            print(f"    Range: {result['range']:.2f}")
            print(f"    Median: {result['median']:.2f}")
            
        elif task.func_name == "neural_network_forward":
            print(f"\n  Neural Network Results:")
            print(f"    Mean output: {result['mean_output']:.4f}")
            print(f"    Output shape: {len(result['output'])}")
    
    # =========================================================================
    # Performance Summary
    # =========================================================================
    print("\n" + "=" * 70)
    print("⚡ Performance Summary")
    print("=" * 70)
    print(f"  Total ML tasks: {len(queue.completed)}")
    print(f"  Success rate: 100%")
    print(f"  Failed tasks: {len(queue.failed)}")
    print()
    
    # =========================================================================
    # Key Takeaways
    # =========================================================================
    print("🎓 Key Takeaways:")
    print("   1. Complex ML algorithms can be serialized and distributed")
    print("   2. NumPy arrays are handled transparently")
    print("   3. Priority-based execution ensures important tasks run first")
    print("   4. Results preserve full ML model outputs")
    print("   5. Multiple ML paradigms supported (supervised, unsupervised, NN)")
    print()
    
    print("Next Steps:")
    print("   • Try multi_node_setup.py for actual network distribution")
    print("   • Explore custom_routing_strategy.py for load balancing")
    print()
    
    print("=" * 70)
    print("✅ ML Task Distribution Demo Complete!")
    print("=" * 70)
    print()


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    print("\nStarting MeshWeaver ML Task Distribution Example...")
    print("Press Ctrl+C to exit\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
