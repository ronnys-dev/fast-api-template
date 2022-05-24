# Структура проекта

Данный проект следует принципам чистой архитектуры. Бизнес-логика не зависит
от веб-фреймворков, баз данных и любых других технологий напрямую.

У нас есть 3 основных модуля, у которых
строжайшим образом разделены зоны ответственности:

| Название модуля  | Зона ответственности     |
|------------------|--------------------------|
| `domain`         | Бизнес-логика            |
| `repository`     | Имплементации сервисов   |
| `application`    | Точки входа в приложение |

## Борьба с внешними зависимостями в слое бизнес-логики

Сценарии бизнес-логики зависят от интерфейсов различных сервисов, что позволяет
для различных точек входа указывать разные реализации этих сервисов.

Вы можете взглянуть на создание DI контейнера
[application/common/container.py](backend/application/common/container.py)
и его использование в файле
[application/web/product/api.py](backend/application//web/product/api.py).

### Локальный запуск:

Обычный запуск:
- <code>pre-commit install</code>
- <code>pip install mypy</code> (установить расширение для PyCharm, запуск через <code>make beauty</code>)
- cd backend
- <code>poetry install</code>
- <code>poetry shell</code>
- <code>python main.py</code>
- http://localhost:8000/docs

Запуск с Dockerfile:
- cd backend
- <code>docker build -t backend .</code>
- <code>docker run -p 8000:8000 backend</code>
- http://localhost:8000/api/healt_hcheck

Запуск с docker-compose:
- запускаем из корня
- <code>docker-compose up --build</code>
- http://localhost:8000/api/healt_hcheck
- пересобираем без кэша при необходимости <code>docker-compose build --no-cache</code>

### pre-commit:
Локально запустите <code>pre-commit install</code>, теперь перед каждым коммитом код будет проходить
проверку mypy, flake8, black и др.<br>
Чтобы проверить ваш код на соответствие всем стилям воспользуйтесь командой <code>pre-commit run --all-files
</code>

### alembic:
Миграции создаются для моделей, импортированных в файл <bold>migrations/env.py</bold><br>
<code>alembic revision --autogenerate -m "migration name"</code> – сгенерировать миграцию<br>
<code>alembic upgrade head</code> – применить миграции<br>
