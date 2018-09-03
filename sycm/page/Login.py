from selenium.webdriver.common.by import By
from .Base import Base
import time
import requests
import logging

logger = logging.getLogger(__name__)


class Login(Base):
    __baseUrl = 'https://sycm.taobao.com/portal/home.htm'

    __error_el = (By.CSS_SELECTOR, ".msg-err")

    __img = (By.ID, 'J_QRCodeImg')

    __filepath = 'screenshot.png'

    __a_market = (By.XPATH,
                  '//*[@id="app"]/div[@class="root-container"]//ul[@class="menu-list clearfix"]/li/a[@class="nameWrapper" and @data-spm="d1057"]/span')

    __a_sycm = (By.XPATH, "//ul[@id='ks-accordion-tab-panel52']/li[4]/span/a")

    __img_close = (By.CSS_SELECTOR, ".ebase-ImageTips__dsImageTipsCloseBtn")

    __img_url = (By.XPATH, '//div[@id="J_QRCodeImg"]/img')

    def __init__(self, *args, **kw):
        super(Login, self).__init__(*args, **kw)

    def login(self):
        self.driver.get(self.__baseUrl)
        try:
            self.script("document.querySelector('#J_Static2Quick').click()")
        except Exception as e:
            logger.info(e)
        count = 0
        while 'https://sycm.taobao.com/portal/home.htm' not in self.driver.current_url:
            logger.info('登陆中')
            if 'https://mai.taobao.com/seller_admin.htm' in self.driver.current_url:
                self.script("window.location.replace('https://sycm.taobao.com/portal/home.htm')")
            if count % 30 == 0:
                try:
                    self.__qrcode_process()
                except Exception as e:
                    logger.error(e)
            else:
                time.sleep(10)
            count += 1
        self.__find_dialog()
        time.sleep(1)
        return self.driver

    def __a_market_click(self):
        self.find_element(*self.__a_market).click()

    def __find_dialog(self):
        try:
            self.quick_find_element(*self.__img_close)
            self.quick_find_element(*self.__img_close).click()
        except Exception as e:
            logger.info(e)

    def __get_error_el(self):
        try:
            self.quick_find_element(*self.__error_el)
            return True
        except Exception as e:
            logger.info(e)
            return False

    def __img_ele(self):
        return self.find_element(*self.__img)

    def __img_src(self):
        return self.find_element(*self.__img_url).get_attribute('src')

    # ITER
    # def cut_image(self, ele):
    #     left = ele.location['x']
    #     top = ele.location['y']
    #     right = ele.location['x'] + ele.size['width']
    #     bottom = ele.location['y'] + ele.size['height']
    #     im = Image.open(self.filepath)
    #     im = im.crop((left, top, right, bottom))
    #     im.save(self.filepath)

    def __qrcode_process(self):
        flag = self.__get_error_el()
        if flag:
            self.script("document.querySelector('.J_QRCodeRefresh').click()")
        img_src = self.__img_src()
        image_byte = requests.get(img_src).content
        img_name = img_src.split('/')[-1]
        url = 'http://120.55.113.9:8080/spider-server/web/api/loginQrCode'
        files = {'file': (img_name, image_byte)}
        sdata = {'spiderServerName': 'spider-10001', 'msg': '测试'}
        response = requests.post(url, data=sdata, files=files)
        logger.info(response)

    def parse_page(self):
        raise NotImplementedError

    # def data_process(self):
    #     raise NotImplementedError
