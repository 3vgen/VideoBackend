# VideoBackend
Весь код отформатирован с помощью форматера black
## Структура проекта

```
.
├── app
│   ├── app.log
│   ├── core
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── config.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── connections.py
│   ├── main.py
│   └── video
│       ├── __init__.py
│       ├── crud.py
│       ├── model.py
│       ├── routers.py
│       └── schemas.py
├── app.log
├── docker-compose.yml
├── Dockerfile
├── logging_config.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Запуск проекта
### 1. Клонировать репозиторий
``` bash
git clone github.com/3vgen/VideoBackend
cd VideoBackend
```
### 2.  Подготовить файл окружения
Создать файл .env на основе шаблона:
``` bash
cp .env.example .env
```
При необходимости изменить значения переменных в .env.
### 3. Собрать Docker-образы
``` bash
docker-compose build
```
### 4. Запустить сервисы
``` bash
docker-compose up -d
```
### 5. Проверить работу API: [http://localhost:8000/docs](http://localhost:8000/docs)
Результаты работы: