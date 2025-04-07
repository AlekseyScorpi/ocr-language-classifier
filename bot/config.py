from dataclasses import dataclass
import os

@dataclass
class BotConfig:
    token: str
    ocr_model_path: str
    fasttext_model_path: str
    tessdata_dir: str

    @staticmethod
    def load():
        return BotConfig(
            token=os.getenv("BOT_TOKEN", "your_token_here"),
            ocr_model_path="./models", 
            fasttext_model_path="./models/lid.176.bin",
            tessdata_dir="./models/tessdata"
        )