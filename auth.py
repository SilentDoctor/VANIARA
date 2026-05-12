"""Аутентификация"""
from typing import Optional, Dict, Any
from database import db


class Auth:
    """Управление аутентификацией и сессией пользователя"""

    _current_user: Optional[Dict[str, Any]] = None

    @classmethod
    def login(cls, username: str, password: str) -> bool:
        user = db.authenticate(username, password)
        if user:
            cls._current_user = user
            return True
        return False

    @classmethod
    def logout(cls):
        cls._current_user = None

    @classmethod
    def get_current_user(cls) -> Optional[Dict[str, Any]]:
        return cls._current_user

    @classmethod
    def is_admin(cls) -> bool:
        return cls._current_user and cls._current_user.get('role') == 'admin'

    @classmethod
    def is_guard(cls) -> bool:
        return cls._current_user and cls._current_user.get('role') == 'guard'

    @classmethod
    def get_user_id(cls) -> Optional[int]:
        return cls._current_user.get('id') if cls._current_user else None

    @classmethod
    def get_user_full_name(cls) -> str:
        return cls._current_user.get('full_name', '') if cls._current_user else ''

    @classmethod
    def get_user_role_display(cls) -> str:
        role = cls._current_user.get('role', '') if cls._current_user else ''
        roles = {
            'admin': 'Администратор',
            'guard': 'Охранник'
        }
        return roles.get(role, role)


auth = Auth()