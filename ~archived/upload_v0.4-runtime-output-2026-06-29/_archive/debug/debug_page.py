from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import json

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 启用性能日志，用于监控网络请求
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

from main import load_cookies_from_netscape_file
driver.get("https://fc2ppvdb.com")
time.sleep(2)

cookie_file = "fc2ppvdb.com_cookies.txt"
if os.path.exists(cookie_file):
    cookies = load_cookies_from_netscape_file(cookie_file)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except:
            pass
    print(f"Loaded {len(cookies)} cookies")

driver.get("https://fc2ppvdb.com/cookie/setage")
time.sleep(3)
try:
    btn = driver.find_element(By.CSS_SELECTOR, "a.text-white, button.text-white")
    print(f"Found button: tag={btn.tag_name} text={btn.text[:30]}")
    btn.click()
except Exception as e:
    print("Click failed:", e)
time.sleep(2)

# 开始监控网络
driver.execute_cdp_cmd("Network.enable", {})
network_log = []

driver.get("https://fc2ppvdb.com/actresses/6061?page=1")
print("Page opened, waiting 10s for AJAX...")
time.sleep(10)

# 收集网络日志
logs = driver.get_log("performance")
for entry in logs:
    try:
        msg = json.loads(entry["message"])["message"]
        if msg["method"] in ("Network.responseReceived", "Network.requestWillBeSent"):
            if msg["method"] == "Network.responseReceived":
                resp = msg["params"]["response"]
                url = resp["url"]
                status = resp["status"]
                if "fc2ppvdb" in url and "actress" in url.lower():
                    print(f"  [RESPONSE] {status} {url}")
            elif msg["method"] == "Network.requestWillBeSent":
                req = msg["params"]["request"]
                url = req["url"]
                if "fc2ppvdb" in url and any(k in url.lower() for k in ["actress", "article", "api"]):
                    print(f"  [REQUEST]  {req['method']} {url}")
    except:
        pass

print("\n--- actress-articles content ---")
els = driver.find_elements(By.ID, "actress-articles")
if els:
    print(els[0].get_attribute("innerHTML")[:500])

print("\n--- Current URL:", driver.current_url)

input("Press Enter to close...")
driver.quit()


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

from main import load_cookies_from_netscape_file
driver.get("https://fc2ppvdb.com")
time.sleep(2)

cookie_file = "fc2ppvdb.com_cookies.txt"
if os.path.exists(cookie_file):
    cookies = load_cookies_from_netscape_file(cookie_file)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except:
            pass
    print(f"Loaded {len(cookies)} cookies")

# 过年龄验证
driver.get("https://fc2ppvdb.com/cookie/setage")
time.sleep(3)
try:
    btn = driver.find_element(By.CLASS_NAME, "text-white")
    print(f"Found button: tag={btn.tag_name} text={btn.text[:30]}")
    btn.click()
    print("Clicked enter button")
except Exception as e:
    print("Click failed:", e)
time.sleep(2)

# 打开目标页面
driver.get("https://fc2ppvdb.com/actresses/6061?page=1")
print("\nPage opened, monitoring...")

# 监测页面加载过程
for i in range(25):
    time.sleep(1)
    state = driver.execute_script("return document.readyState")
    title = driver.title
    url = driver.current_url
    els = driver.find_elements(By.CSS_SELECTOR, "#actress-articles a[href*='/articles/']")
    all_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/articles/']")
    actress_div = driver.find_elements(By.ID, "actress-articles")
    containers = driver.find_elements(By.CSS_SELECTOR, ".py-4")
    print(f"t={i+1:2d}s | state={state:10s} | actress_div={'YES' if actress_div else 'NO '} | article_links={len(els):3d} | all_article_links={len(all_links):3d} | py4_divs={len(containers)} | url={url[:50]}")
    if i == 4:
        # 5秒后保存当前快照
        with open("debug_snapshot_5s.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("  >> 5s snapshot saved")
    if len(els) > 5:
        with open("debug_snapshot.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("  >> STABLE! Snapshot saved")
        break

print("\n--- Final page title:", driver.title)
print("--- Final URL:", driver.current_url)

input("\nPress Enter to close browser...")
driver.quit()
