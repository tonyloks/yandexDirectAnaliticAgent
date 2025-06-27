"""
Тесты для agent/agent.py (инициализация агента с OpenRouter и инструменты)
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from agent.agent import agent
import pytest

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
    resp = agent.run("Привет! Ты кто?")
    print("Ответ агента (объект):", resp)
    print("Текст ответа:", getattr(resp, "content", None))
    assert hasattr(resp, "content")
    assert resp.content, "Ответ агента пустой"
    assert isinstance(resp.content, str)
