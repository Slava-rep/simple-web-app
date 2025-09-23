import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from app import app as flask_app
import threading
import time
import os
from datetime import datetime


#  в начало файла
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Создаем папку для отчетов если ее нет"""
    if not os.path.exists('reports'):
        os.makedirs('reports')

@pytest.fixture(scope="session", autouse=True)
def configure_html_report():
    """Конфигурация для HTML отчетов"""
    # Эта фикстура выполнится перед всеми тестами
    yield
    
    # Код после yield выполнится после всех тестов
    print("\n" + "="*60)
    print("📊 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("Отчет сохранен в: reports/pytest-report.html")
    print("="*60)

# Все фикстуры с правильными областями видимости
@pytest.fixture(scope='session')
def app():
    """Запуск Flask приложения для тестов (session scope)"""
    thread = threading.Thread(target=lambda: flask_app.run(port=5001, debug=False, use_reloader=False))
    thread.daemon = True
    thread.start()
    time.sleep(2)
    yield flask_app

@pytest.fixture(scope='session')
def base_url():
    """Базовый URL (session scope для совместимости с плагинами)"""
    return 'http://localhost:5001'

@pytest.fixture
def client(app):
    """Тестовый клиент для API (function scope)"""
    return app.test_client()

@pytest.fixture
def api_client(base_url):
    """Клиент для HTTP запросов (function scope)"""
    return requests.Session()

@pytest.fixture
def browser():
    """Фикстура для браузера Selenium с улучшенными настройками"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--log-level=3')  # Убирает большинство логов
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

@pytest.fixture
def user_data():
    """Параметризированные данные пользователей (function scope)"""
    return [
        {'name': 'Test User 1', 'email': 'test1@example.com'},
        {'name': 'Test User 2', 'email': 'test2@example.com'},
        {'name': 'Test User 3', 'email': 'test3@example.com'}
    ]

# Фикстуры для unit тестов
@pytest.fixture
def fresh_app():
    """Фикстура для чистого приложения"""
    from app import users
    original_users = users.copy()
    yield flask_app
    users.clear()
    users.extend(original_users)

@pytest.fixture
def test_user():
    """Фикстура с тестовым пользователем"""
    return {'id': 100, 'name': 'Test User', 'email': 'test@example.com'}

@pytest.fixture(autouse=True)
def reset_state_before_tests(api_client, base_url):
    """Автоматически сбрасывает состояние перед каждым тестом"""
    # Код до yield выполняется ПЕРЕД тестом
    print("\n" + "="*50)
    print("Подготовка к тесту...")
    
    yield  # здесь выполняется тест
    
    # Код после yield выполняется ПОСЛЕ теста
    print("Восстановление состояния...")
    try:
        response = api_client.post(f'{base_url}/api/reset')
        if response.status_code == 200:
            print("✓ Данные успешно сброшены")
        else:
            print(f"✗ Ошибка сброса: {response.status_code}")
    except Exception as e:
        print(f"✗ Исключение при сбросе: {e}")
    print("="*50)