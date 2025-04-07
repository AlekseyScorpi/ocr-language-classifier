from dataclasses import dataclass
import os

@dataclass
class BotConfig:
    token: str

    @staticmethod
    def load():
        return BotConfig(
            token=os.getenv("BOT_TOKEN", "your_token_here"),
        )