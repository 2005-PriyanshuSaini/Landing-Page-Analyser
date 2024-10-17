import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from PIL import Image
import uuid

IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')

def upload_to_imgur(image_path):
    if not IMGUR_CLIENT_ID:
        raise ValueError("IMGUR_CLIENT_ID is not set in the environment variables.")

    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    
    try:
        with open(image_path, "rb") as image_file:
            response = requests.post("https://api.imgur.com/3/upload", headers=headers, files={"image": image_file})
        
        if response.status_code == 200:
            return response.json().get('data', {}).get('link')
        else:
            print(f"Error uploading to Imgur: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error during Imgur upload: {e}")
        return None

def capture_web_page_image(url, file_path=None, retries=3):
    if file_path is None:
        file_path = f"screenshot_{uuid.uuid4().hex}.png"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=chrome_options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    attempt = 0
    while attempt < retries:
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            driver.save_screenshot(file_path)
            return file_path
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            attempt += 1
            time.sleep(1)
        finally:
            driver.quit()

    print("Max retries exceeded.")
    return None

def save_uploaded_image(uploaded_file, file_path):
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        print(f"Error saving uploaded image: {e}")
        return None
def resize_image(image_path, size=(224, 224), save_as_new=True):
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if image has 4 channels (RGBA)
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            resized_img = img.resize(size)
            if save_as_new:
                new_path = f"resized_{uuid.uuid4().hex}.png"
                resized_img.save(new_path)
                return new_path
            else:
                resized_img.save(image_path)
        return image_path
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None


def compress_image(image_path, quality=85, save_as_new=True):
    try:
        with Image.open(image_path) as img:
            if save_as_new:
                new_path = f"compressed_{uuid.uuid4().hex}.png"
                img.save(new_path, quality=quality, optimize=True)
                return new_path
            else:
                img.save(image_path, quality=quality, optimize=True)
        return image_path
    except Exception as e:
        print(f"Error compressing image: {e}")
        return None


