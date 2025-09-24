import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from app import app as flask_app
import threading
import time
import os
from datetime import datetime

"""
# в файле описаны Фикстуры для тестов с улучшенной обработкой ошибок и отчетами
# В этом файле опеределены фикстуры с разными областями видимости (scope) для оптимизации тестов то есть
# чтобы не запускать приложение и браузер заново для каждого теста
# Добавлены логи и создание папки для отчетов
# Улучшена фикстура app для запуска Flask приложения в отдельном потоке
# Добавлена фикстура base_url для динамического определения URL
# Добавлена фикстура сброса состояния с повторными попытками
# Улучшена фикстура browser с надежной установкой ChromeDriver
# Добавлена конфигурация для HTML отчетов
# Добавлен хук pytest_configure [он нужен для создания папки reports и для вывода итогов тестирования

"""
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
    """Запуск Flask приложения для тестов с улучшенной обработкой"""
    import socket
    from contextlib import closing
    
    def check_port(port):
        """Проверяет, свободен ли порт"""
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            return sock.connect_ex(('localhost', port)) == 0
    
    port = 5001
    
    # Проверяем, свободен ли порт
    if check_port(port):
        print(f"⚠️  Порт {port} занят. Пробуем использовать порт 5002...")
        port = 5002
        if check_port(port):
            raise Exception(f"Порты 5001 и 5002 заняты. Освободите порты или убейте процессы.")
    
    print(f"🚀 Запуск Flask приложения на порту {port}...")
    
    # Запускаем приложение в отдельном потоке
    thread = threading.Thread(
        target=lambda: flask_app.run(
            host='0.0.0.0',  # Разрешаем подключения с любых адресов
            port=port, 
            debug=False, 
            use_reloader=False,
            threaded=True  # Многопоточный режим
        )
    )
    thread.daemon = True
    thread.start()
    
    # Ждем пока приложение запустится (увеличиваем время ожидания)
    max_attempts = 10
    for i in range(max_attempts):
        try:
            response = requests.get(f'http://localhost:{port}/', timeout=2)
            if response.status_code == 200:
                print(f"✅ Flask приложение запущено на порту {port}")
                break
        except:
            if i < max_attempts - 1:
                time.sleep(1)
            else:
                print(f"❌ Не удалось запустить приложение на порту {port}")
                raise Exception(f"Flask приложение не запустилось за {max_attempts} секунд")
    
    yield flask_app
    
    # Останавливаем приложение (в теории, но на практике daemon thread сам завершится)
    print("🛑 Остановка Flask приложения...")

@pytest.fixture(scope='session')
def base_url(app):
    """Базовый URL с динамическим портом"""
    # Определяем порт на основе того, на каком порту запустилось приложение
    import re
    import requests
    
    # Пробуем разные порты
    for port in [5001, 5002, 5003]:
        try:
            response = requests.get(f'http://localhost:{port}/', timeout=1)
            if response.status_code == 200:
                return f'http://localhost:{port}'
        except:
            continue
    
    # Если не нашли работающий порт, используем по умолчанию
    return 'http://localhost:5001'

# @pytest.fixture(scope='session')
# def app():
#     """Упрощенная фикстура для Flask приложения"""
#     # Не запускаем приложение в отдельном потоке для UI тестов
#     # Вместо этого будем запускать приложение вручную при необходимости
#     return flask_app

# @pytest.fixture(scope='session')
# def base_url():
#     """Базовый URL - для UI тестов будем использовать внешний сервер"""
#     return 'http://localhost:5000'  # Предполагаем, что приложение запущено на порту 5000


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
    """Фикстура для браузера Selenium с надежной установкой"""
    try:
        # Настройки Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--log-level=3')
        
        # Автоматическая установка ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        
        print("✅ ChromeDriver успешно установлен и настроен")
        return driver
        
    except Exception as e:
        print(f"❌ Ошибка настройки браузера: {e}")
        pytest.skip(f"Браузер недоступен: {e}")


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

# ОБНОВЛЕННАЯ фикстура сброса состояния
@pytest.fixture(autouse=True)
def reset_state_before_tests(api_client, base_url):
    """Автоматически сбрасывает состояние перед каждым тестом"""
    print("\n" + "="*50)
    print("Подготовка к тесту...")
    
    # Ждем немного перед тестом
    time.sleep(0.5)
    
    yield  # здесь выполняется тест
    
    # Код после yield выполняется ПОСЛЕ теста
    print("Восстановление состояния...")
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = api_client.post(f'{base_url}/api/reset', timeout=5)
            if response.status_code == 200:
                print("✓ Данные успешно сброшены")
                break
            else:
                print(f"✗ Ошибка сброса: {response.status_code}")
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"✗ Попытка {attempt + 1} не удалась: {e}. Повторяем...")
                time.sleep(1)
            else:
                print(f"✗ Все попытки сброса не удались: {e}")
    print("="*50)