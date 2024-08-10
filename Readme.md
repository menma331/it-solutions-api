# CarServiceAPI

<p>Проект разработан с целью показать результат выполнения тестового задания
</p>

## Запуск

<ol>
<li>В терминал введите команду

```
git clone git@github.com:menma331/it-solutions-api.git
```

</li>
<li>Затем перейдите в папку с проектом

```
cd it-solutions-api
```

</li>
<li>Переходим на ветку master

```
git checkout master
```

</li>
<li>
Устанавливаем зависимости

```
pip install -r requirements.txt
```

</li>
<li>
Создаем файл секретный файл .env в папке it-solutions-api вручную, либо, если Linux

```
touch .env
```

</li>
<li>В файл .env вписываем переменную "DATABASE_URL" и передаем ей URL к вашей БД. Для проекта предусмотрена БД SQLite. Поэтому можете смело копировать отсюда

```
DATABASE_URL=sqlite:///./cars.db
```

</li>
<li>Делаем миграции и грузим фикстуры.
Поочередно вписывайте команды в терминал

```
alembic revision --autogenereate -m 'Init'
```

```
alembic upgrade head
```

```
python3 main.py init_fixtures
```
</li>
<li>
Всё. Теперь можем запускать приложение

```
python3 main.py start
```
</li>
</ol>
