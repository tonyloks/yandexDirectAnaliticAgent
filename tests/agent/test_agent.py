"""
Тесты для agent/agent.py (инициализация агента с OpenRouter и инструменты)
"""
import os
import pytest
from agent import agent

def test_openrouter_api_key_loaded():
    """Проверяет, что OPENROUTER_API_KEY подгружается из окружения."""
    assert os.getenv("OPENROUTER_API_KEY"), "OPENROUTER_API_KEY не найден в окружении"

def test_agent_model_type():
    """Проверяет, что агент использует OpenRouter как модель."""
    assert agent.agent.model.__class__.__name__ == "OpenRouter"
    assert hasattr(agent.agent.model, "api_key")

def test_agent_tools():
    """Проверяет, что у агента есть все необходимые инструменты."""
    tool_names = {t.__name__ for t in agent.agent.tools}
    assert {"add_account", "update_account_goals", "get_account", "delete_account", "list_accounts"}.issubset(tool_names)

@pytest.mark.skipif(os.getenv("CI") == "true", reason="Пропускать в CI без ключа и внешнего API")
def test_agent_model_responds():
    """Проверяет, что агент отвечает на простой запрос."""
    resp = agent.agent.run("Привет! Ты кто?")
    assert resp, "Ответ агента пустой"
    assert isinstance(resp, str)

# Тесты инструментов напрямую (без LLM)
def test_add_account():
    res = agent.add_account("test_acc", "login_acc", "token_acc", [12345678])
    assert hasattr(res, "success")
    assert res.success or "уже существует" in res.message

def test_update_account_goals():
    res = agent.update_account_goals("test_acc", [87654321])
    assert hasattr(res, "success")
    # Может быть не найден, если не добавлен
    assert res.success or "не найден" in res.message

def test_get_account():
    acc = agent.get_account("test_acc")
    # Может быть None, если не добавлен
    assert acc is None or acc.account_name == "test_acc"

def test_list_accounts():
    res = agent.list_accounts()
    assert hasattr(res, "accounts")
    assert isinstance(res.accounts, list)

def test_delete_account():
    res = agent.delete_account("test_acc")
    assert hasattr(res, "success")
    # Может быть не найден, если уже удалён
    assert res.success or "не найден" in res.message

# Можно добавить тест на базовый ответ, если есть stub/mock окружение для OpenRouter
# def test_agent_basic_response():
#     resp = agent.agent.run("Привет!")
#     assert isinstance(resp, str) 