# Тестовое Задание: Разработка API для Управления Библиотекой

RESTful API для управления библиотечным каталогом.
Система позволяет управлять информацией о книгах, авторах, читателях и
выдавать книги.

<hr>

- [Запуск приложения](#run)
- [Тестирование приложения](#test)
- [Эндпоинты](#endpoints)
- [Описание реализации](#realization)

<hr>

<h2 id="run">Запуск приложения</h2>
1. Склонируйте репозиторий:
```commandline
git clone https://github.com/Tarasyonok/library-api
```
2. Перейди в папку с проектом:
```commandline
cd library-api
```
3. Собирите контейнер:
```commandline
docker compose build
```
4. Запустите контейнер:
```commandline
docker compose up
```
5. Прложение будет запущено на `localhost` на `8000` порту. Для тестирования эндпоитнтов перейдите в документацию:
```commandline
http://localhost:8000/docs
```

<h2 id="test">Тестирование приложения</h2>
1. Клонируем репозиторий:
```commandline
git clone https://github.com/Tarasyonok/library-api
```
2. Переходим в папку с проектом:
```commandline
cd library-api
```
3. Создайте виртуальное окружение:
```commandline
python -m venv venv
```
4. Активируйте виртуальное окружение:
```commandline
./venv/Scripts/activate
```
5. Установите зависимости:
```commandline
pip install -r requirements.txt
```
6. Создайте PostgreSQL базу данных и заполните `.env`.  
Шаблон находится в файле `.env-example`.

7. Прогоните миграции:
```commandline
alembic upgrade head
```
8. Протестируйте приложение:
```commandline
pytest
```
9. Можно запустить приложение: в режиме разработки:
```commandline
uvicorn app.main:app --reload --port 8000
```
10. Прложение будет запущено на `localhost` на `8000` порту. Для тестирования эндпоитнтов перейдите в документацию:
```commandline
http://localhost:8000/docs
```

<h2 id="endpoints">Эндпоинты</h2>
<h2 id="realization">Описание реализации</h2>

