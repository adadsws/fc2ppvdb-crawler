from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

def click_enter_button(driver, timeout=10):
    """等待并点击 ENTER 按钮"""
    try:
        enter_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "text-white"))
        )
        enter_button.click()
    except Exception as e:
        print(f"Error clicking the button: {e}")

def wait_for_element(driver, class_name, timeout=10):
    """等待指定元素加载完成"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        return element
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_html(driver):
    """获取并解析网页 HTML"""
    html_content = driver.page_source
    return BeautifulSoup(html_content, "html.parser")

def extract_film_count(soup):
    """提取影片数量信息"""
    film_count_element = soup.find("div", class_="py-4").find("p", class_="text-sm leading-5")
    if film_count_element:
        film_count_text = film_count_element.get_text(strip=True)
        # print(f"影片数量信息: {film_count_text}")
        match = re.search(r"全：\s*(\d+)", film_count_text)
        if match:
            total_films = match.group(1)
            print(f"影片总数: {total_films}")
            return total_films
        else:
            print("未找到影片总数")
            return
    else:
        print("未找到影片数量信息")
        return


def extract_film_data(soup):
    """提取影片信息"""
    containers = soup.find_all("div", class_="2xl:w-1/6 xl:w-1/5 lg:w-1/4 md:w-1/2 w-full p-4")
    for i, container in enumerate(containers):
        try:
            film_number = container.find("span", class_="absolute top-0 left-0 text-white bg-gray-800 px-1").get_text(strip=True)
            film_title = container.find("a", class_="text-white title-font text-base font-medium line-clamp-2").get("title", "").strip()
            producer = container.find("a", class_="text-blue-600 dark:text-blue-700 line-clamp-1").get("title", "").strip()
            
            print("-" * 50)
            
            global count_film
            count_film += 1
            print(f"第{count_film}个影片")
        
            print(f"影片编号: {film_number}")
            print(f"影片名称: {film_title}")
            print(f"制作人: {producer}")
            
            
        except Exception as e:
            print(f"Error extracting data: {e}")


'''
设置演员ID
'''
actresses_id = 4752

# 初始化webdriver
driver = webdriver.Firefox()

# 打开我们要抓取的网页
url = "https://fc2ppvdb.com/cookie/setage"
driver.get(url)

click_enter_button(driver)

count_film = 0
page=1

# 打开目标网页
url = f"https://fc2ppvdb.com/actresses/{actresses_id}"
driver.get(url)
wait_for_element(driver, "lazyload-wrapper")
soup = parse_html(driver)

num_films=int(extract_film_count(soup))
extract_film_data(soup)

while num_films//40>=page:
    page+=1
    url = f"https://fc2ppvdb.com/actresses/{actresses_id}?page={page}"
    print("正在打开",url)
    driver.get(url)
    wait_for_element(driver, "lazyload-wrapper")
    soup = parse_html(driver)
    
    extract_film_data(soup)

# 关闭webdriver
driver.quit()