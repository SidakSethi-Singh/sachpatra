"""Headless browser test verifying UI resilience against XSS payloads and empty stats charts."""

import os
import sys
import threading
import time
import urllib.request
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uvicorn

from app.main import app

PORT = 8769
BASE_URL = f"http://127.0.0.1:{PORT}"


class UvicornServerThread(threading.Thread):
    def __init__(self, host="127.0.0.1", port=PORT):
        super().__init__(daemon=True)
        config = uvicorn.Config(app, host=host, port=port, log_level="warning")
        self.server = uvicorn.Server(config)

    def run(self):
        self.server.run()

    def stop(self):
        self.server.should_exit = True


def wait_for_server(url, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(f"{url}/api/health") as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.3)
    return False


def test_ui_xss_and_empty_dashboard():
    """Verify that XSS injections do NOT execute in the browser DOM and stats work on empty data."""
    server = UvicornServerThread()
    server.start()
    try:
        assert wait_for_server(BASE_URL), "Server failed to start"

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(BASE_URL)
            time.sleep(1)

            # 1. Inject sentinel for XSS tracking
            driver.execute_script("window.__xss_executed = false;")

            # 2. Input malicious XSS payload in textarea
            xss_payload = '<script>window.__xss_executed = true;</script><img src=x onerror="window.__xss_executed = true;"> CBI digital arrest notice pay 50000 rupees to safe account.'
            input_box = driver.find_element(By.ID, "input-text")
            input_box.clear()
            input_box.send_keys(xss_payload)

            # 3. Submit analysis
            btn_analyze = driver.find_element(By.ID, "btn-analyze")
            driver.execute_script("arguments[0].click();", btn_analyze)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "result-container"))
            )
            time.sleep(1)

            # Assert XSS was NOT executed
            xss_result = driver.execute_script("return window.__xss_executed;")
            assert xss_result is False, "XSS payload executed in browser DOM!"

            # Assert no unexpected alert dialogs
            try:
                alert = driver.switch_to.alert
                alert_text = alert.text
                alert.dismiss()
                pytest.fail(f"Unexpected alert popup opened by XSS payload: {alert_text}")
            except Exception:
                pass  # No alert, as expected

            # 4. Test Dashboard empty state handling
            tab_dash = driver.find_element(By.XPATH, "//button[@data-tab='tab-dashboard']")
            driver.execute_script("arguments[0].click();", tab_dash)
            time.sleep(1)

            # Check that dashboard renders without JavaScript errors
            dash_title = driver.find_element(By.CLASS_NAME, "dash-title")
            assert dash_title.is_displayed()

            # Ensure charts container exists and has valid DOM content
            chart_container = driver.find_element(By.ID, "chart-verdicts-container")
            assert len(chart_container.text) > 0 or chart_container.find_elements(By.TAG_NAME, "svg") or chart_container.find_elements(By.TAG_NAME, "p")

        finally:
            driver.quit()
    finally:
        server.stop()
