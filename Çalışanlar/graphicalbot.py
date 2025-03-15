from selenium import webdriver  # Selenium kütüphanesinden webdriver'ı içe aktar
from selenium.webdriver.chrome.options import Options  # Chrome seçeneklerini içe aktar
from selenium.webdriver.common.by import By  # Element bulma yöntemlerini içe aktar
import random  # Rastgele sayı üretmek için random kütüphanesini içe aktar
from time import sleep  # Uyku fonksiyonunu içe aktar
import matplotlib.pyplot as plt  # Grafik çizmek için matplotlib kütüphanesini içe aktar
import datetime  # Tarih ve saat işlemleri için datetime kütüphanesini içe aktar
from colorama import Fore, Style  # Renkli metin için colorama'yı içe aktar

# Tarayıcı oluşturma fonksiyonu
def create_browser():
    options = Options()  # Chrome seçeneklerini başlat
    options.add_argument("--incognito")  # Gizli modda aç
    options.add_argument("--ignore-certificate-errors")  # Sertifika hatalarını görmezden gel
    options.add_argument("--disable-web-security")  # Web güvenliğini devre dışı bırak
    options.add_argument("--ignore-ssl-errors")  # SSL hatalarını görmezden gel
    options.add_argument("--disable-gpu")  # GPU'yu devre dışı bırak
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Kullanıcı aracısını ayarla

    browser = webdriver.Chrome(options=options)  # Chrome tarayıcısını başlat
    browser.maximize_window()  # Tarayıcıyı tam ekran yap
    return browser  # Tarayıcıyı döndür

# Belirli bir elementin yüklenmesini bekleyen fonksiyon
def wait_for_element(driver, xpath):
    while True:  # Sonsuz döngü
        try:
            driver.find_element(By.XPATH, xpath)  # Belirtilen XPATH ile elementi bul
            break  # Element bulunduysa döngüden çık
        except:
            sleep(random.uniform(1, 2))  # Rastgele bekleme süresi

# Sayfayı açma ve elementi bulma fonksiyonu
def open_page(browser, url, xpath):
    print(f"{Fore.CYAN}{url} sayfasına gidiliyor...{Style.RESET_ALL}")  # Sayfa açılıyor mesajı
    browser.get(url)  # URL'yi aç
    sleep(5)  # 5 saniye bekle
    wait_for_element(browser, xpath)  # Elementin yüklenmesini bekle

# Fiyat metnini sayıya dönüştüren fonksiyon
def convert_to_number(price_text):
    price_text = price_text.replace(',', '').replace(' ', '').replace('USD', '').strip()  # Metni temizle
    try:
        return float(price_text)  # Metni float'a çevir
    except ValueError:
        return None  # Hata durumunda None döndür

# Fiyatı alma fonksiyonu
def get_price(browser, xpath):
    try:
        price_text = browser.find_element(By.XPATH, xpath).text  # Fiyat metnini al
        return convert_to_number(price_text)  # Metni sayıya dönüştür
    except:
        return None  # Hata durumunda None döndür

# Fiyatları grafikte gösteren fonksiyon
def plot_prices(time_stamps, price_history):
    plt.clf()  # Mevcut grafiği temizle
    for exchange, prices in price_history.items():  # Her borsa için
        plt.plot(time_stamps, prices, label=exchange)  # Fiyatları çiz
    plt.xlabel('Zaman')  # X eksenine etiket
    plt.ylabel('Fiyat (USD)')  # Y eksenine etiket
    plt.title('Bitcoin Fiyatları')  # Başlık
    plt.legend()  # Efsaneyi göster
    plt.grid(True)  # Izgara çiz
    plt.draw()  # Grafiği çiz
    plt.pause(0.1)  # Kısa bir süre

# Ana fonksiyon
def main():
    # Fiyatları almak için URL'ler ve XPATH'ler
    urls = [
        ("https://www.tradingview.com/symbols/BTCUSD/?exchange=BINANCE", "//*[@id='js-category-content']/div[1]/div[1]/div/div[1]/div/div[3]/div[1]/div/div[1]/span[1]", "Binance"),
        ("https://www.gate.io/tr/trade/BTC_USDT", "//*[@id='spot_coin_info']/div[2]/div[2]/span[1]", "Gate"),
        ("https://crypto.com/price/bitcoin", "//*[@id='__next']/div[3]/div/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/h2/span", "Crypto.com"),
        ("https://www.bybit.com/trade/usdt/BTCUSDT", "//*[@id='root']/main/div[5]/div/div[1]/aside/div[1]/div[1]/div/div[3]/span", "Bybit"),
        ("https://finance.yahoo.com/quote/BTC-USD/", "//*[@id='nimbus-app']/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/fin-streamer[1]/span", "Yahoo")
    ]

    # Her URL için bir tarayıcı oluştur
    browsers = [create_browser() for _ in range(len(urls))]

    # Her tarayıcı ve URL için sayfayı aç
    for browser, (url, xpath, exchange) in zip(browsers, urls):
        open_page(browser, url, xpath)

    # Fiyat geçmişini saklamak için bir sözlük oluştur
    price_history = {exchange: [] for _, _, exchange in urls}
    time_stamps = []  # Zaman damgalarını saklamak için bir liste

    try:
        plt.ion()  # Matplotlib interaktif modunu aç
        while True:  # Sonsuz döngü
            current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Anlık zaman damgası al
            time_stamps.append(current_time)  # Zaman damgasını listeye ekle
            prices = {}  # Fiyatları saklayacağımız boş bir sözlük oluştur

            # Her tarayıcı için fiyatı al
            for browser, (_, xpath, exchange) in zip(browsers, urls):
                price = get_price(browser, xpath)  # Fiyatı al
                if price is not None:
                    prices[exchange] = price  # Fiyatı sözlüğe ekle
                    price_history[exchange].append(price)  # Fiyatı fiyat geçmişine ekle
                else:
                    price_history[exchange].append(None)  # Fiyat alınamazsa None ekle

            # Fiyatları ekrana yazdır
            for exchange, price in prices.items():
                print(f"{Fore.GREEN}{exchange} için anlık fiyat: {price} USD{Style.RESET_ALL}")
                print("---------------------------")  # Çıktı ayırıcı

            plot_prices(time_stamps, price_history)  # Fiyatları grafikte göster
            sleep(1)  # 1 saniye bekle ve tekrar çalıştır

    except KeyboardInterrupt:  # Kullanıcı Ctrl+C ile durdurursa
        print(f"{Fore.MAGENTA}Program durduruldu.{Style.RESET_ALL}")  # Durdurma mesajı yazdır
        print("---------------------------")  # Çıktı ayırıcı

    finally:
        for browser in browsers:
            browser.quit()  # Tarayıcıları kapat

# Programın başlangıç noktası
if __name__ == "__main__":
    plt.ion()  # Matplotlib interaktif modunu aç
    main()  # Ana fonksiyonu çağır