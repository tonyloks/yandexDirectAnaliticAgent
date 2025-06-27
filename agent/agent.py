"""
Агент Agno для работы с аккаунтами Яндекс.Директ (CRUD через db_tools).
"""
# region Импорты
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from tools.db_tools import add_account, update_account_goals, get_account, delete_account, list_accounts
from agent.prompt import SYSTEM_PROMPT
import os
from dotenv import load_dotenv
# endregion

# region Инициализация агента
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY не найден в .env")

agent = Agent(
    model=OpenRouter(id="google/gemini-2.5-flash", api_key=OPENROUTER_API_KEY),
    tools=[
        add_account,
        update_account_goals,
        get_account,
        delete_account,
        list_accounts,
    ],
    description=SYSTEM_PROMPT,
    markdown=True,
)
# endregion 