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
        self.tb_searchresult = 'com.taobao.taobao/com.taobao.search.mmd.SearchResultActivity'
        self.tb_goodsdetail = 'com.taobao.taobao/com.taobao.tao.detail.activity.DetailActivity'

        # Element Info
        self.ViewpageID1 = ''
        self.taobao_search_bar = 'com.taobao.taobao:id/home_searchedit'
        self.taobao_search_btn = 'com.taobao.taobao:id/searchbtn'
        self.gooditem = 'com.taobao.taobao:id/goodsimage'

    def setup(self):
        self.tb_setup.setup(self.tb_pkgname, self.tb_mainActivity)
        self.cm = commonmethod(self.tb_setup.driver)

    def check_tbmainActivity(self):
        topactivity = \
            os.popen('adb shell dumpsys window ^|grep mCurrentFocus').readlines()[0].split(' ')[-1].strip().split('}')[
                0]
        for i in range(5):
            if topactivity != self.tb_surface:
                time.sleep(2)
            else:
                return True
                # if self.cm.waitElementById(self.ViewpageID1):
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

    def find_a_goods(self):
        search_bar = self.cm.driver.find_element_by_id(self.taobao_search_bar)
        if search_bar:
            search_bar.click()
            search_btn = self.cm.driver.find_element_by_id(self.taobao_search_btn)
            if search_btn:
                search_btn.click()
                goods = self.cm.driver.find_element_by_id(self.gooditem)
                if goods:
                    return goods

    def switch_goodspage(self):
        goods = self.find_a_goods()
        for i in range(0, 10):
            goods.click()
            time.sleep(0.3)
            self.cm.back()

    def swipe_goodspage(self):
        goods = self.find_a_goods()
        goods.click()
        time.sleep(0.3)

        if self.cm.driver.find_element_by_id('com.taobao.taobao:id/detail_main_title_text'):
            for i in range(0, 10):
                self.cm.my_swipe_to_down(during=400)
        else:
            print 'not the goods page'

    def teardown(self):
        self.tb_setup.teardown()
