from fastapi import APIRouter, Depends

from app.lendings.dao import LendingDAO
from app.lendings.schemas import SLending, SLendBook
from app.users.dependencies import get_current_admin
from app.users.models import User
from app.mock_data.load_mock_data import load_mock_data

router = APIRouter(
    prefix="/mock_data",
    tags=["Загрузка тестовых данных"],
)


@router.post("", status_code=201)
async def load_mock_data_from_csv_files():
    await load_mock_data()
    return "Тестовые данные успешно загружены"
