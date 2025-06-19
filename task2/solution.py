import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict


def get_animal_counts():
    base_url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    counts = defaultdict(int)

    while True:
        try:
            response = requests.get(base_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Находим все группы животных по буквам
            groups = soup.find_all('div', class_='mw-category-group')
            for group in groups:
                letter = group.find('h3').text.strip()
                # Проверяем, что это русская буква (включая Ё)
                if len(letter) == 1 and letter in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
                    items = group.find_all('li')
                    counts[letter] += len(items)

            # Проверяем наличие следующей страницы
            next_page = soup.find('a', string='Следующая страница')
            if not next_page:
                break
            base_url = "https://ru.wikipedia.org" + next_page['href']

        except Exception as e:
            print(f"Ошибка при обработке страницы: {e}")
            break

    return counts


def save_counts_to_csv(counts, filename='beasts.csv'):
    russian_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Сортируем буквы в порядке русского алфавита
        for letter in sorted(counts.keys(), key=lambda x: russian_alphabet.index(x)):
            writer.writerow([letter, counts[letter]])


if __name__ == '__main__':
    print("Начинаем сбор данных с Википедии...")
    animal_counts = get_animal_counts()
    save_counts_to_csv(animal_counts)
    print("Данные успешно сохранены в файл beasts.csv")