from typing import Optional

from pydantic import BaseModel


class Interaction(BaseModel):
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    user_message: str
    bot_response: str
