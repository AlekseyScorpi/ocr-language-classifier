from dataclasses import dataclass
import os

@dataclass(frozen=True)
class OCRConfig:
    tessdata_path: str
    fasttext_path: str

    @classmethod
    def load(cls) -> "OCRConfig":
        return cls(
            tessdata_path=os.getenv("TESSDATA_PATH", "./data/tessdata"),
            fasttext_path=os.getenv("FASTTEXT_PATH", "./data/models/lid.176.bin"),
        )