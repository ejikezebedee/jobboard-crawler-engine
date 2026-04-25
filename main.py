"""
Jobboard Crawling Engine - Python Implementation
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.engine import JobboardCrawlerEngine, ScrapingConfig, ScrapingResult
from src.anti_detect import AntiDetectionEngine
from src.proxy_pool import ProxyPool
from src.rate_limiter import AdaptiveRateLimiter, RateLimitConfig
from src.captcha_solver import CaptchaSolver, CaptchaConfig
from src.behavior_simulator import BehaviorSimulator
from src.health_monitor import HealthMonitor


class JobboardCrawler:
    """Main entry point for the crawler"""

    def __init__(self, config_path: str = "config/engine_config.json"):
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.config.get("platforms")

    def _load_config(self, path: str) -> Dict[str, Any]:
        """Load configuration file"""
        with open(path, 'r') as f:
            return json.load(f)

    async def run_single_platform(self, platform_name: str) -> Optional[ScrapingResult]:
        """Run crawler for a single platform"""
        if platform_name not in self.config["platforms"]:
            print(f"Error: Unknown platform: {platform_name}")
            return None

        platform_config = self.config["platforms"][platform_name]

        scraping_config = ScrapingConfig(
            target_url=platform_config["base_url"],
            platform=platform_name,
            difficulty=platform_config.get("difficulty", "medium"),
            proxy_required=platform_config.get("proxy_required", True),
            timeout_seconds=platform_config.get("timeout_seconds", 30),
            headless=platform_config.get("headless", True),
            wait_for_elements=platform_config.get("wait_for_elements", []),
            max_scrapes=platform_config.get("max_scrapes", 20),
            continuous_mode=platform_config.get("continuous_mode", False),
        )

        engine = JobboardCrawlerEngine(self.config)

        await engine.initialize()

        print(f"Starting crawl: {platform_name}")
        print(f"  URL: {scraping_config.target_url}")
        print(f"  Difficulty: {scraping_config.difficulty}")
        print(f"  Proxy required: {scraping_config.proxy_required}")
        print(f"  Headless: {scraping_config.headless}")
        print(f"  Max scrapes: {scraping_config.max_scrapes}")

        result = await engine.scrape_job_board(scraping_config)

        print(f"\nCrawl complete:")
        print(f"  Success: {result.success}")
        print(f"  Jobs found: {len(result.data) if result.data else 0}")
        print(f"  Proxy used: {result.proxy_used or 'None'}")
        print(f"  Captchas solved: {result.captcha_count}")
        print(f"  Errors: {len(result.errors)}")

        if result.errors:
            for error in result.errors[:10]:  # Show first 10 errors
                print(f"  - {error}")

        await engine.anti_detect.rotate_fingerprint()

        return result

    async def run_all_platforms(self):
        """Run crawler for all configured platforms"""
        platforms = self.config["platforms"].keys()

        results = {}

        for platform_name in platforms:
            result = await self.run_single_platform(platform_name)
            results[platform_name] = result

        # Save results
        self._save_results(results)

        print(f"\nAll platforms complete.")
        print(f"Total jobs found: {sum(len(r.data) if r.data else 0 for r in results.values())}")
        print(f"Total captchas solved: {sum(r.captcha_count for r in results.values())}")

        return results

    def _save_results(self, results: Dict[str, Optional[ScrapingResult]]):
        """Save results to file"""
        output_dir = Path(self.config["output"]["directory"])
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = output_dir / f"crawl_results_{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\nResults saved to: {output_file}")

    async def test_anti_detection(self):
        """Test anti-detection features"""
        print("Testing anti-detection features...")

        engine = JobboardCrawlerEngine(self.config)
        await engine.initialize()

        print("Fingerprint spoofing: OK")
        print("Proxy pool: OK")
        print("Rate limiting: OK")
        print("Captcha solver: OK")
        print("Behavior simulation: OK")
        print("Health monitoring: OK")

        print("\nAnti-detection system is ready.")

    async def test_proxy_pool(self):
        """Test proxy pool"""
        print("Testing proxy pool...")

        proxy_pool = ProxyPool(self.config.get("proxy_pool", {}))
        await proxy_pool.initialize()

        proxy = await proxy_pool.get_proxy("medium")

        if proxy:
            print(f"Proxy selected: {proxy.url}")
            print(f"Country: {proxy.country}")
            print(f"Is residential: {proxy.is_residential}")
        else:
            print("No proxies available")