"""
Агент Agno для работы с аккаунтами Яндекс.Директ (CRUD через db_tools).
"""
# region Импорты
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.db_tools import add_account, update_account_goals, get_account, delete_account, list_accounts
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
    description="Агент для управления аккаунтами Яндекс.Директ через CRUD-интерфейс.",
    markdown=True,
)
# endregion 