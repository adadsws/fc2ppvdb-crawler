from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

# 初始化webdriver
driver = webdriver.Firefox()

# 打开我们要抓取的网页
url = "https://fc2ppvdb.com/cookie/setage"
driver.get(url)

# 等待并模拟点击ENTER按钮
try:
    # 等待按钮加载并可点击
    enter_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "text-white"))
    )
    enter_button.click()
except Exception as e:
    print(f"Error clicking the button: {e}")

# 打开目标网页
url = "https://fc2ppvdb.com/actresses/4312"
driver.get(url)

# 等待指定的元素加载完成
wait = WebDriverWait(driver, 10)
try:
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "lazyload-wrapper")))
    # print("Element found:", element)  # 打印找到的元素
    print("Element HTML:", element.get_attribute("outerHTML"))  # 打印元素的HTML内容
except Exception as e:
    print(f"Error: {e}")  # 打印错误信息
    
# 获取网页的源代码
html_content = driver.page_source

# # 保存HTML内容到文件
# with open("output.html", "w", encoding="utf-8") as file:
#     file.write(html_content)

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, "html.parser")

# # 格式化HTML
# formatted_html = soup.prettify()

# # 保存格式化后的HTML到文件
# with open("formatted_output.html", "w", encoding="utf-8") as file:
#     file.write(formatted_html)

# 查找包含影片数量的元素
film_count_element = soup.find("div", class_="py-4").find("p", class_="text-sm leading-5")

if film_count_element:
    # 提取影片数量文本
    film_count_text = film_count_element.get_text(strip=True)
    print(f"影片数量信息: {film_count_text}")
    
    # 使用正则表达式提取最后一个数字
    match = re.search(r"全：\s*(\d+)", film_count_text)
    if match:
        total_films = match.group(1)
        print(f"影片总数: {total_films}")
    else:
        print("未找到影片总数")
else:
    print("未找到影片数量信息")

# 查找所有包含影片信息的容器
containers = soup.find_all("div", class_="2xl:w-1/6 xl:w-1/5 lg:w-1/4 md:w-1/2 w-full p-4")

for i,container in enumerate(containers):
    # print(container.prettify())
        
    try:
        # 提取影片编号
        film_number = container.find("span", class_="absolute top-0 left-0 text-white bg-gray-800 px-1").get_text(strip=True)

        # 提取影片名称
        film_title = container.find("a", class_="text-white title-font text-base font-medium line-clamp-2").get("title", "").strip()

        # 提取制作人
        producer = container.find("a", class_="text-blue-600 dark:text-blue-700 line-clamp-1").get("title", "").strip()

        # 打印提取的信息
        print(f"影片编号: {film_number}")
        print(f"影片名称: {film_title}")
        print(f"制作人: {producer}")
        print("-" * 50)
    except Exception as e:
        print(f"Error extracting data: {e}")

# 关闭webdriver
driver.quit()