"""
Инструменты для работы с БД аккаунтов Яндекс.Директ (SQLite).
Создаёт таблицу direct_accounts при первом импорте.
Использует Pydantic для структурированных данных.
"""
# region Импорты
from typing import Optional, List
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field, field_validator, ValidationError
import re
from logger.logger_config import setup_logger  # импорт логгера
# endregion

# region Логгер
logger = setup_logger(__name__)
# endregion

# region Конфиг БД
DB_PATH = Path(__file__).parent.parent / 'database' / 'accounts.sqlite'
DB_PATH.parent.mkdir(exist_ok=True)
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False, future=True)
metadata = MetaData()
# endregion

# region Модели Pydantic
class Account(BaseModel):
    """
    Модель аккаунта Яндекс.Директ для хранения в БД.
    """
    id: Optional[int] = Field(
        default=None,
        description="Уникальный идентификатор записи.",
        json_schema_extra={"example": 1},
        ge=1
    )
    account_name: str = Field(
        ...,
        description="Имя аккаунта для обращения в чате.",
        json_schema_extra={"example": "my_yandex_account"},
        min_length=1,
        max_length=64
    )
    login: str = Field(
        ...,
        description="Логин пользователя в Яндексе.",
        json_schema_extra={"example": "user@yandex.ru"}
    )
    api_token: str = Field(
        ...,
        description="OAuth-токен для доступа к API.",
        json_schema_extra={"example": "AgAAAAABCD1234..."}
    )
    goal_ids: Optional[List[int]] = Field(
        default=None,
        description="Список ID целей Яндекс.Метрики (int, 8-14 цифр).",
        json_schema_extra={"example": [12345678, 98765432101234]}
    )

    @field_validator('goal_ids')
    @classmethod
    def validate_goal_ids(cls, v: Optional[List[int]]) -> Optional[List[int]]:
        if v is None:
            return v
        for goal in v:
            if not isinstance(goal, int) or not (10**7 <= goal < 10**14):
                raise ValueError('Каждый goal_id должен быть int длиной от 8 до 14 цифр')
        return v

class AccountNameList(BaseModel):
    """
    Список имён всех аккаунтов.
    """
    accounts: List[str] = Field(..., description="Список имён аккаунтов.")

class OperationResult(BaseModel):
    """
    Результат операции с аккаунтом.
    """
    success: bool = Field(..., description="True, если операция успешна.")
    message: str = Field(..., description="Сообщение о результате операции.")
# endregion

# region Таблица SQLAlchemy
direct_accounts = Table(
    'direct_accounts', metadata,
    Column('id', Integer, primary_key=True),
    Column('account_name', String, unique=True, nullable=False),
    Column('login', String, nullable=False),
    Column('api_token', String, nullable=False),
    Column('goal_ids', String, nullable=True),
)
metadata.create_all(engine)
# endregion

# region CRUD-функции
def add_account(account_name: str, login: str, api_token: str, goal_ids: Optional[List[int]] = None) -> OperationResult:
    """
    Добавляет новый аккаунт в БД.

    Args:
        account_name (str): Имя аккаунта для обращения в чате (уникальное).
        login (str): Логин пользователя в Яндексе.
        api_token (str): OAuth-токен для доступа к API.
        goal_ids (Optional[List[int]]): Список ID целей Яндекс.Метрики (int, 8-14 цифр).

    Returns:
        OperationResult: success=True, если аккаунт добавлен; success=False с сообщением об ошибке иначе.

    Raises:
        ValueError: Если goal_ids не проходят валидацию (через Pydantic).
    """
    if not goal_ids:
        logger.error(f"Ошибка: не указаны цели (goal_ids) для аккаунта '{account_name}'")
        return OperationResult(success=False, message="Не указаны цели (goal_ids) для аккаунта.")
    try:
        _ = Account(account_name=account_name, login=login, api_token=api_token, goal_ids=goal_ids)
    except ValidationError as e:
        logger.error(f"Ошибка валидации при добавлении аккаунта '{account_name}': {e.errors()[0]['msg']}")
        return OperationResult(success=False, message=f"Ошибка валидации: {e.errors()[0]['msg']}")
    goal_ids_str = None
    if goal_ids:
        goal_ids_str = ','.join(str(g) for g in goal_ids)
    with engine.begin() as conn:
        try:
            conn.execute(insert(direct_accounts).values(
                account_name=account_name,
                login=login,
                api_token=api_token,
                goal_ids=goal_ids_str
            ))
            logger.info(f"Аккаунт '{account_name}' успешно добавлен.")
            return OperationResult(success=True, message=f"Аккаунт '{account_name}' успешно добавлен.")
        except IntegrityError:
            logger.error(f"Ошибка: аккаунт с именем '{account_name}' уже существует.")
            return OperationResult(success=False, message=f"Ошибка: аккаунт с именем '{account_name}' уже существует.")

def update_account_goals(account_name: str, goal_ids: List[int]) -> OperationResult:
    """
    Обновляет список goal_ids для аккаунта.

    Args:
        account_name (str): Имя аккаунта для обновления.
        goal_ids (List[int]): Новый список ID целей (int, 8-14 цифр).

    Returns:
        OperationResult: success=True, если цели обновлены; success=False с сообщением об ошибке иначе.

    Raises:
        ValueError: Если goal_ids не проходят валидацию (через Pydantic).
    """
    try:
        _ = Account(account_name=account_name, login='stub', api_token='stub', goal_ids=goal_ids)
    except ValidationError as e:
        logger.error(f"Ошибка валидации целей для аккаунта '{account_name}': {e.errors()[0]['msg']}")
        return OperationResult(success=False, message=f"Ошибка валидации: {e.errors()[0]['msg']}")
    goal_ids_str = ','.join(str(g) for g in goal_ids) if goal_ids else None
    with engine.begin() as conn:
        result = conn.execute(update(direct_accounts).where(
            direct_accounts.c.account_name == account_name
        ).values(goal_ids=goal_ids_str))
        if result.rowcount:
            logger.info(f"Цели для аккаунта '{account_name}' обновлены.")
            return OperationResult(success=True, message=f"Цели для аккаунта '{account_name}' обновлены.")
        logger.warning(f"Аккаунт '{account_name}' не найден при обновлении целей.")
        return OperationResult(success=False, message=f"Аккаунт '{account_name}' не найден.")

def get_account(account_name: str) -> Optional[Account]:
    """
    Возвращает данные аккаунта по имени.

    Args:
        account_name (str): Имя аккаунта для поиска.

    Returns:
        Optional[Account]: Экземпляр Account, если найден; иначе None.
    """
    with engine.begin() as conn:
        result = conn.execute(select(direct_accounts).where(
            direct_accounts.c.account_name == account_name
        )).mappings().first()
        if not result:
            return None
        # goal_ids: str -> List[int]
        goal_ids = result['goal_ids']
        if goal_ids:
            goal_ids_list = [int(g) for g in goal_ids.split(',') if g.strip()]
        else:
            goal_ids_list = None
        return Account(
            id=result['id'],
            account_name=result['account_name'],
            login=result['login'],
            api_token=result['api_token'],
            goal_ids=goal_ids_list
        )

def delete_account(account_name: str) -> OperationResult:
    """
    Удаляет аккаунт по имени.

    Args:
        account_name (str): Имя аккаунта для удаления.

    Returns:
        OperationResult: success=True, если аккаунт удалён; success=False с сообщением об ошибке иначе.
    """
    with engine.begin() as conn:
        result = conn.execute(delete(direct_accounts).where(
            direct_accounts.c.account_name == account_name
        ))
        if result.rowcount:
            logger.info(f"Аккаунт '{account_name}' удалён.")
            return OperationResult(success=True, message=f"Аккаунт '{account_name}' удалён.")
        logger.warning(f"Аккаунт '{account_name}' не найден при удалении.")
        return OperationResult(success=False, message=f"Аккаунт '{account_name}' не найден.")

def list_accounts() -> AccountNameList:
    """
    Возвращает список имён всех аккаунтов.

    Returns:
        AccountNameList: Список имён всех аккаунтов.
    """
    with engine.begin() as conn:
        result = conn.execute(select(direct_accounts.c.account_name))
        accounts = [row[0] for row in result]
        logger.info(f"Получен список аккаунтов: {accounts}")
        return AccountNameList(accounts=accounts) 