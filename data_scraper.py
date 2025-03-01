import os
import time
import random
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.envv')

# Instagram credentials
username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

# Logs into Instagram
def login(driver):
    driver.get("https://www.instagram.com")

    try:
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        password_input = driver.find_element(By.NAME, "password")

        for char in username:
            username_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        for char in password:
            password_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
        )

        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    except TimeoutException:
        raise
    except Exception as e:
        raise

def load_cookies(driver):
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://www.instagram.com")
        return True
    except FileNotFoundError:
        return False

# Collects comments from a specific Instagram post.
def collect_comments(driver, post_url):
    driver.get(post_url)
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, '_a9zV')]")))
    except TimeoutException:
        return {}

    user_data = {}
    comment_elements = driver.find_elements(By.XPATH, "//div[@class='_a9zr']//span")
    for element in comment_elements:
        try:
            comment_text = element.text
            username = element.find_element(By.XPATH, "./ancestor::div[@class='_a9zs']//a[@class='_a9zc']").text
            if username not in user_data:
                user_data[username] = {'comment_count': 0, 'mention_count': 0}
            user_data[username]['comment_count'] += 1
            mentions = [word[1:] for word in comment_text.split() if word.startswith('@')]
            user_data[username]['mention_count'] += len(mentions)
        except Exception:
            continue
    return user_data

# Collects likes from a specific Instagram post.
def collect_likes(driver, post_url):
    driver.get(post_url)
    try:
        likes_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/likes/')]")))
        likes_button.click()
        time.sleep(3)
        likes = [element.text for element in driver.find_elements(By.XPATH, "//div[@class='_a9zr']//a[@class='_a9zc']")]
        return likes
    except TimeoutException:
        return []

# Collects followers of a specific Instagram account.
def collect_followers(driver, username):
    driver.get(f"https://www.instagram.com/{username}/")
    try:
        followers_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]")))
        followers_button.click()
        time.sleep(3)
        followers = [element.text for element in driver.find_elements(By.XPATH, "//div[@class='_a9zr']//a[@class='_a9zc']")]
        return followers
    except TimeoutException:
        return []

if __name__ == "__main__":
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    try:
        if not load_cookies(driver):
            login(driver)
        time.sleep(5)
        comments = collect_comments(driver, "YOUR_POST_URL")
        print(comments)
        likes = collect_likes(driver, "YOUR_POST_URL")
        print(likes)
        followers = collect_followers(driver, "YOUR_INSTAGRAM_USERNAME")
        print(followers)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()