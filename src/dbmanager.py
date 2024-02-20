import psycopg2
from src.config import config


"""Класс для работы с БД PostgreSQL, каждая функция выполняет SQL запрос к БД и возвращает результат."""


class DBmanager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = psycopg2.connect(dbname=db_name, **config())
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        try:
            query = """
            SELECT employer, COUNT(id) as vacancy_count
            FROM vacancies
            GROUP BY employer;
            """
            self.cur.execute(query)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка при получении данных с БД {e}")
            return []

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.cur.close()

    def get_all_vacancies(self):
        try:
            query = """
                SELECT 
                    e.name as company_name,
                    v.name as vacancy_name,
                    v.salary_from,
                    v.salary_to,
                    v.url
                FROM 
                    vacancies v
                JOIN 
                    employers e ON v.employer = e.name;
            """
            self.cur.execute(query)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка запроса всех вакансий {e}")
            return []

    def get_avg_salary(self):
        try:
            query = """
                SELECT AVG(salary_from) as avg_salary
                FROM vacancies
                WHERE salary_from IS NOT NULL;
            """
            self.cur.execute(query)
            result = self.cur.fetchone()
            avg_salary = result[0] if result[0] is not None else 0
            return avg_salary
        except Exception as e:
            print(f"Error fetching average salary: {e}")
            return 0

    def get_vacancies_with_higher_salary(self):
        try:
            query = """
            SELECT 
    e.name as company_name,
    v.name as vacancy_name,
    v.salary_from,
    v.url
FROM 
    vacancies v
JOIN 
    employers e ON v.employer = e.name
WHERE 
    v.salary_from > (
        SELECT AVG(salary_from)
        FROM vacancies
        WHERE salary_from IS NOT NULL
    );
    """
            self.cur.execute(query)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(f" Ошибка получении данных выше средней ЗП {e}")
            return []

    def get_vacancies_with_keyword(self, keyword):
        try:
            query = """
                SELECT 
                    e.name as company_name,
                    v.name as vacancy_name,
                    v.salary_from,
                    v.salary_to,
                    v.url
                FROM 
                    vacancies v
                JOIN 
                    employers e ON v.employer = e.name
                WHERE 
                    LOWER(v.name) LIKE LOWER(%s);
            """
            self.cur.execute(query, ('%' + keyword + '%',))
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(f"Не найдено вакансий с ключевым словом {keyword} {e}")
            return []
