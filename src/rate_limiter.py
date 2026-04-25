"""
Smart Rate Limiting - Adaptive Backoff, Quota Management, Session-Level Throttling
"""

import asyncio
import time
from typing import Dict, Optional, List
from dataclasses import dataclass
from collections import deque

@dataclass
class RateLimitConfig:
    base_requests_per_second: float
    max_requests_per_second: float
    min_requests_per_second: float
    max_burst_size: int
    adaptive_scaling: bool
    backoff_multiplier: float
    backoff_base_seconds: float
    backoff_max_seconds: float

class AdaptiveRateLimiter:
    """Advanced rate limiter with adaptive scaling and backoff"""

    def __init__(self, config: RateLimitConfig, fingerprint: str):
        self.config = config
        self.fingerprint = fingerprint
        self.last_request_time: float = 0.0
        self.request_count: int = 0
        self.fingerprint: str = fingerprint

        # Per-session tracking
        self.session_requests: Dict[str, deque] = {}
        self.session_ratelimits: Dict[str, RateLimitConfig] = {}

    async def wait_until_ready(self, difficulty: str = "medium"):
        """Wait until rate limit is no longer exceeded"""
        current_delay = self._calculate_delay(difficulty)
        await asyncio.sleep(current_delay)

    def _calculate_delay(self, difficulty: str) -> float:
        """Calculate delay based on difficulty and rate limit"""
        if difficulty == "easy":
            base_rate = self.config.max_requests_per_second
        elif difficulty == "medium":
            base_rate = self.config.base_requests_per_second * 0.8
        else:  # hard
            base_rate = self.config.min_requests_per_second * 0.5

        delay = 1.0 / base_rate if base_rate > 0 else 1.0
        delay = min(self.config.backoff_max_seconds, delay)

        return delay

    async def record_request(self, difficulty: str = "medium") -> float:
        """Record request and calculate delay until next request"""
        now = time.time()
        elapsed = now - self.last_request_time

        current_delay = self._calculate_delay(difficulty)

        if elapsed < current_delay:
            await asyncio.sleep(current_delay - elapsed)

        self.last_request_time = time.time()
        self.request_count += 1

        # Adaptive scaling
        if self.config.adaptive_scaling:
            await self._adaptive_scaling(difficulty)

        # Per-session rate limiting
        await self._session_tracking(difficulty)

        return current_delay

    async def _adaptive_scaling(self, difficulty: str):
        """Adaptively adjust rate limit based on success rate"""
        # TODO: Implement adaptive scaling logic
        pass

    async def _session_tracking(self, difficulty: str):
        """Track requests per session"""
        session_id = self.fingerprint
        if session_id not in self.session_requests:
            self.session_requests[session_id] = deque(maxlen=60)

        self.session_requests[session_id].append(time.time())

        # Calculate requests in last minute
        now = time.time()
        requests_in_last_minute = sum(1 for t in self.session_requests[session_id] if now - t < 60)

        # Adjust rate limit based on session
        if requests_in_last_minute > 10:
            new_rate = self.config.max_requests_per_second * 0.5
            self.session_ratelimits[session_id] = RateLimitConfig(
                base_requests_per_second=min(new_rate, 5.0),
                max_requests_per_second=min(new_rate * 1.5, 10.0),
                min_requests_per_second=1.0,
                max_burst_size=5,
                adaptive_scaling=False,
                backoff_multiplier=2.0,
                backoff_base_seconds=2.0,
                backoff_max_seconds=30.0,
            )

    async def get_quota(self, interval: str = "minute") -> int:
        """Get request quota for specified interval"""
        now = time.time()

        if interval == "minute":
            cutoff = now - 60
            return sum(1 for t in self.session_requests.get(self.fingerprint, []) if t > cutoff)

        elif interval == "hour":
            cutoff = now - 3600
            return sum(1 for t in self.session_requests.get(self.fingerprint, []) if t > cutoff)

        else:
            return self.request_count

    def get_current_rate_limit(self) -> float:
        """Get current rate limit based on difficulty"""
        if self.config.adaptive_scaling:
            return self.config.min_requests_per_second

        return self.config.base_requests_per_second

    def reset_session(self):
        """Reset session tracking"""
        self.session_requests = {}
        self.session_ratelimits = {}
        self.request_count = 0
        self.last_request_time = time.time()