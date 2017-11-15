# coding=utf-8
import os
import subprocess
import datetime
import re
import math
import xlwt
import time


class GetFramestats:
    def __init__(self, pkgname):

        # Flags,IntendedVsync,Vsync,OldestInputEvent,NewestInputEvent,HandleInputStart,AnimationStart,PerformTraversalsStart,
        # DrawStart,SyncQueued,SyncStart,IssueDrawCommandsStart,SwapBuffers,FrameCompleted,DequeueBufferDuration,QueueBufferDuration
        self.patternFps = re.compile(r'[\s]+[\d]+.[\d]+[\s]+[\d]+.[\d]+[\s]+[\d]+.[\d]+[\s\S]*')

        # Draw Prepare Process Execute
        self.patternProfileData = re.compile(r'[\d]+,[\d]+,[\d]+,[\s\S]*')  # 4列 Darw-Prepare-Process-Execute
        self.fileName = ''
        self.fileaddr = ''
        self.pkgname = pkgname

    def __mkdir(self):
        output = os.getcwd() + r'\output'
        if not os.path.isdir(output):
            os.mkdir(output)
            self.fileaddr = output + '\\' + self.pkgname
        else:
            self.fileaddr = output + '\\' + self.pkgname

    def clear_FrameStats(self):
        cmd = "adb shell dumpsys gfxinfo %s reset" % self.pkgname
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if process.stdout.readline().startswith('Applications'):  # Applications Graphics Acceleration Info:
            self.__mkdir()
            print 'Test Going..'
            time.sleep(3)
            return True
        else:
            print 'Reset gfxinfo error !'

    def dumpsysFramestats(self, caseID):
        print("begin dumpsysFramestats:" + str(datetime.datetime.now()))
        cmd = "adb shell dumpsys gfxinfo %s framestats" % self.pkgname
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # countFailGetFps = -1
        # thisTimeHasFps = False
        self.fileName = self.fileaddr + '\\' + caseID + '_AllFrame.txt'
        if not os.path.exists(self.fileaddr):
            os.mkdir(self.fileaddr)
        else:
            if os.path.isfile(self.fileName):
                os.remove(self.fileName)

        profileText = open(self.fileName, 'w')
        # profileText.write("###########################################" + str(countFailGetFps) + "\n")
        while True:
            nextline = process.stdout.readline()
            matchFps = self.patternFps.match(nextline.decode())
            if matchFps:
                # thisTimeHasFps = True
                profileText.write(nextline.decode())  # 匹配framestats信息
            else:
                matchProfileData = self.patternProfileData.match(nextline.decode())  # gfxinfo 取消不展示
                if matchProfileData:
                    profileText.write(nextline.decode())

            if nextline.startswith("Total frames"):
                totalframe = float(nextline.split(":")[-1].strip())
                continue

            if nextline.startswith("Janky frames"):
                jankyframe = nextline.split(":")[-1].strip().split('(')[0]
                # jankrate1 = float(jankyframe) / totalframe
                # print "jank rate1: " + "%.2f%%" % (jankrate1 * 100)
                jankrate = nextline.split("(")[-1].split(")")[0]
                print "jank rate: " + jankrate + " (" + jankyframe + "/" + str(int(totalframe)) + ")"

                continue
            if nextline.startswith("Number Missed Vsync:"):
                realjank = nextline.split(":")[-1].strip()
                realjankrate = float(realjank) / totalframe
                print "real jank rate: " + "%.2f%%" % (realjankrate * 100) + " (" + realjank + "/" + str(
                        int(totalframe)) + ")"
                continue
            if nextline.startswith("Number High input latency"):
                input_latency = nextline.split(":")[-1].strip()
                high_input_rate = float(input_latency) / totalframe
                print "High input latency: " + "%.2f%%" % (high_input_rate * 100) + " (" + input_latency + "/" + str(
                        int(totalframe)) + ")"

                continue
            if nextline.startswith("Number Slow UI thread"):
                slow_UI = nextline.split(":")[-1].strip()
                slow_ui_rate = float(slow_UI) / totalframe
                print "Slow UI thread: " + "%.2f%%" % (slow_ui_rate * 100) + " (" + slow_UI + "/" + str(
                        int(totalframe)) + ")"
                continue
            if nextline.startswith("Number Slow bitmap uploads"):
                slow_bitmapupload = nextline.split(":")[-1].strip()
                slow_bitmap_rate = float(slow_bitmapupload) / totalframe
                print "Slow bitmap uploads: " + "%.2f%%" % (
                    slow_bitmap_rate * 100) + " (" + slow_bitmapupload + " /" + str(int(totalframe)) + ")"
                continue
            if nextline.startswith("Number Slow issue draw commands"):
                slow_draw = nextline.split(":")[-1].strip()
                slow_draw_rate = float(slow_draw) / totalframe
                print "Slow issue draw commands rate: " + "%.2f%%" % (
                    slow_draw_rate * 100) + " (" + slow_draw + " /" + str(int(totalframe)) + ")"
                continue

            if nextline.startswith("HISTOGRAM"):  # 获取帧耗时分布list
                histogramlist = []
                histogram = nextline.split(":")[1].split()
                for temp in histogram:
                    histogramlist.append((int(temp.split("ms=")[0]), int(temp.split("ms=")[1])))

                if histogramlist:
                    time1 = []
                    count1 = []
                    fcount = []
                    ftime = []
                    for h in histogramlist:
                        time1.append(h[0])
                        count1.append(h[1])
                    if time1 or count1:
                        for i in range(len(count1)):
                            if count1[::-1][i] != 0:
                                fcount = count1[:len(count1) - i]
                                ftime = time1[:len(count1) - i]
                                break
                        if not fcount or not ftime:
                            fcount = count1
                            ftime = time1
                        print "Frame Latency:" + str(ftime)
                        print "Frame Count:" + str(fcount)

                    # write HISTOGRAM into EXCEL
                    wb = xlwt.Workbook(encoding='utf-8')
                    ws = wb.add_sheet('帧分布信息')
                    ws.write(0, 0, "Frame(ms)")
                    ws.write(0, 1, "Frame Count(times)")
                    recordRow = 1
                    for frameinfo in histogramlist:
                        ws.write(recordRow, 0, frameinfo[0])
                        ws.write(recordRow, 1, frameinfo[1])
                        recordRow = recordRow + 1
                    wb.save(self.fileaddr + '\\' + caseID + '_FrameInfo.xls')
                    print "frameinfo address: " + self.fileaddr + '\\' + caseID + '_FrameInfo.xls'
                continue

            if "Total DisplayList" in nextline.decode():
                break

        profileText.close()

    def countSplitByComma(self, splitByComma, i, j):
        return (float(splitByComma[i]) - float(splitByComma[j])) / 1000000

    def beginProcessResult(self, caseID):
        print("begin processResult:" + str(datetime.datetime.now()))
        # fpsReadList = []
        profileDataReadList = []
        # fpsTmpReadList = []
        # profileDataTmpReadList = []
        if os.path.isfile(self.fileName):
            profileRead = open(self.fileName, 'r')
            for line in profileRead.readlines():

                # matchFps = self.patternFps.match(line)
                # if matchFps:
                #     fpsReadList.append(line)

                matchProfileData = self.patternProfileData.match(line)
                if matchProfileData:
                    profileDataReadList.append(line)

            # fpsReadListLen = len(fpsReadList)
            profileDataReadListLen = len(profileDataReadList)

            # print("NineFrameLength=" + str(profileDataReadListLen))  # del FourFrameLength= + str(fpsReadListLen)


            # fpsAllFrameRead = open(self.fileaddr + '//FourFrame'+caseID+'.txt', "w")
            # for fpsallframe in fpsReadList:
            #     fpsAllFrameRead.write(fpsallframe)

            profileAllFrameRead = open(self.fileaddr + '\\' + caseID + '_NineFrame.txt', "w")
            for profileallframe in profileDataReadList:
                profileAllFrameRead.write(profileallframe)

            # wb = xlwt.Workbook(encoding='utf-8')
            # ws = wb.add_sheet('FourFrame统计')
            # ws.write(0, 0, "Draw")
            # ws.write(0, 1, "Prepare")
            # ws.write(0, 2, "Process")
            # ws.write(0, 3, "Execute")
            # ws.write(0, 4, "All")
            # ws.write(0, 5, "TimeOut")
            # ws.write(0, 6, "SkipFrame")
            # ws.write(0, 7, "SkipFrameSum")
            # ws.write(0, 8, "DropRate")
            # recordRow = 1
            # skipFrameSum = 0.0
            # for line in fpsReadList:
            #     splitByT = line.split("\t")
            #     ws.write(recordRow, 0, float(splitByT[1]))
            #     ws.write(recordRow, 1, float(splitByT[2]))
            #     ws.write(recordRow, 2, float(splitByT[3]))
            #     ws.write(recordRow, 3, float(splitByT[4].strip()))
            #     allTime = float(splitByT[1]) + float(splitByT[2]) + float(splitByT[3]) + float(splitByT[4].strip())
            #     ws.write(recordRow, 4, str(allTime))
            #     timeout = allTime / (1000.00 / 60.00)
            #     ws.write(recordRow, 5, str(timeout))
            #     skipFrame = math.ceil(timeout) - 1.00
            #     ws.write(recordRow, 6, str(skipFrame))
            #     skipFrameSum = skipFrameSum + skipFrame
            #     ws.write(recordRow, 7, str(skipFrameSum))
            #     DropRate = skipFrameSum / (skipFrameSum + recordRow)
            #     ws.write(recordRow, 8, str(DropRate))
            #     recordRow += 1
            # wb.save(self.fileaddr + '//'+caseID+'_Gfxinfo.xls')

            """
            Html Module
            # /FourFrame/js/data.js
            fin = ""
            c = 0
            e = len(fpsReadList)
            for tmplist in fpsReadList:
                splitByT = tmplist.split("\t")
                if c == 0:
                    fin = fin + "{"
                if c == e - 1:
                    fin = fin + str(c) + ":{\"Draw\":" + splitByT[1] + ",\"Prepare\":" + splitByT[
                        2] + ",\"Process\":" + splitByT[
                              3] + ",\"Execute\":" + splitByT[4].strip() + "}}"
                else:
                    fin = fin + str(c) + ":{\"Draw\":" + splitByT[1] + ",\"Prepare\":" + splitByT[
                        2] + ",\"Process\":" + splitByT[
                              3] + ",\"Execute\":" + splitByT[4].strip() + "},"
                c = c + 1
            frameCount = 25 * e + 50
            fin = "var person_data = " + fin + ";\nvar svg_width = " + str(frameCount) + ";"
            dataWrite = open("./output/A_PhotoSlide/html/FourFrame/js/data.js", "w")
            dataWrite.write(fin)
            print("FourFrameEnd")


            # /NineFrame/js/data.js
            fin = ""
            c = 0
            e = len(profileDataReadList)
            for tmplist in profileDataReadList:
                splitByComma = tmplist.split(",")
                Vsync_IntendedVsync = countSplitByComma(splitByComma, 2, 1)
                HandleInputStart_Vsync = countSplitByComma(splitByComma, 5, 2)
                AnimationStart_HandleInputStart = countSplitByComma(splitByComma, 6, 5)
                PerformTraversalsStart_AnimationStart = countSplitByComma(splitByComma, 7, 6)
                DrawStart_PerformTraversalsStart = countSplitByComma(splitByComma, 8, 7)
                SyncQueued_DrawStart = countSplitByComma(splitByComma, 9, 8)
                SyncStart_SyncQueued = countSplitByComma(splitByComma, 10, 9)
                IssueDrawCommandsStart_SyncStart = countSplitByComma(splitByComma, 11, 10)
                FrameCompleted_IssueDrawCommandsStart = countSplitByComma(splitByComma, 13, 11)
                # if Vsync_IntendedVsync!=0:
                # print(str(Vsync_IntendedVsync))
                if c == 0:
                    fin = fin + "{"
                fin = fin + str(c) + ":{\"Vsync_IntendedVsync\":" + str(
                        Vsync_IntendedVsync) + ",\"HandleInputStart_Vsync\":" + str(
                        HandleInputStart_Vsync) + ",\"AnimationStart_HandleInputStart\":" + str(
                        AnimationStart_HandleInputStart) + ",\"PerformTraversalsStart_AnimationStart\":" + str(
                        PerformTraversalsStart_AnimationStart) + ",\"DrawStart_PerformTraversalsStart\":" + str(
                        DrawStart_PerformTraversalsStart) + ",\"SyncQueued_DrawStart\":" + str(
                        SyncQueued_DrawStart) + ",\"SyncStart_SyncQueued\":" + str(
                        SyncStart_SyncQueued) + ",\"IssueDrawCommandsStart_SyncStart\":" + str(
                        IssueDrawCommandsStart_SyncStart) + ",\"FrameCompleted_IssueDrawCommandsStart\":" + str(
                        FrameCompleted_IssueDrawCommandsStart) + "}"
                if c == e - 1:
                    fin = fin + "}"
                else:
                    fin = fin + ","
                c = c + 1

            frameCount = 25 * e + 50
            fin = "var person_data = " + fin + ";\nvar svg_width = " + str(frameCount) + ";"

            dataWrite = open("./output/html/NineFrame/js/data.js", "w")
            dataWrite.write(fin)
            """

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Framestats统计')

            pattern = xlwt.Pattern()  # Create the Pattern
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
            pattern.pattern_fore_colour = 22  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
            style = xlwt.XFStyle()  # Create the Pattern
            style.pattern = pattern  # Add Pattern to Style

            ws.write(0, 0, "Vsync_IntendedVsync")
            ws.write(0, 1, "HandleInputStart_Vsync")
            ws.write(0, 2, "AnimationStart_HandleInputStart")
            ws.write(0, 3, "PerformTraversalsStart_AnimationStart")
            ws.write(0, 4, "DrawStart_PerformTraversalsStart")
            ws.write(0, 5, "SyncQueued_DrawStart")
            ws.write(0, 6, "SyncStart_SyncQueued")
            ws.write(0, 7, "IssueDrawCommandsStart_SyncStart")
            ws.write(0, 8, "FrameCompleted_IssueDrawCommandsStart")
            ws.write(0, 9, "All")
            ws.write(0, 10, "TimeOut")
            ws.write(0, 11, "SkipFrame")
            ws.write(0, 12, "SkipFrameSum")
            ws.write(0, 13, "DropRate")
            recordRow = 1
            skipFrameSum = 0.0
            for tmplist in profileDataReadList:
                splitByComma = tmplist.split(",")
                Vsync_IntendedVsync = self.countSplitByComma(splitByComma, 2, 1)
                HandleInputStart_Vsync = self.countSplitByComma(splitByComma, 5, 2)
                AnimationStart_HandleInputStart = self.countSplitByComma(splitByComma, 6, 5)
                PerformTraversalsStart_AnimationStart = self.countSplitByComma(splitByComma, 7, 6)
                DrawStart_PerformTraversalsStart = self.countSplitByComma(splitByComma, 8, 7)
                SyncQueued_DrawStart = self.countSplitByComma(splitByComma, 9, 8)
                SyncStart_SyncQueued = self.countSplitByComma(splitByComma, 10, 9)
                IssueDrawCommandsStart_SyncStart = self.countSplitByComma(splitByComma, 11, 10)
                FrameCompleted_IssueDrawCommandsStart = self.countSplitByComma(splitByComma, 13, 11)

                ws.write(recordRow, 0, Vsync_IntendedVsync)
                ws.write(recordRow, 1, HandleInputStart_Vsync)

                if AnimationStart_HandleInputStart >= 2:  # View.onTouchEvent() takes long time
                    ws.write(recordRow, 2, AnimationStart_HandleInputStart, style)
                else:
                    ws.write(recordRow, 2, AnimationStart_HandleInputStart)

                if PerformTraversalsStart_AnimationStart >= 2:
                    ws.write(recordRow, 3, PerformTraversalsStart_AnimationStart, )
                else:
                    ws.write(recordRow, 3, PerformTraversalsStart_AnimationStart)

                ws.write(recordRow, 4, DrawStart_PerformTraversalsStart)
                ws.write(recordRow, 5, SyncQueued_DrawStart)
                ws.write(recordRow, 6, SyncStart_SyncQueued)

                if IssueDrawCommandsStart_SyncStart >= 0.4:  # highlight IssueDrawCommandsStart_SyncStart > 0.4
                    ws.write(recordRow, 7, IssueDrawCommandsStart_SyncStart, style)
                else:
                    ws.write(recordRow, 7, IssueDrawCommandsStart_SyncStart)

                ws.write(recordRow, 8, FrameCompleted_IssueDrawCommandsStart)

                allTime = Vsync_IntendedVsync + HandleInputStart_Vsync + AnimationStart_HandleInputStart + PerformTraversalsStart_AnimationStart + DrawStart_PerformTraversalsStart + SyncQueued_DrawStart + SyncStart_SyncQueued + IssueDrawCommandsStart_SyncStart + FrameCompleted_IssueDrawCommandsStart
                ws.write(recordRow, 9, str(allTime))

                timeout = allTime / (1000.00 / 60.00)
                ws.write(recordRow, 10, str(timeout))

                skipFrame = math.ceil(timeout) - 1.00
                ws.write(recordRow, 11, str(skipFrame))

                skipFrameSum = skipFrameSum + skipFrame
                ws.write(recordRow, 12, str(skipFrameSum))

                DropRate = skipFrameSum / (skipFrameSum + recordRow)
                ws.write(recordRow, 13, str(DropRate))

                recordRow += 1
            wb.save(self.fileaddr + '\\' + caseID + '_FrameStats.xls')
            print("FrameStats Parse End")

# gettask = GetFramestats('com.meizu.media.reader')
# if gettask.clear_FrameStats():
#     gettask.dumpsysFramestats("0")
#     gettask.beginProcessResult("0")
