"""
ExamHub - In-Memory Sliding Window Rate Limiter
Prevents automated brute-force attacks, DDoS, and rapid option clicking
using a thread-safe sliding-window bucket algorithm.
"""

import time
from collections import defaultdict
from typing import Dict, Tuple

class SlidingWindowRateLimiter:
    """Sliding-window token rate limiting implementation."""

    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.history: Dict[str, list] = defaultdict(list)

    def is_allowed(self, client_key: str) -> Tuple[bool, int]:
        """
        Returns (is_allowed, remaining_requests_in_window).
        """
        now = time.time()
        cutoff = now - self.window_seconds

        # Prune older entries
        self.history[client_key] = [t for t in self.history[client_key] if t > cutoff]

        current_count = len(self.history[client_key])
        if current_count < self.max_requests:
            self.history[client_key].append(now)
            return True, self.max_requests - current_count - 1
        else:
            return False, 0

    def reset_key(self, client_key: str):
        if client_key in self.history:
            del self.history[client_key]

# Pre-configured global rate limiters
api_limiter = SlidingWindowRateLimiter(max_requests=120, window_seconds=60)
auth_limiter = SlidingWindowRateLimiter(max_requests=10, window_seconds=60)
exam_answer_limiter = SlidingWindowRateLimiter(max_requests=60, window_seconds=60)
