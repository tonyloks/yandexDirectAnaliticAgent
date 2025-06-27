"""
Агент Agno для работы с аккаунтами Яндекс.Директ (CRUD через db_tools).
"""
# region Импорты
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.db_tools import add_account, update_account_goals, get_account, delete_account, list_accounts
from agent.prompt import SYSTEM_PROMPT
# endregion

# region Инициализация агента
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
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