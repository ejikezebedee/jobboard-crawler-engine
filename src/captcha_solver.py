"""
Captcha Solver Integration - Auto-detection, Solver Selection, Retry Logic
"""

import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class CaptchaConfig:
    enabled: bool = True
    provider: str = "2captcha"
    min_confidence: float = 0.5
    timeout_seconds: int = 60
    retry_attempts: int = 3

@dataclass
class CaptchaResult:
    solved: bool
    solution: Optional[str] = None
    provider: str = "unknown"
    confidence: float = 0.0
    error: Optional[str] = None

class CaptchaSolver:
    """Integrated captcha solver for various CAPTCHA providers"""

    def __init__(self, config: CaptchaConfig):
        self.config = config
        self.providers = {
            "2captcha": self._solve_with_2captcha,
            "9llcok": self._solve_with_9llcok,
            "deathbycaptcha": self._solve_with_deathbycaptcha,
        }

    async def solve(self, captcha_type: str, challenge: str, difficulty: str = "medium") -> CaptchaResult:
        """Solve a CAPTCHA challenge"""
        if not self.config.enabled:
            return CaptchaResult(solved=False, error="Captcha solving disabled")

        if captcha_type.lower() not in self.config.providers:
            return CaptchaResult(solved=False, error=f"Unknown CAPTCHA type: {captcha_type}")

        provider = self.config.providers[captcha_type.lower()]

        for attempt in range(self.config.retry_attempts):
            try:
                result = await provider(captcha_type, challenge, difficulty)

                if result.solved and result.confidence >= self.config.min_confidence:
                    result.provider = captcha_type
                    return result

                await asyncio.sleep(1)  # Wait before retry

            except Exception as e:
                result = CaptchaResult(
                    solved=False,
                    error=str(e)
                )

                if result.error:
                    result.provider = captcha_type

                if attempt == self.config.retry_attempts - 1:
                    return result

        return CaptchaResult(solved=False, error="Failed to solve CAPTCHA")

    async def _solve_with_2captcha(self, captcha_type: str, challenge: str, difficulty: str) -> CaptchaResult:
        """Solve CAPTCHA using 2Captcha"""
        # TODO: Integrate 2Captcha API
        await asyncio.sleep(random.uniform(0.1, 0.5))
        return CaptchaResult(solved=True, solution="solved", provider="2captcha", confidence=0.9)

    async def _solve_with_9llcok(self, captcha_type: str, challenge: str, difficulty: str) -> CaptchaResult:
        """Solve CAPTCHA using 9LLOK"""
        # TODO: Integrate 9LLOK API
        await asyncio.sleep(random.uniform(0.1, 0.5))
        return CaptchaResult(solved=True, solution="solved", provider="9llcok", confidence=0.85)

    async def _solve_with_deathbycaptcha(self, captcha_type: str, challenge: str, difficulty: str) -> CaptchaResult:
        """Solve CAPTCHA using DeathByCAPTCHA"""
        # TODO: Integrate DeathByCAPTCHA API
        await asyncio.sleep(random.uniform(0.1, 0.5))
        return CaptchaResult(solved=True, solution="solved", provider="deathbycaptcha", confidence=0.88)

    def is_captcha(self, response: str) -> bool:
        """Check if response contains CAPTCHA challenge"""
        captcha_indicators = [
            "captcha",
            "hcaptcha",
            "hcaptcha.com",
            "recaptcha",
            "grecaptcha",
            "challenge",
            "token",
            "hcaptcha",
            "hcaptcha_challenge",
            "hcaptcha challenge",
        ]

        response_lower = response.lower()
        return any(indicator in response_lower for indicator in captcha_indicators)

    def get_captcha_type(self, page_content: str) -> str:
        """Detect CAPTCHA type from page content"""
        if "hcaptcha" in page_content.lower():
            return "hcaptcha"
        elif "recaptcha" in page_content.lower():
            return "recaptcha"
        elif "2captcha" in page_content.lower():
            return "2captcha"
        else:
            return "unknown"