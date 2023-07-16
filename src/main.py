import json
from datetime import datetime, date
from typing import List

from tortoise.contrib.fastapi import register_tortoise

from fastapi import FastAPI, HTTPException, File, UploadFile

from src.settings import DATABASE_CONFIG
from src.cargo.models import Cargo
from src.cargo.schemas import (
    CargoCalcSchema,
    UploadCargo
)


app = FastAPI(
    title='Cargo'
)


@app.post(
    '/load-cargo-rate/',
    description='Load cargo rate',
    status_code=201,
    response_model=List[UploadCargo]
)
async def upload(file: UploadFile = File()):
    """ Функция принимает file_data, в которой указано название json файла. """
    json_file = json.loads(await file.read())
    for date_key in json_file:
        try:
            _date = datetime.strptime(date_key, '%Y-%m-%d')
            for item in json_file[date_key]:
                item['date'] = _date
                cargo_scheme = UploadCargo(**item)
                await Cargo.get_or_create(
                    cargo_type=cargo_scheme.cargo_type,
                    rate=cargo_scheme.rate,
                    date=cargo_scheme.date
                )
        except ValueError:
            raise HTTPException(status_code=400, detail='Please check json file!')
    return [cargo for cargo in await Cargo.all()]


@app.get('/cargo', response_model=CargoCalcSchema)
async def calc(cargo_type: str = None, current_date: date = None, declared_value: float = None):
    status = 400
    msg = 'cargo_type, current_date and declared_value are required query params'
    if all([cargo_type, current_date, declared_value]):
        new_date = datetime.strptime(
            f'{current_date.year}-{current_date.month}-01',
            '%Y-%m-%d'
        )
        cargo = await Cargo.get_or_none(cargo_type__icontains=cargo_type, date=new_date)
        if cargo is not None:
            result = declared_value * cargo.rate
            data = {
                'date': current_date,
                'cargo_type': cargo.cargo_type,
                'rate': cargo.rate,
                'declared_value': declared_value,
                'result': result
            }
            return data
        status = 404
        msg = f'Cargo with `cargo_type={cargo_type}`, `date={current_date}` not found!'
    raise HTTPException(
        status_code=status,
        detail=msg
    )

register_tortoise(
        app=app,
        config=DATABASE_CONFIG
    )
