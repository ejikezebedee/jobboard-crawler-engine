"""
Anti-Detection Layer - Browser Fingerprint Spoofing and Stealth
"""

import random
import string
import hashlib
from typing import Dict, Any
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

class AntiDetectionEngine:
    """Engine for spoofing browser fingerprints and avoiding detection"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.fingerprint_cache: Dict[str, str] = {}

    async def get_random_fingerprint(self) -> Dict[str, Any]:
        """Generate random browser fingerprint"""
        import uuid

        fingerprint = {
            "platform": random.choice(["Windows 10", "Windows 11", "macOS 14.0", "Linux x86_64"]),
            "user_agent": self._get_random_user_agent(),
            "viewport": {
                "width": random.choice([1920, 1366, 1440, 1536, 1680, 1920, 2560, 3840]),
                "height": random.choice([1080, 1440, 1600, 720]),
            },
            "language": random.choice(["en-US", "en-GB", "en-AU", "de-DE", "fr-FR", "nl-NL"]),
            "timezone": random.choice([
                "America/New_York",
                "America/Los_Angeles",
                "Europe/London",
                "Europe/Paris",
                "Asia/Tokyo",
                "Asia/Shanghai"
            ]),
            "webgl_vendor": random.choice([
                "Google Inc. (NVIDIA)",
                "Google Inc. (AMD)",
                "Google Inc. (Intel)"
            ]),
            "canvas_fingerprint": self._generate_canvas_fingerprint(),
            "screen_orientation": random.choice(["landscape", "portrait"]),
            "device_pixel_ratio": random.choice([1.0, 1.25, 1.5, 2.0, 2.5, 3.0]),
            "cookies_enabled": True,
            "java_enabled": False,
            "pdf_enabled": True,
            "webgl_enabled": True,
            "speech_recognition_enabled": False,
            "media_encryption": random.choice(["AES-256-GCM", "AES-128-GCM", "ChaCha20-Poly1305"]),
            "hardware_concurrency": random.choice([4, 6, 8, 12, 16]),
            "device_memory": random.choice([4, 8, 16, 32]),
            "cpu_class": random.choice(["low", "medium", "high"]),
        }

        return fingerprint

    def _get_random_user_agent(self) -> str:
        """Generate random user-agent string"""
        from fake_useragent import UserAgent

        try:
            ua = UserAgent()
            return ua.random
        except:
            # Fallback to random string if fake_useragent fails
            return f"Mozilla/5.0 ({random.choice(['Windows NT 10.0; Win64; x64', 'Macintosh; Intel Mac OS X 10_15_7', 'X11; Linux x86_64'])} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(120, 131)}.{random.randint(0, 999)}.0 Safari/537.36"

    def _generate_canvas_fingerprint(self) -> str:
        """Generate random canvas fingerprint"""
        import hashlib
        random_data = "".join(random.choices(string.ascii_letters + string.digits, k=32))
        return hashlib.sha256(random_data.encode()).hexdigest()

    async def create_stealth_browser(self):
        """Create browser with stealth mode enabled"""
        playwright_instance = await async_playwright().start()

        browser = await playwright_instance.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-site-isolation-trials",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-background-networking",
                "--disable-breakpad",
                "--disable-component-extensions-with-background-pages",
                "--disable-extensions",
                "--disable-features=IdleScreenshot",
                "--disable-features=VizDisplayCompositor",
                "--disable-features=VizDisplayCompositor2",
                "--disable-features=SharedArrayBuffer",
                "--disable-features=NewToolbar",
                "--disable-features=LearningMode",
                "--disable-features=ImmersiveToolbar",
                "--disable-features=InteractiveCanvasPlaceholder",
                "--disable-features=HighEfficiencyMode",
                "--disable-features=EnhancedCloudHelp",
                "--disable-features=SiteIsolationTrialsSearchEngines",
                "--disable-features=CookieStorageProcessSharing",
                "--disable-features=VizFeedback,
            ]
        )

        context = await browser.new_context(
            viewport=None,
            user_agent=self._get_random_user_agent(),
            locale=random.choice(["en-US", "en-GB", "en-AU", "de-DE", "fr-FR", "nl-NL"]),
            timezone_id=random.choice([
                "America/New_York",
                "America/Los_Angeles",
                "Europe/London",
                "Europe/Paris",
                "Asia/Tokyo",
                "Asia/Shanghai"
            ]),
            permissions=["geolocation", "notifications", "clipboard-write"],
            extra_http_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": random.choice(["en-US,en;q=0.9,en-GB;q=0.8,en-AU;q=0.7"]),
                "Accept-Encoding": random.choice(["gzip, deflate, br", "gzip, deflate", "br"]),
                "Accept-Charset": "UTF-8",
                "DNT": random.choice(["1", "0"]),
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": random.choice(["document", "iframe", "frame", "object", "xmlhttprequest", "manifest", "ping"]),
                "Sec-Fetch-Mode": random.choice(["navigate", "cors", "no-cors", "same-origin", "opaque"]),
                "Sec-Fetch-Site": random.choice(["none", "cross-site", "same-site"]),
                "Cache-Control": "max-age=0",
                "Connection": random.choice(["keep-alive", "keep-alive", "close"]),
            },
        )

        page = await context.new_page()

        # Apply stealth mode
        await stealth_async(page)

        return browser, context, page

    def get_random_delay(self) -> float:
        """Get random delay for human behavior simulation"""
        return random.uniform(0.1, 3.0)  # 100ms to 3 seconds

    def get_variable_delay(self, base_delay: float, variance: float = 0.5) -> float:
        """Get variable delay with randomness"""
        return base_delay * random.uniform(1 - variance, 1 + variance)

    def rotate_fingerprint(self) -> None:
        """Rotate fingerprint cache"""
        import uuid
        self.fingerprint_cache[str(uuid.uuid4())] = str(uuid.uuid4())