# coding=utf-8
import os
import time
from utill.Setup import appsetUp
from utill.commonMethod import commonmethod


class SystemPage():
    def __init__(self):
        self.systemui_setup = appsetUp(driver=None)

        # App Info
        self.systemui_pkgname = 'com.android.systemui'
        self.systemuirecents_pkgname = 'com.android.systemui:recents'
        self.systemui_surface = 'StatusBar'
        self.systemui_recents_layer = 'com.android.systemui/com.flyme.systemui.recents.RecentsEmptyActivity'
        self.systemui_recents = 'com.android.systemui:recents'
        self.launcher_pkgname = 'com.meizu.flyme.launcher'
        self.launcher_layer = 'com.meizu.flyme.launcher/com.meizu.flyme.launcher.Launcher'

        # Element Info

    # def setup(self):
    #     self.systemui_setup.setup(self.systemui_pkgname, self.systemui_mainActivity)
    #     self.cm = commonmethod(self.systemui_setup.driver)

    # def open_notificaton(self):
    #     self.cm.driver.open_notifications()
    #
    # def teardown(self):
    #     self.systemui_setup.teardown()
