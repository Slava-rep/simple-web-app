import pytest
import requests
from selenium.webdriver.common.by import By

class TestIntegration:
    """Интеграционные тесты, проверяющие взаимодействие компонентов"""
    
    @pytest.mark.nondestructive
    def test_full_user_workflow(self, browser, base_url, api_client):
        """Полный workflow: создание пользователя через API + проверка в UI"""
        user_data = {'name': 'Integration Test User', 'email': 'integration@test.com'}
        api_response = api_client.post(f'{base_url}/api/users', json=user_data)
        assert api_response.status_code == 201
        created_user = api_response.json()
        
        get_response = api_client.get(f'{base_url}/api/users/{created_user["id"]}')
        assert get_response.status_code == 200
        assert get_response.json()['name'] == user_data['name']
        
        browser.get(base_url)
        assert 'Test App' in browser.title
        
        name_input = browser.find_element(By.ID, 'name')
        assert name_input.is_enabled()
    
    @pytest.mark.nondestructive
    @pytest.mark.parametrize('test_scenario', [
        {'api_first': True, 'ui_validation': True},
        {'api_first': False, 'ui_validation': True}
    ])
    def test_different_scenarios(self, browser, base_url, api_client, test_scenario):
        """Параметризированные интеграционные тесты разных сценариев"""
        if test_scenario['api_first']:
            response = api_client.get(f'{base_url}/api/users')
            assert response.status_code == 200
            users_count = len(response.json())
            
            browser.get(base_url)
            assert browser.current_url == f'{base_url}/'
        
        else:
            browser.get(base_url)
            assert 'Test App' in browser.title
            
            response = api_client.get(f'{base_url}/api/users')
            assert response.status_code == 200

@pytest.mark.slow
@pytest.mark.nondestructive
class TestSlowIntegration:
    """Медленные интеграционные тесты"""
    
    def test_multiple_operations(self, browser, base_url, api_client):
        """Тест множественных операций - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        # Сначала получаем текущее количество пользователей
        response = api_client.get(f'{base_url}/api/users')
        initial_count = len(response.json())
        
        # Создаем несколько пользователей
        users_to_create = 3
        for i in range(users_to_create):
            user_data = {'name': f'Test User {i}', 'email': f'test{i}@example.com'}
            response = api_client.post(f'{base_url}/api/users', json=user_data)
            assert response.status_code == 201
        
        # Проверяем общее количество (начальное + созданные)
        response = api_client.get(f'{base_url}/api/users')
        expected_count = initial_count + users_to_create
        assert len(response.json()) == expected_count
        
        # Проверяем UI
        browser.get(base_url)
        assert browser.find_element(By.TAG_NAME, 'h1').text == 'Welcome to Test App'