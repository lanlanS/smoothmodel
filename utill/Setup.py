import os
import threading
from urllib2 import URLError

import time

import sys
from appium import webdriver
from selenium.common.exceptions import WebDriverException

from getDeviceinfo import GetDeviceInfo
from ServerControl import AppiumServer


class appsetUp:
    def __init__(self, driver):
        self.driver = None

    def setup(self, packageName, activityName):
        """
        :param packageName:
        :param activityName:
        :return:
        """

        mutex = threading.Lock()
        myInit = GetDeviceInfo()

        platformVersion = myInit.get_android_version()
        deviceName = myInit.getdevicename()

        platformName = 'Android'
        baseUrl = 'http://127.0.0.1:4723/wd/hub'

        desired_caps = {"platformName": platformName,
                        "platformVersion": platformVersion,
                        "appPackage": packageName,
                        "appActivity": activityName,
                        "deviceName": deviceName,
                        "noReset": True,
                        'newCommandTimeout': 600}
        try:
            if self.driver is None:
                mutex.acquire()
                if self.driver is None:
                    try:
                        self.driver = webdriver.Remote(baseUrl, desired_caps)
                    except URLError:
                        self.driver = None
                mutex.release()
            return self.driver
        except WebDriverException:
            print "Driver not connected "
            sys.exit(1)

    def teardown(self):
        # quit driver
        try:
            self.driver.quit()
        except Exception:
            task = str(os.popen("tasklist").read())
            if "node.exe" in task:
                try:
                    pid = str(os.popen("tasklist").read()).split("node.exe")[1].split()[0]
                    os.popen('tskill' + pid)
                except Exception:
                    print "get node.exe error"
        time.sleep(3)


# if __name__ == '__main__':
#     wxsetup = appsetUp(driver=None)
#     myserver = AppiumServer()
#
#     myserver.start_server()
#     if myserver.is_runnnig():
#         wxsetup.driver = wxsetup.setup('com.tencent.mm', '.ui.LauncherUI')
#         wxsetup.driver.find_element_by_id("com.tencent.mm:id/cjk").click()
#         wxsetup.teardown()
#     myserver.stop_server()

