from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.session import get_async_db
from src.attractions import Attractions
from src.travel import Countries

attraction_router = APIRouter()


# # Endpoint for searching attractions in a city or country
# @attraction_router.route('/attractions/search', methods=['GET'])
# def search_attractions():
#     city = request.args.get('city')
#     country = request.args.get('country')
#     attractions = Attractions.query.filter(Attractions.city == city, Attractions.country == country).all()
#     return jsonify([attraction.to_dict() for attraction in attractions])
