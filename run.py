# -*- coding:utf-8 -*-
import os
import unittest

import time

from utill.xmlreader import XmlReader
from testcase.wechat_testcase import wechattest
from testcase.zhihu_testcase import zhihutest
from testcase.taobao_testcase import tbtest
from testcase.weibo_testcase import weibotest
from testcase.toutiao_testcase import SSnewstest
from testcase.neteasenews_testcase import Neteasenewstest
from testcase.wechat_testcase import wechattest
from testcase.system_testcase import Systemtest
from testcase.setting_testcase import Settingtest
from testcase.gallery_testcase import Gallerytest
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

        failures = unittest.TestResult().failures
        for err in unittest.TestResult().errors:
            print err
        for f in failures:
            print f
    else:
        print u"未获取到正确的测试用例，请检查testcase.xml文件。"


suit_run()
