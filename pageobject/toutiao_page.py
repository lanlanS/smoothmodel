# coding=utf-8
import os
import time
from utill.Setup import appsetUp
from utill.commonMethod import commonmethod


class ToutiaoPage():
    def __init__(self):
        self.toutiao_setup = appsetUp(driver=None)

        # App Info
        self.tt_pkgname = 'com.ss.android.article.news'
        self.tt_mainActivity = 'com.ss.android.article.news.activity.MainActivity'
        self.tt_surface = 'com.ss.android.article.news/com.ss.android.article.news.activity.MainActivity'

        # Element Info
        self.ViewpageID1 = ''

    def setup(self):
        self.toutiao_setup.setup(self.tt_pkgname, self.tt_mainActivity)
        self.cm = commonmethod(self.toutiao_setup.driver)

    def check_toutiaomainActivity(self):
        topactivity = \
            os.popen('adb shell dumpsys window ^|grep mCurrentFocus').readlines()[0].split(' ')[-1].strip().split('}')[0]
        for i in range(5):
            if topactivity != self.tt_surface:
                time.sleep(2)
            else:
                return True

    def swipDown_first_page(self):
        try:
            if self.check_toutiaomainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_up(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot start toutiao news '
        except:
            raise Exception

    def swipUp_first_page(self):

        try:
            if self.check_toutiaomainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_down(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot start toutiao news '
        except:
            raise Exception

    def swipe_alone_first_page(self):
        try:
            if self.check_toutiaomainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_up(during=400)
                    self.cm.my_swipe_to_down(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot start toutiao news '
        except:
            raise Exception

    def teardown(self):
        self.toutiao_setup.teardown()
