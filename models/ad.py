from dataclasses import dataclass, asdict
from typing import Optional, Literal
from datetime import datetime

AdType = Literal['text', 'photo', 'audio', 'voice']

@dataclass
class Ad:
    id: int
    user_id: int
    type: AdType
    content: Optional[str] = None      # for text
    file_id: Optional[str] = None      # for media
    caption: Optional[str] = None
    likes: int = 0
    created_at: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
            d["created_at"] = self.created_at
        return d
