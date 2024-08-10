from sqlalchemy import Column, String, DATE, INTEGER, ForeignKey, NUMERIC
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    """Базовая модель."""

    pass


class BaseModel(Base):
    __abstract__ = True

    id = Column(INTEGER, primary_key=True, autoincrement=True)


class Car(BaseModel):
    __tablename__ = "cars"

    brand = Column(String)
    model = Column(String)
    year = Column(INTEGER)
    fuel_type_id = Column(INTEGER, ForeignKey("fuel_type.id"))
    transmission_id = Column(INTEGER, ForeignKey("transmission.id"))
    mileage = Column(NUMERIC(10, 2))
    price = Column(NUMERIC(7, 2))

    fuel_type = relationship("FuelType", back_populates="car")
    transmission = relationship("Transmission", back_populates="car")

    def as_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "fuel_type_id": self.fuel_type_id,
            "transmission_id": self.transmission_id,
            "mileage": self.mileage,
            "price": self.price,
        }

    def __repr__(self):
        return f"<Car(brand={self.brand}, model={self.model}, year={self.year})>"


class FuelType(BaseModel):
    __tablename__ = "fuel_type"

    name = Column(String)

    car = relationship("Car", back_populates="fuel_type", uselist=True)

    def __repr__(self):
        return f"<FuelType(name={self.name})>"


class Transmission(BaseModel):
    __tablename__ = "transmission"

    name = Column(String)

    car = relationship("Car", back_populates="transmission", uselist=True)

    def __repr__(self):
        return f"<Transmission(name={self.name})>"
