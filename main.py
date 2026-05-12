"""Главный модуль VANIARA - PyQt6"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from login_window import LoginWindow
from main_window import MainWindow
from database import db


def main():
    app = QApplication(sys.argv)

    while True:
        # Окно входа
        login = LoginWindow()
        login.setModal(True)
        login.show()

        if login.exec() != 1:
            break  # Пользователь отменил вход

        # Главное окно
        main_window = MainWindow()
        main_window.show()

        # Ждём закрытия главного окна
        app.exec()

        # Проверяем, вышел ли пользователь
        if main_window.user_logged_out:
            continue  # Показываем окно входа снова
        else:
            break  # Выход из приложения

    db.close()


if __name__ == "__main__":
    main()