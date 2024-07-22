from datetime import datetime

import pytest
import json
from books_manager import BooksManager
from book_class import Book, NotValidDataError

# Тесты для методов BooksManager

@pytest.fixture
def empty_manager(tmp_path):
    db_file = tmp_path / "database.json"
    db_file.write_text("[]", encoding="utf-8")
    return BooksManager(str(db_file))


@pytest.fixture
def manager_with_books(tmp_path):
    db_file = tmp_path / "database.json"
    books = [
        {
            "book_id": 1,
            "title": "Book 1",
            "author": "Author 1",
            "year": "2001",
            "status": "в наличии"
        },
        {
            "book_id": 2,
            "title": "Book 2",
            "author": "Author 2",
            "year": "2002",
            "status": "в наличии"
        }
    ]
    db_file.write_text(json.dumps(books, ensure_ascii=False, indent=4), encoding="utf-8")
    return BooksManager(str(db_file))


def test_get_books_list_empty(empty_manager: BooksManager):
    """
    Тестируем метод, возвращающий список книг из пустой библотеки.
    """

    response = empty_manager.get_books_list()
    assert "error_message" in response
    assert response["error_message"] == "На данный момент в библиотеке нет книг."


def test_get_books_list(manager_with_books: BooksManager):
    """
    Тестируем метод, возвращающий список книг из непустой библотеки.
    """

    response = manager_with_books.get_books_list()
    assert "books_list" in response
    assert len(response["books_list"]) == 2


def test_find_book(manager_with_books: BooksManager):
    """
    Тестируем метод, который ищет книги по совпадениям в названии, авторе, годе.
    """
    response = manager_with_books.find_book("Book 1")
    assert "result_by_title" in response
    assert len(response["result_by_title"]) == 1
    assert response["result_by_title"][0].title == "Book 1"

    response = manager_with_books.find_book("Author 2")
    assert "result_by_author" in response
    assert len(response["result_by_author"]) == 1
    assert response["result_by_author"][0].author == "Author 2"

    response = manager_with_books.find_book("2001")
    assert "result_by_year" in response
    assert len(response["result_by_year"]) == 1
    assert response["result_by_year"][0].year == "2001"


def test_add_book_empty(empty_manager: BooksManager):
    """
    Тестируем метод, добавляющий книгу в пустую юиюлиотеку.
    """
    response = empty_manager.add_book("New Book", "New Author", "2023")
    assert "new_book" in response
    assert response["new_book"].title == "New Book"
    assert response["new_book"].book_id == 1

    response = empty_manager.get_books_list()
    assert len(response["books_list"]) == 1


def test_add_book(manager_with_books: BooksManager):
    """
    Тестируем метод, добавляющий книгу в непустую библиотеку.
    """
    response = manager_with_books.add_book("New Book", "New Author", "2023")
    assert "new_book" in response
    new_book = response["new_book"]
    assert new_book.title == "New Book"

    response = manager_with_books.get_books_list()
    assert max(book.book_id for book in response["books_list"]) == new_book.book_id


def test_delete_book(manager_with_books: BooksManager):
    """
    Тестируем метод, удаляющий книгу по id.
    """
    response = manager_with_books.delete_book("1")
    assert "book_deleted" in response
    assert response["book_deleted"].book_id == 1

    response = manager_with_books.get_books_list()
    assert len(response["books_list"]) == 1


def test_change_status(manager_with_books: BooksManager):
    """
    Тестируем метод, меняющий статус книги.
    """
    response = manager_with_books.change_status("1", "выдана")
    assert "book_changed" in response
    assert response["book_changed"].status == "выдана"

    response = manager_with_books.get_books_list()
    assert response["books_list"][0].status == "выдана"


# Тесты для класса Book


def test_book_creation():
    """
    Тестируем создание Book и назначение его атрибутов
    """
    book = Book(book_id=1, title="Test Title", author="Test Author", year="2023")
    assert book.book_id == 1
    assert book.title == "Test Title"
    assert book.author == "Test Author"
    assert book.year == "2023"
    assert book.status == "в наличии"
    assert book.dict_view == {
        "book_id": 1,
        "title": "Test Title",
        "author": "Test Author",
        "year": "2023",
        "status": "в наличии"
    }


def test_book_str():
    """
    Тестируем поведение Book в функции print
    """
    book = Book(book_id=1, title="Test Title", author="Test Author", year="2023", status="в наличии")
    assert str(book) == '    Книга №1: "Test Title", Test Author, 2023 г. (в наличии)'


def test_invalid_book_id():
    """
    Тестируем невозможность назначения нечислового id
    """
    with pytest.raises(NotValidDataError, match="ОШИБКА: Невозможно присвоить книге нечисловой id!"):
        Book(book_id="one", title="Test Title", author="Test Author", year="2023")


def test_empty_title():
    """
    Тестируем невозможность назначения пустого названия книги
    """
    with pytest.raises(NotValidDataError, match="ОШИБКА: Название книги не может быть пустой строкой!"):
        Book(book_id=1, title="", author="Test Author", year="2023")


def test_empty_author():
    """
    Тестируем автоматическое назначение "Автор не указан", если в author передана пустая строка
    """
    book = Book(book_id=1, title="Test Title", author="", year="2023")
    assert book.author == "Автор не указан"


def test_invalid_year_format():
    """
    Тестируем невозможность назначения нечислового года выпуска
    """
    with pytest.raises(NotValidDataError, match="ОШИБКА: Год должен быть целым положительным числом!"):
        Book(book_id=1, title="Test Title", author="Test Author", year="20xx")


def test_year_in_future():
    """
    Тестируем невозможность назначения года выпуска позже текущего года
    """
    with pytest.raises(NotValidDataError,
                       match=f"ОШИБКА: Указан некорректный год! Можно указать годы от 0 до 2024"):
        Book(book_id=1, title="Test Title", author="Test Author", year=str(datetime.now().year + 1))


def test_invalid_status():
    """
    Тестируем невозможность назначения иного статуса помимо "в наличии" или "выдана"
    """
    with pytest.raises(NotValidDataError, match="ОШИБКА: Возможно лишь два статуса: 'в наличии' или 'выдана'!"):
        Book(book_id=1, title="Test Title", author="Test Author", year="2023", status="пропала")


def test_status_in_uppercase():
    """
    Тестируем возможность назначения верного статуса независимо от регистра ввода
    """
    book = Book(book_id=1, title="Test Title", author="Test Author", year="2023", status="ВЫДАНА")
    assert book.status == "выдана"

    book = Book(book_id=2, title="Another Title", author="Another Author", year="2022", status="В НАЛИЧИИ")
    assert book.status == "в наличии"
