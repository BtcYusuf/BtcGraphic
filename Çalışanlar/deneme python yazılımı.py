#En Basitinden Kripto İşlem Yapma Botu
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# Tarayıcı ayarları
def create_browser():
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-web-security")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    return browser

# Binance üzerinde oturum açma
def login_to_binance(browser, username, password):
    browser.get("https://www.binance.com/en/login")
    sleep(5)
    browser.find_element(By.ID, "email").send_keys(username)
    browser.find_element(By.ID, "password").send_keys(password)
    browser.find_element(By.ID, "login-btn").click()
    sleep(5)  # Güvenlik doğrulaması için bekleyin

# BTC/USDT işlem sayfasına gitme
def go_to_trade_page(browser):
    browser.get("https://www.binance.com/en/trade/BTC_USDT")
    sleep(5)

# İşlem yapma
def place_order(browser, amount, price, order_type="BUY"):
    amount_input = browser.find_element(By.XPATH, "//input[@placeholder='Amount']")
    amount_input.clear()
    amount_input.send_keys(amount)
    
    price_input = browser.find_element(By.XPATH, "//input[@placeholder='Price']")
    price_input.clear()
    price_input.send_keys(price)
    
    if order_type == "BUY":
        buy_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Buy BTC')]")
        buy_button.click()
    elif order_type == "SELL":
        sell_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Sell BTC')]")
        sell_button.click()
    
    sleep(5)

# Ana program akışı
if __name__ == "__main__":
    browser = create_browser()
    username = "your_email@example.com"
    password = "your_password"

    login_to_binance(browser, username, password)
    go_to_trade_page(browser)
    place_order(browser, amount="0.001", price="50000", order_type="BUY")

    browser.quit()
