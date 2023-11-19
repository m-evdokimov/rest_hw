# Домашняя работа "Разработка приложений"
## "Проектирование и реализация REST-API информационной системы для автозаправочной станции"

Приложение предназначено для обработки транзакций на заправочной станции. Приложение имеет четыре эндпоинта:

- `/transaction/create` - создание транзакции, возвращает uuid транзакции в хранилище;

- `/transaction/update/{transaction_id}` - обнавляет поля транзакции с заданным идентификатором; поля, которые не нужно обновлять должны иметь значение None;

- `/transaction/delete/{transaction_id}` - удаляет транзакцию по идентификатору;

- `/transaction/read` - извлекает транзакцию по идентификатору;

- `/transaction/read_all` - извлекает список всех транзакций.


### Запуск:

```bash
$ docker-compose up -d
```

Swagger URL: `localhost:8000/docs`


### Описание реализации:

Язык программирования - python 3.10, веб-фреймворк - FastAPI. Для хранения транзакций в рантайме используется массив транзакций. Описание схемы данных для эндпоинтов описано в сваггере.