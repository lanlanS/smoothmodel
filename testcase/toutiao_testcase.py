# coding=utf-8
import unittest

import time

from datacollector.getFramestats import GetFramestats
from datacollector.getFps import SurfaceStatsCollector
from pageobject.toutiao_page import ToutiaoPage


class SSnewstest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.toutiaonews_po = ToutiaoPage()
        cls.getfps = SurfaceStatsCollector(cls.toutiaonews_po.tt_surface)
        cls.getframe = GetFramestats(cls.toutiaonews_po.tt_pkgname)
        print 'Setup \n'
        cls.toutiaonews_po.setup()

    @classmethod
    def tearDownClass(cls):
        cls.toutiaonews_po.teardown()
        # print "continue to next case"

    def setUp(self):
        # self.weibo_po = ZhihuPage()
        # self.getfps = SurfaceStatsCollector(self.weibo_po.zhihu_surface)
        # self.getframe = GetFramestats(self.weibo_po.zhihu_pkgname)
        # print 'Setup \n'
        # self.weibo_po.setup()
        print 'wait 3s...'
        time.sleep(3)
        print 'Setup end \n'

    def tearDown(self):
        print ' Test end.'
        # self.weibo_po.teardown()

    def test_1_toutiao_swipedown_Mainpage(self):
        caseid = '0'
        caseName = u'今日头条首页快速向下滑动'
        print "case id:" + caseid
        print "case Name:" + caseName
        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(5):
                    self.getfps.Start()  # start collect fps

                    self.toutiaonews_po.swipDown_first_page()

                    results = self.getfps.SampleResults()
                    fps.append(results[1].value)
                    jank_count.append(results[2].value)
                    max_frame_delay.append(results[3].value)

                    self.getfps.Stop()
                    loop += 1
            self.getframe.dumpsysFramestats(caseid)  # start collect framestats

            try:
                print 'fps: ' + str(fps)
                print fps
                print 'jank count: ' + str(max(jank_count))
                print jank_count
                print 'max frame delay: ' + str(max(max_frame_delay))
                print max_frame_delay

                self.getframe.beginProcessResult(caseid)
            except:
                print u'数据收集有误'
        except Exception:
            self.getframe.dumpsysFramestats(caseid)
            self.error_info()

    def test_2_toutiao_swipeup_Mainpage(self):

        caseid = '1'
        caseName = u'今日头条首页快速向上滑动'
        print "case id:" + caseid
        print "case Name:" + caseName
        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(5):
                    self.getfps.Start()  # start collect fps

                    self.toutiaonews_po.swipUp_first_page()

                    results = self.getfps.SampleResults()
                    fps.append(results[1].value)
                    jank_count.append(results[2].value)
                    max_frame_delay.append(results[3].value)

                    self.getfps.Stop()
                    loop += 1
            self.getframe.dumpsysFramestats(caseid)  # start collect framestats

            try:
                print 'fps: ' + str(fps)
                print fps
                print 'jank count: ' + str(max(jank_count))
                print jank_count
                print 'max frame delay: ' + str(max(max_frame_delay))
                print max_frame_delay

                self.getframe.beginProcessResult(caseid)
            except:
                print u'数据收集有误'

        except Exception:
            self.getframe.dumpsysFramestats(caseid)
            self.error_info()

    def error_info(self):
        self.getfps.Stop()
        print 'fps: 0'
        print '0'
        print 'jank count: 0'
        print '0'
        print 'max frame delay: 0'
        print '0'
