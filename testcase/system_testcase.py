# coding=utf-8
import os
import unittest

import time
from datacollector.getFramestats import GetFramestats
from datacollector.getFps import SurfaceStatsCollector
from pageobject.system_page import SystemPage
from utill.adbMethod import adbmethod


class Systemtest(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     cls.system_po = SystemPage()
    #     cls.action = adbmethod()
    #     print 'Setup \n'
    #     # cls.systemui_po.setup()
    #
    # @classmethod
    # # def tearDownClass(cls):
    # # cls.systemui_po.teardown()
    # # print "continue to next case"

    def setUp(self):
        self.system_po = SystemPage()
        self.action = adbmethod()
        print 'Setup \n'
        print 'wait 3s...'
        time.sleep(1)
        print 'Setup end \n'

    def tearDown(self):
        print ' Test end.'

    def test_1_dropDownNotification(self):
        caseid = '0'
        caseName = u'下拉通知栏'
        print "case id:" + caseid
        print "case Name:" + caseName

        self.getfps = SurfaceStatsCollector(self.system_po.systemui_surface)
        self.getframe = GetFramestats(self.system_po.systemui_pkgname)
        self.action.adb_homekey()

        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(5):
                    self.getfps.Start()  # start collect fps

                    for i in range(0, 5):
                        self.action.adb_swipe_action('down')
                        time.sleep(0.3)
                        self.action.adb_backkey()
                        time.sleep(0.3)

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
        self.action.adb_homekey()  # 回到桌面

    def test_2_swipe_recents(self):
        caseid = '0'
        caseName = u'呼出任务管理器'
        print "case id:" + caseid
        print "case Name:" + caseName

        self.getfps = SurfaceStatsCollector(self.system_po.systemui_surface)
        self.getframe = GetFramestats(self.system_po.systemui_pkgname)
        self.action.adb_homekey()

        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(5):
                    self.getfps.Start()  # start collect fps

                    os.popen('adb shell am broadcast -a com.android.systemui.TOGGLE_RECENTS')
                    time.sleep(0.3)
                    for i in range(0, 5):
                        self.action.adb_swipe_action('right')
                        time.sleep(0.3)
                    self.action.adb_backkey()
                    time.sleep(0.3)

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

        self.action.adb_homekey()  # 回到桌面

    def test_3_swipe_launcher(self):
        caseid = '3'
        caseName = u'桌面来回滑动'
        print "case id:" + caseid
        print "case Name:" + caseName

        self.getfps = SurfaceStatsCollector(self.system_po.launcher_layer)
        self.getframe = GetFramestats(self.system_po.launcher_pkgname)
        self.action.adb_homekey()

        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(5):
                    self.getfps.Start()  # start collect fps
                    for i in range(0, 5):
                        self.action.adb_swipe_action('right')
                        time.sleep(0.3)
                    for i in range(0, 5):
                        self.action.adb_swipe_action('left')
                        time.sleep(0.3)

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

        self.action.adb_homekey()  # 回到桌面

    def error_info(self):
        self.getfps.Stop()
        print 'fps: 0'
        print '0'
        print 'jank count: 0'
        print '0'
        print 'max frame delay: 0'
        print '0'
