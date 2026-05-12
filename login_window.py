"""Окно входа - PyQt6"""
from PyQt6.QtWidgets import (QDialog, QLineEdit, QPushButton, QLabel, QVBoxLayout,
                           QFrame, QMessageBox, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor, QEnterEvent
from auth import auth


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VANIARA - Вход в систему")
        self.setFixedSize(400, 480)
        self._setup_ui()
        self.center()

    def _setup_ui(self):
        # Фон
        self.setStyleSheet("""
            QDialog {
                background-color: #E8E8E8;
            }
            QLabel {
                color: #333333;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(10)

        # Заголовок
        title = QLabel("ГЕОМАШ")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #1B5E20;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Система контроля доступа")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #666666;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        # Поля ввода
        login_label = QLabel("Логин")
        login_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(login_label)

        self.entry_username = QLineEdit()
        self.entry_username.setPlaceholderText("Введите логин")
        self.entry_username.setMinimumHeight(45)
        self.entry_username.setFont(QFont("Segoe UI", 13))
        self.entry_username.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #CCCCCC;
                border-radius: 6px;
                padding: 8px 12px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #2E7D32;
                background-color: white;
            }
        """)
        layout.addWidget(self.entry_username)

        pass_label = QLabel("Пароль")
        pass_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(pass_label)

        self.entry_password = QLineEdit()
        self.entry_password.setPlaceholderText("Введите пароль")
        self.entry_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.entry_password.setMinimumHeight(45)
        self.entry_password.setFont(QFont("Segoe UI", 13))
        self.entry_password.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #CCCCCC;
                border-radius: 6px;
                padding: 8px 12px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #2E7D32;
                background-color: white;
            }
        """)
        self.entry_password.returnPressed.connect(self._on_login)
        layout.addWidget(self.entry_password)

        layout.addSpacing(25)

        # Кнопка входа
        self.btn_login = QPushButton("ВОЙТИ")
        self.btn_login.setMinimumHeight(50)
        self.btn_login.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1B5E20;
            }
            QPushButton:pressed {
                background-color: #0D3D14;
            }
        """)
        self.btn_login.clicked.connect(self._on_login)
        layout.addWidget(self.btn_login)

        layout.addSpacing(25)

        # Инфо панель
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #DDDDDD;
                border-radius: 8px;
            }
        """)
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(15, 12, 15, 12)
        info_layout.setSpacing(5)

        info_title = QLabel("Тестовые пользователи:")
        info_title.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        info_title.setStyleSheet("color: #1B5E20;")
        info_layout.addWidget(info_title)

        info_layout.addWidget(QLabel("admin / admin123 (Админ)"))
        info_layout.addWidget(QLabel("guard1 / guard123 (Охранник)"))
        
        for i in range(info_layout.count()):
            widget = info_layout.itemAt(i).widget()
            if widget:
                widget.setStyleSheet("color: #555555;")
        info_frame.setLayout(info_layout)
        layout.addWidget(info_frame)

        layout.addStretch()

        self.setLayout(layout)

    def center(self):
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        if screen:
            size = self.size()
            screen_size = screen.availableGeometry()
            x = (screen_size.width() - size.width()) // 2
            y = (screen_size.height() - size.height()) // 2
            self.move(x, y)

    def _on_login(self):
        username = self.entry_username.text().strip()
        password = self.entry_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        if auth.login(username, password):
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")
            self.entry_password.clear()
            self.entry_password.setFocus()
