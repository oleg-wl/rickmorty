# Название вашего проекта

## Оглавление
- [Системные требования](#системные-требования)
- [Шаги по установке, сборке, запуску](#шаги-по-установке-сборке-запуску)
- [Пример использования](#пример-использования)
- [Схема данных](#схема-данных)


## Системные требования
- Версия языка: python 3.12
- Требования к ресурсам: нет
- Системные зависимости: pipenv или requirements.txt
- Необходимые расширения: docker и docker-compose или бд postgress

## Шаги по установке, сборке, запуску
### Запуск проекта с помощью docker-compose
```
$: docker-compose up --build
```
Будет запущен контейнер с postgress и контейнер с скриптом python для инициализации базы данных, таблиц и получения данных из API
1. rickmorty-postgres - контейнер с бд
2. rickmorty-etl - загрузка данных

```
$: docker exec rickmorti-etl pipenv run python app.py docker
```
Запуск процесса по получению и трансформации данных в ручную при рабочем контейнере rickmorty postgres

### Запуск локально
Запустить postgress
Добавить данные для подключения к базе данных postgress в config.env 
```
$:pip install -r requirements.txt
$:python app.py local
```

## Пример использования
```
$: docker compose up
$: docker exec -it rickmorty-postgres psql -U postgres rickmorty
=>: SELECT * FROM public.characters_from_earth_count_by_month;
```
Пример витрины данных приведен в блокноте example.ipynb 
[Ссылка на блокнот](example.ipynb)

## Схема данных
