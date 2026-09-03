# MeshWeaver Examples

This folder contains practical examples demonstrating how to use MeshWeaver for distributed task execution.

---

## 📂 Examples Overview

| Example | Description | Difficulty |
|---------|-------------|------------|
| **basic_task_execution.py** | Simple task submission and execution | ⭐ Beginner |
| **ml_task_distribution.py** | Distribute ML/AI workloads across nodes | ⭐⭐ Intermediate |
| **multi_node_setup.py** | Set up and configure multiple nodes | ⭐⭐ Intermediate |
| **dht_node_discovery.py** | Demonstrate Kademlia DHT peer discovery | ⭐⭐⭐ Advanced |
| **custom_routing_strategy.py** | Implement custom task routing logic | ⭐⭐⭐ Advanced |

---

## 🚀 Quick Start

### Running an Example

```bash
# Navigate to examples folder
cd examples

# Run basic example
python basic_task_execution.py

# Run ML example
python ml_task_distribution.py
```

---

## 📋 Example Details

### 1. Basic Task Execution (`basic_task_execution.py`)

Learn the fundamentals of MeshWeaver:
- Creating a task queue
- Submitting simple tasks
- Executing tasks with priority
- Viewing execution results

**What you'll learn:**
- Task serialization basics
- Priority queue management
- Result retrieval

**Run time:** ~5 seconds

---

### 2. ML Task Distribution (`ml_task_distribution.py`)

Distribute machine learning workloads:
- Serialize ML functions (regression, clustering, PCA)
- Submit complex computational tasks
- Execute across simulated nodes
- Collect and analyze results

**What you'll learn:**
- ML function serialization
- NumPy array handling
- Distributed computation patterns

**Run time:** ~15 seconds

---

### 3. Multi-Node Setup (`multi_node_setup.py`)

Configure a complete mesh network:
- Create multiple nodes
- Configure gossip protocol
- Set up heartbeat monitoring
- Connect nodes with Kademlia DHT

**What you'll learn:**
- Network topology setup
- Node configuration
- Peer-to-peer connectivity

**Run time:** ~20 seconds

---

### 4. DHT Node Discovery (`dht_node_discovery.py`)

Deep dive into Kademlia DHT:
- Bootstrap node initialization
- New node joining process
- K-bucket management
- Peer lookup and routing

**What you'll learn:**
- Kademlia protocol internals
- XOR distance calculation
- DHT data storage and retrieval

**Run time:** ~10 seconds

---

### 5. Custom Routing Strategy (`custom_routing_strategy.py`)

Implement advanced routing logic:
- Custom routing algorithms
- Load balancing strategies
- Dynamic node selection
- Performance optimization

**What you'll learn:**
- Router customization
- Advanced load balancing
- Network optimization techniques

**Run time:** ~15 seconds

---

## 🎓 Learning Path

### For Beginners

1. Start with `basic_task_execution.py`
2. Read the code comments carefully
3. Experiment by changing priorities
4. Try adding your own simple functions

### For Intermediate Users

1. Run `ml_task_distribution.py`
2. Study how ML functions are serialized
3. Run `multi_node_setup.py`
4. Observe gossip protocol in action

### For Advanced Users

1. Explore `dht_node_discovery.py`
2. Understand Kademlia internals
3. Implement `custom_routing_strategy.py`
4. Optimize for your use case

---

## 💡 Common Use Cases

### Example 1: Distributed Data Processing

```python
import asyncio
from meshweaver.serializer.task_queue import DistributedQueue

async def process_dataset():
    queue = DistributedQueue("processor")
    
    # Process data chunks in parallel
    for chunk in data_chunks:
        await queue.submit(process_chunk, chunk, priority=1)
    
    await queue.run_all()
    return queue.completed
```

### Example 2: ML Model Training

```python
from meshweaver.serializer.ml_functions import logistic_regression_train

async def train_models():
    queue = DistributedQueue("trainer")
    
    # Train multiple models in parallel
    for dataset in datasets:
        await queue.submit(
            logistic_regression_train,
            dataset['X'], dataset['y'],
            priority=2
        )
    
    await queue.run_all()
```

### Example 3: Task Broadcasting

```python
from meshweaver.network.gossip import GossipNode

# Broadcast task to all nodes
node = GossipNode("broadcaster", "127.0.0.1", 8001)
message = node.create_gossip_message()

# Share with all neighbors
for neighbor in node.neighbors:
    node.receive_gossip(message)
```

---

## 🔧 Configuration Tips

### Adjust Task Priorities

```python
# High priority (executed first)
await queue.submit(urgent_task, priority=10)

# Medium priority
await queue.submit(normal_task, priority=5)

# Low priority (executed last)
await queue.submit(background_task, priority=1)
```

### Configure Network Parameters

```python
# Gossip interval (default: 5s)
gossip_interval = 5  # seconds

# Heartbeat timeout (default: 10s)
heartbeat_timeout = 10  # seconds

# K-bucket size (default: 20)
k_bucket_size = 20  # max peers per bucket
```

---

## 🐛 Troubleshooting

### Problem: Tasks not executing

**Solution**: Check if queue has tasks
```python
if queue.queue.empty():
    print("No tasks in queue")
```

### Problem: Serialization errors

**Solution**: Ensure functions use picklable objects
```python
# ❌ Bad: uses unpicklable lambda
task = lambda x: open(x).read()

# ✅ Good: uses regular function
def task(x):
    with open(x) as f:
        return f.read()
```

### Problem: Node connection issues

**Solution**: Verify network configuration
```python
# Check node is listening
print(f"Node listening on {node.host}:{node.port}")

# Verify neighbors are added
print(f"Neighbors: {len(node.neighbors)}")
```

---

## 📚 Additional Resources

- [Main README](../README.md) - Project overview
- [Architecture Documentation](../meshweaver/docs/architecture.md) - System design
- [Testing Report](../meshweaver/docs/TESTING_REPORT.md) - Test results
- [Kademlia Protocol](../meshweaver/docs/kademlia_protocol.md) - DHT details

---

## 🤝 Contributing Examples

Have a useful example? We'd love to include it!

**Guidelines:**
1. Keep examples focused and concise
2. Include detailed comments
3. Provide expected output
4. Test thoroughly before submitting

---

## ❓ Questions?

- Check the main [README](../README.md)
- Review [documentation](../meshweaver/docs/)
- Contact the team

---

**Last Updated**: Week 4, August 2024  
**Maintainer**: MeshWeaver Team
