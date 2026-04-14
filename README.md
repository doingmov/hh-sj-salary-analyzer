# Salary Analyzer (HH + SuperJob)

Проект собирает статистику по зарплатам программистов в Москве с двух платформ:
- HeadHunter
- SuperJob

## 📊 Что делает проект

- Получает вакансии через API
- Анализирует зарплаты по языкам программирования
- Считает:
  - количество найденных вакансий
  - количество обработанных вакансий
  - среднюю зарплату
- Выводит результат в виде таблицы

## 🛠 Используемые технологии

- Python 3
- requests
- terminaltables
- python-dotenv
- HeadHunter API
- SuperJob API

## 🚀 Как запустить

### 1. Установить зависимости

```bash
pip install -r requirements.txt
```

### 2. 🔑 Настройка API ключа SuperJob

Для работы с SuperJob API необходимо получить ключ:

- Зарегистрируйте приложение на [SuperJob](https://api.superjob.ru) и получите `Secret Key`

#### 💡 Установка ключа

После получения `Secret key`
- Создайте файл .env в корне проекта и добавьте туда свой ключ:

```bash
SUPERJOB_API_KEY="ваш_secret_key"
```

#### В коде ключ используется так:

```python
import os
from dotenv import load_dotenv
load_dotenv()

SUPERJOB_API_KEY = os.getenv("SUPERJOB_API_KEY")
```

### 3. Запустить проект

```bash
python main.py
```

## Цель проекта

Понять, какие языки программирования дают лучшие зарплаты и больше вакансий на рынке.
