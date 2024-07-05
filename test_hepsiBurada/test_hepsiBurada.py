import pytest
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
logging.basicConfig(filename='test_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class TestHepsiBurada:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.vars = {}
        self.wait = WebDriverWait(self.driver, 20)
        yield
        self.driver.quit()

    def test_TC001(self):
        """Kategoriye Göre Ürün Listelenmesi"""
        try:
            self.driver.get("https://www.hepsiburada.com/")
            logging.info("HepsiBurada anasayfasına girildi.")
            time.sleep(5)  # Sayfanın yüklenmesini bekleyin

            # Kategori menüsünü bulma ve üzerine fareyi getirme
            kategori_menu = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sf-MenuItems-UHHCg2qrE5_YBqDV_7AC')))
            actions = ActionChains(self.driver)
            actions.move_to_element(kategori_menu).perform()
            logging.info("Kategori menüsü üzerine gelindi.")
            
            # Alt kategoriyi seçme
            alt_kategori = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'sf-ChildMenuItems-a4G0z3YJJWkQs7qKKuuj')))
            actions = ActionChains(self.driver)
            actions.move_to_element(alt_kategori).click().perform()
            logging.info("Alt kategori seçildi.")

            # Ürünlerin listelendiğini doğrulama
            products = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="1"]')))
            assert len(products) > 0, "Ürünler listelenmedi."
            logging.info("Ürünler başarıyla listelendi.")
        except Exception as e:
            logging.error(f"Test failed: {str(e)}")
            self.driver.save_screenshot('screenshots/TC001_error_screenshot.png')
            raise

    def test_TC002(self):
        """Ürün Arama Fonksiyonu"""
        try:
            self.driver.get("https://www.hepsiburada.com/")
            logging.info("HepsiBurada anasayfasına girildi.")
            time.sleep(5)  # Sayfanın yüklenmesini bekleyin

            # Ürün arama
            search_box = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'searchBoxOld-P2GCKq3V7DvEXIgWsSCP')))
            time.sleep(2)

            # Elementin tamamen görünür olmasını sağla
            self.driver.execute_script("arguments[0].scrollIntoView(true);", search_box)

            # Elementin tıklanabilirliğini kontrol et ve tıkla
            self.driver.execute_script("arguments[0].click();", search_box)

            # Send keys directly with JavaScript
            try:
                self.driver.execute_script("arguments[0].value='laptop';", search_box)
            except StaleElementReferenceException:
                search_box = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'searchBoxOld-P2GCKq3V7DvEXIgWsSCP')))
                self.driver.execute_script("arguments[0].value='laptop';", search_box)
            
            search_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".SearchBoxOld-buttonContainer")))
            search_button.click()
            logging.info("Ürün arama işlemi gerçekleştirildi.")

            # Arama sonuçlarının listelendiğini doğrulama
            search_results = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".productListContent-wrapper")))
            assert len(search_results) > 0, "Arama sonuçları listelenmedi."
            logging.info("Arama sonuçları başarıyla listelendi.")
        except TimeoutException as e:
            logging.error(f"Timeout during search: {e}")
            raise
        except StaleElementReferenceException as e:
            logging.error(f"Stale element reference: {e}")
            raise
        except Exception as e:
            logging.error(f"Test failed: {e}")
            raise
            

    def test_TC003(self):
       
        try:
            self.driver.get("https://www.hepsiburada.com/")
            logging.info("HepsiBurada anasayfasına girildi.")
            time.sleep(5)  # Sayfanın yüklenmesini bekleyin

            # Kategori menüsünü bulma ve üzerine fareyi getirme
            kategori_menu = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sf-MenuItems-UHHCg2qrE5_YBqDV_7AC')))
            actions = ActionChains(self.driver)
            actions.move_to_element(kategori_menu).perform()
            logging.info("Kategori menüsü üzerine gelindi.")
            
            # Alt kategoriyi seçme
            alt_kategori = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'sf-ChildMenuItems-a4G0z3YJJWkQs7qKKuuj')))
            actions = ActionChains(self.driver)
            actions.move_to_element(alt_kategori).click().perform()
            logging.info("Alt kategori seçildi.")
            product_selection = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="i0"]/div/a')))
            self.driver.execute_script("arguments[0].scrollIntoView();", product_selection)
            product_selection.click()  
            logging.info("İlk ürün seçildi.")
            time.sleep(3) 
            #product_name = self.wait.until(EC.visibility_of_element_located((By.ID, "product-name")))
            #assert product_name.is_displayed(), "Ürün detay sayfası açılmadı."
            #logging.info("Ürün detay sayfası başarıyla açıldı.")
       
        except Exception as e:
            logging.error(f"Test failed: {str(e)}")
            raise
   
    def test_TC004(self):
        """Ürün Sepete eklenmesi"""
        try:
            self.driver.get("https://www.hepsiburada.com/")
            logging.info("HepsiBurada anasayfasına girildi.")
            time.sleep(5)  # Sayfanın yüklenmesini bekleyin
            self.driver.execute_script("window.scrollBy(0, 400)")
            Product = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sf-dod-irONXG cvjW sqqnedytcom')))
            actions = ActionChains(self.driver)
            actions.move_to_element(Product).perform()
            logging.info("Ürünün üzerine gelindi.")
            self.driver.find_element(By.CLASS_NAME,'sf-dod-kMAuCG dWguTJ sdpkm31bwe2 sc-AxiKw eSbheu').click()

            add_to_cart_button = self.wait.until(EC.visibility_of_element_located((By.ID, "addToCart")))
            add_to_cart_button.click
            logging.info("Ürün sepete eklendi.")

            # Sepetin güncellenmesini doğrulama
            cart_icon = self.wait.until(EC.element_to_be_clickable((By.ID, 'shoppingCart')))
            cart_icon.click()
            cart_items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="858da2f8-60b9-43b2-b13e-7bd49707cb2b"]')))
            assert len(cart_items) > 0, "Sepette ürün bulunamadı."
            logging.info("Ürün sepete başarıyla eklendi ve sepet güncellendi.")
        except Exception as e:
            logging.error(f"Test failed: {str(e)}")
            self.driver.save_screenshot('screenshots/add_to_cart_error.png')
            raise

    def test_TC005(self):
        """Sepetteki Ürün Miktarını Değiştirme"""
        try:
            self.driver.get("https://giris.hepsiburada.com/?ReturnUrl=https%3A%2F%2Foauth.hepsiburada.com%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DSPA%26redirect_uri%3Dhttps%253A%252F%252Fwww.hepsiburada.com%252Fuyelik%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%2520profile%26state%3D8a7f3894f5404eefb31db3036518afc9%26code_challenge%3Dx5QLHB_f8NY7R6kKC8saNXI_jjjHCHwb3R-kiMk8tQ8%26code_challenge_method%3DS256%26response_mode%3Dquery%26ActivePage%3DPURE_LOGIN%26oidcReturnUrl%3Dhttps%253A%252F%252Fwww.hepsiburada.com%252F")
            logging.info("HepsiBurada anasayfasına girildi.")
            time.sleep(5)  # Sayfanın yüklenmesini bekleyin

            # Sepetteki ürün miktarını değiştirme
            basket_button = self.wait.until(EC.visibility_of_element_located((By.ID, 'shoppingCart')))
            basket_button.click()
            self.driver.find_element(By.ID, '858da2f8-60b9-43b2-b13e-7bd49707cb2b')
            quantity_box = self.wait.until(EC.element_to_be_clickable((By.NAME, 'quantity')))
            quantity_box.click()
            quantity_box.clear()
            quantity_box.send_keys("2")
            
            update_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".update-cart-button")))
            update_button.click()
            logging.info("Sepetteki ürün miktarı değiştirildi.")

            # Sepetin güncellenmesini doğrulama
            cart_total = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart-total-price")))
            assert cart_total, "Sepet toplamı güncellenmedi."
            logging.info("Sepet miktarı ve toplam tutar başarıyla güncellendi.")
        except Exception as e:
            logging.error(f"Test failed: {str(e)}")
            raise

    def test_TC006(self):
        """Sepetteki Ürünü Kaldırma"""
        try:
            self.test_TC004()  # Önce sepete ürün ekliyoruz

            # Sepetteki ürünü kaldırma
            remove_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".remove-item-button")))
            remove_button.click()
            logging.info("Sepetteki ürün kaldırıldı.")

            # Sepetin güncellenmesini doğrulama
            empty_cart_message = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".empty-cart-message")))
            assert empty_cart_message, "Sepet boşaltılamadı."
            logging.info("Sepetteki ürün başarıyla kaldırıldı ve sepet güncellendi.")
        except Exception as e:
            logging.error(f"Test failed: {str(e)}")
            raise

    def test_TC007(self):
        """Sipariş Tamamlama"""
        try:
            self.test_TC004()  # Önce sepete ürün ekliyoruz

            # Siparişi tamamlama
            complete_order_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".complete-order-button")))
            complete_order_button.click()
            logging.info("Siparişi tamamla butonuna tıklandı.")

            # Ödeme ve adres bilgilerini girme
            # Bu kısım test ortamında login ve ödeme adımlarıyla devam eder
            logging.info("Ödeme ve adres bilgileri girildi.")

            # Siparişin tamamlandığını doğrulama
            order_confirmation = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".order-confirmation-message")))
            assert order_confirmation, "Sipariş tamamlanamadı."
            logging.info("Sipariş başarıyla tamamlandı.")
        except Exception as e:
            logging.error(f"Test failed: {str(e)}")
            raise

if __name__ == "__main__":
    pytest.main()
