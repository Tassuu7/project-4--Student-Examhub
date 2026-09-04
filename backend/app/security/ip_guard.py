"""
ExamHub - IP Subnet & Exam Hall Guard
Enforces CIDR and IP restriction lists for proctored examination halls and campus networks.
"""

import ipaddress
from typing import List, Set, Optional

class IPGuard:
    """Network-level access control for institutional testing environments."""

    def __init__(self, allowed_cidrs: Optional[List[str]] = None):
        self.networks = []
        if allowed_cidrs:
            for cidr in allowed_cidrs:
                try:
                    self.networks.append(ipaddress.ip_network(cidr, strict=False))
                except ValueError:
                    pass

    def is_ip_authorized(self, client_ip_str: str) -> bool:
        if not self.networks:
            return True  # If no IP restriction configured, allow all

        try:
            client_ip = ipaddress.ip_address(client_ip_str)
            for net in self.networks:
                if client_ip in net:
                    return True
            return False
        except ValueError:
            return False
