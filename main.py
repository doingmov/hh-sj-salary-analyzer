import requests
import os
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from == 0:
        salary_from = None
    if salary_to == 0:
        salary_to = None

    if salary_from is not None and salary_to is not None:
        return (salary_from + salary_to) / 2

    if salary_from is not None:
        return salary_from * 1.2

    if salary_to is not None:
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
    url = "https://api.hh.ru/vacancies"

    params = {
        "text": f"Программист {language}",
        "area": 1,
        "period": 30
    }

    response = requests.get(url, params=params)
    data = response.json()

    salaries = []

    for vac in data["items"]:
        salary = predict_rub_salary_hh(vac)
        if salary is not None:
            salaries.append(salary)

    processed = len(salaries)

    return {
        "vacancies_found": data["found"],
        "vacancies_processed": processed,
        "average_salary": int(sum(salaries) / processed) if processed else 0
    }


def get_sj_stats(language, api_key):
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {"X-Api-App-Id": api_key}

    page = 0
    vacancies = []

    while True:
        params = {
            "town": 4,
            "catalogues": 48,
            "keyword": f"Программист {language}",
            "count": 100,
            "page": page
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        objects = data.get("objects", [])

        if not objects:
            break

        vacancies.extend(objects)

        if len(objects) < 100:
            break

        page += 1

    salaries = []

    for vac in vacancies:
        salary = predict_rub_salary_sj(vac)
        if salary is not None:
            salaries.append(salary)

    processed = len(salaries)

    return {
        "vacancies_found": len(vacancies),
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
    API_KEY = os.getiron("SUPERJOB_KEY")

    languages = ["python", "c", "c#", "c++", "java", "js", "ruby", "go", "1c"]

    hh_stats = {}
    sj_stats = {}

    for lang in languages:
        hh_stats[lang] = get_hh_stats(lang)
        sj_stats[lang] = get_sj_stats(lang, API_KEY)

    print_table("HeadHunter Moscow", hh_stats)
    print_table("SuperJob Moscow", sj_stats)


if __name__ == "__main__":
    main()
