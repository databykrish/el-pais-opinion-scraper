import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import re

USERNAME = "krishagaonkar_Fa1UnS"
ACCESS_KEY = "5ryZLMsCPePdpHqN2kda"

BROWSERSTACK_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# ✅ Create screenshots folder
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")
    print("✓ Created 'screenshots' directory")


browsers = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "Chrome - Windows 10"
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "Firefox - Windows 10"
    },
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "os": "OS X",
        "osVersion": "Monterey",
        "sessionName": "Safari - macOS"
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "realMobile": "true",
        "osVersion": "12.0",
        "sessionName": "Samsung Galaxy S22"
    },
    {
        "deviceName": "iPhone 14",
        "realMobile": "true",
        "osVersion": "16",
        "sessionName": "iPhone 14"
    }
]


# ✅ Safe filename generator
def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def run_test(cap):

    print(f"\n🚀 Starting → {cap['sessionName']}")

    options = Options()

    bstack_options = {
        "userName": USERNAME,
        "accessKey": ACCESS_KEY,
        "sessionName": cap["sessionName"]
    }

    options.set_capability("bstack:options", bstack_options)

    for key, value in cap.items():
        if key != "sessionName":
            options.set_capability(key, value)

    driver = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        options=options
    )

    filename = safe_filename(cap["sessionName"])

    try:
        driver.get("https://elpais.com/opinion/")
        time.sleep(5)

        print(f"🌍 {cap['sessionName']} → Loaded")
        print(f"📝 Title: {driver.title}")

        # ✅ Screenshot after successful load
        screenshot_path = f"screenshots/{filename}.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved → {screenshot_path}")

        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Page loaded successfully"}}'
        )

    except Exception as e:
        print(f"❌ {cap['sessionName']} → {e}")

        # ✅ Screenshot on failure
        error_screenshot = f"screenshots/{filename}_ERROR.png"
        driver.save_screenshot(error_screenshot)
        print(f"📸 Error screenshot saved → {error_screenshot}")

        driver.execute_script(
            f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"failed","reason": "{str(e)}"}}}}'
        )

    finally:
        driver.quit()
        print(f"✅ Finished → {cap['sessionName']}")


threads = []

for browser in browsers:
    thread = threading.Thread(target=run_test, args=(browser,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("\n🎯 All BrowserStack tests completed!")
