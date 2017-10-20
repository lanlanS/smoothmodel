from appium import webdriver


class waitelement:
    def __init__(self, dr, id1, id2, id3):
        self.driver = dr
        self.id1 = id1
        self.id2 = id2
        self.id3 = id3

    def isElementExit(self, id1, id2, id3):
        flag = False
        sourcexml = self.driver.getPageSource().toString()
        try:
            if id1 != "":
                flag = sourcexml.contains(id1)
            if id2 != "":
                flag = sourcexml.contains(id2) and flag
            if id3 != "":
                flag = sourcexml.contains(id3) and flag
        except (Exception, AssertionError):
            print "check element error! "

        return flag
