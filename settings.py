import os

from dotenv import load_dotenv
from fastapi_sa_orm_filter.operators import Operators as ops


class Settings:
    def __init__(self):
        load_dotenv()

        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.car_filter_fields = {
            "mark": [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
            "model": [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
            "year": [ops.eq],
            "fuel_type_id": [ops.eq],
            "transmission_id": [ops.eq],
            "mileage": [ops.eq, ops.between],
            "price": [ops.eq, ops.between],
        }


settings = Settings()
