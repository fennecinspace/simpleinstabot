import os, time, sys, random
from drivers.driver import create_driver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers', 'chromedriver')

INSTAGRAM_URL = "https://www.instagram.com/"
EXPLORE_URL = INSTAGRAM_URL + 'explore/tags/'
LOGIN_URL = INSTAGRAM_URL + 'accounts/login/'

COMMENTS_LIST = ['nice', 'beautiful', 'great', 'amazing', 'i like it', 'looks good', 'perfect ^^', 'amazing ... ^^']

DEFAULT_WAIT_TIME = 15

LIKE_BTN_SELECTOR = "button .glyphsSpriteHeart__outline__24__grey_9"
NEXT_POST_BTN_SELECTOR = ".coreSpriteRightPaginationArrow"

def like_and_comment(driver, seconds):
    l = c = 0
    while True:
        s = 0
        try:
            # liking
            try:
                likebtn = WebDriverWait(driver, DEFAULT_WAIT_TIME).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, LIKE_BTN_SELECTOR))[0]
                likebtn.click()
                try:
                    # check if like btn was clicked
                    WebDriverWait(driver, 5).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, LIKE_BTN_SELECTOR))
                    print(f'Error ! Could not like : {driver.current_url} ')
                except:
                    l += 1
                    s += 1
            except:
                print('Could not find like button ')

            #commenting
            if random.random() > 0.8:
                comment = WebDriverWait(driver, DEFAULT_WAIT_TIME).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, 'textarea[aria-label]'))
                comment[0].click()
                comment = WebDriverWait(driver, DEFAULT_WAIT_TIME).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, 'textarea[aria-label]'))
                comment[0].send_keys(random.choice(COMMENTS_LIST))
                comment[0].submit()
                c += 1
                s += 1

            print(f'l:{l} | c:{c} | current : {driver.current_url} | t:{s}')

        except Exception as e:
            print('-- Error ! --')
            
        time.sleep(random.randint(seconds, seconds + 5))
        url = driver.current_url
        driver.find_element(By.CSS_SELECTOR, NEXT_POST_BTN_SELECTOR).click()
        while url == driver.current_url: pass

def insta_login(driver, username, password):
    driver.get(LOGIN_URL)

    WebDriverWait(driver, DEFAULT_WAIT_TIME).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, '[name="username"]'))

    driver.find_element_by_css_selector('[name="username"]').send_keys(username)
    driver.find_element_by_css_selector('[name="password"]').send_keys(password)

    driver.find_element_by_css_selector('[type="submit"]').click()

    try:
        search_bar = WebDriverWait(driver, DEFAULT_WAIT_TIME).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, '[placeholder="Search"]'))
    except:
        print('Could not login !')

def open_tag(driver, tag):
    driver.get(EXPLORE_URL + tag)
    first_img = WebDriverWait(driver, DEFAULT_WAIT_TIME).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, 'article a'))
    first_img[0].click()

if __name__ == '__main__':
    args = {
        'username': sys.argv[3],
        'password': sys.argv[4],
        'seconds': int(sys.argv[2]),
        'tag': sys.argv[1],
    }

    while True:
        try:
            driver = create_driver(exec_path = DRIVER_PATH, args = ['--headless'], args_experimental = [])
            insta_login(driver, args['username'], args['password'])
            open_tag(driver, args['tag'])
            like_and_comment(driver, args['seconds'])
        except Exception as e:
            print('Failed : Will Reboot !')
            continue