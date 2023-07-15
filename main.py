import json
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException

from database import connect_database
from models import Cargo
from schemas import (
    CargoCalcSchema,
    CargoSchema,
    FileSchema,
    UploadCargo
)


app = FastAPI(
    title='Cargo'
)


@app.post(
    '/load-cargo-rate',
    description='Load cargo rate',
    status_code=201,
    response_model=List[UploadCargo]
)
async def upload(file_data: FileSchema):
    """ Функция принимает file_data, в которой указано название json файла. """

    with open(file_data.file_name, 'r') as file:
        convert_to_json = json.loads(file.read())
        for date_key in convert_to_json:
            try:
                date = datetime.strptime(date_key, '%Y-%m-%d')
                for item in convert_to_json[date_key]:
                    item['date'] = date
                    data = UploadCargo(**item)
                    await Cargo.get_or_create(
                        cargo_type=data.cargo_type,
                        rate=data.rate,
                        date=data.date
                    )
                return [cargo for cargo in await Cargo.all()]
            except ValueError:
                raise HTTPException(status_code=400, detail='Please specify a valid date!')


@app.get('/', response_model=CargoCalcSchema)
async def calc(cargo_data: CargoSchema):
    new_date = datetime.strptime(
        f'{cargo_data.date.year}-{cargo_data.date.month}-01',
        '%Y-%m-%d'
    )
    cargo = await Cargo.get_or_none(cargo_type__icontains=cargo_data.cargo_type, date=new_date)
    if cargo is not None:
        result = cargo_data.declared_value * cargo.rate
        data = {
            'date': cargo_data.date,
            'cargo_type': cargo.cargo_type,
            'rate': cargo.rate,
            'declared_value': cargo_data.declared_value,
            'result': result
        }
        return data
    raise HTTPException(
        status_code=404,
        detail=f'Cargo with `cargo_type={cargo_data.cargo_type}`, `date={cargo_data.date}` not found!'
    )


connect_database(app)
