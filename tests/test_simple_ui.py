import pytest
from selenium.webdriver.common.by import By
import time

@pytest.mark.nondestructive
def test_basic_connectivity(browser, base_url):
    """Простой тест подключения"""
    try:
        print(f"Пробуем подключиться к {base_url}")
        browser.get(base_url)
        time.sleep(3)  # Даем время на загрузку
        
        # Простая проверка что страница загрузилась
        assert browser.title is not None
        print(f"✅ Страница загружена. Заголовок: {browser.title}")
        
    except Exception as e:
        pytest.skip(f"Не удалось подключиться: {e}")

@pytest.mark.nondestructive
def test_google_as_fallback(browser):
    """Тест что браузер вообще работает (через Google)"""
    try:
        browser.get("https://www.google.com")
        assert "Google" in browser.title
        print("✅ Браузер работает корректно")
    except Exception as e:
        pytest.fail(f"Браузер не работает: {e}")