# coding=utf-8
import os
import time
from utill.Setup import appsetUp
from utill.commonMethod import commonmethod


class SettingPage():
    def __init__(self):
        self.settings_setup = appsetUp(driver=None)

        # App Info
        self.settings_pkgname = 'com.android.settings'
        self.settings_mainActivity = '.Settings'
        self.settings_surface = 'com.android.settings/com.android.settings.Settings'

        # Element Info
        self.wifiicon = 'com.android.settings:id/title'  # com.android.settings:id/title [2]
        self.searchicon = 'com.android.settings:id/search'  # com.android.settings:id/search  搜索id

    def setup(self):
        self.settings_setup.setup(self.settings_pkgname, self.settings_mainActivity)
        self.cm = commonmethod(self.settings_setup.driver)

    def check_mainActivity(self):
        topactivity = \
            os.popen('adb shell dumpsys window ^|grep mCurrentFocus').readlines()[0].split(' ')[-1].strip().split('}')[
                0]
        for i in range(5):
            if topactivity != self.settings_mainActivity:
                time.sleep(2)
            else:
                return True

    def swipDown_first_page(self):
        try:
            for i in range(0, 3):
                self.cm.my_swipe_to_up(during=400)
                time.sleep(0.1)
                i += 1
        except:
            raise Exception

    def swipeUp_first_page(self):
        try:
            for i in range(0, 3):
                self.cm.my_swipe_to_down(during=400)
                time.sleep(0.1)
                i += 1
        except:
            raise Exception

    def swipe_alone_first_page(self):
        try:
            for i in range(0, 10):
                self.cm.my_swipe_to_up(during=400)
                self.cm.my_swipe_to_down(during=400)
                time.sleep(0.1)
                i += 1
        except:
            raise Exception

    def wifipage_click(self):  # 无线网络界面 来回切换
        try:
            if self.cm.shortwaitElementById(self.searchicon):  # 进入搜索界面
                for i in range(0, 5):
                    if self.cm.shortwaitElementById(self.wifiicon):
                        self.cm.driver.find_elements_by_id(self.wifiicon)[1].click()
                        time.sleep(0.1)
                        self.cm.back()
            else:
                print 'wifi page click error.'
                raise Exception
        except:
            raise Exception

    def wifipage_swipe(self):  # 无线网络界面上下滑动
        try:
            if self.cm.shortwaitElementById(self.wifiicon):
                self.cm.driver.find_elements_by_id(self.wifiicon)[1].click()
                for i in range(0, 5):
                    self.cm.my_swipe_to_down(during=400)
                for i in range(0, 5):
                    self.cm.my_swipe_to_up(during=400)
                    time.sleep(0.1)
        except:
            raise Exception

    def teardown(self):
        self.settings_setup.teardown()
