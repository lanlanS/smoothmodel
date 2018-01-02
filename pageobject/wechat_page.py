# coding=utf-8
import os
import time
from utill.Setup import appsetUp
from utill.commonMethod import commonmethod


class WechatPage():
    def __init__(self):
        self.wechat_setup = appsetUp(driver=None)

        # App Info
        self.wechat_pkgname = 'com.tencent.mm'
        self.wechat_mainActivity = 'com.tencent.mm.ui.LauncherUI'
        self.wechat_surface = 'com.tencent.mm/com.tencent.mm.ui.LauncherUI'
        self.wechat_moments_layer = 'com.tencent.mm/com.tencent.mm.plugin.sns.ui.En_424b8e16'

        # Element Info
        self.monentsbtn = 'com.tencent.mm:id/ay0'  # 底栏 朋友圈按钮  com.tencent.mm:id/awt
        self.monents_btn = 'com.tencent.mm:id/a92'  # 朋友界面 万花筒图标  com.tencent.mm:id/a95
        self.monent_photo_icon = '(//android.widget.ImageButton[@content-desc="头像"])[1]'  # 朋友圈 朋友头像 com.tencent.mm:id/aoj
        self.me_photo_icon = '//android.widget.ImageView[@content-desc="老化小霸王,我的头像,再点一次可以进入我的相册"]'  # 我的相册界面 个人头像
        self.chatinfo = '//android.widget.ImageButton[@content-desc="聊天信息"]'  # 好友聊天信息（右上角） 按钮
        self.chatinfo_item = 'android:id/title'  # chat info 界面 item信息
        self.nikname = "com.tencent.mm:id/ha"  # 对话详情界面 朋友昵称
        self.friend_name = "com.tencent.mm:id/apd"  # 对话列表界面 昵称
        self.edit = "com.tencent.mm:id/a_z"  # 对话界面 输入框
        self.sendbtn = 'com.tencent.mm:id/aa5'  # 对话界面 发送按钮
        self.contactitem = 'com.tencent.mm:id/j1'  # 联系人界面 好友item
        self.selfalbum = 'com.tencent.mm:id/c8p'   # 个人相册 item

        self.morebtn_xpath = '//android.widget.ImageButton[@content-desc="更多功能按钮，已折叠"]'  # 功能折叠按钮
        self.album = 'com.tencent.mm:id/of'  # 聊天功能item list ID

        self.pic_selected = 'com.tencent.mm:id/bn4'  # 选择第一张图片 勾选框
        self.pic_comfirm = 'com.tencent.mm:id/h5'  # 选择照片中的 确定 按钮
        self.pic = 'com.tencent.mm:id/ady'  # 聊天记录中的图片

        self.searchbtn = '//android.widget.TextView[@content-desc="搜索"]'  # 联系人搜索按钮
        self.search_edit = 'com.tencent.mm:id/hk'  # 联系人搜索框

    def setup(self):
        self.wechat_setup.setup(self.wechat_pkgname, self.wechat_mainActivity)
        self.cm = commonmethod(self.wechat_setup.driver)

    def check_wechatmainActivity(self):
        topactivity = \
            os.popen('adb shell dumpsys window ^|grep mCurrentFocus').readlines()[0].split(' ')[-1].strip().split('}')[
                0]
        for i in range(5):
            if topactivity != self.wechat_surface:
                time.sleep(2)
            else:
                return True

    def swipDown_first_page(self):
        try:
            for i in range(0, 10):
                self.cm.my_swipe_to_up(during=400)
                time.sleep(0.1)
                i += 1
        except:
            raise Exception

    def click_wechat(self):
        self.cm.driver.find_elements_by_id(self.monentsbtn)[0].click()

    def click_cintacts(self):
        self.cm.driver.find_elements_by_id(self.monentsbtn)[1].click()

    def click_Discover(self):
        self.cm.driver.find_elements_by_id(self.monentsbtn)[2].click()

    def click_me(self):
        self.cm.driver.find_elements_by_id(self.monentsbtn)[3].click()

    def enter_monents_page(self):
        try:
            # if self.cm.shortwaitElementById(self.monentsbtn):
            #     for i in range(0, 2):
            #         self.cm.my_swipe_to_right(during=500)
            #         time.sleep(3)
            try:
                if self.cm.shortwaitElementById(self.monentsbtn):
                    self.click_Discover()  # 点击切换到发现界面
                    if self.cm.shortwaitElementById(self.monents_btn):
                        self.cm.driver.find_elements_by_id(self.monents_btn)[0].click()  # 点击进入朋友圈
                        time.sleep(3)
                        if self.cm.driver.find_elements_by_xpath(self.monent_photo_icon):
                            for i in range(0, 20):
                                self.cm.my_swipe_to_up(during=400)
                            for i in range(0, 20):
                                self.cm.my_swipe_to_down(during=400)
                                # time.sleep(1)
                            self.cm.back()

            except Exception:
                print "Connot get Wechat Moments page."
                # else:
                #     print "connot tap moment button"
        except:
            raise Exception

    def chatwithsb(self):
        try:
            if self.cm.shortwaitElementById(self.monentsbtn):
                self.click_wechat()  # 进入对话列表界面
                friend_btn = self.cm.shortwaitElementById(self.friend_name)
                if friend_btn.text == u'懒懒':
                    friend_btn.click()  # 进入朋友对话详情界面
                    if self.cm.shortwaitElementById(self.nikname):
                        for i in range(0, 5):
                            editview = self.cm.driver.find_elements_by_id(self.edit)
                            editview[0].send_keys("hello  ")  # 输入聊天信息
                            send = self.cm.shortwaitElementById(self.sendbtn)
                            send.click()  # 点击send 发送聊天信息
                        self.cm.back()
                    else:
                        print "connot open the chat page."
            else:
                print "open Wechat failed."
        except:
            raise Exception

    def view_pic(self):  # 查看聊天中的图片
        try:
            if self.cm.shortwaitElementById(self.monentsbtn):
                self.click_wechat()  # 进入对话列表界面
                friend_btn = self.cm.shortwaitElementById(self.friend_name)
                if friend_btn.text == u'懒懒':
                    friend_btn.click()  # 进入朋友对话详情界面
                    if self.cm.shortwaitElementById(self.nikname):
                        # 发送一张图片
                        self.cm.driver.find_elements_by_xpath(self.morebtn_xpath)[0].click()   # 点击‘+’号
                        for tmp in self.cm.driver.find_elements_by_id(self.album):   # 查找 相册 按钮
                            if tmp.text == u'相册':
                                tmp.click()   # 点击相册按钮
                                time.sleep(0.5)
                                self.cm.driver.find_elements_by_id(self.pic_selected)[0].click()   # 勾选第一张照片
                                self.cm.driver.find_elements_by_id(self.pic_comfirm)[0].click()   # 点击确认按钮
                                time.sleep(1)  # 等待发送图片
                                for i in range(0, 5):
                                    self.cm.driver.find_elements_by_id(self.pic)[0].click()  # 点击展开图片
                                    time.sleep(0.3)
                                    self.cm.back()  # 还原图片
                                self.cm.back()
                    else:
                        print "connot open the chat page."
            else:
                print "open Wechat failed."
        except:
            raise Exception

    def switchwindow(self):
        try:
            if self.cm.shortwaitElementById(self.monentsbtn):
                self.click_wechat()  # 进入对话列表界面
                friend_btn = self.cm.shortwaitElementById(self.friend_name)
                if friend_btn:
                    friend_btn.click()  # 进入朋友对话详情界面
                    if self.cm.shortwaitElementById(self.nikname):
                        self.cm.back()  # 退回到主界面
                    else:
                        print "connot open the chat page."
            else:
                print "open Wechat failed."
        except:
            raise Exception

    def swipUp_chatpage(self):
        try:
            if self.cm.shortwaitElementById(self.monentsbtn):
                self.click_wechat()  # 进入对话列表界面
                friend_btn = self.cm.shortwaitElementById(self.friend_name)
                if friend_btn:
                    friend_btn.click()  # 进入朋友对话详情界面
                    if self.cm.shortwaitElementById(self.nikname):
                        for i in range(0, 15):
                            self.cm.my_swipe_to_down(during=400)
                        for i in range(0, 15):
                            self.cm.my_swipe_to_up(during=400)
                            time.sleep(0.1)
                            i += 1
                        self.cm.back()
            else:
                print 'Connot start wechat '
        except:
            raise Exception

    def swipe_subscription(self):  # 滑动订阅号列表
        try:
            if self.cm.shortwaitElementById(self.monentsbtn):
                self.click_wechat()  # 进入对话列表界面
                news_btn = self.cm.driver.find_elements_by_id(self.friend_name)
                if news_btn:
                    for tem in news_btn:
                        if tem.text == u'订阅号':
                            tem.click()  # 进入订阅号详情界面
                            if self.cm.shortwaitElementById(self.nikname):
                                for i in range(0, 2):
                                    self.cm.my_swipe_to_up(during=400)
                                for i in range(0, 2):
                                    self.cm.my_swipe_to_down(during=400)
                                    time.sleep(0.1)
                                self.cm.back()
            else:
                print 'Connot start wechat '
        except:
            raise Exception

    def swipe_subscription_news(self):  # 滑动任意订阅号历史文章内容
        try:
            if self.cm.shortwaitElementById(self.monentsbtn):
                self.click_wechat()  # 进入对话列表界面
                news_btn = self.cm.driver.find_elements_by_id(self.friend_name)
                if news_btn:
                    for tem in news_btn:
                        if tem.text == u'订阅号':
                            tem.click()  # 进入订阅号详情界面
                            if self.cm.shortwaitElementById(self.nikname):
                                news_btn = self.cm.driver.find_elements_by_id(self.friend_name)
                                news_btn.click()
                                if self.cm.driver.find_elements_by_xpath(self.chatinfo):
                                    self.cm.driver.find_elements_by_xpath(self.chatinfo).click()
                                    for tem in self.cm.driver.find_elements_by_id(self.chatinfo_item):
                                        if tem.text == u'查看历史消息':
                                            tem.click()
                                            # 点击 订阅号文章链接 进入
        except:
            raise Exception

    def swipe_myPosts(self):
        try:
            if self.cm.shortwaitElementById(self.monentsbtn):
                self.click_me()  # 进入个人信息列表界面
                myposts_btn = self.cm.driver.find_elements_by_id(self.chatinfo_item)
                if myposts_btn:
                    for tem in myposts_btn:
                        if tem.text == u'相册':
                            tem.click()
                            if self.cm.driver.find_elements_by_id(self.friend_name) \
                                    and self.cm.driver.find_elements_by_id(self.friend_name)[0].text == u'老化小霸王':
                                for i in range(0, 5):     # 滑动个人朋友圈
                                    self.cm.my_swipe_to_up(during=400)
                                    time.sleep(0.3)
                                for i in range(0, 5):
                                    self.cm.my_swipe_to_down(during=400)
                                    time.sleep(0.3)
                                self.cm.back()
                                self.click_wechat()
        except:
            raise Exception

    def swipe_friendsAlbum(self):
        try:
            if self.cm.shortwaitElementById(self.monentsbtn):
                self.click_cintacts()  # 进入朋友列表界面
                for tem in self.cm.driver.find_elements_by_id(self.contactitem):  # 查找固定好友
                    if tem.text == u'懒懒':
                        tem.click()
                        selfalbum = self.cm.driver.find_elements_by_id(self.selfalbum)[0]
                        if selfalbum.text == u'个人相册':   # 判断进入个人相册
                            selfalbum.click()
                            for i in range(0, 2):  # 滑动好友朋友圈
                                self.cm.my_swipe_to_up(during=400)
                                time.sleep(0.3)
                            for i in range(0, 2):
                                self.cm.my_swipe_to_down(during=400)
                                time.sleep(0.3)
                            self.cm.back()  # 返回到 个人信息界面
                            self.cm.back()  # 返回到 联系人界面
                            self.click_wechat()
        except:
            raise Exception

    def swipe_friendlist(self):
        try:
            if self.cm.shortwaitElementById(self.monentsbtn):
                self.click_cintacts()  # 进入朋友列表界面
                for i in range(0, 2):     # 滑动朋友列表
                    self.cm.my_swipe_to_up(during=400)
                    time.sleep(0.3)
                for i in range(0, 2):
                    self.cm.my_swipe_to_down(during=400)
                    time.sleep(0.3)
                self.click_wechat()
        except:
            raise Exception

    def teardown(self):
        self.wechat_setup.teardown()
