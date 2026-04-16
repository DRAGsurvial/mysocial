Запуск проекта:

1) Создай и активируй виртуальное окружение
   python -m venv venv
   venv\Scripts\activate

2) Установи зависимости
   pip install -r requirements.txt

3) Выполни миграции
   python manage.py makemigrations
   python manage.py migrate

4) Создай админа admin/admin
   python manage.py create_default_admin

5) Запусти сервер
   python manage.py runserver

Адреса:
- сайт: http://127.0.0.1:8000
- админка: http://127.0.0.1:8000/admin

Возможности админки:
- просмотр всех пользователей
- выдача moderator/admin роли
- полный бан/разбан пользователя
- удаление каналов
- удаление статей
- деактивация / активация аккаунта

Важно:
- admin/admin только для локального теста
