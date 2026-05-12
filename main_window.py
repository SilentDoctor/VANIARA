"""Главное окно - PyQt6"""
from PyQt6.QtWidgets import (QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                           QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QFrame,
                           QComboBox, QDialog, QDialogButtonBox, QGridLayout, QScrollArea, QSizePolicy,
                           QDateEdit)
from PyQt6.QtCore import QDate
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from auth import auth
from database import db


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VANIARA - Геомаш")
        self.setMinimumSize(1100, 700)
        self.user_logged_out = False
        self._setup_ui()
        self._update_stats()
        self.center()

    def _show_message(self, icon, title, text):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #333333;
                font-size: 13px;
            }
            QMessageBox QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                min-width: 80px;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background-color: #1B5E20;
            }
        """)
        return msg.exec()

    def _setup_ui(self):
        # Глобальные стили
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QLabel {
                color: #222222;
            }
            QPushButton {
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                opacity: 0.85;
            }
            QLineEdit {
                background-color: white;
                color: #222222;
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                padding: 8px;
            }
            QLineEdit:focus {
                border-color: #2E7D32;
            }
            QLineEdit:disabled {
                background-color: #E0E0E0;
                color: #666666;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #CCCCCC;
                gridline-color: #DDDDDD;
                alternate-background-color: #FAFAFA;
            }
            QTableWidget::item {
                color: #222222;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #2E7D32;
                color: white;
            }
            QHeaderView::section {
                background-color: #E0E0E0;
                color: #222222;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QComboBox {
                background-color: white;
                color: #222222;
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                padding: 6px;
            }
            QComboBox:focus {
                border-color: #2E7D32;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #222222;
                selection-background-color: #2E7D32;
            }
            QDateEdit {
                background-color: white;
                color: #222222;
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                padding: 6px;
            }
            QDateEdit:focus {
                border-color: #2E7D32;
            }
            QDateEdit::drop-down {
                border: none;
                width: 20px;
                background-color: transparent;
            }
            QDateEdit::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #2E7D32;
                width: 0px;
                height: 0px;
                margin-right: 5px;
            }
            QDialog {
                background-color: #F5F5F5;
            }
            QDialogButtonBox button {
                background-color: #2E7D32;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QDialogButtonBox button:hover {
                background-color: #1B5E20;
            }
            QDialogButtonBox button:pressed {
                background-color: #0D3D0D;
            }
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #333333;
            }
            QMessageBox QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #1B5E20;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Content area with sidebar
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = self._create_sidebar()
        content_layout.addWidget(self.sidebar)

        # Scroll area for content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #F0F0F0; }")

        self.content_container = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(15)
        self.content_container.setLayout(self.content_layout)
        self.scroll_area.setWidget(self.content_container)
        content_layout.addWidget(self.scroll_area, 1)

        main_layout.addLayout(content_layout)
        central.setLayout(main_layout)

        self._show_welcome()

    def _create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #1B5E20;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Logo
        header = QLabel("ГЕОМАШ")
        header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header.setStyleSheet("color: white; padding: 20px; background-color: #0D3D0D;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Menu
        menu_items = [
            ("🏠  Главная", self._show_welcome),
            ("📋  Журнал проходов", self._show_pass_log),
            ("🚪  Проход сотрудника", self._show_employee_pass),
            ("👥  Посетители", self._show_visitors),
        ]

        if auth.is_admin():
            menu_items.extend([
                ("👔  Сотрудники", self._show_employees),
                ("⚙️  Пользователи", self._show_users),
                ("📊  Статистика", self._show_statistics),
            ])

        for text, callback in menu_items:
            btn = QPushButton(text)
            btn.setFont(QFont("Segoe UI", 11))
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                    text-align: left;
                    padding: 15px 20px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #2E7D32;
                }
            """)
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        layout.addStretch()

        # User panel
        user_frame = QFrame()
        user_frame.setStyleSheet("background-color: #2E7D32; padding: 15px;")
        user_layout = QVBoxLayout()

        self.lbl_user = QLabel(f"{auth.get_user_full_name()}")
        self.lbl_user.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.lbl_user.setStyleSheet("color: white;")
        self.lbl_user.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_layout.addWidget(self.lbl_user)

        role_label = QLabel(auth.get_user_role_display())
        role_label.setFont(QFont("Segoe UI", 9))
        role_label.setStyleSheet("color: #CCFFCC;")
        role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_layout.addWidget(role_label)

        user_layout.addSpacing(10)

        btn_logout = QPushButton("🚪 Выйти")
        btn_logout.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #C62828;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #B71C1C;
            }
        """)
        btn_logout.clicked.connect(self._on_logout)
        user_layout.addWidget(btn_logout)

        user_frame.setLayout(user_layout)
        layout.addWidget(user_frame)

        sidebar.setLayout(layout)
        return sidebar

    def _create_header(self):
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: #2E7D32;")
        header_layout = QHBoxLayout()

        self.lbl_passes = QLabel("Проходов сегодня: 0")
        self.lbl_passes.setFont(QFont("Segoe UI", 12))
        self.lbl_passes.setStyleSheet("color: white; padding: 10px;")
        header_layout.addWidget(self.lbl_passes)

        self.lbl_visitors = QLabel("Посетителей в здании: 0")
        self.lbl_visitors.setFont(QFont("Segoe UI", 12))
        self.lbl_visitors.setStyleSheet("color: white; padding: 10px;")
        header_layout.addWidget(self.lbl_visitors)

        header_layout.addStretch()

        header.setLayout(header_layout)
        return header

    def center(self):
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen()
        if screen:
            size = self.size()
            screen_size = screen.availableGeometry()
            x = (screen_size.width() - size.width()) // 2
            y = (screen_size.height() - size.height()) // 2
            self.move(x, y)

    def _clear_content(self):
        # Recursively delete all items
        def delete_items(layout):
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    delete_items(item.layout())
                    item.layout().deleteLater()
        
        delete_items(self.content_layout)

    def _update_stats(self):
        passes = db.get_today_pass_count()
        visitors = db.get_current_visitors_count()
        self.lbl_passes.setText(f"Проходов сегодня: {passes}")
        self.lbl_visitors.setText(f"Посетителей в здании: {visitors}")

    def _show_welcome(self):
        self._clear_content()

        title = QLabel("Добро пожаловать!")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #1B5E20;")
        self.content_layout.addWidget(title)

        role = "Администратор" if auth.is_admin() else "Охранник"
        subtitle = QLabel(f"Вы вошли как: {role}")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #666666; margin-bottom: 20px;")
        self.content_layout.addWidget(subtitle)

        # Stats cards
        cards_layout = QHBoxLayout()

        passes_today = db.get_today_pass_count()
        visitors_count = db.get_current_visitors_count()
        employees_count = len(db.get_employees())

        cards = [
            ("Проходов сегодня", str(passes_today), "#2E7D32"),
            ("Посетителей в здании", str(visitors_count), "#1565C0"),
            ("Сотрудников в базе", str(employees_count), "#7B1FA2"),
        ]

        for text, value, color in cards:
            card = QFrame()
            card.setStyleSheet(f"background-color: {color}; border-radius: 10px;")
            card.setFixedSize(220, 100)

            card_layout = QVBoxLayout()
            card_layout.setContentsMargins(20, 20, 20, 20)

            val_lbl = QLabel(value)
            val_lbl.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
            val_lbl.setStyleSheet("color: white;")
            card_layout.addWidget(val_lbl)

            txt_lbl = QLabel(text)
            txt_lbl.setFont(QFont("Segoe UI", 11))
            txt_lbl.setStyleSheet("color: white; opacity: 0.9;")
            card_layout.addWidget(txt_lbl)

            card.setLayout(card_layout)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        self.content_layout.addLayout(cards_layout)
        self.content_layout.addStretch()

    def _show_pass_log(self):
        self._clear_content()

        title = QLabel("Журнал проходов")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1B5E20;")
        self.content_layout.addWidget(title)

        # Filter bar
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Дата:"))

        self.pass_log_date = QLineEdit()
        self.pass_log_date.setText(datetime.now().strftime("%Y-%m-%d"))
        self.pass_log_date.setFixedWidth(120)
        filter_layout.addWidget(self.pass_log_date)

        btn_filter = QPushButton("Найти")
        btn_filter.setStyleSheet("background-color: #2E7D32;")
        btn_filter.clicked.connect(self._load_pass_log)
        filter_layout.addWidget(btn_filter)

        btn_refresh = QPushButton("Обновить")
        btn_refresh.setStyleSheet("background-color: #1976D2;")
        btn_refresh.clicked.connect(self._show_pass_log)
        filter_layout.addWidget(btn_refresh)

        filter_layout.addStretch()
        self.content_layout.addLayout(filter_layout)

        self.pass_log_table = QTableWidget()
        self.pass_log_table.setColumnCount(7)
        self.pass_log_table.setHorizontalHeaderLabels(["Время", "ФИО", "Таб.№", "Отдел", "Тип", "Охранник", "Примечание"])
        self.pass_log_table.horizontalHeader().setStretchLastSection(True)
        self.pass_log_table.setAlternatingRowColors(True)
        self.pass_log_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.content_layout.addWidget(self.pass_log_table, 1)

        self._load_pass_log()

    def _load_pass_log(self):
        self.pass_log_table.setRowCount(0)
        date = self.pass_log_date.text().strip() or None
        logs = db.get_pass_logs(date=date)

        for log in logs:
            row = self.pass_log_table.rowCount()
            self.pass_log_table.insertRow(row)

            pass_type = "Вход" if log['pass_type'] == 'in' else "Выход"
            time_str = datetime.strptime(log['timestamp'], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")

            self.pass_log_table.setItem(row, 0, QTableWidgetItem(time_str))
            self.pass_log_table.setItem(row, 1, QTableWidgetItem(log['full_name']))
            self.pass_log_table.setItem(row, 2, QTableWidgetItem(log['tab_number']))
            self.pass_log_table.setItem(row, 3, QTableWidgetItem(log['department']))
            self.pass_log_table.setItem(row, 4, QTableWidgetItem(pass_type))
            self.pass_log_table.setItem(row, 5, QTableWidgetItem(log['guard_name']))
            self.pass_log_table.setItem(row, 6, QTableWidgetItem(log['notes'] or "-"))

    def _show_employee_pass(self):
        self._clear_content()

        title = QLabel("Регистрация прохода сотрудника")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1B5E20;")
        self.content_layout.addWidget(title)

        # Search
        search_layout = QVBoxLayout()
        search_layout.addWidget(QLabel("Поиск сотрудника (ФИО или табельный номер):"))

        self.emp_search = QLineEdit()
        self.emp_search.setPlaceholderText("Введите для поиска...")
        self.emp_search.textChanged.connect(self._search_employees)
        search_layout.addWidget(self.emp_search)

        self.content_layout.addLayout(search_layout)

        # Table
        self.emp_table = QTableWidget()
        self.emp_table.setColumnCount(4)
        self.emp_table.setHorizontalHeaderLabels(["Таб.№", "ФИО", "Отдел", "Должность"])
        self.emp_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.emp_table.setAlternatingRowColors(True)
        self.emp_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.content_layout.addWidget(self.emp_table, 1)

        # Buttons
        btn_layout = QHBoxLayout()

        btn_in = QPushButton("🚪 ВХОД")
        btn_in.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        btn_in.setStyleSheet("background-color: #2E7D32; padding: 15px 40px;")
        btn_in.clicked.connect(lambda: self._register_pass("in"))
        btn_layout.addWidget(btn_in)

        btn_out = QPushButton("🚪 ВЫХОД")
        btn_out.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        btn_out.setStyleSheet("background-color: #1565C0; padding: 15px 40px;")
        btn_out.clicked.connect(lambda: self._register_pass("out"))
        btn_layout.addWidget(btn_out)

        btn_layout.addStretch()
        self.content_layout.addLayout(btn_layout)

    def _search_employees(self):
        self.emp_table.setRowCount(0)
        query = self.emp_search.text().strip()
        if len(query) < 1:
            return

        employees = db.search_employees(query)
        for emp in employees:
            row = self.emp_table.rowCount()
            self.emp_table.insertRow(row)
            self.emp_table.setItem(row, 0, QTableWidgetItem(emp['tab_number']))
            self.emp_table.setItem(row, 1, QTableWidgetItem(emp['full_name']))
            self.emp_table.setItem(row, 2, QTableWidgetItem(emp['department']))
            self.emp_table.setItem(row, 3, QTableWidgetItem(emp['position']))

    def _register_pass(self, pass_type: str):
        selected = self.emp_table.selectedItems()
        if not selected:
            self._show_message(QMessageBox.Icon.Warning, "Внимание", "Выберите сотрудника из списка!")
            return

        row = selected[0].row()
        tab = self.emp_table.item(row, 0).text()
        name = self.emp_table.item(row, 1).text()

        employees = db.search_employees(name)
        employee = next((e for e in employees if e['tab_number'] == tab), None)

        if not employee:
            self._show_message(QMessageBox.Icon.Warning, "Ошибка", "Сотрудник не найден!")
            return

        if db.add_pass_log(employee['id'], pass_type, auth.get_user_id()):
            action = "вход" if pass_type == "in" else "выход"
            self._show_message(QMessageBox.Icon.Information, "Успех", f"Проход зарегистрирован!\n{name} - {action}")
            self._update_stats()
        else:
            self._show_message(QMessageBox.Icon.Warning, "Ошибка", "Не удалось зарегистрировать проход!")

    def _show_visitors(self):
        self._clear_content()

        title = QLabel("Посетители")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1B5E20;")
        self.content_layout.addWidget(title)

        # Buttons
        btn_layout = QHBoxLayout()

        btn_add = QPushButton("➕ Зарегистрировать посетителя")
        btn_add.setStyleSheet("background-color: #2E7D32;")
        btn_add.clicked.connect(self._add_visitor_dialog)
        btn_layout.addWidget(btn_add)

        btn_checkout = QPushButton("📝 Отметить уход")
        btn_checkout.setStyleSheet("background-color: #1565C0;")
        btn_checkout.clicked.connect(self._checkout_visitor)
        btn_layout.addWidget(btn_checkout)

        btn_refresh = QPushButton("🔄 Обновить")
        btn_refresh.setStyleSheet("background-color: #757575;")
        btn_refresh.clicked.connect(self._show_visitors)
        btn_layout.addWidget(btn_refresh)

        btn_layout.addStretch()
        self.content_layout.addLayout(btn_layout)

        # Table
        self.visitor_table = QTableWidget()
        self.visitor_table.setColumnCount(8)
        self.visitor_table.setHorizontalHeaderLabels(["ID", "ФИО", "Телефон", "Организация", "Цель", "Время прихода", "К кому", "Охранник"])
        self.visitor_table.horizontalHeader().setStretchLastSection(True)
        self.visitor_table.setAlternatingRowColors(True)
        self.visitor_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.content_layout.addWidget(self.visitor_table, 1)

        self._load_visitors()

    def _load_visitors(self):
        self.visitor_table.setRowCount(0)
        visitors = db.get_visitors(active_only=True)

        for v in visitors:
            row = self.visitor_table.rowCount()
            self.visitor_table.insertRow(row)

            arrival = datetime.strptime(v['arrival_time'], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M")

            self.visitor_table.setItem(row, 0, QTableWidgetItem(str(v['id'])))
            self.visitor_table.setItem(row, 1, QTableWidgetItem(v['full_name']))
            self.visitor_table.setItem(row, 2, QTableWidgetItem(v['phone'] or "-"))
            self.visitor_table.setItem(row, 3, QTableWidgetItem(v['organization'] or "-"))
            self.visitor_table.setItem(row, 4, QTableWidgetItem(v['purpose'] or "-"))
            self.visitor_table.setItem(row, 5, QTableWidgetItem(arrival))
            self.visitor_table.setItem(row, 6, QTableWidgetItem(v['employee_name'] or "-"))
            self.visitor_table.setItem(row, 7, QTableWidgetItem(v['guard_name']))

    def _add_visitor_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Регистрация посетителя")
        dialog.setFixedSize(450, 400)
        dialog.setStyleSheet("""
            QDialog { background-color: #F5F5F5; }
            QLabel { color: #333333; }
            QLineEdit { background-color: white; color: #333333; border: 2px solid #CCCCCC; border-radius: 5px; padding: 8px; }
            QComboBox { background-color: white; color: #333333; border: 2px solid #CCCCCC; border-radius: 5px; padding: 6px; }
        """)

        layout = QGridLayout()
        layout.setSpacing(12)

        layout.addWidget(QLabel("ФИО посетителя:*"), 0, 0)
        visitor_name = QLineEdit()
        layout.addWidget(visitor_name, 0, 1)

        layout.addWidget(QLabel("Телефон:"), 1, 0)
        visitor_phone = QLineEdit()
        layout.addWidget(visitor_phone, 1, 1)

        layout.addWidget(QLabel("Организация:"), 2, 0)
        visitor_org = QLineEdit()
        layout.addWidget(visitor_org, 2, 1)

        layout.addWidget(QLabel("Цель визита:"), 3, 0)
        visitor_purpose = QLineEdit()
        layout.addWidget(visitor_purpose, 3, 1)

        layout.addWidget(QLabel("Кому:"), 4, 0)
        employees = db.get_employees()
        emp_names = ["Не указано"] + [e['full_name'] for e in employees]
        visitor_emp_combo = QComboBox()
        visitor_emp_combo.addItems(emp_names)
        layout.addWidget(visitor_emp_combo, 4, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1B5E20;
            }
        """)
        buttons.accepted.connect(lambda: self._save_visitor(dialog, visitor_name, visitor_phone, visitor_org, visitor_purpose, visitor_emp_combo, employees))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons, 5, 0, 1, 2)

        dialog.setLayout(layout)
        dialog.exec()

    def _save_visitor(self, dialog, name_field, phone_field, org_field, purpose_field, combo, employees):
        name = name_field.text().strip()
        if not name:
            QMessageBox.warning(self, "Внимание", "Введите ФИО посетителя!")
            return

        employee_idx = combo.currentIndex()
        employee_id = None
        if employee_idx > 0:
            employee_id = employees[employee_idx - 1]['id']

        if db.add_visitor(
            full_name=name,
            phone=phone_field.text().strip(),
            organization=org_field.text().strip(),
            purpose=purpose_field.text().strip(),
            guard_id=auth.get_user_id(),
            employee_visited_id=employee_id
        ):
            QMessageBox.information(self, "Успех", "Посетитель зарегистрирован!")
            dialog.accept()
            self._load_visitors()
            self._update_stats()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось сохранить посетителя!")

    def _checkout_visitor(self):
        selected = self.visitor_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Внимание", "Выберите посетителя!")
            return

        row = selected[0].row()
        visitor_id = int(self.visitor_table.item(row, 0).text())

        if db.checkout_visitor(visitor_id):
            QMessageBox.information(self, "Успех", "Уход посетителя отмечен!")
            self._load_visitors()
            self._update_stats()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось отметить уход!")

    def _show_employees(self):
        if not auth.is_admin():
            return

        self._clear_content()

        title = QLabel("Сотрудники предприятия")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1B5E20;")
        self.content_layout.addWidget(title)

        btn_layout = QHBoxLayout()

        self.emp_admin_search = QLineEdit()
        self.emp_admin_search.setPlaceholderText("Поиск...")
        self.emp_admin_search.textChanged.connect(self._load_employees_admin)
        btn_layout.addWidget(self.emp_admin_search)

        btn_add = QPushButton("➕ Добавить")
        btn_add.setStyleSheet("background-color: #1565C0;")
        btn_add.clicked.connect(self._add_employee_dialog)
        btn_layout.addWidget(btn_add)

        btn_layout.addStretch()
        self.content_layout.addLayout(btn_layout)

        self.emp_admin_table = QTableWidget()
        self.emp_admin_table.setColumnCount(5)
        self.emp_admin_table.setHorizontalHeaderLabels(["Таб.№", "ФИО", "Отдел", "Должность", "Статус"])
        self.emp_admin_table.horizontalHeader().setStretchLastSection(True)
        self.emp_admin_table.setAlternatingRowColors(True)
        self.emp_admin_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.content_layout.addWidget(self.emp_admin_table, 1)

        self._load_employees_admin()

    def _load_employees_admin(self):
        self.emp_admin_table.setRowCount(0)
        query = self.emp_admin_search.text().strip()
        employees = db.search_employees(query) if query else db.get_employees(active_only=False)

        for emp in employees:
            row = self.emp_admin_table.rowCount()
            self.emp_admin_table.insertRow(row)

            status = "Активен" if emp['is_active'] else "Уволен"

            self.emp_admin_table.setItem(row, 0, QTableWidgetItem(emp['tab_number']))
            self.emp_admin_table.setItem(row, 1, QTableWidgetItem(emp['full_name']))
            self.emp_admin_table.setItem(row, 2, QTableWidgetItem(emp['department']))
            self.emp_admin_table.setItem(row, 3, QTableWidgetItem(emp['position']))
            self.emp_admin_table.setItem(row, 4, QTableWidgetItem(status))

    def _add_employee_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить сотрудника")
        dialog.setFixedSize(400, 280)
        dialog.setStyleSheet("""
            QDialog { background-color: #F5F5F5; }
            QLabel { color: #333333; }
            QLineEdit { background-color: white; color: #333333; border: 2px solid #CCCCCC; border-radius: 5px; padding: 8px; }
        """)

        layout = QGridLayout()
        layout.setSpacing(12)

        layout.addWidget(QLabel("Табельный номер:*"), 0, 0)
        emp_tab = QLineEdit()
        layout.addWidget(emp_tab, 0, 1)

        layout.addWidget(QLabel("ФИО:*"), 1, 0)
        emp_name = QLineEdit()
        layout.addWidget(emp_name, 1, 1)

        layout.addWidget(QLabel("Отдел:*"), 2, 0)
        emp_dept = QLineEdit()
        layout.addWidget(emp_dept, 2, 1)

        layout.addWidget(QLabel("Должность:*"), 3, 0)
        emp_pos = QLineEdit()
        layout.addWidget(emp_pos, 3, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1B5E20;
            }
        """)
        buttons.accepted.connect(lambda: self._save_employee(dialog, emp_tab, emp_name, emp_dept, emp_pos))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons, 4, 0, 1, 2)

        dialog.setLayout(layout)
        dialog.exec()

    def _save_employee(self, dialog, tab_field, name_field, dept_field, pos_field):
        tab = tab_field.text().strip()
        name = name_field.text().strip()
        dept = dept_field.text().strip()
        pos = pos_field.text().strip()

        if not all([tab, name, dept, pos]):
            QMessageBox.warning(self, "Внимание", "Заполните все поля!")
            return

        if db.create_employee(tab, name, dept, pos):
            QMessageBox.information(self, "Успех", "Сотрудник добавлен!")
            dialog.accept()
            self._load_employees_admin()
        else:
            QMessageBox.warning(self, "Ошибка", "Такой табельный номер уже существует!")

    def _show_users(self):
        if not auth.is_admin():
            return

        self._clear_content()

        title = QLabel("Пользователи системы")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1B5E20;")
        self.content_layout.addWidget(title)

        btn_add = QPushButton("➕ Добавить пользователя")
        btn_add.setStyleSheet("background-color: #1565C0;")
        btn_add.clicked.connect(self._add_user_dialog)
        self.content_layout.addWidget(btn_add)

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["Логин", "ФИО", "Роль", "Создан"])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.setAlternatingRowColors(True)
        self.user_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.content_layout.addWidget(self.user_table, 1)

        self._load_users()

    def _load_users(self):
        self.user_table.setRowCount(0)
        users = db.get_users()

        for u in users:
            row = self.user_table.rowCount()
            self.user_table.insertRow(row)

            role = "Администратор" if u['role'] == 'admin' else "Охранник"
            created = datetime.strptime(u['created_at'], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")

            self.user_table.setItem(row, 0, QTableWidgetItem(u['username']))
            self.user_table.setItem(row, 1, QTableWidgetItem(u['full_name']))
            self.user_table.setItem(row, 2, QTableWidgetItem(role))
            self.user_table.setItem(row, 3, QTableWidgetItem(created))

    def _add_user_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить пользователя")
        dialog.setFixedSize(400, 280)
        dialog.setStyleSheet("""
            QDialog { background-color: #F5F5F5; }
            QLabel { color: #333333; }
            QLineEdit { background-color: white; color: #333333; border: 2px solid #CCCCCC; border-radius: 5px; padding: 8px; }
            QComboBox { background-color: white; color: #333333; border: 2px solid #CCCCCC; border-radius: 5px; padding: 6px; }
        """)

        layout = QGridLayout()
        layout.setSpacing(12)

        layout.addWidget(QLabel("Логин:*"), 0, 0)
        user_login = QLineEdit()
        layout.addWidget(user_login, 0, 1)

        layout.addWidget(QLabel("Пароль:*"), 1, 0)
        user_pass = QLineEdit()
        user_pass.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(user_pass, 1, 1)

        layout.addWidget(QLabel("ФИО:*"), 2, 0)
        user_name = QLineEdit()
        layout.addWidget(user_name, 2, 1)

        layout.addWidget(QLabel("Роль:"), 3, 0)
        user_role = QComboBox()
        user_role.addItems(["Охранник", "Администратор"])
        layout.addWidget(user_role, 3, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1B5E20;
            }
        """)
        buttons.accepted.connect(lambda: self._save_user(dialog, user_login, user_pass, user_name, user_role))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons, 4, 0, 1, 2)

        dialog.setLayout(layout)
        dialog.exec()

    def _save_user(self, dialog, login_field, pass_field, name_field, role_combo):
        username = login_field.text().strip()
        password = pass_field.text().strip()
        name = name_field.text().strip()
        role = "admin" if role_combo.currentIndex() == 1 else "guard"

        if not all([username, password, name]):
            QMessageBox.warning(self, "Внимание", "Заполните все поля!")
            return

        if db.create_user(username, password, role, name):
            QMessageBox.information(self, "Успех", "Пользователь создан!")
            dialog.accept()
            self._load_users()
        else:
            QMessageBox.warning(self, "Ошибка", "Такой логин уже существует!")

    def _show_statistics(self):
        if not auth.is_admin():
            return

        self._clear_content()

        title = QLabel("Статистика проходов")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1B5E20;")
        self.content_layout.addWidget(title)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("С:"))

        self.stat_date_from = QDateEdit()
        self.stat_date_from.setCalendarPopup(True)
        self.stat_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.stat_date_from.setDisplayFormat("yyyy-MM-dd")
        self.stat_date_from.setFixedWidth(120)
        filter_layout.addWidget(self.stat_date_from)

        filter_layout.addWidget(QLabel("По:"))
        self.stat_date_to = QDateEdit()
        self.stat_date_to.setCalendarPopup(True)
        self.stat_date_to.setDate(QDate.currentDate())
        self.stat_date_to.setDisplayFormat("yyyy-MM-dd")
        self.stat_date_to.setFixedWidth(120)
        filter_layout.addWidget(self.stat_date_to)

        btn_show = QPushButton("Показать")
        btn_show.setStyleSheet("background-color: #2E7D32;")
        btn_show.clicked.connect(self._load_statistics)
        filter_layout.addWidget(btn_show)

        filter_layout.addStretch()
        self.content_layout.addLayout(filter_layout)

        self.stat_container = QWidget()
        stat_layout = QVBoxLayout()
        self.stat_container.setLayout(stat_layout)
        self.content_layout.addWidget(self.stat_container)

        self._load_statistics()

    def _load_statistics(self):
        # Remove old container and create new one
        if hasattr(self, 'stat_container'):
            self.stat_container.deleteLater()
        
        self.stat_container = QWidget()
        stat_layout = QVBoxLayout()
        self.stat_container.setLayout(stat_layout)
        self.content_layout.addWidget(self.stat_container)

        date_from = self.stat_date_from.text().strip()
        date_to = self.stat_date_to.text().strip()

        stats = db.get_statistics(date_from, date_to)
        
        # Calculate additional stats
        from_days = max(1, (datetime.strptime(date_to, "%Y-%m-%d") - datetime.strptime(date_from, "%Y-%m-%d")).days + 1)
        avg_passes = stats['total_passes'] / from_days if from_days > 0 else 0
        in_passes = stats['total_passes'] // 2 if stats['total_passes'] > 0 else 0

        # Main cards row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        cards = [
            ("Всего проходов", str(stats['total_passes']), "#2E7D32"),
            ("Входов", str(in_passes), "#1565C0"),
            ("Уникальных сотрудников", str(stats['unique_employees']), "#7B1FA2"),
            ("Ср. проходов/день", f"{avg_passes:.1f}", "#E65100"),
        ]

        for text, value, color in cards:
            card = QFrame()
            card.setStyleSheet(f"background-color: {color}; border-radius: 15px;")
            card.setMinimumSize(180, 120)

            card_layout = QVBoxLayout()
            card_layout.setContentsMargins(20, 15, 20, 15)
            card_layout.setSpacing(5)

            val_lbl = QLabel(value)
            val_lbl.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
            val_lbl.setStyleSheet("color: white;")
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(val_lbl)

            txt_lbl = QLabel(text)
            txt_lbl.setFont(QFont("Segoe UI", 11))
            txt_lbl.setStyleSheet("color: white; opacity: 0.9;")
            txt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(txt_lbl)

            card.setLayout(card_layout)
            cards_layout.addWidget(card)

        stat_layout.addLayout(cards_layout)
        
        # Period info
        period_lbl = QLabel(f"Период: {date_from} — {date_to} ({from_days} дней)")
        period_lbl.setFont(QFont("Segoe UI", 10))
        period_lbl.setStyleSheet("color: #666666; padding: 10px 0;")
        stat_layout.addWidget(period_lbl)
        
        # Department stats section - only show if there are any passes
        has_passes = stats['total_passes'] > 0
        if has_passes and stats.get('department_stats'):
            dept_title = QLabel("Проходы по отделам")
            dept_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            dept_title.setStyleSheet("color: #1B5E20; padding-top: 15px;")
            stat_layout.addWidget(dept_title)
            
            dept_layout = QGridLayout()
            dept_layout.setSpacing(10)
            
            for i, dept in enumerate(stats['department_stats'][:8]):  # Top 8 departments
                dept_card = QFrame()
                dept_card.setStyleSheet("""
                    background-color: white;
                    border-radius: 8px;
                    border-left: 4px solid #2E7D32;
                """)
                dept_card.setMinimumHeight(60)
                
                dept_inner = QVBoxLayout()
                dept_inner.setContentsMargins(15, 10, 15, 10)
                
                dept_name = QLabel(dept['department'])
                dept_name.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
                dept_name.setStyleSheet("color: #333333;")
                dept_inner.addWidget(dept_name)
                
                dept_count = QLabel(f"{dept['count']} проходов")
                dept_count.setFont(QFont("Segoe UI", 10))
                dept_count.setStyleSheet("color: #666666;")
                dept_inner.addWidget(dept_count)
                
                dept_card.setLayout(dept_inner)
                dept_layout.addWidget(dept_card, i // 2, i % 2)
            
            stat_layout.addLayout(dept_layout)
        
        # Daily breakdown table
        daily_data = db.get_daily_pass_stats(date_from, date_to)
        if daily_data:
            daily_title = QLabel("Проходы по дням")
            daily_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            daily_title.setStyleSheet("color: #1B5E20; padding-top: 15px;")
            stat_layout.addWidget(daily_title)
            
            self.stat_daily_table = QTableWidget()
            self.stat_daily_table.setColumnCount(3)
            self.stat_daily_table.setHorizontalHeaderLabels(["Дата", "Проходов", "Сотрудников"])
            self.stat_daily_table.horizontalHeader().setStretchLastSection(True)
            self.stat_daily_table.setAlternatingRowColors(True)
            self.stat_daily_table.setMaximumHeight(250)
            self.stat_daily_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            
            for row_data in daily_data:
                row = self.stat_daily_table.rowCount()
                self.stat_daily_table.insertRow(row)
                self.stat_daily_table.setItem(row, 0, QTableWidgetItem(row_data['date']))
                self.stat_daily_table.setItem(row, 1, QTableWidgetItem(str(row_data['passes'])))
                self.stat_daily_table.setItem(row, 2, QTableWidgetItem(str(row_data['employees'])))
            
            stat_layout.addWidget(self.stat_daily_table)
        
        stat_layout.addStretch()

    def _on_logout(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Выход")
        msg.setText("Вы уверены, что хотите выйти?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setStyleSheet("""
            QMessageBox { background-color: white; }
            QMessageBox QLabel { color: #333333; font-size: 13px; }
            QMessageBox QPushButton { background-color: #2E7D32; color: white; border: none; border-radius: 5px; padding: 8px 20px; min-width: 80px; font-weight: bold; }
            QMessageBox QPushButton:hover { background-color: #1B5E20; }
        """)
        reply = msg.exec()

        if reply == QMessageBox.StandardButton.Yes:
            self.user_logged_out = True
            auth.logout()
            self.close()
