class db_reader:
    def __init__(self, cursor):
        self.cursor = cursor

    def books_with_most_pages(self):
        self.cursor.execute('SELECT title FROM books WHERE page_count = (SELECT MAX(page_count) FROM books)')
        result_tuple = self.cursor.fetchall()
        return result_tuple

    def average_page_count(self):
        self.cursor.execute('SELECT AVG(page_count) FROM books')
        return self.cursor.fetchone()[0]

    def youngest_author(self):

        self.cursor.execute(
            'SELECT first_name, last_name FROM authors WHERE birth_date = (SELECT MAX(birth_date) FROM authors)')
        result_tuple = self.cursor.fetchone()
        return f'{result_tuple[0]} {result_tuple[1]}'

    def authors_without_books(self):

        self.cursor.execute('SELECT * FROM authors a WHERE (SELECT COUNT(*) FROM books b '
                            'WHERE a.author_id = b.author_id) = 0')
        result_tuple = self.cursor.fetchall()
        return result_tuple
