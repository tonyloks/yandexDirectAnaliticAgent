"""
Тесты для agent/agent.py (инициализация агента с OpenRouter и инструменты)
"""
import sys
import os
import sqlite3
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from agent.agent import agent

@pytest.fixture(autouse=True)
def clear_accounts_table():
    """Очищает таблицу direct_accounts перед каждым тестом."""
    db_path = os.path.join(os.path.dirname(__file__), '../../database/accounts.sqlite')
    conn = sqlite3.connect(db_path)
    try:
        conn.execute('DELETE FROM direct_accounts')
        conn.commit()
    finally:
        conn.close()

def test_openrouter_api_key_loaded():
    """Проверяет, что OPENROUTER_API_KEY подгружается из окружения."""
    assert os.getenv("OPENROUTER_API_KEY"), "OPENROUTER_API_KEY не найден в окружении"

def test_agent_model_type():
    """Проверяет, что агент использует OpenRouter как модель."""
    assert agent.model.__class__.__name__ == "OpenRouter"
    assert hasattr(agent.model, "api_key")

def test_agent_tools():
    """Проверяет, что у агента есть все необходимые инструменты."""
    tool_names = {t.__name__ for t in agent.tools}
    assert {"add_account", "update_account_goals", "get_account", "delete_account", "list_accounts"}.issubset(tool_names)

@pytest.mark.skipif(os.getenv("CI") == "true", reason="Пропускать в CI без ключа и внешнего API")
def test_agent_model_responds():
    """Проверяет, что агент отвечает на простой запрос."""
    resp = agent.run("Привет! Ты кто?")
    print("Текст ответа:", getattr(resp, "content", None))
    assert hasattr(resp, "content")
    assert resp.content, "Ответ агента пустой"
    assert isinstance(resp.content, str)

@pytest.mark.skipif(os.getenv("CI") == "true", reason="Пропускать в CI без ключа и внешнего API")
def test_agent_add_account_via_prompt():
    """Проверяет добавление аккаунта через промпт к агенту."""
    prompt = (
        "Добавь аккаунт с именем 'pytest_user', логином 'pytest_login', токеном 'pytest_token', целями 12345678, 87654321."
    )
    resp = agent.run(prompt)
    print("[ADD_ACCOUNT] Текст ответа:", getattr(resp, "content", None))
    assert hasattr(resp, "content")
    assert resp.content, "Ответ агента пустой"
    # Проверяем, что в ответе есть подтверждение или сообщение об ошибке
    assert (
        "добавлен" in resp.content.lower()
        or "уже существует" in resp.content.lower()
        or "успешно" in resp.content.lower()
    )

@pytest.mark.skipif(os.getenv("CI") == "true", reason="Пропускать в CI без ключа и внешнего API")
def test_agent_list_accounts_via_prompt():
    """Проверяет получение списка аккаунтов через промпт к агенту (добавление тоже через промпт)."""
    prompt1 = "Добавь аккаунт с именем 'pytest_user1', логином 'login1', токеном 'token1', целями 12345678."
    prompt2 = "Добавь аккаунт с именем 'pytest_user2', логином 'login2', токеном 'token2', целями 87654321."
    resp1 = agent.run(prompt1)
    print("[ADD_ACCOUNT_1] Текст ответа:", getattr(resp1, "content", None))
    resp2 = agent.run(prompt2)
    print("[ADD_ACCOUNT_2] Текст ответа:", getattr(resp2, "content", None))
    prompt = "Покажи список всех аккаунтов."
    resp = agent.run(prompt)
    print("[LIST_ACCOUNTS] Текст ответа:", getattr(resp, "content", None))
    assert hasattr(resp, "content")
    assert resp.content, "Ответ агента пустой"
    # Проверяем, что оба аккаунта есть в ответе
    assert "pytest_user1" in resp.content
    assert "pytest_user2" in resp.content

@pytest.mark.skipif(os.getenv("CI") == "true", reason="Пропускать в CI без ключа и внешнего API")
def test_agent_update_account_goals_via_prompt():
    """Проверяет обновление целей аккаунта через промпт к агенту."""
    # Сначала добавим аккаунт через промпт
    agent.run("Добавь аккаунт с именем 'pytest_user', логином 'login', токеном 'token', целями 12345678.")
    # До обновления
    resp_before = agent.run("Покажи данные аккаунта 'pytest_user'.")
    print("[BEFORE_UPDATE] Текст ответа:", getattr(resp_before, "content", None))
    prompt = "Обнови цели аккаунта 'pytest_user' на 87654321, 22222222."
    resp = agent.run(prompt)
    print("[UPDATE] Текст ответа:", getattr(resp, "content", None))
    # После обновления
    resp_after = agent.run("Покажи данные аккаунта 'pytest_user'.")
    print("[AFTER_UPDATE] Текст ответа:", getattr(resp_after, "content", None))
    assert hasattr(resp, "content")
    assert resp.content, "Ответ агента пустой"

@pytest.mark.skipif(os.getenv("CI") == "true", reason="Пропускать в CI без ключа и внешнего API")
def test_agent_get_account_via_prompt():
    """Проверяет получение информации об аккаунте через промпт к агенту."""
    agent.run("Добавь аккаунт с именем 'pytest_user', логином 'login', токеном 'token', целями 12345678.")
    prompt = "Покажи данные аккаунта 'pytest_user'."
    resp = agent.run(prompt)
    print("[GET_ACCOUNT] Текст ответа:", getattr(resp, "content", None))
    assert hasattr(resp, "content")
    assert resp.content, "Ответ агента пустой"
    assert "pytest_user" in resp.content and "login" in resp.content

@pytest.mark.skipif(os.getenv("CI") == "true", reason="Пропускать в CI без ключа и внешнего API")
def test_agent_delete_account_via_prompt():
    """Проверяет удаление аккаунта через промпт к агенту."""
    agent.run("Добавь аккаунт с именем 'pytest_user', логином 'login', токеном 'token', целями 12345678.")
    prompt = "Удалить аккаунт 'pytest_user'."
    resp = agent.run(prompt)
    print("[DELETE_ACCOUNT] Текст ответа:", getattr(resp, "content", None))
    assert hasattr(resp, "content")
    assert resp.content, "Ответ агента пустой"
