# Architecture Diagrams

This folder contains visual diagrams for the MeshWeaver architecture.

## 📁 Contents

### Planned Diagrams

1. **architecture_diagram.png** - High-level system architecture
   - Shows the 4-layer architecture (Application, Coordination, Discovery, Transport)
   - Component interactions
   - Data flow paths

2. **network_topology.png** - Mesh network visualization
   - Node interconnections
   - Gossip protocol propagation
   - DHT routing structure

3. **task_flow_diagram.png** - Task execution flow
   - Task submission → serialization → routing → execution
   - Component interactions at each stage

4. **kademlia_routing.png** - Kademlia DHT routing
   - K-bucket structure
   - XOR distance visualization
   - Peer lookup process

## 🎨 Creating Diagrams

### Tools You Can Use

- **Draw.io** (https://app.diagrams.net/) - Free, web-based
- **Lucidchart** (https://www.lucidchart.com/) - Professional diagramming
- **Microsoft Visio** - Enterprise diagramming tool
- **PlantUML** - Text-based UML diagrams
- **Mermaid** - Markdown-based diagrams (already in architecture.md)

### Diagram Guidelines

1. **Keep it Simple**: Focus on key components
2. **Use Consistent Colors**: 
   - Blue for network components
   - Green for successful operations
   - Red for failures
   - Yellow for pending/queued items
3. **Label Everything**: Clear labels for nodes, connections, data flows
4. **Add a Legend**: Explain symbols and colors used

## 📝 Diagram Specifications

### Architecture Diagram
- **Size**: 1920x1080 px
- **Format**: PNG with transparency
- **Elements**: 
  - 4 layers stacked vertically
  - Arrows showing data flow
  - Component boxes with labels

### Network Topology
- **Size**: 1600x1200 px
- **Format**: PNG
- **Elements**:
  - Nodes as circles with IDs
  - Connections as lines
  - CPU/RAM stats in labels
  - Gossip messages as animated arrows (optional)

## 🔄 Updating Diagrams

When the architecture changes:
1. Update the diagram files
2. Update references in architecture.md
3. Update this README
4. Commit with descriptive message

## 📚 References

The text-based diagrams in `../architecture.md` serve as ASCII alternatives and should match the visual diagrams.

---

**Note**: Until PNG diagrams are created, refer to the ASCII diagrams in [architecture.md](../architecture.md).
