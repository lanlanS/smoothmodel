# coding=utf-8
import os
import time
from utill.Setup import appsetUp
from utill.commonMethod import commonmethod


class GalleryPage():
    def __init__(self):
        self.gallery_setup = appsetUp(driver=None)

        # App Info
        self.gallery_pkgname = 'com.meizu.media.gallery'
        self.gallery_mainActivity = '.GalleryActivity'
        self.gallery_surface = 'com.meizu.media.gallery/com.meizu.media.gallery.GalleryActivity'

        # Element Info

    def setup(self):
        self.gallery_setup.setup(self.gallery_pkgname, self.gallery_mainActivity)
        self.cm = commonmethod(self.gallery_setup.driver)

    def check_mainActivity(self):
        topactivity = \
            os.popen('adb shell dumpsys window ^|grep mCurrentFocus').readlines()[0].split(' ')[-1].strip().split('}')[
                0]
        for i in range(5):
            if topactivity != self.gallery_mainActivity:
                time.sleep(2)
            else:
                return True

    def swipDown_first_page(self):
        try:
            for i in range(0, 3):
                self.cm.my_swipe_to_up(during=400)
                time.sleep(0.1)
                i += 1
        except:
            raise Exception

    def swipeUp_first_page(self):
        try:
            for i in range(0, 3):
                self.cm.my_swipe_to_down(during=400)
                time.sleep(0.1)
                i += 1
        except:
            raise Exception

    def swipe_alone_first_page(self):
        try:
            for i in range(0, 10):
                self.cm.my_swipe_to_up(during=400)
                self.cm.my_swipe_to_down(during=400)
                time.sleep(0.1)
                i += 1
        except:
            raise Exception

    def teardown(self):
        self.gallery_setup.teardown()
