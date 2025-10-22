# Куда пойти — Москва глазами Артёма

Приложение для отображения интересных мест Москвы на интерактивной карте

![&#x41A;&#x443;&#x434;&#x430; &#x43F;&#x43E;&#x439;&#x442;&#x438;](.gitbook/assets/site.png)

[Демка сайта](https://devmanorg.github.io/where-to-go-frontend/).

## Установка 
1. Клонирование репозитория
```
git clone <URL репозитория>
cd <имя директории>
```
2. Установить зависимости
```
pip install -r requirements.txt
```
3. Создать файл .env в корне проекта со следующими переменными
```
SECRET_KEY, 
DEBUG = булево значение (True или False), включающее или отключающее режим отладки.
ALLOWED_HOSTS = список разрешённых доменов/хостов, разделённых запятыми.
```
4. Создайте базу данных и примените миграции, создайте админ пользователя и запустите сервер:
```
python manage.py makemigrations
python manage,py migrate
python manage,py createsuperuser
python manage.py runserver
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

Тестовые данные взяты с сайта [KudaGo](https://kudago.com).

