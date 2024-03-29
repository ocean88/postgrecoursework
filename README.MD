# Курсовая работа: Парсер вакансий с HeadHunter и работа с PostgreSQL

**Студент:** Макаров А.А. (Курс Skypro 30)

## Описание

Программа представляет собой парсер вакансий с сайта HeadHunter, а также инструмент для работы с базой данных PostgreSQL. Проект разработан в рамках курса Skypro и предназначен для демонстрации навыков работы с веб-скрапингом, базами данных и языком программирования Python.

## Функциональность

1. **Парсинг данных:** При помощи парсера осуществляется сбор информации о вакансиях и компаниях с сайта HeadHunter.
2. **Загрузка данных в базу данных:** Полученные данные вставляются в базу данных PostgreSQL для последующего анализа и использования.
3. **Анализ данных в базе:** Реализованы методы класса `DBManager` для выполнения запросов к базе данных, такие как:
    - Получение списка всех компаний и количества вакансий у каждой компании.
    - Получение списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
    - Расчет средней зарплаты по вакансиям.
    - Получение списка вакансий с зарплатой выше средней.
    - Поиск вакансий по ключевому слову.

## Использование

1. Установите необходимые зависимости с помощью команды `poetry install`. 
2. Укажите ваш логин и пароль в файле  `database.ini` **от базы PostgreSQL**
3. Запустите скрипт `main.py` для парсинга данных с HeadHunter и загрузки их в базу данных.


