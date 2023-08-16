# Foodgram 
#### *— сайт для ваших рецептов* 

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
