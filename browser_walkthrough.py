"""Browser walkthrough script for SachPatra.
Uses Selenium Chrome headless to thoroughly exercise every UI flow,
validate layouts at 1280px and 375px, check Devanagari/Gurmukhi rendering,
and capture screenshots for review.
"""

import os
import shutil
import sys
import threading
import time
import urllib.request
from PIL import Image, ImageDraw, ImageFont
import uvicorn
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Ensure sachpatra app is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from app.main import app

ARTIFACT_DIR = r"C:\Users\sidak\.gemini\antigravity\brain\35d8beac-67af-4ddc-b468-cf425363c059"
SCREENSHOTS_DIR = os.path.join(CURRENT_DIR, "screenshots")
PORT = 8765
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


def create_sample_notice_image(path):
    img = Image.new("RGB", (600, 400), color="#ffffff")
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 590, 390], outline="#0a192f", width=4)
    draw.text((40, 40), "CENTRAL BUREAU OF INVESTIGATION (CBI)", fill="#990000")
    draw.text((40, 80), "NOTICE OF DIGITAL ARREST", fill="#000000")
    draw.text((40, 130), "Allegation: Money Laundering & Contraband Courier", fill="#333333")
    draw.text((40, 170), "You are directed to stay on continuous video call.", fill="#333333")
    draw.text((40, 210), "Transfer security deposit to safe account: Rs 50,000", fill="#990000")
    draw.rectangle([400, 260, 540, 350], outline="#990000", width=2)
    draw.text((420, 290), "OFFICIAL SEAL\nCBI DELHI", fill="#990000")
    img.save(path, format="JPEG")


def safe_click(driver, el):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", el)


def main():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    print(f"Starting SachPatra server on {BASE_URL}...")
    server = UvicornServerThread()
    server.start()

    if not wait_for_server(BASE_URL):
        print("Failed to start server within timeout.")
        sys.exit(1)
    print("Server is UP and healthy!")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--force-device-scale-factor=1")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        # =====================================================================
        # 1. Desktop Walkthrough (1280 x 900)
        # =====================================================================
        driver.set_window_size(1280, 900)
        driver.get(BASE_URL)
        time.sleep(1)

        print("Testing Desktop English Home...")
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_01_english_home.png"))

        # Language Switch: Hindi
        print("Testing Hindi Switch...")
        btn_hi = driver.find_element(By.XPATH, "//button[@data-lang='hi']")
        safe_click(driver, btn_hi)
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_02_hindi_home.png"))

        # Language Switch: Punjabi
        print("Testing Punjabi Switch...")
        btn_pa = driver.find_element(By.XPATH, "//button[@data-lang='pa']")
        safe_click(driver, btn_pa)
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_03_punjabi_home.png"))

        # Switch back to English for standard flow
        btn_en = driver.find_element(By.XPATH, "//button[@data-lang='en']")
        safe_click(driver, btn_en)
        time.sleep(0.5)

        # Click Sample Chip: "CBI Digital Arrest"
        print("Testing Sample Chip: CBI Digital Arrest...")
        chip_cbi = driver.find_element(By.XPATH, "//button[@data-sample='scam_cbi']")
        safe_click(driver, chip_cbi)
        time.sleep(0.3)

        # Click "Check for Digital Arrest" button
        btn_analyze = driver.find_element(By.ID, "btn-analyze")
        safe_click(driver, btn_analyze)

        # Wait for result container
        wait.until(EC.visibility_of_element_located((By.ID, "result-container")))
        time.sleep(1)

        # Check action checklist boxes (steps 1 and 2)
        chk_1 = driver.find_element(By.ID, "step-check-1")
        chk_2 = driver.find_element(By.ID, "step-check-2")
        safe_click(driver, chk_1)
        safe_click(driver, chk_2)

        # Capture Desktop Scam Result (verdict card + score meter)
        driver.execute_script("document.getElementById('result-container').scrollIntoView({block: 'start'});")
        time.sleep(0.5)
        print("Captured Desktop Scam Result...")
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_04_scam_result.png"))

        # Switch Draft Tab to "1930 Call Script"
        tab_script = driver.find_element(By.XPATH, "//button[@data-draft='script']")
        safe_click(driver, tab_script)
        time.sleep(0.3)

        # Click Copy Draft button
        btn_copy = driver.find_element(By.ID, "btn-copy-draft")
        safe_click(driver, btn_copy)
        time.sleep(0.5)

        driver.execute_script("document.querySelector('.drafts-card').scrollIntoView({block: 'center'});")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_04b_drafts.png"))

        # Test Benign Sample Chip: Normal Bank OTP
        print("Testing Benign OTP Sample...")
        chip_otp = driver.find_element(By.XPATH, "//button[@data-sample='benign_otp']")
        safe_click(driver, chip_otp)
        time.sleep(0.3)
        safe_click(driver, btn_analyze)
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_05_benign_result.png"))

        # Test Empty Error State
        print("Testing Empty Input Error...")
        btn_clear = driver.find_element(By.ID, "btn-clear-text")
        safe_click(driver, btn_clear)
        time.sleep(0.3)
        safe_click(driver, btn_analyze)
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_06_error_toast.png"))

        # Test Image Mode with upload preview
        print("Testing Image Mode Upload...")
        mode_img = driver.find_element(By.XPATH, "//button[@data-mode='image']")
        safe_click(driver, mode_img)
        time.sleep(0.5)

        sample_img_path = os.path.join(CURRENT_DIR, "sample_notice.jpg")
        create_sample_notice_image(sample_img_path)
        file_input = driver.find_element(By.ID, "file-input")
        file_input.send_keys(sample_img_path)
        time.sleep(0.8)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_07_image_preview.png"))

        # Test Dashboard Tab
        print("Testing Dashboard Tab...")
        tab_dash = driver.find_element(By.XPATH, "//button[@data-tab='tab-dashboard']")
        safe_click(driver, tab_dash)
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_08_dashboard.png"))

        # Test How It Works / Transparency Tab
        print("Testing Transparency Tab...")
        tab_trans = driver.find_element(By.XPATH, "//button[@data-tab='tab-transparency']")
        safe_click(driver, tab_trans)
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "desktop_09_transparency.png"))

        # =====================================================================
        # 2. Mobile Walkthrough (375 x 812 - iPhone SE / Modern Mobile)
        # =====================================================================
        print("Switching to Mobile Viewport (375x812)...")
        driver.set_window_size(375, 812)
        time.sleep(0.5)

        # Check Tab Mobile
        tab_check = driver.find_element(By.XPATH, "//button[@data-tab='tab-check']")
        safe_click(driver, tab_check)
        driver.execute_script("document.getElementById('result-container').classList.add('hidden'); document.getElementById('input-text').value = '';")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "mobile_01_home_375px.png"))

        # Mobile Hindi
        safe_click(driver, btn_hi)
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "mobile_02_hindi_375px.png"))

        # Mobile Punjabi
        safe_click(driver, btn_pa)
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "mobile_03_punjabi_375px.png"))

        # Mobile Scam Result
        safe_click(driver, btn_en)
        time.sleep(0.3)
        chip_cbi = driver.find_element(By.XPATH, "//button[@data-sample='scam_cbi']")
        safe_click(driver, chip_cbi)
        time.sleep(0.3)
        safe_click(driver, btn_analyze)
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "mobile_04_scam_result_375px.png"))

        # Mobile Dashboard
        safe_click(driver, tab_dash)
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, "mobile_05_dashboard_375px.png"))

        print("All browser steps completed successfully!")

        # Copy screenshots to artifact directory
        for f in os.listdir(SCREENSHOTS_DIR):
            if f.endswith(".png"):
                src = os.path.join(SCREENSHOTS_DIR, f)
                dst = os.path.join(ARTIFACT_DIR, f)
                shutil.copy2(src, dst)
        print(f"Screenshots copied to artifact directory: {ARTIFACT_DIR}")

    finally:
        driver.quit()
        server.stop()


if __name__ == "__main__":
    main()
