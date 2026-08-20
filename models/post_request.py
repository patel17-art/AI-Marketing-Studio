from dataclasses import dataclass


@dataclass
class PostRequest:
    topic: str
    post_type: str
    platform: str = "Instagram"