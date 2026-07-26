import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

options = uc.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = uc.Chrome(options=options, use_subprocess=True)

driver.get("https://fc2ppvdb.com/cookie/setage")
time.sleep(4)
try:
    btn = driver.find_element("css selector", "a.text-white, button.text-white")
    btn.click()
    print("Age gate clicked")
except Exception as e:
    print("Click err:", e)
time.sleep(2)

driver.get("https://fc2ppvdb.com/actresses/6061?page=1")
time.sleep(6)

driver.set_script_timeout(30)
html = driver.execute_async_script("""
    var cb = arguments[arguments.length-1];
    fetch("/actresses/actress-articles?actressid=6061&page=1", {credentials: "include"})
        .then(function(r) { return r.text().then(function(t) { cb(t); }); })
        .catch(function(e) { cb("ERR:" + e.message); });
""")

print(f"Response length: {len(html)}")

soup = BeautifulSoup(html, "html.parser")

# Check for Inertia.js data-page
app_div = soup.find("div", id="app")
if app_div and app_div.get("data-page"):
    import json
    page_data = json.loads(app_div["data-page"])
    print("Inertia component:", page_data.get("component"))
    props = page_data.get("props", {})
    print("Inertia props keys:", list(props.keys()))
    # Look for articles
    for k in props:
        v = props[k]
        if isinstance(v, (list, dict)):
            print(f"  props[{k}] type={type(v).__name__} len={len(v) if isinstance(v, (list, dict)) else 'N/A'}")
else:
    print("No Inertia data-page found")
    # Check for film containers
    containers = soup.find_all("div", class_="2xl:w-1/6 xl:w-1/5 lg:w-1/4 md:w-1/2 w-full p-4")
    print(f"Film containers: {len(containers)}")
    print("HTML preview (last 1000 chars):")
    print(html[-1000:])

driver.quit()


