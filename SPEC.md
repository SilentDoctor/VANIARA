# VANIARA - Система Контроля Доступа для Геомаш

## 1. Project Overview

**Type**: Desktop Application (Python + SQLite)  
**Purpose**: Система контроля доступа для сотрудников и посетителей предприятия  
**Users**: Администраторы, Охранники

## 2. User Roles

### Охранник
- Просмотр журнала проходов
- Регистрация посетителей (приход/уход)
- Поиск сотрудника по ФИО/табелю
- Отметка опозданий

### Администратор
- Все функции охранника
- Управление сотрудниками (добавление/редактирование/удаление)
- Управление пользователями системы (охранники)
- Просмотр статистики проходов
- Экспорт отчётов

## 3. UI/UX Design

### Login Window
- Поля: Логин, Пароль
- Кнопка "Войти"
- Логотип компании

### Main Window (after login)
- Верхняя панель: логотип, роль пользователя, кнопка выхода
- Боковое меню (sidebar)
- Основная область контента

### Color Scheme
- Primary: #2E7D32 (зелёный - Геомаш)
- Secondary: #1565C0 (синий)
- Background: #F5F5F5
- Text: #212121
- Accent: #FF6F00 (оранжевый для предупреждений)

### Typography
- Headers: Segoe UI Bold
- Body: Segoe UI Regular

## 4. Database Schema (SQLite)

### users
- id (INTEGER PRIMARY KEY)
- username (TEXT UNIQUE)
- password_hash (TEXT)
- role (TEXT: 'admin'/'guard')
- full_name (TEXT)
- created_at (DATETIME)

### employees
- id (INTEGER PRIMARY KEY)
- tab_number (TEXT UNIQUE)
- full_name (TEXT)
- department (TEXT)
- position (TEXT)
- photo_path (TEXT, nullable)
- is_active (BOOLEAN)

### pass_logs
- id (INTEGER PRIMARY KEY)
- employee_id (INTEGER FK)
- pass_type (TEXT: 'in'/'out')
- timestamp (DATETIME)
- guard_id (INTEGER FK)
- notes (TEXT, nullable)

### visitors
- id (INTEGER PRIMARY KEY)
- full_name (TEXT)
- phone (TEXT)
- organization (TEXT)
- purpose (TEXT)
- arrival_time (DATETIME)
- departure_time (DATETIME, nullable)
- guard_id (INTEGER FK)
- employee_visited_id (INTEGER FK, nullable)

## 5. Core Features

### Authentication
- Login with username/password
- Session management
- Password hashing (bcrypt)
- Role-based access

### Журнал проходов
- Список проходов за день
- Фильтры по дате, сотруднику
- Поиск по ФИО/табелю

### Регистрация посетителей
- Форма регистрации
- Автоматическая отметка времени
- Отметка ухода

### Управление сотрудниками (Admin)
- CRUD операции
- Поиск
- Импорт из CSV (future)

### Статистика (Admin)
- Количество проходов за период
- График посещаемости
- Список опоздавших

## 6. Technical Stack

- Python 3.10+
- Tkinter (GUI)
- SQLite3
- bcrypt (password hashing)
- matplotlib (графики)
