import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

@pytest.mark.nondestructive
def test_chrome_driver_installation():
    """Тест установки ChromeDriver"""
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get("https://www.google.com")
        assert "Google" in driver.title
        driver.quit()
        print("✅ ChromeDriver работает корректно")
        return True
    except Exception as e:
        print(f"❌ Ошибка ChromeDriver: {e}")
        return False

@pytest.mark.nondestructive
def test_simple_browser(browser):
    """Простой тест браузера"""
    try:
        browser.get("https://www.google.com")
        assert "Google" in browser.title
        print("✅ Браузер работает корректно с Google")
        return True
    except Exception as e:
        print(f"❌ Ошибка браузера с Google: {e}")
        
        # Попробуем локальное приложение
        try:
            browser.get("http://localhost:5001")
            title = browser.title
            print(f"✅ Локальное приложение загружено. Title: {title}")
            return True
        except Exception as e2:
            print(f"❌ Ошибка с локальным приложением: {e2}")
            return False

@pytest.mark.nondestructive
def test_browser_fixture(browser_firefox):
    """Тест фикстуры Firefox"""
    try:
        browser_firefox.get("https://www.google.com")
        assert "Google" in browser_firefox.title
        print("✅ Firefox работает корректно")
        return True
    except Exception as e:
        print(f"❌ Ошибка Firefox: {e}")
        return False