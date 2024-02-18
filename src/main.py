import requests


def get_vacancies(api_key, company_ids):
    base_url = 'https://api.hh.ru/vacancies'

    for company_id in company_ids:
        params = {'employer_id': company_id, 'per_page': 5, 'page': 0}

        headers = {'Authorization': f'Bearer {api_key}'}

        response = requests.get(base_url, params=params, headers=headers)

        if response.status_code == 200:
            vacancies = response.json()

            for vacancy in vacancies['items']:
                print(f"Company: {vacancy['employer']['name']}")
                print(f"Title: {vacancy['name']}")
                print(f"Location: {vacancy['area']['name']}")
                print(f"Salary: {vacancy.get('salary', 'Not specified')}")
                print("\n")
        else:
            print(f"Error {response.status_code}: {response.text}")


if __name__ == '__main__':
    api_key = 'YOUR_HH_API_KEY'
    company_ids = ['company_id_1', 'company_id_2', 'company_id_3', 'company_id_4', 'company_id_5',
                   'company_id_6', 'company_id_7', 'company_id_8', 'company_id_9', 'company_id_10']

    get_vacancies(api_key, company_ids)
