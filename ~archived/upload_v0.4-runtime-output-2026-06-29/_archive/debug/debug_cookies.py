from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def load_cookies_valid(file_path):
    cookies = []
    now = time.time()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 6:
                expiry = int(parts[4]) if parts[4].isdigit() else 0
                if expiry > 0 and expiry < now:
                    print(f"  [SKIP expired] {parts[5]} (expiry={parts[4]})")
                    continue
                cookies.append({"domain": parts[0], "path": parts[2],
                                 "name": parts[5], "value": parts[6] if len(parts) > 6 else ""})
    return cookies

driver.get("https://fc2ppvdb.com")
time.sleep(2)
cookies = load_cookies_valid("fc2ppvdb.com_cookies.txt")
print(f"Loading {len(cookies)} valid cookies")
for c in cookies:
    try:
        driver.add_cookie(c)
    except Exception as e:
        print(f"  [COOKIE ERR] {c['name']}: {e}")

driver.get("https://fc2ppvdb.com/cookie/setage")
time.sleep(3)
try:
    btn = driver.find_element("css selector", "a.text-white, button.text-white")
    print(f"Age gate button: {btn.text[:30]}")
    btn.click()
except Exception as e:
    print(f"Age gate click failed: {e}")
time.sleep(2)

driver.get("https://fc2ppvdb.com/actresses/6061?page=1")
time.sleep(5)

print("\n=== BROWSER COOKIES AFTER FULL FLOW ===")
for c in driver.get_cookies():
    val = c["value"][:50] + "..." if len(c["value"]) > 50 else c["value"]
    print(f"  {c['name']}: {val} (expires={c.get('expiry', 'session')})")

xsrf = next((c for c in driver.get_cookies() if c["name"] == "XSRF-TOKEN"), None)
print(f"\nXSRF-TOKEN present: {xsrf is not None}")
if xsrf:
    print(f"XSRF value: {xsrf['value'][:80]}")

driver.set_script_timeout(30)

print("\n=== FETCH WITH X-XSRF-TOKEN ===")
result = driver.execute_async_script("""
    var xsrf = document.cookie.split('; ').find(function(r){ return r.startsWith('XSRF-TOKEN='); });
    var xsrfVal = xsrf ? decodeURIComponent(xsrf.split('=')[1]) : '';
    var cb = arguments[arguments.length-1];
    fetch('https://fc2ppvdb.com/actresses/actress-articles?actressid=6061&page=1', {
        credentials: 'include',
        headers: {
            'X-XSRF-TOKEN': xsrfVal,
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'text/html, */*'
        }
    })
    .then(function(r) {
        return r.text().then(function(t) {
            cb('STATUS:' + r.status + ' LEN:' + t.length + ' PREVIEW:' + t.slice(0, 500));
        });
    })
    .catch(function(e) { cb('FETCH_ERROR:' + e.message); });
""")
print(result)

input("\nPress Enter to close...")
driver.quit()
