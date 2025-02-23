# api_final

## Автор

Stepan Dilman
https://github.com/sdilman

## Использованные технологии

- Django 3.2.16 (https://www.djangoproject.com/)
- Django REST Framework 3.12.4 (https://www.django-rest-framework.org/)
- Django REST Framework SimpleJWT 4.7.2 (https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- Djoser 2.1.0 (https://djoser.readthedocs.io/en/latest/)
- Pillow 9.3.0 (https://python-pillow.org/)
- PyJWT 2.1.0 (https://pyjwt.readthedocs.io/en/stable/)
- pytest 6.2.4 (https://pytest.org/)
- pytest-pythonpath 0.7.3 (https://pypi.org/project/pytest-pythonpath/)
- pytest-django 4.4.0 (https://pytest-django.readthedocs.io/en/latest/)
- requests 2.26.0 (https://docs.python-requests.org/en/latest/)

## Описание

Проект реализует API для управления записями в блоге и комментариями к ним.

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:sdilman/api_final_yatube.git
```

```
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры

1. GET запрос `http://127.0.0.1:8000/api/v1/posts/`
   возвращает все посты
2. GET запрос `http://127.0.0.1:8000/api/v1/posts/1/`
   возвращает пост с `id = 1`
3. POST запрос `http://127.0.0.1:8000/api/v1/posts/` с payload 
    ```
    {
       "text": "текст поста"
    }
    ```
    создает пост с указанным текстом от имени авторизованного пользователя.

Подробное описание API находится по ссылке `http://127.0.0.1:8000/redoc/`