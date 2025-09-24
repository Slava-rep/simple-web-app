import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class TestAdvancedUI:
    """Расширенные UI тесты для нового интерфейса"""
    
    @pytest.mark.nondestructive
    def test_bootstrap_elements(self, browser, base_url):
        """Тест наличия Bootstrap элементов"""
        browser.get(base_url)
        
        # Проверяем навигацию
        navbar = browser.find_element(By.TAG_NAME, 'nav')
        assert 'navbar' in navbar.get_attribute('class')
        
        # Проверяем карточки статистики
        stats_cards = browser.find_elements(By.CLASS_NAME, 'stats-card')
        assert len(stats_cards) > 0
        
        # Проверяем таблицу
        table = browser.find_element(By.ID, 'users-table')
        assert table.is_displayed()
    
    @pytest.mark.nondestructive
    def test_user_interface_flow(self, browser, base_url):
        """Полный тест пользовательского интерфейса"""
        browser.get(base_url)
        
        # Заполняем форму логина
        username_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'login-username'))
        )
        password_input = browser.find_element(By.ID, 'login-password')
        login_button = browser.find_element(By.CSS_SELECTOR, '#login-form button[type="submit"]')
        
        username_input.send_keys('testuser')
        password_input.send_keys('password')
        
        # Кликаем через JavaScript
        browser.execute_script("arguments[0].click();", login_button)
        
        # Ждем обновления интерфейса
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'toast'))
        )
    
    @pytest.mark.nondestructive
    @pytest.mark.parametrize('name,email,department', [
        ('John Doe', 'john@example.com', 'Engineering'),
        ('Jane Smith', 'jane@example.com', 'Marketing')
    ])
    def test_add_user_with_department(self, browser, base_url, name, email, department):
        """Тест добавления пользователя с отделом - ИСПРАВЛЕНО"""
        browser.get(base_url)
        
        # Ждем загрузки формы
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'name'))
        )
        
        # Заполняем форму
        name_input = browser.find_element(By.ID, 'name')
        email_input = browser.find_element(By.ID, 'email')
        department_select = browser.find_element(By.ID, 'department')
        
        name_input.send_keys(name)
        email_input.send_keys(email)
        
        # Выбираем отдел
        select = Select(department_select)
        select.select_by_visible_text(department)
        
        # Находим и кликаем кнопку
        submit_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#user-form button[type="submit"]'))
        )
        browser.execute_script("arguments[0].click();", submit_button)
        
        # Проверяем уведомление
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'toast'))
        )
    
    @pytest.mark.nondestructive
    def test_table_interaction(self, browser, base_url):
        """Тест взаимодействия с таблицей - ИСПРАВЛЕНО"""
        browser.get(base_url)
        
        # Ждем загрузки таблицы
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.ID, 'users-tbody'))
        )
        
        # Даем время для загрузки данных через JavaScript
        import time
        time.sleep(2)
        
        # Проверяем наличие строк таблицы
        rows = browser.find_elements(By.CSS_SELECTOR, '#users-tbody tr')
        assert len(rows) > 0
        
        # Проверяем кнопки действий
        action_buttons = browser.find_elements(By.CSS_SELECTOR, '.btn-outline-primary, .btn-outline-danger')
        assert len(action_buttons) >= 2  # Кнопки edit/delete

class TestSessionManagement:
    """Тесты управления сессиями"""
    
    @pytest.mark.nondestructive
    def test_login_logout_flow(self, client):
        """Тест цикла логин/логаут"""
        # Логин
        response = client.post('/api/login', json={'username': 'testuser'})
        assert response.status_code == 200
        assert response.get_json()['status'] == 'success'
        
        # Логаут
        response = client.post('/api/logout')
        assert response.status_code == 200
        assert response.get_json()['status'] == 'success'