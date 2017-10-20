# coding=utf-8
import unittest

import time

from datacollector.getFps import SurfaceStatsCollector
from utill.Setup import appsetUp
from utill.commonMethod import commonmethod


class wechattest(unittest.TestCase):
    def setUp(self):
        self.windowname = 'com.meizu.media.reader/com.meizu.media.reader.ReaderMainActivity'
        self.getfps = SurfaceStatsCollector(self.windowname)
        print 'Setup \n'
        self.wechatsetup = appsetUp(driver=None)
        self.wechatsetup.setup('com.meizu.media.reader',
                               '.ReaderMainActivity')  # com.meizu.media.reader/.ReaderMainActivity
        # initialize GetFPS()...
        self.cm = commonmethod(self.wechatsetup.driver)
        print 'Setup end \n'

    def tearDown(self):
        print 'teardown'
        self.wechatsetup.teardown()

    def test_swip_recordlist(self):
        try:
            print 'start test: swipe list'
            self.cm.waitElementById('com.meizu.media.reader:id/action_bar')
            time.sleep(2)
        except Exception:
            print 'open reader error...\n'

        try:
            fps = []
            jank_count = []
            max_frame_delay = []

            for loop in range(5):
                self.getfps.Start()
                for i in range(0, 10):
                    self.cm.my_swipe_to_up(during=400)
                    time.sleep(0.1)
                    i += 1
                results = self.getfps.SampleResults()

                fps.append(results[1].value)
                jank_count.append(results[2].value)
                max_frame_delay.append(results[3].value)

                self.getfps.Stop()
                loop += 1

            try:
                print 'fps: ' + str(fps)
                print fps
                print 'jank count: ' + str(max(jank_count))
                print jank_count
                print 'max frame delay: ' + str(max(max_frame_delay))
                print max_frame_delay
            except:
                print u'数据收集有误'

        except Exception:
            print 'swipe action error..'


# if __name__ == '__main__':
#     test_suit = unittest.TestLoader().loadTestsFromTestCase(wechattest)
#     test_suit.run(unittest.TestResult())
#     for err in unittest.TestResult().errors:
#         print err
#     for fail in unittest.TestResult().failures:
#         print fail
