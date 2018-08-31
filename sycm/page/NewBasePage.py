# coding=utf-8
'''
Created on 2018-3-6
@author: Zhouyi
Project:基础类BasePage，封装所有页面都公用的方法，
定义open函数，重定义find_element，switch_frame，send_keys等函数。
在初始化方法中定义驱动driver，基本url，title
WebDriverWait提供了显式等待方式。
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.webdriver.support.events import EventFiringWebDriver
import time

base_logger = logging.getLogger('基础模块')


class NewBasePage(object):
    """
    BasePage封装所有页面都公用的方法，例如driver, url ,FindElement等
    """

    def __init__(self, *, driver):
        self.driver = driver
        pass

    def on_page(self, pagetitle):
        """[通过title断言进入的页面是否正确。
        使用title获取当前窗口title，检查输入的title是否在当前title中，返回比较结果（True 或 False）]

        Arguments:
            pagetitle {[type]} -- [description]

        Returns:
            [str] -- [description]
        """
        return pagetitle in self.driver.title

    def _open(self, url):
        """[ #以单下划线_开头的方法，在使用import *时，该方法不会被导入，保证该方法为类私有的。]

        Arguments:
            url {[type]} -- [description]
            pagetitle {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        self.driver.get(url)
        self.driver.maximize_window()

    def open(self):
        self._open(self.base_url)

    def find_element(self, *loc):
        #        return self.driver.find_element(*loc)
        """[确保元素是可见的。
            注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver,10).until
            (lambda driver: driver.find_element(*loc).is_displayed())
            注意：以下入参本身是元组，不需要加*]
        Returns:
            [type] -- [description]
        """
        try:
            ele = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(loc))
            self.script("window.scroll(0,%r-window.innerHeight)" % ele.location["y"])
            return ele
        except TimeoutError as e:
            base_logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
            raise e

    def quick_find_element(self, *loc):
        #        return self.driver.find_element(*loc)
        """[确保元素是可见的。
            注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver,10).until
            (lambda driver: driver.find_element(*loc).is_displayed())
            注意：以下入参本身是元组，不需要加*]
        Returns:
            [type] -- [description]
        """
        try:
            ele = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(loc))
            self.script("window.scroll(0,%r-window.innerHeight)" % ele.location["y"])
            return ele
        except TimeoutError as e:
            base_logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
            raise e

    def find_elements(self, *loc):
        """[查找元素]
        """
        try:
            eles = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(loc))
            # self.script("window.scroll(0,%r-window.innerHeight)" % eles[len(eles) - 1].location["y"])
            return eles
        except Exception as e:
            base_logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
            raise e

    def switch_frame(self, loc):
        """[切换frame]

        Arguments:
            loc {[type]} -- [description]
        """
        return self.driver.switch_to_frame(loc)

    def script(self, src):
        """[执行js脚本]

        Arguments:
            src {[String]} -- [description]
        """
        self.driver.execute_script(src)

    def send_keys(self, loc, vaule, clear_first=True, click_first=True):
        """[输入值]

        Arguments:
            loc {[type]} -- [元素]
            vaule {[String]} -- [字符串]

        Keyword Arguments:
            clear_first {bool} -- [是否先清清除] (default: {True})
            click_first {bool} -- [是否先点击] (default: {True})
        """
        try:
            loc = getattr(self, "_%s" % loc)
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            base_logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
            print(u"%s 页面中未能找到 %s 元素" % (self, loc))
            raise AttributeError

    def click_item(self, *loc):
        try:
            ele = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(loc))
            self.script("window.scroll(0,%r-window.innerHeight)" % (ele.location["y"] + 100))
            self.script("document.querySelector(%r).click()" % loc[1])
            return ele
        except Exception as e:
            base_logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
            raise e

    def click_items(self, index,*loc):
        try:
            ele = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(loc))
            self.script("document.querySelectorAll(%r)[%r].click()" % (loc[1], index))
        except Exception as e:
            base_logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
            raise e

    def session_expired(self):
        try:
            ele = self.find_element(By.CSS_SELECTOR, ".ui-message-error .ui-message-content")
            if ele.text == "亲，您的登录信息已过期，请重新登录。":
                return True
            else:
                print(ele.text)
                return False
        except TimeoutError as e:
            print(e)
            return False
