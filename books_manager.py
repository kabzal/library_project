import json
from book_class import Book, NotValidDataError

class BooksManager:
    """
    Класс для управления библиотекой книг.

    Атрибуты:
        filename (str): Имя файла, в котором хранится база данных книг.
        books_list (list[Book]): Список объектов книг.
    """

    def __init__(self, filename: str):
        """
        Инициализация объекта BooksManager.

        Параметры:
            filename (str): Имя файла базы данных книг.
        """
        self.filename = filename
        self.books_list = self.load_all_books()

    def load_all_books(self) -> list[Book]:
        """
        Загружает все книги из файла и создает список объектов Book.

        Возвращает:
            list[Book]: Список объектов Book.
        """
        with open(self.filename, "r", encoding="utf-8") as f:
            return [Book(**obj) for obj in json.load(f)]

    def get_books_list(self) -> dict[str, list | str]:
        """
        Возвращает список книг или сообщение об ошибке, если список пуст.

        Возвращает:
            dict[str, list | str]: Словарь с ключом "books_list" и списком книг или с ключом "error_message" и сообщением об ошибке.
        """
        if self.books_list:
            return {"books_list": self.books_list}
        return {"error_message": "На данный момент в библиотеке нет книг."}

    def find_book(self, search_data: str) -> dict[str, list | str]:
        """
        Ищет книги по заголовку, автору или году.

        Параметры:
            search_data (str): Строка для поиска.

        Возвращает:
            dict[str, list | str]: Словарь с результатами поиска по заголовку, автору и году или сообщение об ошибке.
        """
        search_data = search_data.upper()  # Приводим строку поиска к верхнему регистру для сравнения

        result_by_title = list(filter(lambda x: search_data in x.title.upper(), self.books_list))
        result_by_author = list(filter(lambda x: search_data in x.author.upper(), self.books_list))
        result_by_year = list(filter(lambda x: search_data in x.year.upper(), self.books_list))

        if not any((result_by_title, result_by_author, result_by_year)):
            return {"error_message": "Увы, совпадений не найдено."}
        return {
            "result_by_title": result_by_title,
            "result_by_author": result_by_author,
            "result_by_year": result_by_year
        }

    def add_book(self, new_title: str, new_author: str, new_year: str) -> dict[str, Book | str]:
        """
        Добавляет новую книгу в библиотеку.

        Параметры:
            new_title (str): Название книги.
            new_author (str): Автор книги.
            new_year (str): Год издания книги.

        Возвращает:
            dict[str, Book | str]: Словарь с добавленной книгой или сообщение об ошибке.
        """
        try:
            new_book = Book(
                book_id=self.create_new_id(),
                title=new_title,
                author=new_author,
                year=new_year
            )
            self.books_list.append(new_book)
            self.save_to_database()
            return {"new_book": new_book}
        except NotValidDataError as e:
            return {"error_message": str(e)}

    def create_new_id(self) -> int:
        """
        Создает новый уникальный идентификатор для книги.

        Возвращает:
            int: Новый уникальный идентификатор.
        """
        if not self.books_list:
            return 1
        previous_max_id = max(book.book_id for book in self.books_list)
        return previous_max_id + 1

    def save_to_database(self):
        """
        Сохраняет текущий список книг в файл базы данных.
        """
        book_dicts = [book.dict_view for book in self.books_list]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(book_dicts, f, indent=4, ensure_ascii=False)

    def delete_book(self, book_id: str) -> dict[str, Book | str]:
        """
        Удаляет книгу из библиотеки по идентификатору.

        Параметры:
            book_id (str): Идентификатор книги.

        Возвращает:
            dict[str, Book | str]: Словарь с удаленной книгой или сообщение об ошибке.
        """
        if not book_id.isdigit():
            return {"error_message": "ОШИБКА: Некорректно введен id книги. Это должно быть целое число!"}
        else:
            for book in self.books_list:
                if book.book_id == int(book_id):
                    self.books_list.remove(book)
                    self.save_to_database()
                    return {"book_deleted": book}
            return {"error_message": f"Книга с id={book_id} не найдена."}

    def change_status(self, book_id: str, new_status: str) -> dict[str, Book | str]:
        """
        Изменяет статус книги по идентификатору.

        Параметры:
            book_id (str): Идентификатор книги.
            new_status (str): Новый статус книги.

        Возвращает:
            dict[str, Book | str]: Словарь с измененной книгой или сообщение об ошибке.
        """
        if not book_id.isdigit():
            return {"error_message": "ОШИБКА: Некорректно введен id книги. Это должно быть целое число!"}
        else:
            for book in self.books_list:
                if book.book_id == int(book_id):
                    if book.status == new_status:
                        return {"error_message": f"Данная книга уже имеет статус '{new_status}'."}
                    else:
                        try:
                            book.status = new_status
                            self.save_to_database()
                            return {"book_changed": book}
                        except NotValidDataError as e:
                            return {"error_message": str(e)}
            return {"error_message": f"Книга с id={book_id} не найдена."}
