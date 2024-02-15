# Тестовое задание RickMorty

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
$: docker-compose up --build -d
```
Будет запущен контейнер с postgress и создан контейнер с скриптом python для инициализации базы данных, таблиц и получения данных из API
1. rickmorty-postgres - контейнер с бд
2. rickmorty-etl - скрипт загрузки данных

```
$: docker start rickmorti-etl -i
```
Запуск процесса по получению и трансформации данных в ручную при рабочем контейнере rickmorty postgres

### Запуск локально
1. Запустить postgres
2. Добавить данные для подключения к базе данных postgress в config.env 

```bash
$:pip install -r requirements.txt
$:python app.py local
```

## Пример использования
```
$: docker compose up
$: docker exec -it rickmorty-postgres psql -U postgres rickmorty
=>: SELECT * FROM public.characters_from_earth_count_by_month;
```
Витрина данных - VIEW public.characters_from_earth_count_by_month

Пример витрины данных приведен в блокноте example.ipynb 
[Ссылка на блокнот](example.ipynb)

## Схема данных

![Схема бд](schema.png)


LOCATIONS
id - айди планеты
name - название планеты или места рождения

ORIGIN
id - айди персонажа
name - имя персонажа
origin_id - форинкей к таблице с планетами

EPISODES
id - индекс
episode_id - айди эпизода
name - название эпизода
episode - код эпизода пример - S1E3
air_date - дата эфира
characters_id - форинкей к персонажу

В базу данных загружены все персонажи и все локации их рождения. Можно сделать выборку не только по планете Земля, но и по любому месту или персонажу. Примеры в блокноте
