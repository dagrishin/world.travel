from datetime import datetime

from pydantic import BaseModel


class BookingCreate(BaseModel):
    start_date: datetime
    end_date: datetime
    user_id: str
    hotel_id: str = None
    restaurant_id: str = None
