# LLM Агент для Яндекс.Директ на базе Agno

## Описание
Интеллектуальный ассистент для управления аккаунтами Яндекс.Директа и получения статистики через диалог на естественном языке. Веб-интерфейс на Streamlit.

## Структура проекта
```
yandexDirectAnaliticAgent/
├── agent/         # Логика и состояние агента
├── database/      # SQLite база аккаунтов (accounts.sqlite)
├── logger/        # Конфиг логгера
├── logs/          # Логи с ротацией
├── main.py        # Запуск Streamlit-приложения
├── requirements.txt
├── tools/         # Инструменты для работы с БД и API Яндекс.Директа
```

## Быстрый старт
1. Установить [uv](https://github.com/astral-sh/uv):
   ```bash
   pip install uv
   ```
2. Создать и активировать виртуальное окружение:
   ```bash
   uv venv
   .venv/Scripts/activate  # Windows
   # или
   source .venv/bin/activate  # Linux/Mac
   ```
3. Установить зависимости:
   ```bash
   uv pip install -r requirements.txt
   ```
4. Запустить приложение:
   ```bash
   streamlit run main.py
   ```

## Зависимости
- agno
- streamlit
- sqlalchemy
- python-dotenv
- requests
- pydantic
- pytest (для тестов)

## Тесты
- Тесты лежат в папке `tests/` и повторяют структуру проекта.
- Запуск:
  ```bash
  pytest
  ```

## Конфиденциальные данные
- Все секреты (API-ключи) хранятся в `.env` (не коммитить в git).

## Логи
- Все логи пишутся в папку `logs/` с ротацией по 500 КБ.

---

## Описание папок

### agent/
- `main_agent.py` — логика агента Agno
- `agent_state.py` — состояние и входящие сообщения

### database/
- `accounts.sqlite` — база аккаунтов (автоматически создаётся)

### logger/
- `logger_config.py` — настройка логгера

### logs/
- Логи работы приложения

### tools/
- `db_tools.py` — инструменты для работы с БД
- `yandex_direct_tools.py` — инструменты для работы с API Яндекс.Директа 