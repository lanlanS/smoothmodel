# coding=utf-8
import os
import time

from selenium.common.exceptions import NoSuchElementException

from utill.Setup import appsetUp
from utill.commonMethod import commonmethod


class WeiboPage():
    def __init__(self):
        self.weibo_setup = appsetUp(driver=None)

        # App Info
        self.weibo_pkgname = 'com.sina.weibo'
        self.weibo_mainActivity = 'com.sina.weibo.VisitorMainTabActivity'
        self.weibo_surface = 'com.sina.weibo/com.sina.weibo.VisitorMainTabActivity'

        # Element Info
        self.ViewpageID1 = 'com.sina.weibo:id/plus_icon'
        self.firstpage_xpath = '//android.view.View[@content-desc="微博"]'

    def setup(self):
        self.weibo_setup.setup(self.weibo_pkgname, self.weibo_mainActivity)
        self.cm = commonmethod(self.weibo_setup.driver)

    def check_mainActivity(self):
        topactivity = \
            os.popen('adb shell dumpsys window ^|grep mCurrentFocus').readlines()[0].split(' ')[-1].strip().split('}')[
                0]
        for i in range(5):
            if topactivity != self.weibo_surface:
                time.sleep(2)
            else:
                return True

    def swipDown_first_page(self):
        try:
            if self.check_mainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_up(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot open Weibo'
        except:
            raise Exception

    def swipUp_first_page(self):

        try:
            if self.check_mainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_down(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot open Weibo'
        except:
            raise Exception

    def swipe_alone_first_page(self):
        try:
            if self.check_mainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_up(during=400)
                    self.cm.my_swipe_to_down(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot open Weibo'
        except:
            raise Exception

    def _isMov(self):
        not_pic = 'com.sina.weibo:id/surface_view'
        try:
            self.cm.driver.find_element_by_id(not_pic)
            return True
        except NoSuchElementException:
            print not_pic + 'not found'
            return False
            pass

    def _isPic(self):
        pic = 'com.sina.weibo:id/blog_picture_view'  # 8.0.1 com.sina.weibo:id/blog_picture_view
        try:
            self.cm.driver.find_element_by_id(pic)
            return True
        except NoSuchElementException:
            # print pic + 'not found'
            return False
            pass

    def clickpic(self):
        while self._isMov():  # 判断是否有图片
            time.sleep(0.3)
            self.cm.driver.find_element_by_xpath(self.firstpage_xpath).click()
            if self._isPic():
                for i in range(0, 8):
                    time.sleep(0.8)
                    self.cm.driver.find_element_by_id('com.sina.weibo:id/blog_picture_view').click()
                    time.sleep(0.8)
                    self.cm.back()
                break
            else:
                self.cm.driver.find_element_by_xpath(self.firstpage_xpath).click()
                pass
        else:
            if self._isPic():
                for i in range(0, 8):
                    self.cm.shortwaitElementById('com.sina.weibo:id/blog_picture_view').click()
                    time.sleep(0.8)
                    self.cm.back()
                    time.sleep(0.8)

    def teardown(self):
        self.weibo_setup.teardown()
