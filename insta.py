import os, time, sys, random
from drivers.driver import create_driver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers', 'chromedriver')
url = 'https://www.instagram.com/explore/tags'

username = sys.argv[3]
password = sys.argv[4]

l = c = 0

seconds = int(sys.argv[2])

comments_list = ['nice', 'beautiful', 'great one', 'nice one', 'amazing', 'i like it', 'looks good', 'perfect ^^', 'amazing ... ^^']

tag = sys.argv[1]  # love. #instagood. #photooftheday. #fashion. #beautiful. #happy. #cute. #tbt.

driver = create_driver(exec_path = DRIVER_PATH, args = ['--headless'], args_experimental = [])
driver.get("https://www.instagram.com/accounts/login/")

WebDriverWait(driver, 15).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, '[name="username"]'))

driver.find_element_by_css_selector('[name="username"]').send_keys(username)
driver.find_element_by_css_selector('[name="password"]').send_keys(password)

driver.find_element_by_css_selector('[type="submit"]').click()

search_bar = WebDriverWait(driver, 15).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, '[placeholder="Search"]'))

driver.get(f"https://www.instagram.com/explore/tags/{tag}/")
first_img = WebDriverWait(driver, 15).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, 'article a'))
first_img[0].click()

while True:
    ln = cn = False
    try:
        # liking
        likebtn = WebDriverWait(driver, 15).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, '[aria-label="Like"]'))
        likebtn[0].click() 
        ln = True
        l += 1
        #commenting
        if random.random() > 0.7:
            comment = WebDriverWait(driver, 15).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, 'textarea[aria-label]'))
            comment[0].click()
            comment = WebDriverWait(driver, 15).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, 'textarea[aria-label]'))
            comment[0].send_keys(random.choice(comments_list))
            comment[0].submit()
            cn = True
            c += 1
        print(f'l:{l} | c:{c} | current : {driver.current_url} | ', end ="")
        if ln and cn: print('t:2')
        elif ln: print('t:1')
        else: print('t:0')

    except Exception as e:
        # print(e)
        print('-- Error ! --')
    time.sleep(random.randint(seconds, seconds + 5))   
    url = driver.current_url
    driver.find_element(By.CSS_SELECTOR, '.coreSpriteRightPaginationArrow').click()
    while url == driver.current_url: pass