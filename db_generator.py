from datetime import datetime, timedelta
from faker import Faker
import random


class db_generator:
    def __init__(self, cursor):
        self.cursor = cursor
        self.fake = Faker()

    def generate_authors(self, count):
        self.cursor.execute('DROP TABLE IF EXISTS authors')
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS authors (
                                author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                first_name TEXT NOT NULL,
                                last_name TEXT NOT NULL,
                                birth_date DATE NOT NULL,
                                birth_place TEXT NOT NULL
                            )
                        ''')

        for i in range(count):
            first_name = self.fake.first_name()

            last_name = self.fake.last_name()
            birth_date = self.fake.date_between(start_date='-500y', end_date='-18y')
            birth_place = self.fake.city()

            self.cursor.execute(
                'INSERT INTO authors (first_name, last_name, birth_date, birth_place) VALUES (?, ?, ?, ?)',
                (first_name, last_name, birth_date, birth_place))

    def generate_books(self, count):
        self.cursor.execute('''DROP TABLE IF EXISTS books''')
        self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS books (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title TEXT NOT NULL,
                                    genre TEXT NOT NULL,
                                    page_count INTEGER NOT NULL,
                                    release_date DATE NOT NULL,
                                    author_id INTEGER NOT NULL,
                                    FOREIGN KEY(author_id) REFERENCES authors(author_id)
                                )
                            ''')

        genres = ['Romance', 'Mystery', 'Science Fiction', 'Thriller', 'Biography', 'Inspirational', 'Fantasy',
                  'Horror']

        for i in range(count):
            title = self.fake.sentence(5, True)
            genre = random.choice(genres)
            page_count = random.randint(1, 2000)
            author_id = random.randint(1, 500)

            self.cursor.execute('SELECT birth_date FROM authors WHERE author_id = ?', (author_id,))
            date_str = self.cursor.fetchone()[0]

            release_date = random_release_date(date_str)

            self.cursor.execute(
                'INSERT INTO books (title, genre, page_count, release_date, author_id) VALUES (?, ?, ?, ?, ?)',
                (title, genre, page_count, release_date, author_id))


def random_release_date(author_birth_date):

    birth_date = datetime.strptime(author_birth_date, '%Y-%m-%d')

    if birth_date.month == 2 and birth_date.day == 29:
        birth_date = birth_date.replace(day=28)
    release_start = birth_date.replace(year=birth_date.year + 18)
    max_year = min(birth_date.year + 100, datetime.today().year)
    release_end = birth_date.replace(year=max_year)
    offset_range = (release_end - release_start).days
    random_day_offset = random.randint(0, offset_range)

    release_date = release_start + timedelta(random_day_offset)

    return release_date.date()
