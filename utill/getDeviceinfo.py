import os
import subprocess

import re


class GetDeviceInfo:
    def connect_phone(self):
        """
        check the phone is connect
        """
        value = os.popen("adb get-state")

        for data in value.readline():
            s_date = str(data)
            if s_date.find("device"):
                return True
        return False

    def getdevicename(self):
        """get deviceName
            :return:deviceName
        """
        device_list = []

        return_value = os.popen("adb devices")
        for value in return_value.readlines():
            s_value = str(value)
            if s_value.rfind('device'):
                if not s_value.startswith("List"):
                    device_list.append(s_value[:s_value.find('device')].strip())
        if len(device_list) != 0:
            return device_list[0]
        else:
            return None

    def get_android_version(self):
        """get androidVersion
        :return:androidVersion
        """
        adb_getandroidversion = "adb shell grep ro.build.version.release /system/build.prop"
        return_value = str(os.popen(adb_getandroidversion).read())

        if return_value != '':
            pop = return_value.rfind(str('='))
            return return_value[pop + 1:].strip('\n')
        else:
            return None

    def start_server(self):
        """start the adb server
        :return:
        """
        os.system("adb start-server")

    def close_server(self):
        """close the adb server
        :return:
        """
        os.popen("adb kill-server")

    def re_start(self):
        """reStart the adb server
        :return:
        """
        self.close_server()
        self.start_server()

    def get_top_view(self):
        out = subprocess.check_output(['adb', 'shell', 'dumpsys', 'SurfaceFlinger'])
        lines = out.replace('\r\n', '\n').splitlines()
        max_area = 0
        top_view = None
        for index, line in enumerate(lines):
            line = line.strip()
            if not line.startswith('+ Layer '):
                continue
            m = re.search(r'\((.+)\)', line)
            if not m:
                continue
            view_name = m.group(1)
            (x0, y0, x1, y1) = map(int, re.findall(r'(\d+)', lines[index + 4]))
            cur_area = (x1 - x0) * (y1 - y0)
            if cur_area > max_area:
                max_area = cur_area
                top_view = view_name
        return top_view

# test = GetDeviceInfo()
# top = test.get_top_view()
# print(top)

