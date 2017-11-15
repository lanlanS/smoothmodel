# coding=utf-8
import unittest

import time

from datacollector.getFramestats import GetFramestats
from datacollector.getFps import SurfaceStatsCollector
from pageobject.zhihu_page import ZhihuPage


class zhihutest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.zhihu_po = ZhihuPage()
        cls.getfps = SurfaceStatsCollector(cls.zhihu_po.zhihu_surface)
        cls.getframe = GetFramestats(cls.zhihu_po.zhihu_pkgname)
        print 'Setup \n'
        cls.zhihu_po.setup()

    @classmethod
    def tearDownClass(cls):
        cls.zhihu_po.teardown()
        # print "continue to next case"

    def setUp(self):
        # self.zhihu_po = ZhihuPage()
        # self.getfps = SurfaceStatsCollector(self.zhihu_po.zhihu_surface)
        # self.getframe = GetFramestats(self.zhihu_po.zhihu_pkgname)
        # print 'Setup \n'
        # self.zhihu_po.setup()
        print 'wait 3s...'
        time.sleep(3)
        print 'Setup end \n'

    def tearDown(self):
        print ' Test end.'
        # self.zhihu_po.teardown()

    def test_1_swipedown_Mainpage(self):
        caseid = '0'
        caseName = u'知乎首页向下滑动'
        print "case id:" + caseid
        print "case Name:" + caseName
        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(5):
                    self.getfps.Start()  # start collect fps

                    self.zhihu_po.swipDown_first_page()

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
            print 'swipe action error..'

    def test_2_swipe_Mainpage(self):

        caseid = '1'
        caseName = u'知乎首页来回滑动'
        print "case id:" + caseid
        print "case Name:" + caseName
        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(5):
                    self.getfps.Start()  # start collect fps

                    self.zhihu_po.swipe_alone_first_page()

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
            print 'swipe action error..'

    def _output(self, fps, jank_count, max_frame_delay):
        print 'fps: ' + str(fps)
        print fps
        print 'jank count: ' + str(max(jank_count))
        print jank_count
        print 'max frame delay: ' + str(max(max_frame_delay))
        print max_frame_delay
