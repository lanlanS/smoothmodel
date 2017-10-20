# coding=utf-8
import os
import urllib2

from multiprocessing import Process
import threading
from urllib2 import URLError


class AppiumServer:

    def __init__(self):
        global openAppium, baseUrl
        openAppium = "appium &"
        baseUrl = "http://127.0.0.1:4723/wd/hub"

    def start_server(self):
        """start the appium server
        :return:
        """
        t1 = RunServer(openAppium)
        p = Process(target=t1.start())
        p.start()

    def stop_server(self):
        """stop the appium server
        :return:
        """
        # kill appium Server
        if "node.exe" in str(os.popen("tasklist").read()):
            try:
                pid = str(os.popen("tasklist").read()).split("node.exe")[1].split()[0]
                os.popen('tskill' + pid)
            except Exception:
                print "get node.exe error"

    def re_start_server(self):
        """reStart the appium server
        """
        self.stop_server()
        self.start_server()

    def is_runnnig(self):
        """Determine whether server is running
        :return:True or False
        """
        response = None
        url = baseUrl+"/status"
        try:
            response = urllib2.urlopen(url, timeout=5)

            if response.readlines().split(",")[0].split(":")[1] == 0:  # status = 0 for sucess
                return True
            else:
                return False
        except URLError:
            return False
        finally:
            if response:
                response.close()


class RunServer(threading.Thread):

    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)


if __name__ == "__main__":
    oo = AppiumServer()
    oo.start_server()
    print("strart server")
    print("running server")
    oo.stop_server()
    print("stop server")