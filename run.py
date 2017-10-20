# -*- coding:utf-8 -*-
import os
import unittest

import time

from utill.xmlreader import XmlReader
from testcase.wechat_testcase import wechattest
from testcase.zhihu_testcase import zhihutest
from report.HTMLTestRunner_mz import HTMLTestRunner


def getcaselist():
    caseReader = XmlReader()
    caselist = caseReader.getModule()
    print caselist
    return caselist


def suit_run():
    caselist = getcaselist()
    suit = unittest.TestSuite()

    # test_suit1 = unittest.TestLoader().loadTestsFromTestCase(wechattest)
    # test_suit2 = unittest.TestLoader().loadTestsFromTestCase(zhihutest)
    # suit.addTests(test_suit1)
    timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    filename = os.getcwd() + "\\result_" + timestr + ".html"
    print (filename)
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(
            stream=fp,
            title=u'性能流畅度模型 测试报告',
            description=u'执行人：ShengXia'
    )

    if caselist:
        for case in caselist:
            testclass = case.split('/')[0]
            testcase = case.split('/')[1]
            suit.addTest(eval(testclass)(testcase))  # case : zhihutest("test_1_swipedown_Mainpage")

        # suit.run(unittest.TestResult())
        runner.run(suit)
        fp.close()
        for err in unittest.TestResult().errors:
            print err
        for fail in unittest.TestResult().failures:
            print fail
    else:
        print u"未获取到正确的测试用例，请检查testcase.xml文件。"


suit_run()
