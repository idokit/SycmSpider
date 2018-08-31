from selenium.webdriver.common.by import By
from .NewBasePage import NewBasePage
import time
from PIL import Image
import requests


class NewLogin(NewBasePage):
    _baseUrl = 'https://sycm.taobao.com/portal/home.htm'

    def __init__(self, *args, **kw):
        super(NewLogin, self).__init__(*args, **kw)

    def open(self):
        self._open(self._baseUrl)

    error_el = (By.CSS_SELECTOR, ".msg-err")

    img = (By.ID, 'J_QRCodeImg')

    filepath = 'screenshot.png'

    a_market = (By.XPATH,
                '//*[@id="app"]/div[@class="root-container"]//ul[@class="menu-list clearfix"]/li/a[@class="nameWrapper" and @data-spm="d1057"]/span')

    a_sycm = (By.XPATH, "//ul[@id='ks-accordion-tab-panel52']/li[4]/span/a")

    img_close = (By.CSS_SELECTOR, ".ebase-ImageTips__dsImageTipsCloseBtn")

    img_url = (By.XPATH, '//div[@id="J_QRCodeImg"]/img')

    def a_market_click(self):
        """[点击市场]
       """
        self.find_element(*self.a_market).click()

    def find_dialog(self):
        try:
            self.quick_find_element(*self.img_close)
            self.quick_find_element(*self.img_close).click()
        except Exception as e:
            # self.logger.info()
            print(str(e))

    def get_error_el(self):
        try:
            self.quick_find_element(*self.error_el)
            return True
        except Exception as e:
            print(e)
            return False

    def img_ele(self):
        return self.find_element(*self.img)

    def img_src(self):
        return self.find_element(*self.img_url).get_attribute('src')

    def cut_image(self, ele):
        left = ele.location['x']
        top = ele.location['y']
        right = ele.location['x'] + ele.size['width']
        bottom = ele.location['y'] + ele.size['height']
        im = Image.open(self.filepath)
        im = im.crop((left, top, right, bottom))
        im.save(self.filepath)

    def qrcode_process(self):
        flag = self.get_error_el()
        if flag:
            self.script("document.querySelector('.J_QRCodeRefresh').click()")
        img_src = self.img_src()
        image_byte = requests.get(img_src).content
        img_name = img_src.split('/')[-1]

        url = 'http://120.55.113.9:8080/spider-server/web/api/loginQrCode'
        files = {'file': (img_name, image_byte)}
        sdata = {'spiderServerName': 'spider-10001', 'msg': '测试'}

        response = requests.post(url, data=sdata,
                                 files=files)
        print(response)

    def login(self):
        self.open()
        try:
            self.script("document.querySelector('#J_Static2Quick').click()")
        except Exception as e:
            print(e)
        count = 0
        while 'https://sycm.taobao.com/portal/home.htm' not in self.driver.current_url:
            print('登陆中')
            if 'https://mai.taobao.com/seller_admin.htm' in self.driver.current_url:
                self.script("window.location.replace('https://sycm.taobao.com/portal/home.htm')")
            if count % 30 == 0:
                try:
                    self.qrcode_process()
                except Exception as e:
                    print(e)
            else:
                time.sleep(10)
            count += 1
        print('登陆成功')
        self.find_dialog()
        time.sleep(1)
        return self
