import requests
import os
from terminaltables import AsciiTable
from dotenv import load_dotenv

load_dotenv()

SUPERJOB_API_KEY = os.getenv("SUPERJOB_API_KEY")


HH_URL = "https://api.hh.ru/vacancies"
HH_AREA_MOSCOW = 1
HH_PERIOD_DAYS = 30


SJ_URL = "https://api.superjob.ru/2.0/vacancies/"
SJ_TOWN_MOSCOW = 4
SJ_CATALOGUE_PROGRAMMING = 48
SJ_PAGE_SIZE = 100


def predict_salary(salary_from, salary_to):
    if not salary_from:
        salary_from = None
    if not salary_to:
        salary_to = None

    if salary_from and salary_to:
        return (salary_from + salary_to) / 2

    if salary_from:
        return salary_from * 1.2

    if salary_to:
        return salary_to * 0.8

    return None


def predict_rub_salary_hh(vacancy):
    salary = vacancy.get("salary")

    if not salary:
        return None

    if salary.get("currency") != "RUR":
        return None

    return predict_salary(salary.get("from"), salary.get("to"))


def predict_rub_salary_sj(vacancy):
    if vacancy.get("currency", "").lower() != "rub":
        return None

    return predict_salary(
        vacancy.get("payment_from"),
        vacancy.get("payment_to")
    )


def get_hh_stats(language):
    url = HH_URL

    page = 0
    pages = 1

    vacancies = []

    while page < pages:
        params = {
            "text": f"Программист {language}",
            "area": HH_AREA_MOSCOW,
            "period": HH_PERIOD_DAYS,
            "page": page,
            "per_page": 100
        }

        response = requests.get(url, params=params)
        data = response.json()

        vacancies.extend(data.get("items", []))

        pages = data["pages"]
        page += 1

    salaries = []

    for vac in vacancies:
        salary = predict_rub_salary_hh(vac)
        if salary:
            salaries.append(salary)

    processed = len(salaries)

    return {
        "vacancies_found": data["found"],
        "vacancies_processed": processed,
        "average_salary": int(sum(salaries) / processed) if processed else 0
    }


def get_sj_stats(language, api_key):
    headers = {"X-Api-App-Id": api_key}

    page = 0
    vacancies = []

    total_found = 0

    while True:
        params = {
            "town": SJ_TOWN_MOSCOW,
            "catalogues": SJ_CATALOGUE_PROGRAMMING,
            "keyword": f"Программист {language}",
            "count": SJ_PAGE_SIZE,
            "page": page
        }

        response = requests.get(SJ_URL, headers=headers, params=params)
        data = response.json()

        total_found = data.get("total", 0)

        objects = data.get("objects", [])

        if not objects:
            break

        vacancies.extend(objects)

        if len(objects) < SJ_PAGE_SIZE:
            break

        page += 1

    salaries = []

    for vac in vacancies:
        salary = predict_rub_salary_sj(vac)
        if salary:
            salaries.append(salary)

    processed = len(salaries)

    return {
        "vacancies_found": total_found,
        "vacancies_processed": processed,
        "average_salary": int(sum(salaries) / processed) if processed else 0
    }


def print_table(title, stats):
    table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]

    for lang, data in stats.items():
        table_data.append([
            lang,
            data["vacancies_found"],
            data["vacancies_processed"],
            data["average_salary"]
        ])

    table = AsciiTable(table_data)
    table.title = title
    print(table.table)


def main():
    languages = ["python", "c", "c#", "c++", "java", "js", "ruby", "go", "1c"]

    hh_stats = {}
    sj_stats = {}

    for lang in languages:
        hh_stats[lang] = get_hh_stats(lang)
        sj_stats[lang] = get_sj_stats(lang, SUPERJOB_API_KEY)

    print_table("HeadHunter Moscow", hh_stats)
    print_table("SuperJob Moscow", sj_stats)


if __name__ == "__main__":
    main()
