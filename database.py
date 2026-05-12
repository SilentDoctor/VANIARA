"""Модуль работы с базой данных SQLite"""
import sqlite3
import os
import bcrypt
from datetime import datetime
from typing import Optional, List, Dict, Any


class Database:
    def __init__(self, db_path: str = "geomach.db"):
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'guard')),
                full_name TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tab_number TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                photo_path TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pass_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                pass_type TEXT NOT NULL CHECK(pass_type IN ('in', 'out')),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                guard_id INTEGER NOT NULL,
                notes TEXT,
                FOREIGN KEY (employee_id) REFERENCES employees(id),
                FOREIGN KEY (guard_id) REFERENCES users(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                phone TEXT,
                organization TEXT,
                purpose TEXT,
                arrival_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                departure_time DATETIME,
                guard_id INTEGER NOT NULL,
                employee_visited_id INTEGER,
                FOREIGN KEY (guard_id) REFERENCES users(id),
                FOREIGN KEY (employee_visited_id) REFERENCES employees(id)
            )
        ''')

        conn.commit()
        self._create_default_admin()

    def _create_default_admin(self):
        cursor = self._get_connection().cursor()
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if cursor.fetchone() is None:
            password_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
                ("admin", password_hash.decode(), "admin", "Администратор")
            )
            self._get_connection().commit()

    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        cursor = self._get_connection().cursor()
        cursor.execute(
            "SELECT id, username, password_hash, role, full_name FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            return {
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'full_name': user['full_name']
            }
        return None

    def get_users(self) -> List[Dict[str, Any]]:
        cursor = self._get_connection().cursor()
        cursor.execute("SELECT id, username, role, full_name, created_at FROM users ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

    def create_user(self, username: str, password: str, role: str, full_name: str) -> bool:
        try:
            cursor = self._get_connection().cursor()
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
                (username, password_hash.decode(), role, full_name)
            )
            self._get_connection().commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_user_password(self, user_id: int, new_password: str) -> bool:
        try:
            cursor = self._get_connection().cursor()
            password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            cursor.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (password_hash.decode(), user_id)
            )
            self._get_connection().commit()
            return True
        except Exception:
            return False

    def delete_user(self, user_id: int) -> bool:
        try:
            cursor = self._get_connection().cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self._get_connection().commit()
            return True
        except Exception:
            return False

    def get_employees(self, active_only: bool = True) -> List[Dict[str, Any]]:
        cursor = self._get_connection().cursor()
        if active_only:
            cursor.execute("SELECT * FROM employees WHERE is_active = 1 ORDER BY full_name")
        else:
            cursor.execute("SELECT * FROM employees ORDER BY full_name")
        return [dict(row) for row in cursor.fetchall()]

    def get_employee_by_id(self, employee_id: int) -> Optional[Dict[str, Any]]:
        cursor = self._get_connection().cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def search_employees(self, query: str) -> List[Dict[str, Any]]:
        cursor = self._get_connection().cursor()
        search = f"%{query}%"
        cursor.execute(
            "SELECT * FROM employees WHERE is_active = 1 AND (full_name LIKE ? OR tab_number LIKE ?) ORDER BY full_name",
            (search, search)
        )
        return [dict(row) for row in cursor.fetchall()]

    def create_employee(self, tab_number: str, full_name: str, department: str, position: str) -> bool:
        try:
            cursor = self._get_connection().cursor()
            cursor.execute(
                "INSERT INTO employees (tab_number, full_name, department, position) VALUES (?, ?, ?, ?)",
                (tab_number, full_name, department, position)
            )
            self._get_connection().commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_employee(self, employee_id: int, full_name: str, department: str, position: str, is_active: bool) -> bool:
        try:
            cursor = self._get_connection().cursor()
            cursor.execute(
                "UPDATE employees SET full_name = ?, department = ?, position = ?, is_active = ? WHERE id = ?",
                (full_name, department, position, is_active, employee_id)
            )
            self._get_connection().commit()
            return True
        except Exception:
            return False

    def delete_employee(self, employee_id: int) -> bool:
        try:
            cursor = self._get_connection().cursor()
            cursor.execute("UPDATE employees SET is_active = 0 WHERE id = ?", (employee_id,))
            self._get_connection().commit()
            return True
        except Exception:
            return False

    def add_pass_log(self, employee_id: int, pass_type: str, guard_id: int, notes: str = None) -> bool:
        try:
            cursor = self._get_connection().cursor()
            cursor.execute(
                "INSERT INTO pass_logs (employee_id, pass_type, guard_id, notes) VALUES (?, ?, ?, ?)",
                (employee_id, pass_type, guard_id, notes)
            )
            self._get_connection().commit()
            return True
        except Exception:
            return False

    def get_pass_logs(self, date: str = None, employee_id: int = None) -> List[Dict[str, Any]]:
        cursor = self._get_connection().cursor()

        query = '''
            SELECT pl.*, e.full_name, e.tab_number, e.department,
                   u.full_name as guard_name
            FROM pass_logs pl
            JOIN employees e ON pl.employee_id = e.id
            JOIN users u ON pl.guard_id = u.id
            WHERE 1=1
        '''
        params = []

        if date:
            query += " AND DATE(pl.timestamp) = ?"
            params.append(date)

        if employee_id:
            query += " AND pl.employee_id = ?"
            params.append(employee_id)

        query += " ORDER BY pl.timestamp DESC"

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_today_pass_count(self) -> int:
        cursor = self._get_connection().cursor()
        cursor.execute("SELECT COUNT(*) FROM pass_logs WHERE DATE(timestamp) = DATE('now')")
        return cursor.fetchone()[0]

    def add_visitor(self, full_name: str, phone: str, organization: str, purpose: str,
                   guard_id: int, employee_visited_id: int = None) -> bool:
        try:
            cursor = self._get_connection().cursor()
            cursor.execute(
                """INSERT INTO visitors (full_name, phone, organization, purpose, guard_id, employee_visited_id)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (full_name, phone, organization, purpose, guard_id, employee_visited_id)
            )
            self._get_connection().commit()
            return True
        except Exception:
            return False

    def get_visitors(self, active_only: bool = True) -> List[Dict[str, Any]]:
        cursor = self._get_connection().cursor()

        if active_only:
            cursor.execute(
                """SELECT v.*, e.full_name as employee_name, u.full_name as guard_name
                   FROM visitors v
                   LEFT JOIN employees e ON v.employee_visited_id = e.id
                   JOIN users u ON v.guard_id = u.id
                   WHERE v.departure_time IS NULL
                   ORDER BY v.arrival_time DESC"""
            )
        else:
            cursor.execute(
                """SELECT v.*, e.full_name as employee_name, u.full_name as guard_name
                   FROM visitors v
                   LEFT JOIN employees e ON v.employee_visited_id = e.id
                   JOIN users u ON v.guard_id = u.id
                   ORDER BY v.arrival_time DESC"""
            )

        return [dict(row) for row in cursor.fetchall()]

    def checkout_visitor(self, visitor_id: int) -> bool:
        try:
            cursor = self._get_connection().cursor()
            cursor.execute(
                "UPDATE visitors SET departure_time = CURRENT_TIMESTAMP WHERE id = ?",
                (visitor_id,)
            )
            self._get_connection().commit()
            return True
        except Exception:
            return False

    def get_current_visitors_count(self) -> int:
        cursor = self._get_connection().cursor()
        cursor.execute("SELECT COUNT(*) FROM visitors WHERE departure_time IS NULL")
        return cursor.fetchone()[0]

    def get_statistics(self, start_date: str, end_date: str) -> Dict[str, Any]:
        cursor = self._get_connection().cursor()

        cursor.execute(
            """SELECT COUNT(*) FROM pass_logs
               WHERE DATE(timestamp) BETWEEN ? AND ?""",
            (start_date, end_date)
        )
        total_passes = cursor.fetchone()[0]

        cursor.execute(
            """SELECT COUNT(DISTINCT employee_id) FROM pass_logs
               WHERE DATE(timestamp) BETWEEN ? AND ?""",
            (start_date, end_date)
        )
        unique_employees = cursor.fetchone()[0]

        cursor.execute(
            """SELECT e.department, COUNT(*) as count
               FROM pass_logs pl
               JOIN employees e ON pl.employee_id = e.id
               WHERE DATE(pl.timestamp) BETWEEN ? AND ?
               GROUP BY e.department
               ORDER BY count DESC""",
            (start_date, end_date)
        )
        department_stats = [dict(row) for row in cursor.fetchall()]

        return {
            'total_passes': total_passes,
            'unique_employees': unique_employees,
            'department_stats': department_stats
        }

    def get_daily_pass_stats(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        cursor = self._get_connection().cursor()
        cursor.execute(
            """SELECT DATE(timestamp) as date, COUNT(*) as passes, COUNT(DISTINCT employee_id) as employees
               FROM pass_logs
               WHERE DATE(timestamp) BETWEEN ? AND ?
               GROUP BY DATE(timestamp)
               ORDER BY date DESC""",
            (start_date, end_date)
        )
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None


db = Database()