import requests
import sqlite3
import time
import threading


# Функция для создания таблицы в базе данных
def create_table():
    conn = sqlite3.connect('star_wars_characters.db')
    c = conn.cursor()

    # Создание таблицы characters
    c.execute('''CREATE TABLE IF NOT EXISTS characters
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 age INTEGER,
                 gender TEXT)''')

    conn.commit()
    conn.close()


# Функция для сохранения персонажа в базу данных
def save_character(character):
    conn = sqlite3.connect('star_wars_characters.db')
    c = conn.cursor()

    # Вставка данных персонажа в таблицу
    c.execute("INSERT INTO characters (name, age, gender) VALUES (?, ?, ?)",
              (character['name'], character['age'], character['gender']))

    conn.commit()
    conn.close()


# Функция для получения данных персонажа по его URL
def get_character_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        character = response.json()
        birth_year = character['birth_year']
        if birth_year != 'unknown' and birth_year != 'n/a':
            # Расчет возраста на основе года рождения персонажа
            age = birth_year[:-3]
        else:
            age = None

        character_data = {
            'name': character['name'],
            'age': age,
            'gender': character['gender']
        }
        return character_data

    return None


def process_character(url):
    character_data = get_character_data(url)
    if character_data:
        save_character(character_data)


def main():
    create_table()

    start_time = time.time()

    base_url = 'https://swapi.dev/api/people/'
    threads = []

    for i in range(1, 21):
        character_url = base_url + str(i) + '/'
        thread = threading.Thread(target=process_character,
                                  args=(character_url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения программы: {execution_time} сек")


if __name__ == '__main__':
    main()
