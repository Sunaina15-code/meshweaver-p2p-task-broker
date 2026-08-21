# MeshWeaver - TLS Security - Aug 17 - Sunaina
# Cryptographic signatures for task execution

import hashlib
import hmac
import json
import secrets
from datetime import datetime

class MeshSecurity:
    """
    Handles cryptographic security for MeshWeaver
    - Message signing and verification
    - Node authentication
    - Secure task requests
    """
    def __init__(self, node_id):
        self.node_id = node_id
        self.secret_key = secrets.token_hex(32)
        self.trusted_nodes = {}
        self.blocked_nodes = set()

    def generate_signature(self, message):
        """Generate HMAC signature for message"""
        msg_bytes = json.dumps(message, sort_keys=True).encode()
        signature = hmac.new(
            self.secret_key.encode(),
            msg_bytes,
            hashlib.sha256
        ).hexdigest()
        return signature

    def verify_signature(self, message, signature, sender_key):
        """Verify message signature from sender"""
        msg_bytes = json.dumps(message, sort_keys=True).encode()
        expected = hmac.new(
            sender_key.encode(),
            msg_bytes,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)

    def create_signed_message(self, msg_type, data):
        """Create a cryptographically signed message"""
        message = {
            'type': msg_type,
            'node_id': self.node_id,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'nonce': secrets.token_hex(8)
        }
        signature = self.generate_signature(message)
        return {
            'message': message,
            'signature': signature,
            'public_key': self.secret_key[:16]
        }

    def trust_node(self, node_id, public_key):
        """Add node to trusted list"""
        self.trusted_nodes[node_id] = public_key
        print(f"[{self.node_id}] Trusted: {node_id}")

    def block_node(self, node_id):
        """Block untrusted node"""
        self.blocked_nodes.add(node_id)
        print(f"[{self.node_id}] Blocked: {node_id}")

    def is_trusted(self, node_id):
        return node_id in self.trusted_nodes

    def secure_task_request(self, task_name, task_data, target_node):
        """Create a secure task execution request"""
        if target_node in self.blocked_nodes:
            print(f"[{self.node_id}] ❌ Blocked node: {target_node}")
            return None

        request = self.create_signed_message('task_request', {
            'task': task_name,
            'data': task_data,
            'target': target_node
        })
        print(f"[{self.node_id}] ✅ Secure request: {task_name} → {target_node}")
        return request

    def display_security_info(self):
        print(f"\n=== Security Info [{self.node_id}] ===")
        print(f"Trusted nodes: {len(self.trusted_nodes)}")
        print(f"Blocked nodes: {len(self.blocked_nodes)}")
        print(f"Key (partial): {self.secret_key[:16]}...")

if __name__ == "__main__":
    print("=== MeshWeaver Security Demo ===\n")

    node1 = MeshSecurity("node-alpha")
    node2 = MeshSecurity("node-beta")

    # Trust each other
    node1.trust_node("node-beta", node2.secret_key[:16])
    node2.trust_node("node-alpha", node1.secret_key[:16])

    # Create signed message
    signed = node1.create_signed_message("ping", {"data": "hello"})
    print(f"\nSigned message created!")
    print(f"Signature: {signed['signature'][:20]}...")

    # Secure task request
    request = node1.secure_task_request(
        "ml_inference", {"model": "bert"}, "node-beta"
    )

    # Block a node
    node1.block_node("evil-node")
    blocked = node1.secure_task_request("task", {}, "evil-node")

    node1.display_security_info()
    print("\n✅ Security Demo Complete!")