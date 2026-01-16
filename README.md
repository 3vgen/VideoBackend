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

## Результаты работы:

Логгирование

<img width="928" height="380" alt="image" src="https://github.com/user-attachments/assets/020bb5c9-5f6c-4072-9dfa-c71de057b808" />

Создать видео

<img width="1435" height="206" alt="image" src="https://github.com/user-attachments/assets/a18e26b7-ef57-4286-b164-82911cfe9369" />

Получить все видео

<img width="1437" height="98" alt="image" src="https://github.com/user-attachments/assets/978a40a3-91bd-4172-b201-75ade60deabe" />

Получить видео с фильтрацией

<img width="1433" height="61" alt="image" src="https://github.com/user-attachments/assets/886b6380-de98-4b41-a7f9-3bd0e2c703e6" />

Получить видео по id

<img width="1435" height="57" alt="image" src="https://github.com/user-attachments/assets/d31f403c-0e72-4e20-a957-f7dfa448826f" />

Обновить статус

<img width="1431" height="98" alt="image" src="https://github.com/user-attachments/assets/a1df7f5d-4c5e-4c7f-b6e3-042dda243dab" />





