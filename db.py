from typing import Union, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from fixtures import fixture_cars
from models.models import Car, FuelType, Transmission
from schema.schema import CarSchema, CarFilterSchema, CarUpdateSchema
from settings import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class DatabaseManager:
    def __init__(self):
        self.__session_local = SessionLocal
        self.__session = self.__session_local()

    @staticmethod
    def ___car_to_dict(car: Car) -> dict:
        attributes = [
            "id",
            "brand",
            "model",
            "year",
            "fuel_type",
            "transmission",
            "mileage",
            "price"
        ]

        result = {}
        for attr in attributes:
            # Проверяем наличие атрибута и его значение
            if hasattr(car, attr):
                value = getattr(car, attr)
                # Если атрибут является отношением (relationship), обрабатываем его соответственно
                if isinstance(value, (FuelType, Transmission)):
                    result[attr] = getattr(value, 'name', None)
                else:
                    result[attr] = str(value) if value is not None else None

        # Убираем ключи со значениями None
        result = {k: v for k, v in result.items() if v is not None}
        return result

    @staticmethod
    def __row_to_dict(row) -> dict:
        return {
            column.name: getattr(row, column.name) for column in row.__table__.columns
        }

    def add_car(self, car: CarSchema) -> Union[Car, None]:
        car_instance = Car(
            brand=car.brand,
            model=car.model,
            year=car.year,
            fuel_type_id=car.fuel_type_id,
            transmission_id=car.transmission_id,
            mileage=car.mileage,
            price=car.price,
        )

        try:
            self.__session.add(car_instance)  # Добавляем объект Car
            self.__session.commit()  # Сохраняем изменения
            return car_instance
        except Exception as e:
            print(f"Error adding car: {e}")
            self.__session.rollback()  # Откатываем изменения при ошибке

    def get_car_by_id(self, pk: int) -> Union[Car, None]:
        car_unprocessed = (
            self.__session.query(Car)
            .join(FuelType, Car.fuel_type_id == FuelType.id)
            .join(Transmission, Car.transmission_id == Transmission.id)
            .filter(Car.id == pk)
            .first()  # Используем first(), так как get() больше не поддерживается
        )
        if car_unprocessed:
            car_processed = self.___car_to_dict(car_unprocessed)
            return jsonable_encoder(car_processed)
        else:
            return None

    def update_car_by_id(self, car_id: int, updating_data: CarUpdateSchema) -> Optional[bool]:
        try:
            # Создание запроса на обновление
            stmt = (
                update(Car)
                .where(Car.id == car_id)
                .values(**updating_data.model_dump(exclude_unset=True))
                .returning(Car)
            )

            # Выполнение запроса
            result = self.__session.execute(stmt)
            updated_car = result.fetchone()

            if not updated_car:
                return None  # Возвращаем None, если машина не найдена

            self.__session.commit()  # Сохраняем изменения
            # unprocessed_update_car = self.__row_to_dict(updated_car)
            # return jsonable_encoder(unprocessed_update_car)  # Возвращаем обновленное представление машины
            return True

        except SQLAlchemyError as e:
            self.__session.rollback()  # Откатываем изменения при ошибке
            print(f"Error updating car: {e}")
            return None  # Возвращаем None при ошибке

    def get_car_by_parameters(self, page: int, page_size: int, car_filters: CarFilterSchema):
        query = select(Car)

        brand = car_filters.brand
        model = car_filters.model
        year = car_filters.year
        fuel_type_id = car_filters.fuel_type_id
        transmission_id = car_filters.transmission_id
        mileage_min = car_filters.mileage_min
        mileage_max = car_filters.mileage_max
        price_min = car_filters.price_min
        price_max = car_filters.price_max

        if mileage_min > mileage_max > 0:
            raise ValueError(
                "Минимальный пробег не может быть больше максимального."
            )
        if price_max > price_min > 0:
            raise ValueError("Минимальная цена не может быть больше максимальной.")

        if brand:
            query = query.filter(Car.brand == brand)
        if model:
            query = query.filter(Car.model == model)
        if year:
            query = query.filter(Car.year == year)
        if fuel_type_id:
            query = query.filter(Car.fuel_type_id == fuel_type_id)
        if transmission_id:
            query = query.filter(Car.transmission_id == transmission_id)
        if mileage_max:
            query = query.filter(Car.mileage.between(mileage_min, mileage_max))
        if price_max:
            query = query.filter(Car.price.between(price_min, price_max))
        if mileage_min > 0 and mileage_max == 0:
            query = query.filter(Car.mileage >= mileage_min)
        if price_min > 0 and price_max == 0:
            query = query.filter(Car.price >= price_min)

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = self.__session.execute(query).scalars().all()
        return [self.__row_to_dict(car) for car in result]

    def delete_car_by_id(self, pk):
        car_to_delete = self.__session.query(Car).get(pk)

        if car_to_delete:
            try:
                self.__session.delete(car_to_delete)
                self.__session.commit()
                return True
            except SQLAlchemyError as e:
                self.__session.rollback()
                print(f"Error deleting car: {e}")
                return False
        else:
            return False

    def __init_fuel_types(self) -> None:
        fuel_types = ["Бензин", "Дизель", "Электричество", "Гибрид"]

        for name in fuel_types:
            if not self.__session.query(FuelType).filter(FuelType.name == name).first():
                fuel_type = FuelType(name=name)
                self.__session.add(fuel_type)
        self.__session.commit()
        print("Типы топлива успешно загружены в бд.")

    def __init_transmission(self) -> None:
        transmissions = ["Механическая", "Автоматическая", "Вариатор", "Робот"]
        for name in transmissions:
            if (
                    not self.__session.query(Transmission)
                            .filter(Transmission.name == name)
                            .first()
            ):
                transmission = Transmission(name=name)
                self.__session.add(transmission)
        self.__session.commit()
        print("Передачи успешно загружены в бд.")

    def __init_cars(self) -> None:
        for car in fixture_cars:
            self.add_car(car)
        print('Машины успешно добавлены.')

    def init_fixtures(self):
        self.__init_fuel_types()
        self.__init_transmission()
        self.__init_cars()

    def __del__(self) -> None:
        self.__session.close_all()


db_manager = DatabaseManager()
