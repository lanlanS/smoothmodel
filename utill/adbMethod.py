import os
from utill.getDeviceinfo import GetDeviceInfo


class adbmethod:
    def __init__(self):
        device = GetDeviceInfo()
        self.sn = device.getdevicename()

    def getWindowSize(self):
        adb_getwinsize = 'adb -s ' + self.sn + ' shell wm size'
        return_value = str(os.popen(adb_getwinsize).read())
        if return_value != '':
            width = return_value.split(':')[1].split('x')[0]
            height = return_value.strip().split('x')[1]
            return {int(height), int(width)}
        else:
            return None

    def adb_swipe_action(self, direction):
        width, height = self.getWindowSize()
        dirc = {
            'left': [str(width / 4), str(height / 2), str(width * 3 / 4), str(height / 2)],
            'right': [str(width * 4 / 5), str(height / 2), str(width / 5), str(height / 2)],
            'up': [str(width / 2), str(height), str(width / 2), str(height / 4)],
            'down': [str(width / 2), str(height / 4), str(width / 2), str(height * 3 / 4)]
        }

        if direction in dirc.keys():
            os.popen('adb -s ' + self.sn + ' shell input swipe ' + ' '.join(dirc[direction]) + ' 200')

    def adb_swipe(self, arry):
        # arry string list
        os.popen('adb -s ' + self.sn + ' shell input swipe ' + arry + ' 200')

    def adb_click(self, arry):
        # arry string list
        os.popen('adb -s ' + self.sn + ' shell input tap ' + arry)

    def adb_backkey(self):
        os.popen('adb -s ' + self.sn + ' shell input keyevent 4')

    def adb_homekey(self):
        os.popen('adb -s ' + self.sn + ' shell input keyevent 3')
