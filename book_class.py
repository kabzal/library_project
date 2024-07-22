from datetime import datetime


class NotValidDataError(ValueError):
    """Кастомное исключение для обозначения ошибок валидации данных."""
    pass


class Book:
    """
        Класс для представления книги.

        Атрибуты:
            book_id (int): Уникальный идентификатор книги.
            title (str): Название книги.
            author (str): Автор книги.
            year (str): Год выпуска книги.
            status (str): Статус книги (в наличии или выдана).
    """

    def __init__(self, book_id: int,
                 title: str,
                 author: str,
                 year: str,
                 status: str = "в наличии"):

        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

        self.dict_view = {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    def __str__(self):
        """
            Возвращает строковое представление объекта Book.
        """
        return f'    Книга №{self.book_id}: "{self.title}", {self.author}, {self.year} г. ({self.status})'

    @property
    def book_id(self):
        """Возвращает идентификатор книги."""
        return self._book_id

    @book_id.setter
    def book_id(self, value: int):
        """
            Устанавливает идентификатор книги с проверкой типа данных.

            Параметры:
                value (int): Идентификатор книги.

            Исключения:
                NotValidDataError: Если value не является целым числом.
        """
        if not isinstance(value, int):
            raise NotValidDataError("ОШИБКА: Невозможно присвоить книге нечисловой id!")
        else:
            self._book_id = value

    @property
    def title(self):
        """Возвращает название книги."""
        return self._title

    @title.setter
    def title(self, value: str):
        """
        Устанавливает название книги с проверкой данных.

        Параметры:
            value (str): Название книги.

        Исключения:
            NotValidDataError: Если value пустое или не является строкой.
        """
        if not value:
            raise NotValidDataError("ОШИБКА: Название книги не может быть пустой строкой!")
        elif not isinstance(value, str):
            raise NotValidDataError("ОШИБКА: Название книги должно быть непустой строкой!")
        else:
            self._title = value

    @property
    def author(self):
        """Возвращает имя автора книги."""
        return self._author

    @author.setter
    def author(self, value: str):
        """
        Устанавливает автора книги с проверкой данных.

        Параметры:
            value (str): Автор книги.

        Исключения:
            NotValidDataError: Если value не является строкой.
        """
        if not value:
            self._author = "Автор не указан"
        elif not isinstance(value, str):
            raise NotValidDataError("ОШИБКА: Данные об авторе должны быть представлены в виде строки!")
        else:
            self._author = value

    @property
    def year(self):
        """Возвращает год выпуска книги."""
        return self._year

    @year.setter
    def year(self, value: str):
        """
        Устанавливает год издания книги с проверкой данных.

        Параметры:
            value (str): Год выпуска книги.

        Исключения:
            NotValidDataError: Если value не является строкой, не содержит только цифры или выходит за пределы допустимых значений.
        """
        if not value or value == "Год не указан":
            self._year = "Год не указан"
        elif not isinstance(value, str) or not value.isdigit():
            raise NotValidDataError("ОШИБКА: Год должен быть целым положительным числом!")
        elif datetime.now().year < int(value) or int(value) < 0:
            raise NotValidDataError(f"ОШИБКА: Указан некорректный год! Можно указать годы от 0 до {datetime.now().year}")
        else:
            self._year = value

    @property
    def status(self):
        """Возвращает статус книги."""
        return self._status

    @status.setter
    def status(self, value: str):
        """
        Устанавливает статус книги с проверкой данных.

        Параметры:
            value (str): Статус книги.

        Исключения:
            NotValidDataError: Если value не является допустимым статусом ('в наличии' или 'выдана').
        """
        if value.upper() == "ВЫДАНА":
            self._status = "выдана"
        elif value.upper() == "В НАЛИЧИИ":
            self._status = "в наличии"
        else:
            raise NotValidDataError("ОШИБКА: Возможно лишь два статуса: 'в наличии' или 'выдана'!")
