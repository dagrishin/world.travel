from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.session import get_async_db
from src.travel import Countries

travel_router = APIRouter()


@travel_router.get("/countries/{country_id}")
async def read_country(country_id: int, db: AsyncSession = Depends(get_async_db)):
    query = select(Countries).where(Countries.id == country_id)
    countries = await db.execute(query)
    (country,) = countries.first()
    return country.to_dict()
