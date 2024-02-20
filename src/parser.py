import requests

"""Парсер hh.ru"""


class HHParser:
    def __init__(self):
        self.base_url = 'https://api.hh.ru'
        self.employer_ids = [2180, 78638, 2748, 1122462, 87021, 3529, 1740, 2537115, 10317521, 1025275]

    def get_vacancies_by_employer(self, employer_id):
        params = {
            "employer_id": employer_id,
            "per_page": 10
        }
        response = requests.get(f'{self.base_url}/vacancies', params=params)
        if response.status_code == 200:
            return response.json().get('items', [])
        return []

    def get_requests(self):
        params = {
            "per_page": 10,
            "sort_by": "by_vacancies_open"
        }
        response = requests.get(f'{self.base_url}/employers', params=params)
        if response.status_code == 200:
            return response.json()['items']

    def get_employers(self):
        data = self.get_requests()
        employers = []
        for employer in data:
            employers.append({
                "id": employer["id"],
                "name": employer["name"]
            })
        return employers

    def get_vacancies_from_company(self, employer_id):
        params = {
            "per_page": 20,
            "employer_id": employer_id
        }
        response = requests.get(f'{self.base_url}/vacancies', params=params)
        if response.status_code == 200:
            return response.json()['items']

    def get_all_vacancies(self, only_with_salary=True):
        all_vacancies = []
        for employer_id in self.employer_ids:
            vacancies = self.get_vacancies_from_company(employer_id)
            if only_with_salary:
                vacancies = [vacancy for vacancy in vacancies if vacancy.get('salary')]
            all_vacancies.extend(vacancies)
        return all_vacancies

    def filter_vacancies(self):
        vacancies = self.get_all_vacancies()
        filter_data = []
        for vacancy in vacancies:
            if not vacancy["salary"]:
                salary_from = 0
                salary_to = 0
            else:
                salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
                salary_to = vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0
            filter_data.append({
                "employer": vacancy["employer"]["name"],
                "name": vacancy["name"],
                "salary_from": salary_from,
                "salary_to": salary_to,
                "url": vacancy["alternate_url"],
                "area": vacancy["area"]["name"],
                "published_at": vacancy["published_at"]
            })
        return filter_data
