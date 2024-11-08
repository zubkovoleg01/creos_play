Инструкция

Клонирование репозитория

git clone https://github.com/zubkovoleg01/creos_play.git

Создание виртуального окружения

venv\Scripts\activate

source venv/bin/activate

Установка зависимостей

pip install -r requirements.txt

Настройка базы данных

python manage.py migrate

Запуск веб-сервера

python manage.py runserver

Запуск Telegram-бота

python -m weather.telegram_bot.bot

Запуск тестов

python manage.py test

Запуск контейнера docker compose

docker compose up --build
