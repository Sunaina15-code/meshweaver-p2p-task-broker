# 🕸️ MeshWeaver: P2P Distributed Task Broker

<div align="center">

**A decentralized peer-to-peer task distribution platform with Kademlia DHT**

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/Status-Active-success.svg)]()

</div>

---

## 🎯 Overview

**MeshWeaver** is a distributed computing platform that enables decentralized execution of computational tasks, including ML/AI algorithms, across a peer-to-peer network. Built on Kademlia DHT for efficient node discovery and intelligent task routing based on real-time resource availability.

### Key Features

- **🔍 Kademlia DHT**: Efficient O(log n) peer discovery and routing
- **⚡ Intelligent Task Routing**: CPU-based load balancing across nodes
- **🔒 Secure Transmission**: HMAC-based cryptographic message signing
- **📡 Gossip Protocol**: Distributed resource monitoring and state propagation
- **💓 Heartbeat Monitor**: Automatic failure detection and task re-routing
- **🧠 ML Function Serialization**: Transmit and execute complex ML algorithms remotely
- **📊 Priority Task Queue**: Priority-based distributed task execution
- **🎨 Real-time Dashboard**: Rich CLI monitoring of network topology and node health

---

## 🏗️ Architecture

MeshWeaver uses a fully decentralized architecture with no central coordinator:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Node A    │────▶│   Node B    │────▶│   Node C    │
│  (Worker)   │     │  (Worker)   │     │  (Worker)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    Gossip Protocol
                  (Resource Broadcast)
                           │
                  ┌────────▼────────┐
                  │  Kademlia DHT   │
                  │ (Peer Discovery)│
                  └─────────────────┘
```

See [docs/architecture.md](meshweaver/docs/architecture.md) for detailed architecture diagrams.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/meshweaver-p2p-task-broker.git
cd meshweaver-p2p-task-broker

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
import asyncio
from meshweaver.serializer.task_queue import DistributedQueue

# Create a distributed task queue
async def main():
    queue = DistributedQueue("node-001")
    
    # Submit tasks
    def compute_sum(numbers):
        return sum(numbers)
    
    task_id = await queue.submit(compute_sum, [1, 2, 3, 4, 5], priority=1)
    
    # Execute tasks
    await queue.run_all()
    queue.display_stats()

asyncio.run(main())
```

See [examples/](examples/) for more usage examples.

---

## 📦 Project Structure

```
meshweaver-p2p-task-broker/
├── meshweaver/
│   ├── dht/                    # Kademlia DHT implementation
│   │   └── kademlia.py         # K-bucket routing & peer discovery
│   ├── network/                # Network layer protocols
│   │   ├── gossip.py           # Resource state broadcasting
│   │   ├── heartbeat.py        # Failure detection monitor
│   │   ├── task_router.py      # CPU-based task routing
│   │   ├── peer_discovery.py   # Bootstrap & discovery
│   │   └── security.py         # HMAC message signing
│   ├── serializer/             # Task serialization
│   │   ├── task_serializer.py  # Function serialization (cloudpickle)
│   │   ├── task_queue.py       # Priority-based task queue
│   │   └── ml_functions.py     # ML algorithm library
│   ├── dashboard/              # Monitoring & visualization
│   │   └── mesh_monitor.py     # Real-time network dashboard
│   ├── benchmarks/             # Performance testing
│   │   ├── benchmark_latency.py
│   │   ├── benchmark_throughput.py
│   │   └── benchmark_reliability.py
│   ├── tests/                  # Test suite
│   └── docs/                   # Documentation
├── examples/                   # Usage examples
├── requirements.txt
└── README.md
```

---

## 🔬 Core Components

### 1. Kademlia DHT (`dht/kademlia.py`)

Distributed hash table for peer discovery:
- **XOR Distance Metric**: Efficient routing based on XOR distance
- **K-Bucket Architecture**: 160 buckets for peer organization
- **Operations**: PING, STORE, FIND_NODE, FIND_VALUE
- **Complexity**: O(log n) lookup time

### 2. Task Serialization (`serializer/task_serializer.py`)

Serialize Python functions and ML models for network transmission:
- **cloudpickle**: Serialize complex closures and ML functions
- **Type Support**: Functions, classes, ML models (NumPy, scikit-learn)
- **Safety**: Hash-based task identification

### 3. Gossip Protocol (`network/gossip.py`)

Epidemic-style resource state propagation:
- **Periodic Broadcasting**: Nodes share CPU/RAM load every 5s
- **Exponential Spread**: O(log n) convergence time
- **Eventual Consistency**: All nodes converge to global state

### 4. Task Router (`network/task_router.py`)

Intelligent task distribution:
- **CPU-Based Routing**: Route to node with lowest CPU load
- **Real-time Monitoring**: Track resource availability
- **Routing History**: Audit trail of all routing decisions

### 5. Heartbeat Monitor (`network/heartbeat.py`)

Failure detection and recovery:
- **Periodic Health Checks**: Configurable timeout (default: 10s)
- **Failure Detection**: Identify unresponsive nodes
- **Auto Re-routing**: Redistribute tasks from failed nodes

### 6. Priority Task Queue (`serializer/task_queue.py`)

Distributed task execution:
- **Priority-Based**: Execute high-priority tasks first
- **Async Execution**: Non-blocking task processing
- **Status Tracking**: PENDING → RUNNING → COMPLETE/FAILED

---

## 🧪 Testing

### Run All Tests

```bash
# Serialization tests
python meshweaver/tests/test_serialization.py

# ML function tests
python meshweaver/tests/test_ml_functions.py

# Network transmission tests
python meshweaver/tests/test_network_transmission.py

# Full demo
python meshweaver/tests/ml_network_transmission_demo.py
```

### Performance Benchmarks

```bash
# Latency benchmarks
python meshweaver/benchmarks/benchmark_latency.py

# Throughput benchmarks
python meshweaver/benchmarks/benchmark_throughput.py

# Reliability benchmarks
python meshweaver/benchmarks/benchmark_reliability.py
```

See [docs/TESTING_REPORT.md](meshweaver/docs/TESTING_REPORT.md) for complete test results.

---

## 📈 Performance

| Metric | Result | Target |
|--------|--------|--------|
| **Task Routing Latency** | < 2ms | < 5ms |
| **DHT Lookup Time** | < 10ms | < 15ms |
| **Gossip Propagation** | < 5ms | < 10ms |
| **Task Throughput** | > 1000 tasks/sec | > 500 tasks/sec |
| **Failure Detection** | < 100ms | < 150ms |
| **Network Recovery** | > 95% | > 90% |

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Core Language** | Python 3.13 | Async/await support |
| **Networking** | asyncio | Asynchronous I/O |
| **Serialization** | cloudpickle | Function serialization |
| **DHT** | Kademlia | Peer discovery |
| **Security** | hmac/hashlib | Message signing |
| **Dashboard** | Rich/Textual | Terminal UI |
| **HTTP** | aiohttp | Async HTTP client |

---

## 📚 Documentation

- [Architecture Overview](meshweaver/docs/architecture.md)
- [Kademlia Protocol](meshweaver/docs/kademlia_protocol.md)
- [Node Discovery](meshweaver/docs/node_discovery.md)
- [Performance Benchmarks](meshweaver/docs/performance_benchmarks.md)
- [Testing Report](meshweaver/docs/TESTING_REPORT.md)
- [Week 2 Serialization Check](meshweaver/docs/week2_serialization_check.md)

---

## 🎓 Use Cases

- **Distributed ML Training**: Train models across multiple nodes
- **Batch Data Processing**: Process large datasets in parallel
- **Scientific Computing**: Distribute compute-intensive simulations
- **CI/CD Pipelines**: Distribute build and test tasks
- **Edge Computing**: Coordinate edge device computations

---

## 🗓️ Development Timeline

| Week | Focus | Status |
|------|-------|--------|
| **Week 1** | Kademlia DHT Research & Foundation | ✅ Complete |
| **Week 2** | Serialization & Network Transmission | ✅ Complete |
| **Week 3** | Task Queue, Monitoring, Integration | ✅ Complete |
| **Week 4** | Final Documentation & Testing | ✅ Complete |

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 👥 Team

**Advanced Python Engineering - Infotact Solutions**

- Athrva - Task Router & Serialization
- John - Kademlia DHT Implementation
- Sunaina - Gossip Protocol
- Noah - Heartbeat Monitor & Task Queue

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 References

- [Kademlia: A Peer-to-Peer Information System Based on the XOR Metric](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf)
- [Gossip Protocols for Large-Scale Distributed Systems](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/2007PromiseAndLimitations.pdf)
- [cloudpickle Documentation](https://github.com/cloudpipe/cloudpickle)

---

<div align="center">

**Built with ❤️ by the MeshWeaver Team**

[Report Bug](https://github.com/yourusername/meshweaver/issues) · [Request Feature](https://github.com/yourusername/meshweaver/issues)

</div>
