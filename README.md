# api_final

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

http://127.0.0.1:8000/redoc/