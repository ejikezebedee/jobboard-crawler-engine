"""
Anti-Ban Analytics - Monitoring, IP Reputation, Request Analytics
"""

import asyncio
import aiohttp
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict

@dataclass
class HealthMetrics:
    total_requests: int
    successful_requests: int
    failed_requests: int
    captcha_requests: int
    blocked_requests: int
    proxy_failures: int
    request_success_rate: float
    avg_response_time: float

class HealthMonitor:
    """Monitor and analyze anti-ban metrics"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.metrics = HealthMetrics(
            total_requests=0,
            successful_requests=0,
            failed_requests=0,
            captcha_requests=0,
            blocked_requests=0,
            proxy_failures=0,
            request_success_rate=0.0,
            avg_response_time=0.0,
        )

        # IP reputation tracking
        self.ip_reputation: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "requests": 0,
            "successes": 0,
            "failures": 0,
            "last_used": None,
            "block_reason": None,
        })

        # Request tracking
        self.request_history: List[Dict[str, Any]] = []

        # HTTP session
        self.session: Optional[aiohttp.ClientSession] = None

    async def initialize(self):
        """Initialize health monitor session"""
        self.session = aiohttp.ClientSession()

    async def record_request(
        self,
        fingerprint: str,
        success: bool,
        captcha: bool = False,
        blocked: bool = False,
        proxy_used: Optional[str] = None,
        response_time: float = 0.0,
    ):
        """Record request metrics"""
        self.metrics.total_requests += 1

        if success:
            self.metrics.successful_requests += 1
            if proxy_used:
                self.ip_reputation[proxy_used]["requests"] += 1
                self.ip_reputation[proxy_used]["successes"] += 1
                self.ip_reputation[proxy_used]["last_used"] = datetime.now().timestamp()

        if not success:
            self.metrics.failed_requests += 1

        if captcha:
            self.metrics.captcha_requests += 1

        if blocked:
            self.metrics.blocked_requests += 1
            if proxy_used:
                self.ip_reputation[proxy_used]["block_reason"] = "blocked"

        self.metrics.request_success_rate = (
            self.metrics.successful_requests / self.metrics.total_requests
        ) if self.metrics.total_requests > 0 else 0.0

        self.request_history.append({
            "timestamp": datetime.now().isoformat(),
            "fingerprint": fingerprint,
            "success": success,
            "captcha": captcha,
            "blocked": blocked,
            "response_time": response_time,
            "proxy": proxy_used,
        })

        # Prune old request history
        self._cleanup_old_history()

    async def check_ip_reputation(self, ip: str) -> bool:
        """Check if IP has suspicious reputation"""
        reputation = self.ip_reputation[ip]

        total_requests = reputation["requests"]
        success_rate = reputation["successes"] / total_requests if total_requests > 0 else 0.0

        # If IP has low success rate, block it
        if success_rate < 0.3 and total_requests > 10:
            return True

        # If IP has many failures, block it
        if reputation["failures"] > 5:
            return True

        # If IP has been blocked recently, block it
        if reputation["block_reason"] == "blocked":
            if datetime.now().timestamp() - reputation["last_used"] < 3600:  # Block for 1 hour
                return True

        return False

    async def detect_dns_leak(self) -> bool:
        """Detect DNS leaks"""
        # TODO: Implement DNS leak detection
        return False

    async def get_health_metrics(self) -> HealthMetrics:
        """Get current health metrics"""
        return self.metrics

    async def get_analytics_report(self, hours: int = 1) -> Dict[str, Any]:
        """Generate analytics report for specified time window"""
        now = datetime.now()
        cutoff = now - timedelta(hours=hours)

        # Filter request history
        recent_requests = [
            r for r in self.request_history
            if datetime.fromisoformat(r["timestamp"]) > cutoff
        ]

        return {
            "time_range": f"{hours} hours",
            "total_requests": len(recent_requests),
            "successful_requests": sum(1 for r in recent_requests if r["success"]),
            "failed_requests": sum(1 for r in recent_requests if not r["success"]),
            "captcha_requests": sum(1 for r in recent_requests if r["captcha"]),
            "blocked_requests": sum(1 for r in recent_requests if r["blocked"]),
            "avg_response_time": sum(r["response_time"] for r in recent_requests) / len(recent_requests) if recent_requests else 0.0,
            "request_success_rate": (
                sum(1 for r in recent_requests if r["success"]) / len(recent_requests) if recent_requests else 0.0
            ),
            "top_fingerprints": self._get_top_fingerprints(recent_requests),
            "most_common_failures": self._get_common_failures(recent_requests),
        }

    def _cleanup_old_history(self):
        """Cleanup old request history"""
        now = datetime.now()
        # Keep last 1000 requests
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-1000:]

    def _get_top_fingerprints(self, requests: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
        """Get top fingerprints by request count"""
        fingerprint_counts: Dict[str, int] = defaultdict(int)

        for request in requests:
            fingerprint = request["fingerprint"]
            fingerprint_counts[fingerprint] += 1

        sorted_fingerprints = sorted(
            fingerprint_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [{"fingerprint": fp, "count": count} for fp, count in sorted_fingerprints[:limit]]

    def _get_common_failures(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get most common failure reasons"""
        failure_reasons: Dict[str, int] = defaultdict(int)

        for request in requests:
            if not request["success"]:
                reason = request.get("error", "unknown")
                failure_reasons[reason] += 1

        sorted_failures = sorted(
            failure_reasons.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [{"reason": reason, "count": count} for reason, count in sorted_failures[:10]]

    async def check_proxy_reputation(self, proxy: str) -> bool:
        """Check proxy reputation"""
        reputation = self.ip_reputation.get(proxy, {"successes": 0, "failures": 0})

        success_rate = reputation["successes"] / reputation["requests"] if reputation["requests"] > 0 else 0.0

        if success_rate < 0.3 and reputation["requests"] > 10:
            return True

        return False

    async def close(self):
        """Close health monitor session"""
        if self.session:
            await self.session.close()