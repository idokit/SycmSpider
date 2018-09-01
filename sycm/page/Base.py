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

logger = logging.getLogger(__name__)


class Base(object):

    def __init__(self, driver,  **kwargs):
        self.driver = driver

    def on_page(self, pagetitle):
        return pagetitle in self.driver.title



    def find_element(self, *loc):
        try:
            ele = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(loc))
            self.script("window.scroll(0,%r-window.innerHeight)" % ele.location["y"])
            return ele
        except TimeoutError as e:
            logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
            raise e

    def quick_find_element(self, *loc):
        try:
            ele = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(loc))
            self.script("window.scroll(0,%r-window.innerHeight)" % ele.location["y"])
            return ele
        except TimeoutError as e:
            logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
            raise e

    def find_elements(self, *loc):
        try:
            eles = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(loc))
            return eles
        except Exception as e:
            logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
            raise e

    def switch_frame(self, loc):
        return self.driver.switch_to_frame(loc)

    def script(self, src):
        self.driver.execute_script(src)

    def send_keys(self, loc, vaule, clear_first=True, click_first=True):
        try:
            loc = getattr(self, "_%s" % loc)
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
            raise AttributeError

    def click_item(self, *loc):
        try:
            ele = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(loc))
            self.script("window.scroll(0,%r-window.innerHeight)" % (ele.location["y"] + 100))
            self.script("document.querySelector(%r).click()" % loc[1])
            return ele
        except Exception as e:
            logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
            raise e

    def click_items(self, index, *loc):
        try:
            ele = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(loc))
            self.script("document.querySelectorAll(%r)[%r].click()" % (loc[1], index))
        except Exception as e:
            logger.error(u"%s 页面中未能找到 %s 元素" % (self, loc))
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
            logger.info(e)
            return False

    def get_cookie(self):
        if self.driver.get_cookies():
            return [item["name"] + "=" + item["value"] for item in self.driver.get_cookies()]
        else:
            logger.info('未获取到cookie')
            return None
