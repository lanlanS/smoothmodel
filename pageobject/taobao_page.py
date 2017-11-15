# coding=utf-8
import os
import time
from utill.Setup import appsetUp
from utill.commonMethod import commonmethod


class TbPage():
    def __init__(self):
        self.tb_setup = appsetUp(driver=None)

        # App Info
        self.tb_pkgname = 'com.taobao.taobao'
        self.tb_mainActivity = 'com.taobao.tao.homepage.MainActivity3'
        self.tb_surface = 'com.taobao.taobao/com.taobao.tao.homepage.MainActivity3'

        # Element Info
        self.ViewpageID1 = ''

    def setup(self):
        self.tb_setup.setup(self.tb_pkgname, self.tb_mainActivity)
        self.cm = commonmethod(self.tb_setup.driver)

    def check_tbmainActivity(self):
        topactivity = \
            os.popen('adb shell dumpsys window ^|grep mCurrentFocus').readlines()[0].split(' ')[-1].strip().split('}')[0]
        for i in range(5):
            if topactivity != self.tb_surface:
                time.sleep(2)
            else:
                return True
                #if self.cm.waitElementById(self.ViewpageID1):
                # retrun True

    def swipDown_first_page(self):
        try:
            if self.check_tbmainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_up(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot start taobao '
        except:
            raise Exception

    def swipUp_first_page(self):

        try:
            if self.check_tbmainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_down(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot start taobao'
        except:
            raise Exception

    def swipe_alone_first_page(self):
        try:
            if self.check_tbmainActivity():
                for i in range(0, 10):
                    self.cm.my_swipe_to_up(during=400)
                    self.cm.my_swipe_to_down(during=400)
                    time.sleep(0.1)
                    i += 1
            else:
                print 'Connot start taobao '
        except:
            raise Exception

    def teardown(self):
        self.tb_setup.teardown()
