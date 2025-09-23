import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUI:
    """Тестирование пользовательского интерфейса"""
    
    @pytest.mark.nondestructive
    def test_home_page_loads(self, browser, base_url):
        """Тест загрузки домашней страницы"""
        browser.get(base_url)
        
        assert 'Test App' in browser.title
        
        h1_element = browser.find_element(By.TAG_NAME, 'h1')
        assert h1_element.text == 'Welcome to Test App'
        
        name_input = browser.find_element(By.ID, 'name')
        email_input = browser.find_element(By.ID, 'email')
        submit_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        assert name_input.is_displayed()
        assert email_input.is_displayed()
        assert submit_button.is_displayed()
    
    @pytest.mark.nondestructive
    @pytest.mark.parametrize('name,email', [
        ('John Doe', 'john@example.com'),
        ('Jane Smith', 'jane@example.com')
    ])
    def test_form_submission(self, browser, base_url, name, email):
        """Параметризированный тест отправки формы"""
        browser.get(base_url)
        
        name_input = browser.find_element(By.ID, 'name')
        email_input = browser.find_element(By.ID, 'email')
        
        name_input.send_keys(name)
        email_input.send_keys(email)
        
        submit_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        WebDriverWait(browser, 5).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Welcome to Test App')
        )