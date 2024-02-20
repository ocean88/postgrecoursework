import psycopg2
from config import config
from src.parser import HHParser


"""Модуль для создания и удаления базы данных и таблиц, а также загрузки данных 
из класса HHParser в базу данных."""


def terminate_connections(db_name):
    try:
        # Connect to the default 'postgres' database to terminate connections
        conn_terminate = psycopg2.connect(dbname='postgres', **config())
        conn_terminate.autocommit = True
        cur_terminate = conn_terminate.cursor()

        # Terminate connections to the specified database
        query_terminate = f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{db_name}'
              AND pid <> pg_backend_pid();
        """
        cur_terminate.execute(query_terminate)
        cur_terminate.close()
        conn_terminate.close()
    except Exception as e:
        print(f"Error terminating connections: {e}")


def create_database(db_name):
    # Terminate connections before dropping the database
    terminate_connections(db_name)

    # Now connect to the default 'postgres' database and drop/create the specified database
    try:
        conn = psycopg2.connect(dbname='postgres', **config())
        conn.autocommit = True
        cur = conn.cursor()

        # Drop the existing database if it exists
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")

        # Create the new database
        cur.execute(f"CREATE DATABASE {db_name}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

# Example usage:
# create_database('your_database_name')


def create_tables(db_name):
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            # cur.execute("DROP TABLE IF EXISTS employers, vacancies")
            cur.execute("""CREATE TABLE employers 
                            (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(255) UNIQUE NOT NULL
                            )
                        """)
            cur.execute("""CREATE TABLE vacancies 
                            (
                                id SERIAL PRIMARY KEY,
                                employer VARCHAR(255) NOT NULL,
                                name VARCHAR(255) NOT NULL,
                                salary_from INT,
                                salary_to INT,
                                url VARCHAR(255),
                                area VARCHAR(255),
                                published_at TIMESTAMP
                            )
                        """)
    conn.close()
    cur.close()


def insert_data_into_tables(db_name):
    conn = psycopg2.connect(dbname=db_name, **config())

    # Создание объекта парсера
    parser = HHParser()
    employers = parser.get_employers()
    vacancies = parser.filter_vacancies()
    with conn:
        with conn.cursor() as cur:
            # Вставка данных о компаниях в таблицу employers
            for employer in employers:
                cur.execute("""
                    INSERT INTO employers (id, name) VALUES (%s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (employer['id'], employer['name']))

            # Вставка данных о вакансиях в таблицу vacancies
            for vacancy in vacancies:
                cur.execute("""
                        INSERT INTO vacancies (employer, name, salary_from, salary_to, url, area, published_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                    vacancy['employer'],
                    vacancy['name'],
                    vacancy['salary_from'],
                    vacancy['salary_to'],
                    vacancy['url'],
                    vacancy['area'],
                    vacancy['published_at'],
                ))
    cur.close()
    conn.close()