import requests

class HHParser:
    """Топ компаний с множеством вакансий"""
    def get_companies(self, per_page=20, sort_by="by_vacancies_open"):
        params = {
            "per_page": per_page,
            "sort_by": sort_by
        }
        response = requests.get('https://api.hh.ru/employers', params=params)
        if response.status_code == 200:
            return response.json()['items']


if __name__ == "__main__":
    hh_parser = HHParser()
    companies = hh_parser.get_companies(per_page=100)  # Укажите необходимое количество компаний

    if companies:
        for i, company in enumerate(companies, start=1):
            print(f"{i}. Company: {company['name']}")
            print(f"   ID: {company['id']}")
            print(f"   URL: {company['url']}")
            if 'open_vacancies' in company:
                print(f"   Open Vacancies: {company['open_vacancies']}")
            else:
                print("   Open Vacancies information not available.")
            print("\n")
    else:
        print("No data available.")
