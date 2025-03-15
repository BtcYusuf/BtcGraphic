from selenium import webdriver  # Selenium modülünü tarayıcı otomasyonu için import ediyoruz
from selenium.webdriver.chrome.options import Options  # Chrome tarayıcı ayarlarını yapılandırmak için
from selenium.webdriver.common.by import By  # Web elemanlarını bulmak için 'By' sınıfını import ediyoruz
import random  # Rastgele bekleme süreleri oluşturmak için random modülünü import ediyoruz
from time import sleep  # İşlemler arasında beklemek için sleep fonksiyonunu import ediyoruz
import matplotlib.pyplot as plt  # Matplotlib modülünü grafik çizmek için import ediyoruz
import datetime  # Zaman damgaları oluşturmak için datetime modülünü import ediyoruz

def create_browser():  # Tarayıcı oluşturma fonksiyonu
    options = Options()  # Tarayıcı ayarlarını tutacak Options nesnesini oluşturuyoruz
    options.add_argument("--incognito")  # Tarayıcıyı gizli modda açıyoruz
    options.add_argument("--ignore-certificate-errors")  # SSL sertifika hatalarını yok sayıyoruz
    options.add_argument("--disable-web-security")  # Web güvenlik ayarlarını devre dışı bırakıyoruz
    options.add_argument("--ignore-ssl-errors")  # SSL hatalarını göz ardı ediyoruz
    options.add_argument("--disable-gpu")  # GPU kullanımını devre dışı bırakıyoruz (genellikle performans artırımı için)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Tarayıcı kullanıcı ajanını ayarlıyoruz

    browser = webdriver.Chrome(options=options)  # Ayarları içeren Chrome tarayıcısını başlatıyoruz
    browser.maximize_window()  # Tarayıcıyı tam ekran moduna geçiriyoruz
    return browser  # Tarayıcı nesnesini döndürüyoruz

def wait_for_element(driver, xpath):  # Elementi bekleme fonksiyonu
    while True:  # Sürekli döngü
        try:
            driver.find_element(By.XPATH, xpath)  # Belirtilen XPATH ile elementi bul
            break  # Eleman bulunursa döngüden çık
        except:
            print(f"Element bulunamadı, tekrar deniyorum: {xpath}")  # Hata mesajı yazdır
            sleep(random.uniform(1, 2))  # Eleman bulunamazsa rastgele süre bekle

def open_page(browser, url, xpath):  # Sayfa açma fonksiyonu
    print(f"{url} sayfasına gidiliyor...")  # Sayfaya gidildiğini bildiren mesaj yazdır
    browser.get(url)  # Tarayıcıyı belirtilen URL'ye yönlendir
    sleep(5)  # Sayfanın yüklenmesi için bekleyin
    wait_for_element(browser, xpath)  # Sayfa yüklendiğinde elementi kontrol et

def convert_to_number(price_text):  # Fiyat metnini sayıya dönüştürme fonksiyonu
    price_text = price_text.replace(',', '').replace(' ', '').replace('USD', '').strip()  # Metni temizle
    try:
        return float(price_text)  # Sayıya dönüştür
    except ValueError:
        print(f"Bir hata oluştu: {price_text}")  # Hata mesajı yazdır
        return None  # Hata durumunda None döndür

def get_price(browser, xpath):  # Fiyatı almak için fonksiyon
    try:
        price_text = browser.find_element(By.XPATH, xpath).text  # Belirtilen XPATH ile fiyatı al
        return convert_to_number(price_text)  # Fiyat metnini sayıya çevir
    except Exception as e:
        print(f"Fiyat alınırken hata oluştu: {e}")  # Hata mesajı yazdır
        return None  # Hata durumunda None döndür

def plot_prices(time_stamps, price_history):  # Fiyatları grafikte gösterme fonksiyonu
    plt.clf()  # Önceki grafiği temizle
    for exchange, prices in price_history.items():  # Her borsa için fiyatları çiz
        plt.plot(time_stamps, prices, label=exchange)  # Fiyatları grafikte çiz
    plt.xlabel('Zaman')  # X eksenine zaman etiketini ekle
    plt.ylabel('Fiyat (USD)')  # Y eksenine fiyat etiketini ekle
    plt.title('Bitcoin Fiyatları')  # Grafik başlığını ayarla
    plt.legend()  # Legend (açıklama) ekle
    plt.grid(True)  # Izgara çizgilerini ekle
    plt.draw()  # Grafiği çiz ama pencereyi kapatma
    plt.pause(0.1)  # Grafiği güncellemek için kısa bir süre bekle

def main():  # Ana program akışı
    # URL'ler ve XPATH'ler
    urls = [
        ("https://www.tradingview.com/symbols/BTCUSD/?exchange=BINANCE", "//*[@id='js-category-content']/div[1]/div[1]/div/div[1]/div/div[3]/div[1]/div/div[1]/span[1]", "Binance"),
        ("https://www.gate.io/tr/trade/BTC_USDT", "//*[@id='spot_coin_info']/div[2]/div[2]/span[1]", "Gate"),
        ("https://crypto.com/price/bitcoin", "//*[@id='__next']/div[3]/div/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/h2/span", "Crypto.com"),
        ("https://www.bybit.com/trade/usdt/BTCUSDT", "//*[@id='root']/main/div[5]/div/div[1]/aside/div[1]/div[1]/div/div[3]/span", "Bybit"),
        ("https://finance.yahoo.com/quote/BTC-USD/", "//*[@id='nimbus-app']/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/fin-streamer[1]/span", "Yahoo")
    ]

    browsers = [create_browser() for _ in range(len(urls))]  # Her URL için yeni tarayıcı oluştur ve tarayıcılar listesine ekle

    for browser, (url, xpath, exchange) in zip(browsers, urls):  # Her bir borsa için URL'leri tarayıcı için aç
        open_page(browser, url, xpath)  # Tarayıcıyı URL'ye yönlendir

    price_history = {exchange: [] for _, _, exchange in urls}  # Fiyat geçmişi saklamak için bir sözlük oluştur
    time_stamps = []  # Zaman damgalarını saklamak için bir liste oluştur

    try:
        plt.ion()  # Matplotlib interaktif modunu aç
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Anlık zaman damgası al
            time_stamps.append(current_time)  # Zaman damgasını listeye ekle
            prices = {}  # Fiyatları saklayacağımız boş bir sözlük oluştur

            for browser, (_, xpath, exchange) in zip(browsers, urls):  # Her borsa için fiyatlar al ve fiyatlar sözlüğüne ekle
                price = get_price(browser, xpath)  # Fiyatı al
                if price is not None:
                    prices[exchange] = price  # Fiyatı sözlüğe ekle
                    price_history[exchange].append(price)  # Fiyatı fiyat geçmişine ekle
                else:
                    price_history[exchange].append(None)  # Fiyat alınamazsa None ekle

            for exchange, price in prices.items():  # Her borsa için anlık fiyatları yazdır
                print(f"{exchange} için anlık fiyat: {price} USD")

            plot_prices(time_stamps, price_history)  # Fiyatları grafikte göster
            sleep(1)  # 1 saniye bekle ve tekrar çalıştır

    except KeyboardInterrupt:  # Program kullanıcı tarafından durdurulduğunda uyarı mesajı göster
        print("Program durduruldu.")

    finally:
        for browser in browsers:  # Program sonlandığında tüm tarayıcıları kapat
            browser.quit()  # Tarayıcıları kapat

if __name__ == "__main__":  # Ana programı çalıştır
    plt.ion()  # Matplotlib interaktif modunu aç
    main()  # Ana fonksiyonu çağır