import datetime
import os
from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.cargo.models import Cargo


@pytest.mark.asyncio
async def test_upload_without_file(client: AsyncClient):
    msg = 'Field required'
    loc = 'file'
    cargo_count = await Cargo.all().count()
    response = await client.post('/load-cargo-rate/')
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == msg
    assert loc in response.json()['detail'][0]['loc']
    assert await Cargo.all().count() == cargo_count


async def make_upload_with_invalid_json_file(client, file_name, script_dir):
    cargo_count = await Cargo.all().count()
    with open(os.path.join(script_dir, file_name), 'rb') as file:
        response = await client.post('/load-cargo-rate/', files={'file': (file_name, file)})
        assert response.status_code == HTTPStatus.BAD_REQUEST
    assert cargo_count == await Cargo.all().count()


@pytest.mark.asyncio
async def test_upload_invalid_date_file(client: AsyncClient):
    script_dir = os.path.dirname(__file__)
    file_name = 'test_invalid_date.json'
    await make_upload_with_invalid_json_file(client, file_name, script_dir)


@pytest.mark.asyncio
async def test_upload_invalid_cargo_type_file(client: AsyncClient):
    script_dir = os.path.dirname(__file__)
    file_name = 'test_invalid_cargo_type.json'
    await make_upload_with_invalid_json_file(client, file_name, script_dir)


@pytest.mark.asyncio
async def test_upload_valid_file(client: AsyncClient):
    script_dir = os.path.dirname(__file__)
    file_name = 'test_valid.json'
    cargo_count = await Cargo.all().count()
    with open(os.path.join(script_dir, file_name), 'rb') as file:
        response = await client.post('/load-cargo-rate/', files={'file': (file_name, file)})
        assert response.status_code == HTTPStatus.CREATED
    assert cargo_count + 4 == await Cargo.all().count()
    await Cargo.all().delete()


@pytest.mark.asyncio
async def test_get_unexisting_data(client: AsyncClient):
    unexisting_cargo_type = {
        "cargo_type": "test",
        "current_date": "2020-06-02",
        "declared_value": "100"
    }
    msg = f'Cargo with `cargo_type={unexisting_cargo_type["cargo_type"]}`, `date={unexisting_cargo_type["current_date"]}` not found!'
    response = await client.get('/cargo', params=unexisting_cargo_type)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == msg

    unexisting_date = {
        "cargo_type": "glass",
        "current_date": "2020-05-02",
        "declared_value": "100"
    }
    msg = f'Cargo with `cargo_type={unexisting_date["cargo_type"]}`, `date={unexisting_date["current_date"]}` not found!'
    response = await client.get('/cargo', params=unexisting_date)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == msg


@pytest.mark.asyncio
async def test_get_cargo_with_incorrect_data(client: AsyncClient):
    incorrect_declared_value = {
        "cargo_type": "glass",
        "current_date": "2020-06-02",
        "declared_value": "sto"
    }
    response = await client.get('/cargo', params=incorrect_declared_value)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    incorrect_current_date = {
        "cargo_type": "glass",
        "current_date": "date",
        "declared_value": "100"
    }
    response = await client.get('/cargo', params=incorrect_current_date)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    incorrect_cargo_type = {
        'cargo_type': 111,
        "current_date": '2020-06-02',
        'declared_value': 'sto'
    }
    response = await client.get('/cargo', params=incorrect_cargo_type)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_cargo(client: AsyncClient):
    cargo = await Cargo.create(
        cargo_type='Test',
        date=datetime.date(2020, 6, 1),
        rate=0.045
    )
    params = {
        'cargo_type': 'test',
        'current_date': '2020-06-15',
        'declared_value': 100
    }
    response = await client.get('/cargo', params=params)
    assert response.status_code == HTTPStatus.OK
    calc = cargo.rate * params['declared_value']
    assert response.json()['result'] == calc
