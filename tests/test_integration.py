import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestIntegration:
    """Интеграционные тесты, проверяющие взаимодействие компонентов"""
    
    @pytest.mark.nondestructive
    def test_full_user_workflow(self, browser, base_url, api_client):
        """Полный workflow - ИСПРАВЛЕНО"""
        # Шаг 1: Создаем пользователя через API
        user_data = {'name': 'Integration Test User', 'email': 'integration@test.com', 'department': 'Engineering'}
        api_response = api_client.post(f'{base_url}/api/users', json=user_data)
        assert api_response.status_code == 201
        created_user = api_response.json()
        
        # Шаг 2: Проверяем через API
        get_response = api_client.get(f'{base_url}/api/users/{created_user["id"]}')
        assert get_response.status_code == 200
        assert get_response.json()['name'] == user_data['name']
        
        # Шаг 3: Проверяем в UI
        browser.get(base_url)
        
        # Ожидаем новый заголовок
        WebDriverWait(browser, 10).until(
            EC.title_contains('User Management System')
        )
        
        # Проверяем что страница загрузилась
        assert 'User Management System' in browser.title
        
        # Проверяем что форма доступна
        name_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'name'))
        )
        assert name_input.is_enabled()
    
    @pytest.mark.parametrize('test_scenario', [
        {'api_first': True, 'ui_validation': True},
        {'api_first': False, 'ui_validation': True}
    ])
    def test_different_scenarios(self, browser, base_url, api_client, test_scenario):
        """Параметризированные интеграционные тесты - ИСПРАВЛЕНО"""
        if test_scenario['api_first']:
            # Сценарий 1: Сначала API, потом UI
            response = api_client.get(f'{base_url}/api/users')
            assert response.status_code == 200
            users_count = len(response.json())
            
            browser.get(base_url)
            WebDriverWait(browser, 10).until(
                EC.title_contains('User Management System')
            )
            assert 'User Management System' in browser.title
        
        else:
            # Сценарий 2: Сначала UI, потом API
            browser.get(base_url)
            WebDriverWait(browser, 10).until(
                EC.title_contains('User Management System')
            )
            assert 'User Management System' in browser.title
            
            response = api_client.get(f'{base_url}/api/users')
            assert response.status_code == 200

@pytest.mark.slow
class TestSlowIntegration:
    """Медленные интеграционные тесты"""
    
    def test_multiple_operations(self, browser, base_url, api_client):
        """Тест множественных операций - ИСПРАВЛЕНО"""
        # Сначала получаем текущее количество пользователей
        response = api_client.get(f'{base_url}/api/users')
        initial_count = len(response.json())
        
        # Создаем несколько пользователей
        users_to_create = 3
        for i in range(users_to_create):
            user_data = {'name': f'Test User {i}', 'email': f'test{i}@example.com', 'department': 'Engineering'}
            response = api_client.post(f'{base_url}/api/users', json=user_data)
            assert response.status_code == 201
        
        # Проверяем общее количество
        response = api_client.get(f'{base_url}/api/users')
        expected_count = initial_count + users_to_create
        assert len(response.json()) == expected_count
        
        # Проверяем UI - исправленный локатор
        browser.get(base_url)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'nav'))
        )
        
        # Ищем заголовок в навигации или в содержимом страницы
        nav_brand = browser.find_element(By.CLASS_NAME, 'navbar-brand')
        assert 'UserManager' in nav_brand.text