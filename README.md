и# YaMDb

REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке. Написан на Django Rest Framework.


### Вам понадобятся

Для установки и сборки приложения понадобится Docker, инструкцию по установке можно найти [здесь](https://docs.docker.com/get-docker/)

### Установка и запуск

1. Склонируйте репозиторий на локальный компьютер 
2. В директории ```api_yamdb``` создайте файл ```.env``` и пропишите в нем: 
``` 
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
DB_USER=postgres 
DB_PASSWORD=postgres 
DB_HOST=db 
DB_PORT=5432 
``` 
3. В корневой директории выполните команду ```docker-compose up```, запустится контейнер 
4. В новой вкладке терминала выполните команду ```docker container ls``` и скопируйте ID контейнера ```api_yamdb_web``` 
5. Перейдите в контейнер командой ```docker container exec -it <CONTAINER ID> bash . ```
6. Внутри контейнера выполните миграции командой ```python manage.py migrate```
7. Создайте суперпользователя командой ```python manage.py createsuperuser``` 
8. Заполните базу тестовыми данными, выполнив команду ```python manage.py loaddata fixtures.json``` 


## Использованные технологии

* [Django REST Framework](https://www.django-rest-framework.org/) - Веб-фреймворк
* [Docker](https://www.docker.com/) - Управление сборкой и запуском приложения
* [PostgreSQL](https://www.postgresql.org/) - СУБД

## Автор

* **Артем Коломацкий** - [Roxe322](https://github.com/Roxe322)
