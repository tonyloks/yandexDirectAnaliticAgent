"""
Тесты для tools/db_tools.py (работа с аккаунтами Яндекс.Директ)
"""
# region Импорты
import pytest
from pathlib import Path
from sqlalchemy import create_engine, MetaData
from tools import db_tools
from tools.db_tools import add_account, update_account_goals, get_account, delete_account, list_accounts, Account, OperationResult
import shutil
import os
# endregion

# region Фикстуры
@pytest.fixture(scope="function")
def temp_db(monkeypatch, tmp_path):
    """
    Создаёт временную БД для каждого теста и подменяет путь в db_tools.
    """
    db_file = tmp_path / "test_accounts.sqlite"
    engine = create_engine(f"sqlite:///{db_file}", echo=False, future=True)
    metadata = db_tools.metadata
    metadata.create_all(engine)
    monkeypatch.setattr(db_tools, "engine", engine)
    yield db_file
    # cleanup не нужен: tmp_path сам очищается
# endregion

# region Тесты
class TestDBTools:
    def test_add_and_get_account(self, temp_db):
        res = add_account("test1", "login1", "token1", [12345678, 87654321])
        assert res.success
        acc = get_account("test1")
        assert acc is not None
        assert acc.account_name == "test1"
        assert acc.login == "login1"
        assert acc.api_token == "token1"
        assert acc.goal_ids == [12345678, 87654321]

    def test_add_account_duplicate(self, temp_db):
        add_account("test2", "login2", "token2")
        res = add_account("test2", "login2", "token2")
        assert not res.success
        assert "уже существует" in res.message

    def test_update_account_goals(self, temp_db):
        add_account("test3", "login3", "token3")
        res = update_account_goals("test3", [11111111, 22222222])
        assert res.success
        acc = get_account("test3")
        assert acc.goal_ids == [11111111, 22222222]

    def test_update_account_goals_invalid(self, temp_db):
        add_account("test4", "login4", "token4")
        res = update_account_goals("test4", [1, 2])
        assert not res.success
        assert "Ошибка валидации" in res.message

    def test_delete_account(self, temp_db):
        add_account("test5", "login5", "token5")
        res = delete_account("test5")
        assert res.success
        acc = get_account("test5")
        assert acc is None

    def test_delete_account_not_found(self, temp_db):
        res = delete_account("not_exist")
        assert not res.success
        assert "не найден" in res.message

    def test_list_accounts(self, temp_db):
        add_account("a1", "l1", "t1")
        add_account("a2", "l2", "t2")
        names = list_accounts().accounts
        assert set(names) == {"a1", "a2"}
# endregion 