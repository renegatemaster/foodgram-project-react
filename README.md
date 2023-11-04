# Foodgram 
_Cайт для ваших рецептов_ 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

### Информация для проверки

Адрес сайта:
https://food-gram.sytes.net/

Для входа в админку:
```
email: admin@admin.com
password: admin
```

### Как с этим работать? 


Клонируем репозиторий и переходим в него в командной строке:

```bash
git clone git@github.com:renegatemaster/foodgram-project-react.git
cd foodgram-project-react
```

Cоздаём и активируем виртуальное окружение, устанавливаем зависимости:

```bash
python3.9 -m venv venv && \ 
    source venv/bin/activate && \
    python -m pip install --upgrade pip && \
    pip install -r backend/requirements.txt
```

Устанавливаем [докер](https://www.docker.com/) на свой компьютер.

Запускаем проект через docker-compose:

```bash
docker compose -f docker-compose.yml up --build -d
```

Выполняем миграции:

```bash
docker compose -f docker-compose.yml exec backend python manage.py migrate
```

Соберём статику и скопируем ее:

```bash
docker compose -f docker-compose.yml exec backend python manage.py collectstatic  && \
docker compose -f docker-compose.yml exec backend cp -r /app/static_backend/. /backend_static/static/
```

В корне проекта создайте файл .env и пропишите в него свои данные.

Пример:

```apache
SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEBUG=False
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_NAME=foodgram
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS='127.0.0.1 localhost'
```

Для развёртывания на удалённом сервере ипользуется GitHub Actions
При пуше проекта на гит происходит проверка тестами/линтерами, создаются и пушатся контейнеры на DockerHub, приложение разворачивается в сети контейнеров на удалённом сервере.
