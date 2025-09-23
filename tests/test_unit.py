import pytest
from app import app, users

@pytest.mark.unit
@pytest.mark.nondestructive  # ← ДОБАВЬТЕ ЭТОТ МАРКЕР
class TestUnit:
    """Unit тесты для отдельных компонентов приложения"""
    
    @pytest.mark.nondestructive  # ← И ДЛЯ КАЖДОГО МЕТОДА
    def test_users_list_initialization(self):
        """Тест инициализации списка пользователей"""
        assert len(users) == 2
        assert users[0]['name'] == 'Alice'
        assert users[1]['email'] == 'bob@test.com'
    
    @pytest.mark.nondestructive
    @pytest.mark.parametrize('user_id,expected', [
        (1, True),
        (2, True),
        (3, False),
        (999, False)
    ])
    def test_find_user_by_id(self, user_id, expected):
        """Параметризированный тест поиска пользователя по ID"""
        user_found = any(user['id'] == user_id for user in users)
        assert user_found == expected

@pytest.mark.unit
@pytest.mark.nondestructive
def test_simple_unit():
    """Простой unit тест"""
    assert 1 + 1 == 2

@pytest.mark.unit
@pytest.mark.nondestructive
@pytest.mark.parametrize('a,b,expected', [
    (1, 1, 2),
    (2, 3, 5)
])
def test_parametrized_unit(a, b, expected):
    """Параметризированный unit тест"""
    assert a + b == expected