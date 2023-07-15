import os
from datetime import date

from pydantic import BaseModel, field_validator


class SuccessSchema(BaseModel):
    status: str


class FileSchema(BaseModel):
    file_name: str

    @field_validator('file_name')
    @classmethod
    def validate_date(cls, value):
        if value in os.listdir():
            return value
        raise ValueError('Unexisting file name')


class CargoCalcSchema(BaseModel):
    date: date
    cargo_type: str
    rate: float
    declared_value: float
    result: float


class CargoSchema(BaseModel):
    cargo_type: str
    declared_value: float
    date: date


class UploadCargo(BaseModel):
    cargo_type: str
    rate: float
    date: date
