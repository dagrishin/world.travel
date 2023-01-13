from datetime import datetime

from pydantic import BaseModel


class TrackCreate(BaseModel):
    title: str
    start_date: datetime
    end_date: datetime
    user_id: str
