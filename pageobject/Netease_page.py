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
            time.sleep(0.5)
            news_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/' \
                         'android.widget.LinearLayout/android.widget.FrameLayout/com.netease.nr.phone.main.view.NTDrawerLayout/' \
                         'android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/' \
                         'android.widget.FrameLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout/' \
                         'android.view.ViewGroup/android.view.ViewGroup/android.support.v7.widget.RecyclerView/' \
                         'android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout/' \
                         'android.widget.TextView'
            content = self.cm.driver.find_element_by_xpath(news_xpath)  # com.netease.newsreader.activity:id/eu
            time.sleep(0.3)
            content.click()
            time.sleep(0.5)
            self.cm.back()

    def teardown(self):
        self.neteasenews_setup.teardown()
