
## Сервис YaMDb

### 1. Коротко о главном

###### > YaMDb - это место, где вы можете свободно (свободнее, чем на ФильмоПоиске) делиться информцией о любимых произведениях искусства и оставлять отзывы на понравившиеся лично вам работы. Прокачайте своего внутреннего критика.
###### > Изначально вам доступно три категории: книги, фильмы и музыка. 
###### > Став администратором проекта, вы сможете добавлять новые категории и жанры.
_________________
В чём секрет успеха:
~ `Python 3.7.15` - простой и понятный язык ООП
~ `Django 2.2.16` - такой же фреймворк для создания веб-приложений
~ `Django restframework 3.12.4` - не менее простой фреймворк для создания REST API
~ `PyJWT 2.1.0` - простая аутентификация по токенам
~ `PostgreSQL 9.5.25` - едва ли не самая надёжная база данных
~ `Docker 20.10.7` - менеджер контейнеров, по которым распиханы части проекта
~ `Nginx 1.21.3-alpine` - самый надёжный и популярный сервер в мире
~ `Gunicorn 20.0.4` - простой сервер для Django-приложений

### 2. Cоздаём файл .env с паролями и прочими важными данными
```sh
DB_ENGINE=django.db.backends.postgresql # в проекте используем Postgresql
DB_NAME=postgres # даём имя нашей базе данных
POSTGRES_USER=<login> # придумываем базе логин (пишем без кавычек)
POSTGRES_PASSWORD=<password> # придумываем пароль для подключения к базе (пишем без кавычек)
DB_HOST=db # как обращаться к базе в проекте
DB_PORT=5432 # по какому порту к ней стучаться
SECRET_KEY = <ваш-секретный-ключ> # секретный ключ для файла settings.py (пишем без кавычек)
```
### 3. Запускаем проект в контейнерах:
* Сначала клонируем репозиторий с гитхаба к себе
* Заходим в папку проекта и ищем в ней директорию "docker-compose.yaml"
* А именно по пути cd /infra_sp2/infra
* Устанавливаем docker, если ещё не установили (да, да. Всё по-взрослому)
Но сначала устанавливаем curl, которым и скачаем пакет с docker-ом
```sh
sudo apt install curl
```
* Скачиваем скрипт для установки докера
```sh
curl -fsSL https://get.docker.com -o get-docker.sh
```
* Запускаем докер лёгким движением пальцев
```sh
sh get-docker.sh
```
А вообще, есть целый куст официальной макулатуры о том, как же установить докер на Линукс
[get Docker on Linux](https://docs.docker.com/desktop/install/linux-install/)

* И ещё немного настроек докера.
* Удалим предыдущие докеры (вдруг вы шпион на чужом компьютере или впали в маразм и не помните, что раньше ставили докер)
```sh
sudo apt remove docker docker-engine docker.io containerd runc
```
* Должен получиться ответ вроде
```sh
E: Unable to locate package docker-engine
```
* Обновляем список пакетов, т.к. недавно добавили новый
```sh
sudo apt update
```
* Устанавливаем пакеты для работы через https
```sh
sudo apt install \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common -y
```

* Добавляем ключ GPG для подтверждения подлинности в процессе установки:
```sh
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
* В консоли должно вывестись ОК
* Наконец, добавляем репозиторий Docker в пакеты apt:
```sh
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```
* И ещё раз обновляем репозиторий, куда добавлен новый пакет:
```sh
sudo apt update
```
* Теперь всё готово. Можем установить бесплатную версию докера (Community Edition (CE))
```sh
sudo apt install docker-ce docker-compose -y
```
* Проверяем, что всё робит и Docker работает:
sudo systemctl status docker
* Если всё запустилось, появится зелёная строчка. Можем нажимать Ctrl+C, чтобы выйти из демона.
* А теперь, когда вы расслабились, снова возвращаемся в папку с docker-compose.yaml. Собираем образ, запихнутый в контейнер, который тут же запускаем:

```sh
sudo docker-compose up -d --build
```
Осталось чуть-чуть. Выполняем по очереди:
* Делаем миграции
* Создаём суперпользователя
* Подгружаем статику
```sh
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
```

* Проверяем, что всё работает. Идём по адресу http://localhost/admin/
* Заходим под суперпользователем и создаём шок-контент
* Тестируем работу API, например, через Postman
* Всё настроено и работает. Можем остановить контейнеры и закончить:
```sh
sudo docker-compose down -v
```
Контейнеры остановлены и удалены вместе со всеми зависимостями. Остались только образы

УРА!!!


### Наполняем базу данных сервиса
Делаем это, перенося данные из локального проекта Yatube (того, что хранится на вашем компьютере) на сервер.
Для этого:
* Через консоль переходим к проекту на локальном компьютере.
* Заходим в директорию с файлом manage.py.
* Экспортируем данные в файл:
```sh
python manage.py dumpdata > dump.json
```
* Данные сохранятся в dump.json 

* Копируем файл dump.json с локального компьютера на сервер. Для такой задачи есть утилита scp (от англ. secure copy — «защищённая копия»). Она копирует файлы на сервер по протоколу SSH:
```sh
scp my_file username@host:<путь-на-сервере>
```

### Указываем IP своего сервера и путь до своей домашней директории на сервере
```sh
scp dump.json praktikum@84.201.161.196:/home/имя_пользователя/.../папка_проекта_с_manage.py/
```
* После выполнения этой команды файл dump.json появится в директории проекта на нашем сервере. Подключаемся к серверу и убеждаемся в этом.
Работа на локальном компьютере завершена, продолжайте работать уже на сервере: выполните команды для переноса данных с SQLite на PostgreSQL:

* Закинув dump.json на сервер через scp, выполняем там

```sh
python3 manage.py shell
```
* Выполняем в открывшемся терминале:
```sh
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()

python manage.py loaddata dump.json 
```

Готово. Теперь все данные перенесены на сервер и доступны посетителям проекта. Открываем проект в браузере и убеждаемся в этом.

```sh
python manage.py load-data *filename*.csv
```

### Как запустить проект:

* Открываем bash-терминал
* Клонируем репозиторий 

```sh
git clone https://github.com/Ivan-Maksimov/infra_sp2.git
```
* Заходим в склонированную директорию

```sh
cd infra_sp2/
```

Создаём и активируем виртуальное окружение:

для Windows
```sh
python3 -m venv venv
source venv/Scripts/activate
```

для Linux
```sh
python3 -m venv venv
. venv/bin/activate
```


Устанавливаем зависимости из файла `requirements.txt`:

```sh
python3 -m pip install --upgrade pip
cd api_yamdb/
pip install -r requirements.txt
```

Выполняем миграции:

```sh
python3 manage.py migrate
```

Запускаем сервер разработки:

```sh
python3 manage.py runserver
```

После того, как сервер запустится, можем почитать документацию по API проекта. В ней описана основная логика приложения, подробнее см. ссылку: http://127.0.0.1:8000/redoc/


### Если надо загрузить данные в базу sqlite3 (если мы в режиме разработки приложения)

Для этого написана команда, добавляющая данные через Django ORM.

CSV-файлы находятся в папке со статикой. После применения миграций можем добавить данные из CSV-файла в базу данных, набрав в терминале

```sh
python manage.py load-data *filename*.csv
```

### Роли пользователей (описаны на английском - и мне проще, и вам меньше путаницы)
 - Anonymous — can view descriptions of works, read reviews and comments.
 - Authenticated user (user) — can read everything, as well as Anonymous, can publish reviews and rate works (films / books / songs), can comment on reviews; can edit and delete their reviews and comments, edit their ratings of works. This role is assigned by default to each new user.
 - Moderator — the same rights as an Authenticated User, plus the right to delete and edit any reviews and comments.
 - Admin — full rights to manage all the content of the project. Can create and delete works, categories and genres. Can assign roles to users.
 - The Django superuser must always have administrator rights, a user with admin rights. Even if you change the user role of the superuser, it will not deprive him of administrator rights. A superuser is always an administrator, but an administrator is not necessarily a superuser.

### User registration algorithm
 - The user sends a POST request with the email and username parameters to the endpoint /api/v1/auth/signup/.
 -The YaMDB service sends an email with a confirmation code (confirmation_code) to the specified email address.
 - The user sends a POST request with the username and confirmation_code parameters to the endpoint /api/v1/auth/token/, in response to the request he receives a token (JWT token).
 - As a result, the user receives a token and can work with the project API by sending this token with each request.
 - After registering and receiving the token, the user can send a PATCH request to the endpoint /api/v1/users/me/ and fill in the fields in his profile (the description of the fields is in the documentation at the link: http://127.0.0.1:8000/redoc/).
 
### Creating a user by an administrator
 - The user can be created by an administrator — through the site's admin zone or through a POST request to a special api endpoint/v1/users/ (the description of the request fields for this case is in the documentation).
 - - At this point, the user does not need to send an email with a confirmation code.
After that, the user must independently send his email and username to the endpoint /api/v1/auth/signup/, in response he should receive an email with a confirmation code.
 - Next, the user sends a POST request with the username and confirmation_code parameters to the endpoint /api/v1/auth/token/, in response to the request, he receives a token (JWT token), as with self-registration.

 ### Resources of the YaMDb API service
- auth: authentication.
- users: users.
- titles: works that are reviewed (a certain movie, book or song).
- categories: categories (types) of works ("Movies", "Books", "Music").
- genres: genres of works. One work can be linked to several genres.
- reviews: reviews of works. The review is tied to a specific work.
- comments: comments on reviews. The comment is linked to a specific review.

 ### Examples of requests:
> The full list of possible requests and responses can be seen after installing and running the API on the local server by `http://127.0.0.1:8000/redoc/#tag/api`

 ### 1.`POST` Adding a new category, endpoint `api/v1/categories/`:
>Permissions class: Administrator.
```sh
{
    "name": "string",
    "slug": "string"
}
```
Example of a successful response:
```sh
{
    "name": "string",
    "slug": "string"
}
```
 ### 2.`GET` Getting a list of all genres, endpoint `api/v1/genre/`:
>Permissions class: Available without token.
Example of a successful response:
```sh
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": []
    }
]
```
 ### 3. `POST` Adding a masterpiece, endpoint `api/v1/titles/`:
>Permissions class: Administrator.
```sh
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```
Example of a successful response:
```sh
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {}
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```
 ### 4. `POST` Adding a new review, endpoint `api/v1/titles/{title_id}/reviews/`:
>Permissions class: Authenticated users.
```sh
{
    "text": "string",
    "score": 1
}
```
Example of a successful response:
```sh
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
```
 ### 5. `POST` Adding a comment to the review, endpoint `api/v1/titles/{title_id}/reviews/{review_id}/comments/`:
>Permissions class: Authenticated users.
```sh
{
    "text": "string"
}
```
Example of a successful response:
```sh
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}
```
 ### 6. `GET` Getting a list of all users, endpoint `api/v1/users/`:
>Permissions class: Administrator.
Example of a successful response:
```sh
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "username": "string",
                "email": "user@example.com",
                "first_name": "string",
                "last_name": "string",
                "bio": "string",
                "role": "user"
            }
        ]
    }
]
```
 ### 7. `POST` New user registration, endpoint `api/v1/auth/signup/`:
>Permissions class: Available without token.
```sh
{
    "email": "string",
    "username": "string"
}
```
Example of a successful response:
```sh
{
    "email": "string",
    "username": "string"
}
```
 
## License
**Prepared by the development team: 

Ivan Maksimov [GitHub Profile](https://github.com/Ivan-Maksimov), 
Petr Buikin [GitHub Profile](https://github.com/nikpup), 
Anastasiia Tonkova [GitHub Profile](https://github.com/nastyatonkova)
**
