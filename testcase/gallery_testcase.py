# coding=utf-8
import unittest

import time

from datacollector.getFramestats import GetFramestats
from datacollector.getFps import SurfaceStatsCollector
from pageobject.gallery_page import GalleryPage


class Gallerytest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gallery_po = GalleryPage()
        cls.getfps = SurfaceStatsCollector(cls.gallery_po.gallery_surface)
        cls.getframe = GetFramestats(cls.gallery_po.gallery_pkgname)
        print 'Setup \n'
        cls.gallery_po.setup()

    @classmethod
    def tearDownClass(cls):
        cls.gallery_po.teardown()

    def setUp(self):
        # self.weibo_po = ZhihuPage()
        # self.getfps = SurfaceStatsCollector(self.weibo_po.zhihu_surface)
        # self.getframe = GetFramestats(self.weibo_po.zhihu_pkgname)
        # print 'Setup \n'
        # self.weibo_po.setup()
        print 'wait 3s...'
        time.sleep(1.5)
        print 'Setup end \n'

    def tearDown(self):
        print ' Test end.'
        # self.weibo_po.teardown()

    def test_1_gallery_swipedown_Mainpage(self):
        caseid = '1'
        caseName = u'图库滑动'
        print "case id:" + caseid
        print "case Name:" + caseName
        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(5):
                    self.getfps.Start()  # start collect fps

                    self.gallery_po.swipDown_first_page()
                    self.gallery_po.swipeUp_first_page()

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
