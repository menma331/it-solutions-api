from typing import Union, Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field


class CarSchema(BaseModel):
    id: Optional[Union[int, None]] = None
    brand: str = Field()
    model: str = Field()
    year: int
    fuel_type_id: int
    transmission_id: int
    mileage: float
    price: float

    class Config:
        from_attributes = True


class CarUpdateSchema(BaseModel):
    brand: str = Field(default=None)
    model: str = Field(default=None)
    year: int = Field(default=None)
    fuel_type_id: int = Field(default=None)
    transmission_id: int = Field(default=None)
    mileage: float = Field(default=None)
    price: float = Field(default=None)


class CarFilterSchema(Filter):
    brand: Optional[Union[str, None]] = Field(default=None)
    model: Optional[Union[str, None]] = Field(default=None)
    year: Optional[Union[int, None]] = Field(default=0, gt=1930)
    fuel_type_id: Optional[Union[int, None]] = Field(default=None)
    transmission_id: Optional[Union[int, None]] = Field(default=None)
    mileage_min: Optional[Union[float, None]] = Field(default=0, ge=0)
    mileage_max: Optional[Union[float, None]] = Field(default=0, ge=0)
    price_min: Optional[Union[float, None]] = Field(default=0, ge=0)
    price_max: Optional[Union[float, None]] = Field(default=0, ge=0)

    class Config:
        from_attributes = True


class FuelTypeSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class TransmissionSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
