# Task Manager - Менеджер задач

Веб-приложение для управления задачами

##  Возможности

-  Создание, чтение, обновление и удаление задач
-  Статусы задач: новая, в работе, выполнена
-  Приоритеты: низкий, средний, высокий
-  Установка дедлайнов
-  Фильтрация задач по статусу
-  Статистика по задачам
-  REST API с автоматической документацией Swagger

##  Технологии

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM для работы с базой данных
- **SQLite** - база данных
- **Jinja2** - шаблонизатор для HTML
- **Bootstrap 5** - CSS фреймворк
- **Pydantic** - валидация данных

##  Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/Jeko1J/task-manager.git
cd task-manager
```

### 2. Запуск приложения в терминале Pycharm
```bash
uvicorn app.main:app --reload
```
### 3. Открыть в браузере
- Веб-интерфейс: http://localhost:8000
- API документация: http://localhost:8000/docs

##  Интерфейс приложения
<img width="1384" height="736" alt="изображение" src="https://github.com/user-attachments/assets/bf2dc68d-be07-467c-bd70-43d6323fd1e3" />
<img width="901" height="712" alt="изображение" src="https://github.com/user-attachments/assets/936daf00-17e4-404b-867f-fc9fa7246fd5" />
