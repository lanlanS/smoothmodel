# coding=utf-8
import os
import time

from selenium.common.exceptions import NoSuchElementException

from utill.Setup import appsetUp
from utill.commonMethod import commonmethod


class ZhihuPage():
    def __init__(self):
        self.zhihu_setup = appsetUp(driver=None)

        # App Info
        self.zhihu_pkgname = 'com.zhihu.android'
        self.zhihu_mainActivity = '.app.ui.activity.MainActivity'
        self.zhihu_surface = 'com.zhihu.android/com.zhihu.android.app.ui.activity.MainActivity'

        # Element Info
        self.ViewpageID1 = ' com.zhihu.android:id / tab_title'

    def setup(self):
        self.zhihu_setup.setup(self.zhihu_pkgname, self.zhihu_mainActivity)
        self.cm = commonmethod(self.zhihu_setup.driver)

    def check_mainActivity(self):
        topactivity = \
            os.popen('adb shell dumpsys window ^|grep mCurrentFocus').readlines()[0].split(' ')[-1].strip().split('}')[0]
        for i in range(5):
            if topactivity != self.zhihu_surface:
                time.sleep(2)
            else:
                return True
                #if self.cm.waitElementById(self.ViewpageID1):
                # retrun True

    def swipDown_first_page(self):
        try:
            if self.check_mainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_up(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot open zhihu APP\'s MainPage'
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
                print 'Connot open zhihu APP\'s MainPage'
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
                print 'Connot open zhihu APP\'s MainPage'
        except:
            raise Exception

    def find_context(self):
        try:
            content = self.cm.driver.find_element_by_id("com.zhihu.android:id/body")
            if content:
                return content
        except NoSuchElementException:
            raise Exception

    def swipe_down_contentpage(self):
        content = self.find_context()
        content.click()
        time.sleep(1)
        if self.cm.driver.find_element_by_id('com.zhihu.android:id/comment_btn'):  # 判断是否进入文章界面，存在 评论id
            for i in range(0, 5):
                self.cm.my_swipe_to_up(during=400)
            for i in range(0, 5):
                self.cm.my_swipe_to_down(during=400)
            self.cm.back()

    def swich_contentpage(self):
        for i in range(0, 3):
            content = self.find_context()
            content.click()
            time.sleep(1)
            self.cm.back()

    def teardown(self):
        self.zhihu_setup.teardown()
