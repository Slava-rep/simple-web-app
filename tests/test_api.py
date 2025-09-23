import pytest
import requests

class TestAPI:
    """Тестирование API endpoints"""
    
    @pytest.mark.nondestructive
    @pytest.mark.parametrize('expected_count', [2])
    def test_get_users(self, client, expected_count):
        """Тест получения списка пользователей"""
        response = client.get('/api/users')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == expected_count
        assert all('id' in user and 'name' in user and 'email' in user for user in data)
    
    # ИСПРАВЛЕННЫЕ ТЕСТЫ - обновленные имена
    @pytest.mark.nondestructive
    @pytest.mark.parametrize('user_id,expected_name', [
        (1, 'Alice Johnson'),  # ← ИСПРАВЛЕНО
        (2, 'Bob Smith')       # ← ИСПРАВЛЕНО
    ])
    def test_get_user_by_id(self, client, user_id, expected_name):
        """Параметризированный тест получения пользователя по ID"""
        response = client.get(f'/api/users/{user_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == expected_name
    
    @pytest.mark.nondestructive
    @pytest.mark.parametrize('name,email', [
        ('Charlie', 'charlie@test.com'),
        ('Diana', 'diana@test.com')
    ])
    def test_create_user(self, client, name, email):
        """Тест создания пользователя с параметризацией"""
        user_data = {'name': name, 'email': email}
        response = client.post('/api/users', json=user_data)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == name
        assert data['email'] == email
        assert 'id' in data
    
    @pytest.mark.nondestructive
    def test_create_user_invalid_data(self, client):
        """Тест создания пользователя с невалидными данными"""
        response = client.post('/api/users', json={})
        assert response.status_code == 400
    
    @pytest.mark.nondestructive
    @pytest.mark.parametrize('invalid_id', [999, 0, -1])
    def test_get_nonexistent_user(self, client, invalid_id):
        """Тест получения несуществующего пользователя"""
        response = client.get(f'/api/users/{invalid_id}')
        assert response.status_code == 404