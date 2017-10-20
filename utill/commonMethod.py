import os
from selenium.webdriver.support.wait import WebDriverWait


class commonmethod:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.wait_short = WebDriverWait(driver, 3)

    def get_window_size(self):
        """
        get current windows size mnn
        :return:windowSize
        """
        global windowSize
        windowSize = self.driver.get_window_size()
        return windowSize

    def my_swipe_to_up(self, during=None):
        """
        swipe UP
        :param during:
        :return:
        """
        # if windowSize == None:
        window_size = self.get_window_size()

        width = window_size.get("width")
        height = window_size.get("height")
        self.driver.swipe(width / 2, height * 3 / 4, width / 2, height / 4, during)

    def my_swipe_to_down(self, during=None):
        """
        swipe down
        :param during:
        :return:
        """
        window_size = self.get_window_size()
        width = window_size.get("width")
        height = window_size.get("height")
        self.driver.swipe(width / 2, height / 4, width / 2, height * 3 / 4, during)

    def my_swipe_to_left(self, during=None):
        """
        swipe left
        :param during:
        :return:
        """
        window_size = self.get_window_size()
        width = window_size.get("width")
        height = window_size.get("height")
        self.driver.swipe(width / 4, height / 2, width * 3 / 4, height / 2, during)

    def my_swipe_to_right(self, during=None):
        """
        swipe right
        :param during:
        :return:
        """
        window_size = self.get_window_size()
        width = window_size.get("width")
        height = window_size.get("height")
        self.driver.swipe(width * 4 / 5, height / 2, width / 5, height / 2, during)

    def back(self):
        """
        press back key
        """
        os.popen("adb shell input keyevent 4")

    # 10 s wait element
    def waitElementById(self, elementid):
        self.wait.until(lambda x: x.find_element_by_id(elementid))

    def waitElementByName(self, elementname):
        self.wait.until(lambda x: x.find_element_by_name(elementname))

    def waitElementByClassNmae(self, elementclass):
        self.wait.until(lambda x: x.find_element_by_class_name(elementclass))

    # 3s short wait element
    def shortwaitElementById(self, elementid):
        self.wait_short.until(lambda x: x.find_element_by_id(elementid))

    def shortwaitElementByName(self, elementname):
        self.wait_short.until(lambda x: x.find_element_by_name(elementname))

    def shortwaitElementByClassNmae(self, elementclass):
        self.wait_short.until(lambda x: x.find_element_by_class_name(elementclass))
