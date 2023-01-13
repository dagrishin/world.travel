from typing import Mapping

from pydantic import UUID4


class DreamTripNotFound(Exception):
    pass


async def valid_dream_trip_id(dream_trip_id: UUID4) -> Mapping:
    dream_trip = await service.get_by_id(dream_trip_id)
    if not dream_trip:
        raise DreamTripNotFound()
    return dream_trip
