# coding=utf-8
import unittest

import time

from datacollector.getFramestats import GetFramestats
from datacollector.getFps import SurfaceStatsCollector
from utill.Setup import appsetUp
from utill.commonMethod import commonmethod
from pageobject.wechat_page import WechatPage
from utill.func_tools import func


class wechattest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wechat_po = WechatPage()
        cls.getfps = SurfaceStatsCollector(cls.wechat_po.wechat_surface)
        cls.getframe = GetFramestats(cls.wechat_po.wechat_pkgname)
        print 'Setup \n'
        cls.wechat_po.setup()

    @classmethod
    def tearDownClass(cls):
        cls.wechat_po.teardown()
        # print "continue to next case"

    def setUp(self):
        # self.wechat_po = wechatPage()
        # self.getfps = SurfaceStatsCollector(self.wechat_po.wechat_surface)
        # self.getframe = GetFramestats(self.wechat_po.wechat_pkgname)
        # print 'Setup \n'
        # self.wechat_po.setup()
        print 'wait 3s...'
        time.sleep(3)
        print 'Setup end \n'

    def tearDown(self):
        print ' Test end.'

    def test_1_enterMonents(self):
        caseid = '1'
        caseName = u'滑动朋友圈'
        print "case id:" + caseid
        print "case Name:" + caseName
        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(1):
                    self.getfps.Start()  # start collect fps

                    self.wechat_po.enter_monents_page()

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
            pass

    def test_2_chatpage(self):
        caseid = '2'
        caseName = u'快速输入聊天信息'
        print "case id:" + caseid
        print "case Name:" + caseName
        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(1):
                    self.getfps.Start()  # start collect fps

                    self.wechat_po.chatwithsb()

                    results = self.getfps.SampleResults()
                    fps.append(results[1].value)
                    jank_count.append(results[2].value)
                    max_frame_delay.append(results[3].value)

                    self.getfps.Stop()
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
            pass

    def test_3_switchwindow(self):
        caseid = '3'
        caseName = u"连续窗口切换"
        print "case id:" + caseid
        print "case Name:" + caseName
        try:
            fps = []
            jank_count = []
            max_frame_delay = []
            if self.getframe.clear_FrameStats():
                for loop in range(5):
                    self.getfps.Start()  # start collect fps
                    self.wechat_po.switchwindow()
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
                print 'jank count: ' + str(max(jank_count[1:]))
                print jank_count
                print 'max frame delay: ' + str(max(max_frame_delay[1:]))
                print max_frame_delay

                self.getframe.beginProcessResult(caseid)
            except:
                print u'数据收集有误'

        except Exception:
            self.getframe.dumpsysFramestats(caseid)
            self.error_info()
            pass

    def test_4_switchchatpage(self):
        caseid = '4'
        caseName = u"连续滑动聊天记录界面"
        print "case id:" + caseid
        print "case Name:" + caseName
        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(1):
                    self.getfps.Start()  # start collect fps

                    self.wechat_po.swipUp_chatpage()

                    results = self.getfps.SampleResults()
                    fps.append(results[1].value)
                    jank_count.append(results[2].value)
                    max_frame_delay.append(results[3].value)

                    self.getfps.Stop()
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
            pass

    def test_5_swipesubscription(self):
        caseid = '5'
        caseName = u"连续滑动订阅号"
        print "case id:" + caseid
        print "case Name:" + caseName
        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            if self.getframe.clear_FrameStats():
                for loop in range(1):
                    self.getfps.Start()  # start collect fps

                    self.wechat_po.swipe_subscription()

                    results = self.getfps.SampleResults()
                    fps.append(results[1].value)
                    jank_count.append(results[2].value)
                    max_frame_delay.append(results[3].value)

                    self.getfps.Stop()
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
            pass

    def test_6_swipeMyPosts(self):
        caseid = '6'
        caseName = u"连续滑动我-相册"
        # funcname = 'self.wechat_po.swipe_myPosts()'
        # func(caseid, caseName, funcname)
        print "case id:" + caseid
        print "case Name:" + caseName

        fps = []
        jank_count = []
        max_frame_delay = []

        try:
            if self.getframe.clear_FrameStats():
                for loop in range(1):
                    self.getfps.Start()  # start collect fps

                    eval('self.wechat_po.swipe_myPosts()')

                    results = self.getfps.SampleResults()
                    fps.append(results[1].value)
                    jank_count.append(results[2].value)
                    max_frame_delay.append(results[3].value)

                    self.getfps.Stop()
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
            pass

    def test_7_swipeMyFriendList(self):
        caseid = '7'
        caseName = u"连续滑动联系人列表"
        # funcname = 'self.wechat_po.swipe_myPosts()'
        # func(caseid, caseName, funcname)
        print "case id:" + caseid
        print "case Name:" + caseName

        fps = []
        jank_count = []
        max_frame_delay = []

        try:
            if self.getframe.clear_FrameStats():
                for loop in range(1):
                    self.getfps.Start()  # start collect fps

                    self.wechat_po.swipe_friendlist()

                    results = self.getfps.SampleResults()
                    fps.append(results[1].value)
                    jank_count.append(results[2].value)
                    max_frame_delay.append(results[3].value)

                    self.getfps.Stop()
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

    def test_8_swipe_friendalbum(self):
        caseid = '8'
        caseName = u"查看好友朋友圈"
        # funcname = 'self.wechat_po.swipe_myPosts()'
        # func(caseid, caseName, funcname)
        print "case id:" + caseid
        print "case Name:" + caseName

        fps = []
        jank_count = []
        max_frame_delay = []

        try:
            if self.getframe.clear_FrameStats():
                for loop in range(1):
                    self.getfps.Start()  # start collect fps

                    self.wechat_po.swipe_friendsAlbum()

                    results = self.getfps.SampleResults()
                    fps.append(results[1].value)
                    jank_count.append(results[2].value)
                    max_frame_delay.append(results[3].value)

                    self.getfps.Stop()
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

    def test_9_view_pic(self):
        caseid = '9'
        caseName = u"放大查看聊天中图片"
        # funcname = 'self.wechat_po.swipe_myPosts()'
        # func(caseid, caseName, funcname)
        print "case id:" + caseid
        print "case Name:" + caseName

        fps = []
        jank_count = []
        max_frame_delay = []

        try:
            if self.getframe.clear_FrameStats():
                for loop in range(1):
                    self.getfps.Start()  # start collect fps

                    self.wechat_po.view_pic()

                    results = self.getfps.SampleResults()
                    fps.append(results[1].value)
                    jank_count.append(results[2].value)
                    max_frame_delay.append(results[3].value)

                    self.getfps.Stop()
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
