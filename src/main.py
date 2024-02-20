from src.sql import create_database, create_tables, insert_data_into_tables
from src.dbmanager import DBmanager

"""Создание базы данных и таблиц и загрузка с парсинга вакансий с hh.ru"""
create_database('course_work_5')
create_tables('course_work_5')
insert_data_into_tables('course_work_5')

""" Вызов меню для пользователя"""


def main_menu():
    print("Добро пожаловать в Менеджер базы данных вакансий!")
    while True:
        print("\nГлавное меню:")
        print("1. Показать список всех компаний и количество вакансий у каждой компании")
        print("2. Показать все вакансии")
        print("3. Показать среднюю зарплату")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выйти")

        choice = input("Введите ваш выбор (0-5): ")

        if choice == '1':
            show_companies_and_vacancies_count()
        elif choice == '2':
            show_all_vacancies()
        elif choice == '3':
            show_average_salary()
        elif choice == '4':
            show_higher_salary_vacancies()
        elif choice == '5':
            keyword = input("Введите ключевое слово для поиска: ")
            show_keyword_vacancies(keyword)
        elif choice == '0':
            print("Завершение программы. До свидания!")
            break
        else:
            print("Некорректный выбор. Пожалуйста, введите число от 0 до 5.")


def show_companies_and_vacancies_count():
    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
    for company in companies_and_vacancies_count:
        print(f"Компания: {company[0]}, Количество вакансий: {company[1]}")


def show_all_vacancies():
    all_vacancies = db_manager.get_all_vacancies()
    for vacancy in all_vacancies:
        company_name, vacancy_name, salary_from, salary_to, url = vacancy
        print(f"Компания: {company_name}")
        print(f"Вакансия: {vacancy_name}")
        if salary_to == 0:
            print(f"Зарплата от {salary_from}")
        else:
            print(f"Зарплата {salary_from} - {salary_to}")
        print(f"URL: {url}\n")


def show_average_salary():
    average_salary = db_manager.get_avg_salary()
    print(f"Средняя зарплата: {average_salary}")


def show_higher_salary_vacancies():
    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    for idx, vacancy in enumerate(higher_salary_vacancies, start=1):
        print(f"{idx}. Компания: {vacancy[0]}")
        print(f"   Вакансия: {vacancy[1]}")
        print(f"   Зарплата от: {vacancy[2]}")
        print(f"   URL: {vacancy[3]}\n")


def show_keyword_vacancies(keyword):
    keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
    for idx, vacancy in enumerate(keyword_vacancies, start=1):
        print(f"{idx}. Компания: {vacancy[0]}")
        print(f"   Вакансия: {vacancy[1]}")
        print(f"   Зарплата от: {vacancy[2]}")
        print(f"   Зарплата до: {vacancy[3]}")
        print(f"   URL: {vacancy[4]}\n")


# Инициализация DBManager
db_manager = DBmanager('course_work_5')

# Запуск основного меню
main_menu()

# Закрытие соединения по завершении
db_manager.close_connection()
