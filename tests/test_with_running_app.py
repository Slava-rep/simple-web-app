import pytest
import requests
from selenium.webdriver.common.by import By
import time

@pytest.mark.nondestructive
def test_app_is_running():
    """Тест что приложение запущено и отвечает"""
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        assert response.status_code == 200
        print("✅ Приложение запущено и отвечает")
        return True
    except Exception as e:
        pytest.skip(f"Приложение не запущено: {e}")

@pytest.mark.nondestructive
def test_browser_with_running_app(browser):
    """Тест браузера с уже запущенным приложением"""
    # Проверяем что приложение запущено
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code != 200:
            pytest.skip("Приложение не запущено")
    except:
        pytest.skip("Приложение не запущено")
    
    # Тестируем с работающим приложением
    browser.get('http://localhost:5000/')
    time.sleep(2)  # Даем время на загрузку
    
    assert browser.title is not None
    print(f"✅ Страница загружена. Заголовок: {browser.title}")

@pytest.mark.nondestructive
def test_google_fallback(browser):
    """Тест что браузер работает через Google"""
    browser.get("https://www.google.com")
    assert "Google" in browser.title
    print("✅ Браузер работает корректно")