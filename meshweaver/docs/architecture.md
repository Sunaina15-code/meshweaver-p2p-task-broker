# MeshWeaver Architecture

## System Architecture Overview

MeshWeaver is a fully decentralized P2P task distribution platform built on four core architectural layers:

---

## 🏛️ Architectural Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │ Task Queue │  │  Dashboard │  │   User API │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└───────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│                    COORDINATION LAYER                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │   Gossip   │  │  Heartbeat │  │   Router   │               │
│  │  Protocol  │  │  Monitor   │  │            │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└───────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│                      DISCOVERY LAYER                            │
│  ┌────────────────────────────────────────────────────┐        │
│  │              Kademlia DHT Network                  │        │
│  │  • K-Bucket Routing Tables (160 buckets)          │        │
│  │  • XOR Distance Metric                             │        │
│  │  • FIND_NODE, STORE, PING Operations              │        │
│  └────────────────────────────────────────────────────┘        │
└───────────────────────┬─────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│                     TRANSPORT LAYER                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │   asyncio  │  │  Security  │  │Serializer  │               │
│  │  Sockets   │  │   (HMAC)   │  │(cloudpickle│               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

### Task Submission & Execution Flow

```
┌─────────┐
│  Client │
└────┬────┘
     │
     │ 1. Submit Task
     ▼
┌──────────────────┐
│  Task Serializer │ ◄── cloudpickle serialization
└────┬─────────────┘
     │
     │ 2. Serialize Function + Args
     ▼
┌──────────────────┐
│   Task Router    │
└────┬─────────────┘
     │
     │ 3. Query Gossip State
     ▼
┌──────────────────┐
│  Gossip Protocol │ ◄── CPU/RAM load from all nodes
└────┬─────────────┘
     │
     │ 4. Find Lowest CPU Node
     ▼
┌──────────────────┐
│  Kademlia DHT    │ ◄── Resolve node address
└────┬─────────────┘
     │
     │ 5. Route to Target Node
     ▼
┌──────────────────┐
│   Target Node    │
└────┬─────────────┘
     │
     │ 6. Deserialize & Execute
     ▼
┌──────────────────┐
│  Task Execution  │
└────┬─────────────┘
     │
     │ 7. Return Result
     ▼
┌─────────┐
│  Client │
└─────────┘
```

---

## 🕸️ Network Topology

### Mesh Network Structure

```
                    ┌──────────┐
                    │  Node A  │
                    │ CPU: 25% │
                    └────┬─────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐     ┌────▼────┐    ┌────▼────┐
    │ Node B  │     │ Node C  │    │ Node D  │
    │CPU: 45% │     │CPU: 12% │    │CPU: 78% │
    └────┬────┘     └────┬────┘    └────┬────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                    ┌────▼────┐
                    │ Node E  │
                    │CPU: 33% │
                    └─────────┘

Gossip Protocol: Each node broadcasts state every 5s
Task Routing: Task routed to Node C (lowest CPU: 12%)
Heartbeat: All nodes ping every 10s
```

---

## 🔍 Kademlia DHT Architecture

### K-Bucket Routing Table

```
Node ID: aaaa1111bbbb2222 (160-bit)

Bucket  Distance Range    Peers
─────────────────────────────────────────────
  0     2^0  - 2^1        []
  1     2^1  - 2^2        []
  2     2^2  - 2^3        [peer_1]
  ...
 42     2^42 - 2^43       [peer_2, peer_3]
  ...
159     2^159- 2^160      [peer_n]

Each bucket: max 20 peers (k=20)
Total capacity: 3200 peers (160 * 20)
```

### XOR Distance Metric

```
Node A: aaaa1111bbbb2222
Node B: cccc3333dddd4444

XOR Distance:
aaaa1111bbbb2222
⊕
cccc3333dddd4444
─────────────────
6666222266666666

Closer nodes = smaller XOR distance
Routing decision: O(log n) lookup
```

---

## 📡 Gossip Protocol State Propagation

### Epidemic Broadcast Model

```
Round 0:
  Node A knows: [A's state]

Round 1:
  Node A → Node B, Node C
  Nodes [A, B, C] know: [A's state]

Round 2:
  Node A → Node D
  Node B → Node E
  Node C → Node F
  Nodes [A,B,C,D,E,F] know: [A's state]

Convergence: O(log n) rounds
Total messages: n * log(n)
```

### Gossip Message Structure

```json
{
  "type": "gossip",
  "node_id": "node-alpha",
  "host": "192.168.1.10",
  "port": 8001,
  "load": {
    "cpu": 45.2,
    "ram": 62.1,
    "timestamp": "2024-08-21T10:30:00"
  },
  "known_nodes": {
    "node-beta": {"cpu": 23.4, "ram": 50.0},
    "node-gamma": {"cpu": 67.8, "ram": 75.5}
  }
}
```

---

## 💓 Heartbeat & Failure Detection

### State Machine

```
    ┌─────────┐
    │  ACTIVE │ ◄──┐
    └────┬────┘    │
         │         │
         │ timeout │ heartbeat
         │ > 10s   │ received
         │         │
    ┌────▼────┐    │
    │ SUSPECT │────┘
    └────┬────┘
         │
         │ timeout
         │ > 20s
         │
    ┌────▼────┐
    │ FAILED  │
    └────┬────┘
         │
         │ re-route
         │ tasks
         ▼
    ┌─────────┐
    │ REMOVED │
    └─────────┘
```

### Failure Recovery Flow

```
1. Heartbeat timeout detected
   └─▶ Node marked as FAILED

2. Query pending tasks on failed node
   └─▶ Find affected tasks

3. Gossip protocol provides updated node list
   └─▶ Get healthy nodes

4. Task Router re-routes tasks
   └─▶ Route to next best node

5. Resume task execution
   └─▶ Update task status to RUNNING
```

---

## 🔐 Security Architecture

### Message Signing with HMAC

```
┌─────────────┐
│   Message   │
└──────┬──────┘
       │
       │ + Secret Key
       ▼
┌─────────────┐
│ HMAC-SHA256 │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Signature  │
└──────┬──────┘
       │
       │ Transmitted together
       ▼
┌─────────────────────┐
│ Message + Signature │
└─────────────────────┘
       │
       │ Verify on receiver
       ▼
┌─────────────┐
│  ✅ Valid   │
│  ❌ Invalid │
└─────────────┘
```

---

## 🎯 Task Routing Algorithm

### CPU-Based Load Balancing

```python
def route_task(task):
    # 1. Get all active nodes from gossip protocol
    nodes = gossip.get_active_nodes()
    
    # 2. Filter out failed nodes (from heartbeat)
    healthy = [n for n in nodes if n not in heartbeat.failed_nodes]
    
    # 3. Sort by CPU load (ascending)
    sorted_nodes = sorted(healthy, key=lambda n: n.cpu_load)
    
    # 4. Select node with lowest CPU
    target = sorted_nodes[0]
    
    # 5. Transmit serialized task
    send_task(target, serialize(task))
    
    return target
```

### Routing Decision Tree

```
Task Arrives
     │
     ▼
Available Nodes? ──No──▶ Queue locally
     │
    Yes
     │
     ▼
Healthy Nodes? ──No──▶ Trigger recovery
     │
    Yes
     │
     ▼
Find Lowest CPU
     │
     ▼
CPU < 70%? ──No──▶ Find next best
     │
    Yes
     │
     ▼
Route to Node
     │
     ▼
Monitor with Heartbeat
```

---

## 📊 Component Interaction Diagram

```
┌──────────────┐         ┌──────────────┐
│    Client    │────────▶│ Task Queue   │
└──────────────┘         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ TaskRouter   │
                         └──────┬───────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
         ┌──────────┐    ┌──────────┐   ┌──────────┐
         │  Gossip  │    │Heartbeat │   │Kademlia  │
         │ Protocol │    │ Monitor  │   │   DHT    │
         └────┬─────┘    └────┬─────┘   └────┬─────┘
              │               │              │
              └───────────────┼──────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │ Peer Network │
                       └──────────────┘
```

---

## 🔧 Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| **K-Bucket Size** | 20 | Max peers per bucket |
| **DHT Buckets** | 160 | Total routing buckets |
| **Gossip Interval** | 5s | State broadcast frequency |
| **Heartbeat Timeout** | 10s | Failure detection threshold |
| **Task Priority Levels** | 1-10 | Higher = more urgent |
| **Max Concurrent Tasks** | 50 | Per-node task limit |
| **Network Buffer Size** | 64KB | Socket buffer size |

---

## 📈 Scalability Characteristics

| Metric | Complexity | Notes |
|--------|-----------|-------|
| **Peer Discovery** | O(log n) | Kademlia DHT lookup |
| **Gossip Convergence** | O(log n) | Rounds to full propagation |
| **Routing Decision** | O(n) | Linear scan of known nodes |
| **Task Queue Insert** | O(log n) | Priority queue (heap) |
| **Failure Detection** | O(1) | Per-node timeout check |

---

## 🚀 Deployment Architecture

### Single-Machine Development

```
┌────────────────────────────────────┐
│        Host Machine (Dev)          │
│                                    │
│  ┌──────┐  ┌──────┐  ┌──────┐    │
│  │Node A│  │Node B│  │Node C│    │
│  │:8001 │  │:8002 │  │:8003 │    │
│  └──────┘  └──────┘  └──────┘    │
│     │         │         │         │
│     └─────────┼─────────┘         │
│          localhost                │
└────────────────────────────────────┘
```

### Multi-Machine Production

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Server A    │   │  Server B    │   │  Server C    │
│ 10.0.1.10    │   │ 10.0.1.11    │   │ 10.0.1.12    │
│              │   │              │   │              │
│ ┌──────────┐ │   │ ┌──────────┐ │   │ ┌──────────┐ │
│ │ Node A1  │ │   │ │ Node B1  │ │   │ │ Node C1  │ │
│ │  :8001   │ │   │ │  :8001   │ │   │ │  :8001   │ │
│ └──────────┘ │   │ └──────────┘ │   │ └──────────┘ │
│ ┌──────────┐ │   │ ┌──────────┐ │   │ ┌──────────┐ │
│ │ Node A2  │ │   │ │ Node B2  │ │   │ │ Node C2  │ │
│ │  :8002   │ │   │ │  :8002   │ │   │ │  :8002   │ │
│ └──────────┘ │   │ └──────────┘ │   │ └──────────┘ │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                     Internet/LAN
```

---

## 🎓 Design Decisions

### Why Kademlia DHT?

- **Logarithmic Complexity**: O(log n) lookup time
- **Self-Organizing**: No manual routing configuration
- **Fault Tolerant**: Survives node failures gracefully
- **Proven**: Used in BitTorrent, Ethereum, IPFS

### Why Gossip Protocol?

- **Scalable**: Works well with thousands of nodes
- **Fault Tolerant**: No single point of failure
- **Eventual Consistency**: All nodes converge to same state
- **Low Overhead**: Periodic, not real-time

### Why cloudpickle?

- **Closure Support**: Serialize nested functions
- **ML Model Support**: Works with NumPy, scikit-learn
- **Python Native**: No external serialization format
- **Flexible**: Handles arbitrary Python objects

---

## 📝 Future Enhancements

1. **NAT Traversal**: STUN/TURN for firewall penetration
2. **Data Sharding**: Distribute large datasets across nodes
3. **Byzantine Fault Tolerance**: Handle malicious nodes
4. **GPU Task Support**: Route GPU-intensive tasks
5. **Web Dashboard**: Browser-based monitoring UI
6. **Kubernetes Deployment**: Container orchestration support

---

## 📚 References

- [Kademlia Paper (MIT)](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf)
- [Gossip Protocols (Cornell)](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/2007PromiseAndLimitations.pdf)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

---

**Last Updated**: Week 4, August 2024  
**Maintainer**: MeshWeaver Team - Infotact Solutions
