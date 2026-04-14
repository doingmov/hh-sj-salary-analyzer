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

#### 💡 Установка ключа (через переменную окружения)

1. Windows (PowerShell):
```bash
setx SUPERJOB_API_KEY "ваш_ключ"
```

2. macOS / Linux: 
```bash
export SUPERJOB_API_KEY="ваш_ключ"
```

#### В коде ключ используется так:

```python
import os

SUPERJOB_API_KEY = os.getenv("SUPERJOB_API_KEY")
```

### 3. Запустить проект

```bash
python main.py
```

## Цель проекта

Понять, какие языки программирования дают лучшие зарплаты и больше вакансий на рынке.
