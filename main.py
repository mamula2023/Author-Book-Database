import sqlite3

from db_generator import db_generator
from db_reader import db_reader

if __name__ == '__main__':
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    db_gen = db_generator(cursor)

    db_gen.generate_authors(500)
    db_gen.generate_books(1000)

    reader = db_reader(cursor)

    print('books with most pages: ')
    result = reader.books_with_most_pages()
    for i in range(len(result)):
        print(f"{i+1}. {result[i][0]}")

    result = reader.average_page_count()
    print(f'\naverage number of pages: {result}')

    result = reader.youngest_author()
    print(f'\nyoungest author: {result}')

    result = reader.authors_without_books()
    print(f'\nauthors without books: ')
    for i in range(len(result)):
        print(f"{i+1}. {result[i][1]} {result[i][2]}")

    conn.commit()
    conn.close()
