from books_manager import BooksManager
from lexicon import MAIN_MENU, COMMANDS


def command_processing(command: str, books_manager: BooksManager):

    """
    Функция по обработке команд, введенных в консоль.

    Параметры:
        command (str): одна из команд из MAIN_MENU;
        books_manager (BooksManager): объект управления библиотекой;

    В ответ выводится некоторая информация в консоль.
    """

    if command == "MENU":
        print(MAIN_MENU)

    elif command == "ALL_BOOKS":
        response = books_manager.get_books_list()
        print()

        if response.get("error_message", False):
            print(response["error_message"])
        else:
            print("Книги, представленные в библиотеке: ")
            for book in response["books_list"]:
                print(book)

    elif command == "FIND_BOOK":
        search_data = input(">>> Введите данные для поиска (название книги, автор или год): ")
        print()

        response = books_manager.find_book(search_data)

        if response.get("error_message", False):
            print(response["error_message"])
        else:

            if response["result_by_title"]:
                print("Совпадения по названию книги:")
                for book in response["result_by_title"]:
                    print(book)
                print()

            if response["result_by_author"]:
                print("Совпадения по автору:")
                for book in response["result_by_author"]:
                    print(book)
                print()

            if response["result_by_year"]:
                print("Совпадения по году:")
                for book in response["result_by_year"]:
                    print(book)

    elif command == "ADD_BOOK":
        new_book_title = input(">>> Введите название новой книги: ")
        new_book_author = input(">>> Введита автора новой книги: ")
        new_book_year = input(">>> Введите год выпуска новой книги: ")
        print()

        response = books_manager.add_book(
            new_title=new_book_title,
            new_author=new_book_author,
            new_year=new_book_year)

        if response.get("error_message", False):
            print(response["error_message"])
        else:
            print("Новая книга успешно добавлена в библиотеку: ")
            print(response["new_book"])

    elif command == "DELETE_BOOK":
        book_id_to_delete = input(">>> Введите id книги, которую хотите удалить: ")

        response = books_manager.delete_book(book_id=book_id_to_delete)

        print()
        if response.get("error_message", False):
            print(response["error_message"])
        else:
            print("Следующая книга была удалена из библиотеки: ")
            print(response["book_deleted"])

    elif command == "CHANGE_STATUS":
        book_id_to_change_status = input(">>> Введите id книги, чей статус хотите поменять: ")
        new_status = input(">>> Введите новый статус ('в наличии' или 'выдана'): ")

        response = books_manager.change_status(book_id=book_id_to_change_status, new_status=new_status)

        print()
        if response.get("error_message", False):
            print(response["error_message"])
        else:
            print("У следующей книги установлен новый статус: ")
            print(response["book_changed"])


def run_library():
    """
    Основная функция, запускающая работу с библиотекой.
    Цикл прерывается командой exit
    """

    books_manager = BooksManager("database.json")  # Создается объект управления библиотекой

    print(MAIN_MENU)  # Выводится главное меню с перечнем команд

    while True:
        print('-' * 50)
        command = input("> Введите команду: ").upper()

        if command not in COMMANDS:
            print("Кажется, Вы ввели что-то не то. Попробуйте снова!")
            continue

        elif command == "EXIT":
            print("Работа завершена. До новых встреч!")
            break

        else:
            command_processing(command=command, books_manager=books_manager)


if __name__ == "__main__":
    run_library()
