# coding=utf-8
import os
import time
from utill.Setup import appsetUp
from utill.commonMethod import commonmethod


class NeteasePage():
    def __init__(self):
        self.neteasenews_setup = appsetUp(driver=None)

        # App Info
        self.neteasenews_pkgname = 'com.netease.newsreader.activity'
        self.neteasenews_mainActivity = 'com.netease.nr.biz.ad.AdActivity'
        self.neteasenews_surface = 'com.netease.newsreader.activity/com.netease.nr.phone.main.MainActivity'
        self.neteasenews_detailActivity = 'com.netease.newsreader.activity/com.netease.nr.biz.news.detailpage.NewsPageActivity'

        # Element Info
        self.newsitem = ''

    def setup(self):
        self.neteasenews_setup.setup(self.neteasenews_pkgname, self.neteasenews_mainActivity)
        self.cm = commonmethod(self.neteasenews_setup.driver)

    def check_neteasenewsmainActivity(self):
        topactivity = \
            os.popen('adb shell dumpsys window ^|grep mCurrentFocus').readlines()[0].split(' ')[-1].strip().split('}')[
                0]
        for i in range(5):
            if topactivity != self.neteasenews_surface:
                time.sleep(2)
            else:
                return True

    def swipDown_first_page(self):
        try:
            if self.check_neteasenewsmainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_up(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot start Netease News Reader '
        except:
            raise Exception

    def swipUp_first_page(self):

        try:
            if self.check_neteasenewsmainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_down(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot start Netease News Reader '
        except:
            raise Exception

    def swipe_alone_first_page(self):
        try:
            if self.check_neteasenewsmainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_up(during=400)
                    self.cm.my_swipe_to_down(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot start Netease News Reader '
        except:
            raise Exception

    def switch_newspage(self):
        for i in range(0, 5):
            content = self.cm.driver.find_element_by_id("com.netease.newsreader.activity:id/ea")
            content.click()
            time.sleep(1)
            self.cm.back()

    def teardown(self):
        self.neteasenews_setup.teardown()
