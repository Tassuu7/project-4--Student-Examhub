"""
ExamHub Merkle Audit Tree Engine
Constructs cryptographic Merkle Trees over audit events to provide tamper-evident mathematical proof.
"""

import hashlib
from typing import List, Dict, Tuple, Optional
from backend.app.audit_compliance.schemas import MerkleAuditProof


class MerkleAuditTree:
    """
    Binary Merkle Tree implementation for immutable tamper detection of exam logs.
    """

    @classmethod
    def hash_pair(cls, left: str, right: str) -> str:
        combined = f"{left}:{right}".encode("utf-8")
        return hashlib.sha256(combined).hexdigest()

    @classmethod
    def build_tree(cls, leaf_hashes: List[str]) -> Tuple[str, List[List[str]]]:
        """
        Builds Merkle tree levels from list of SHA256 leaf hashes.
        Returns: (root_hash, levels)
        """
        if not leaf_hashes:
            empty_root = hashlib.sha256(b"empty_exam_audit_tree").hexdigest()
            return empty_root, [[]]

        current_level = list(leaf_hashes)
        levels = [current_level]

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                if i + 1 < len(current_level):
                    right = current_level[i + 1]
                else:
                    right = left  # Duplicate odd trailing leaf
                parent = cls.hash_pair(left, right)
                next_level.append(parent)

            levels.append(next_level)
            current_level = next_level

        return current_level[0], levels

    @classmethod
    def generate_proof(cls, leaf_index: int, levels: List[List[str]]) -> List[Dict[str, str]]:
        """
        Generate Merkle audit path for a specific leaf index.
        """
        proof = []
        idx = leaf_index

        for level_idx in range(len(levels) - 1):
            level = levels[level_idx]
            is_right_child = (idx % 2 == 1)
            sibling_idx = idx - 1 if is_right_child else idx + 1

            if sibling_idx < len(level):
                sibling_hash = level[sibling_idx]
            else:
                sibling_hash = level[idx]

            proof.append({
                "position": "left" if is_right_child else "right",
                "hash": sibling_hash
            })
            idx = idx // 2

        return proof

    @classmethod
    def verify_proof(cls, leaf_hash: str, proof: List[Dict[str, str]], expected_root: str) -> bool:
        """
        Verifies that leaf_hash belongs to expected_root via proof path.
        """
        current = leaf_hash
        for step in proof:
            pos = step["position"]
            sibling = step["hash"]

            if pos == "left":
                current = cls.hash_pair(sibling, current)
            else:
                current = cls.hash_pair(current, sibling)

        return current.lower() == expected_root.lower()
