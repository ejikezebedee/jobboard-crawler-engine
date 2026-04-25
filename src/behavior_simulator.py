"""
Human Behavior Simulation - Random Delays, Mouse Movements, Scroll Patterns
"""

import asyncio
import random
import time
from typing import Optional

class BehaviorSimulator:
    """Simulate human-like behavior to avoid detection"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.mouse_positions = []
        self.current_mouse_position = (0, 0)

    async def simulate_typing_delay(self, text_length: int, difficulty: str = "medium") -> float:
        """
        Simulate typing speed based on text length
        Average typing speed: 30-50 WPM
        """
        words_per_minute = random.choice([30, 40, 45, 50, 60]) if difficulty == "easy" else random.choice([20, 25, 30, 35])
        characters_per_second = words_per_minute * 5.0 / 60.0
        delay = random.uniform(characters_per_second * 0.5, characters_per_second * 1.5)

        return delay

    async def simulate_scroll_delay(self, scroll_type: str = "down") -> float:
        """Simulate human-like scroll behavior"""
        if scroll_type == "down":
            delay = random.uniform(500, 2000)
        elif scroll_type == "up":
            delay = random.uniform(400, 1500)
        else:  # smooth scroll
            delay = random.uniform(100, 300)

        return delay

    async def simulate_click_delay(self) -> float:
        """Simulate mouse click delays"""
        return random.uniform(50, 200)

    async def simulate_navigation_delay(self, difficulty: str = "medium") -> float:
        """Simulate page navigation delays"""
        if difficulty == "easy":
            delay = random.uniform(500, 1500)
        elif difficulty == "hard":
            delay = random.uniform(3000, 8000)
        else:
            delay = random.uniform(1000, 3000)

        return delay

    async def move_mouse_randomly(self, page_height: int, page_width: int, steps: int = 10) -> None:
        """
        Simulate random mouse movements across the page
        """
        if page_width == 0 or page_height == 0:
            return

        start_x = self.current_mouse_position[0]
        start_y = self.current_mouse_position[1]

        for _ in range(steps):
            # Generate random mouse position with boundary checks
            new_x = random.randint(max(0, start_x - 100), min(page_width - 1, start_x + 100))
            new_y = random.randint(max(0, start_y - 100), min(page_height - 1, start_y + 100))

            self.current_mouse_position = (new_x, new_y)
            self.mouse_positions.append(self.current_mouse_position)

            # Simulate mouse movement delay (random duration)
            await asyncio.sleep(random.uniform(10, 100))

    async def simulate_delay_with_variance(self, base_delay: float, variance: float = 0.5) -> float:
        """
        Simulate delay with random variance to avoid detection
        """
        delay = base_delay * random.uniform(1 - variance, 1 + variance)

        return delay

    async def simulate_reading_delay(self, text_length: int, difficulty: str = "medium") -> float:
        """
        Simulate reading delay (time spent on page before moving on)
        Reading speed: 200-300 words per minute
        """
        words_per_minute = random.choice([200, 250, 280, 300]) if difficulty == "easy" else random.choice([150, 180, 200, 220])
        reading_time = text_length / words_per_minute  # in minutes
        reading_time = min(reading_time, 5.0)  # Max 5 minutes

        return reading_time * 60  # Convert to seconds

    async def simulate_form_interaction_delay(self, field_type: str) -> float:
        """Simulate form field interaction delays"""
        field_type_lower = field_type.lower()

        if "search" in field_type_lower:
            delay = random.uniform(500, 1500)
        elif "input" in field_type_lower or "field" in field_type_lower:
            delay = random.uniform(100, 300)
        elif "button" in field_type_lower or "submit" in field_type_lower:
            delay = random.uniform(200, 500)
        else:
            delay = random.uniform(100, 300)

        return delay

    async def simulate_session_behavior(self, current_page_url: str, difficulty: str = "medium") -> float:
        """Simulate session-level behavior patterns"""
        if difficulty == "hard":
            # For hard difficulty, simulate more human-like behavior
            if "search" in current_page_url:
                # Search results: random delay
                delay = random.uniform(2000, 5000)
            elif "home" in current_page_url:
                # Homepage: longer delay
                delay = random.uniform(5000, 10000)
            else:
                # Other pages: medium delay
                delay = random.uniform(1000, 3000)
        else:
            # For easier difficulty, faster behavior
            delay = random.uniform(500, 2000)

        return delay

    async def simulate_exit_intent(self, difficulty: str = "medium") -> bool:
        """
        Simulate exit intent behavior
        5-10% chance of simulating exit intent
        """
        random_percent = random.random() * 100

        if difficulty == "hard":
            probability = 10
        elif difficulty == "easy":
            probability = 5
        else:
            probability = 7

        return random_percent < probability

    def get_behavior_config(self) -> Dict[str, Any]:
        """Get behavior simulation configuration"""
        return self.config.get("behavior_simulation", {
            "enable_random_delays": True,
            "enable_mouse_movements": False,
            "enable_scroll_patterns": True,
            "typing_variance": 0.5,
            "scroll_variance": 0.3,
        })