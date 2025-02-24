import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Instagram credentials
username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

# Logs into Instagram
def login(driver):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)

    # Locates the username, password, and login button
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    # Enters the username and password.
    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(3)



# Collects comments from a specific Instagram post.
def collect_comments(driver, post_url):

    # Navigates to the Instagram post.
    driver.get(post_url)

    # Waits for the comments section to load.
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'Mr508')]")))

    user_data = {}  
    comment_elements = driver.find_elements(By.XPATH, "//span[@class='comment_text_class']")
    
    # Extracts the comment text and username.
    for element in comment_elements:
        comment_text = element.text
        username = element.find_element(By.XPATH, ".//preceding-sibling::span[@class='username_class']").text  

        if username not in user_data:
            user_data[username] = {
                'comment_count': 0,  
                'mention_count': 0  
            }

        user_data[username]['comment_count'] += 1

        mentions = [word[1:] for word in comment_text.split() if word.startswith('@')]  
        user_data[username]['mention_count'] += int(len(mentions) // 5) 

    return user_data 