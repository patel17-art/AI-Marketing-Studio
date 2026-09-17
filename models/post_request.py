from dataclasses import dataclass
from typing import Optional


@dataclass
class PostRequest:
  topic: str
  post_type: str
  platform: str = "Instagram"
  educational_layout: Optional[str] = None