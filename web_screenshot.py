import os
import time
import requests
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # Add this import
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from PIL import Image
import uuid
from webdriver_manager.chrome import ChromeDriverManager

IMGUR_CLIENT_ID = "742600efeee11e1"

# Setup logging
logging.basicConfig(level=logging.INFO)

def upload_to_imgur(image_path):
    if not IMGUR_CLIENT_ID:
        raise ValueError("IMGUR_CLIENT_ID is not set in the environment variables.")
    
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    
    try:
        with open(image_path, "rb") as image_file:
            response = requests.post("https://api.imgur.com/3/upload", headers=headers, files={"image": image_file})
        
        if response.status_code == 200:
            logging.info("Upload successful!")
            return response.json().get('data', {}).get('link')
        else:
            logging.error(f"Error uploading to Imgur: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"Error during Imgur upload: {e}")
        return None

def is_valid_url(url):
    try:
        result = requests.get(url)
        if result.status_code == 200:
            return True
        else:
            logging.error(f"Invalid URL: {url} returned status code {result.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Invalid URL: {e}")
        return False

def capture_web_page_image(url, file_path=None, retries=3, retry_delay=2):
    if not is_valid_url(url):
        logging.error("Invalid URL provided.")
        return None

    if file_path is None:
        file_path = f"screenshot_{uuid.uuid4().hex}.png"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    attempt = 1
    while attempt <= retries:
        driver = None
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True)
            logging.info(f"Attempt {attempt}: Navigating to {url}")
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            driver.save_screenshot(file_path)
            logging.info(f"Screenshot saved to {file_path}")
            return file_path
        except Exception as e:
            logging.error(f"Error capturing screenshot on attempt {attempt}: {e}")
            attempt += 1
            time.sleep(retry_delay * attempt)
        finally:
            if driver:
                driver.quit()

    logging.error("Max retries exceeded.")
    return None

def save_uploaded_image(uploaded_file, file_path):
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        logging.info(f"Image saved to {file_path}")
        return file_path
    except Exception as e:
        logging.error(f"Error saving uploaded image: {e}")
        return None

def resize_image(image_path, size=(224, 224), save_as_new=True):
    try:
        with Image.open(image_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            resized_img = img.resize(size)
            if save_as_new:
                new_path = f"resized_{uuid.uuid4().hex}.png"
                resized_img.save(new_path)
                logging.info(f"Image resized and saved as {new_path}")
                return new_path
            else:
                resized_img.save(image_path)
            logging.info(f"Image resized and saved to {image_path}")
        return image_path
    except Exception as e:
        logging.error(f"Error resizing image: {e}")
        return None

def compress_image(image_path, quality=85, save_as_new=True):
    try:
        with Image.open(image_path) as img:
            if save_as_new:
                new_path = f"compressed_{uuid.uuid4().hex}.png"
                img.save(new_path, quality=quality, optimize=True)
                logging.info(f"Image compressed and saved as {new_path}")
                return new_path
            else:
                img.save(image_path, quality=quality, optimize=True)
            logging.info(f"Image compressed and saved to {image_path}")
        return image_path
    except Exception as e:
        logging.error(f"Error compressing image: {e}")
        return None
