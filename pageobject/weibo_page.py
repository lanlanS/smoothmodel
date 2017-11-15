# coding=utf-8
import os
import time
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

    def setup(self):
        self.weibo_setup.setup(self.weibo_pkgname, self.weibo_mainActivity)
        self.cm = commonmethod(self.weibo_setup.driver)

    def check_mainActivity(self):
        topactivity = \
            os.popen('adb shell dumpsys window ^|grep mCurrentFocus').readlines()[0].split(' ')[-1].strip().split('}')[0]
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

    def teardown(self):
        self.weibo_setup.teardown()
