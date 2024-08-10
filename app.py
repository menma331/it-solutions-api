from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, JSONResponse

from db import db_manager
from schema.schema import CarSchema, CarFilterSchema, CarUpdateSchema

app = FastAPI()


@app.get("/")
async def get_hello_message() -> HTMLResponse:
    return HTMLResponse(
        "<h3>Привет !</h3>"
        '<p>Это результат выполнения тестового задания от <a href="https://www.linkedin.com/in/sysa-roman/">Романа Алексеевича</a>. '
        'Перейдите по <a href="/docs">ссылке</a>, чтобы ознакомиться с документацией.</p>'
    )


@app.get("/car")
async def get_car_by_id(pk: int) -> JSONResponse:
    car = db_manager.get_car_by_id(pk)
    if car:
        return JSONResponse(content={"car": car}, status_code=200)
    else:
        return JSONResponse(
            content={"message": "Машина не найдена."}, status_code=404
        )


@app.post("/add_car")
async def add_car(car: Annotated[dict, Depends(CarSchema)]) -> dict:
    car_instance = db_manager.add_car(car)
    if car_instance:
        return {
            "message": "Машина успешно добавлена.",
            "car": car_instance,
        }
    else:
        return {"message": "Ошибка при добавлении машины."}


@app.post("/car_filter")
async def get_car_by_parameters(
        page: int, page_size: int,
        car_filters: CarFilterSchema,
):
    if page < 1 or page_size < 1:
        return JSONResponse(
            content={"error": {"message": "Номер страницы и размер страницы должны быть положительными числами."}},
            status_code=400,
        )
    try:
        result = db_manager.get_car_by_parameters(page, page_size, car_filters)
        return result
    except ValueError:
        return JSONResponse(content={"error": {"message": "Проверьте, что минимальное значение не превышает максимального."}}, status_code=400)


@app.patch('/update_car')
async def update_car(car_id: int, updating_car: CarUpdateSchema):
    is_updated_car = db_manager.update_car_by_id(car_id, updating_car)
    if is_updated_car:
        return JSONResponse(
            content={
                'message': f'Машина с id {car_id} обновлена.'
            }, status_code=200
        )

    return JSONResponse(content={'message': f'Машина с id {car_id} не найдена.'}, status_code=404)


@app.delete('/delete_car')
async def delete_car_by_id(pk: int):
    car_is_delete = db_manager.delete_car_by_id(pk)
    if car_is_delete:
        return JSONResponse(
            content={
                'message': f'Машина с id {pk} удалена.'
            }, status_code=200
        )
    return JSONResponse(content={'message': f'Машина с id {pk} не найдена.'}, status_code=404)