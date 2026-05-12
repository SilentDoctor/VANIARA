"""Скрипт для добавления тестовых данных"""
from database import db
from datetime import datetime, timedelta
import sqlite3


def init_test_data():
    """Добавление тестовых данных"""
    print("Добавление тестовых данных...")

    # Создаем охранника
    try:
        db.create_user("guard1", "guard123", "guard", "Иванов Иван Петрович")
        print("Охранник создан: guard1 / guard123")
    except:
        print("Охранник уже существует")

    # Создаем сотрудников
    employees = [
        ("001", "Петров Сергей Алексеевич", "Бухгалтерия", "Бухгалтер"),
        ("002", "Сидорова Анна Владимировна", "Отдел кадров", "Инспектор"),
        ("003", "Козлов Дмитрий Иванович", "IT-отдел", "Сисадмин"),
    ]

    for tab, name, dept, pos in employees:
        try:
            db.create_employee(tab, name, dept, pos)
        except:
            pass

    print(f"Добавлено {len(employees)} сотрудников")

    # Получаем ID охранника
    users = db.get_users()
    guard = next((u for u in users if u['username'] == 'guard1'), None)
    guard_id = guard['id'] if guard else 1

    # Добавляем посетителей
    visitors = [
        ("Смирнов Алексей", "+79001234567", "ООО Ромашка", "Встреча с бухгалтером", "002"),
        ("Волков Кирилл", "+79009876543", "ИП Петров", "Доставка документов", "003"),
    ]

    for name, phone, org, purpose, emp_id in visitors:
        try:
            db.add_visitor(name, phone, org, purpose, guard_id, int(emp_id))
        except:
            pass

    print(f"Добавлено {len(visitors)} посетителей")

    # Добавляем проходы
    employees_list = db.get_employees()
    if employees_list:
        for emp in employees_list[:2]:
            db.add_pass_log(emp['id'], 'in', guard_id)

        # Проход за вчера
        conn = sqlite3.connect("geomach.db")
        cursor = conn.cursor()
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 08:30:00")
        cursor.execute(
            "INSERT INTO pass_logs (employee_id, pass_type, timestamp, guard_id) VALUES (?, ?, ?, ?)",
            (employees_list[0]['id'], 'in', yesterday, guard_id)
        )
        conn.commit()
        conn.close()
        print("Добавлены тестовые проходы")

    print("\nТестовые данные готовы!")
    print("\nТестовые пользователи:")
    print("  admin / admin123 (админ)")
    print("  guard1 / guard123 (охранник)")


if __name__ == "__main__":
    init_test_data()
    db.close()