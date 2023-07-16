from datetime import date

from pydantic import BaseModel


class CargoCalcSchema(BaseModel):
    date: date
    cargo_type: str
    rate: float
    declared_value: float
    result: float


class UploadCargo(BaseModel):
    cargo_type: str
    rate: float
    date: date
