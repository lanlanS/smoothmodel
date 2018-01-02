# coding=utf-8


def error_info():
    print 'fps: 0'
    print '0'
    print 'jank count: 0'
    print '0'
    print 'max frame delay: 0'
    print '0'


def func(caseid, caseName, func_name):
    print "case id:" + caseid
    print "case Name:" + caseName

    fps = []
    jank_count = []
    max_frame_delay = []

    try:
        if eval('self.getframe.clear_FrameStats()'):
            for loop in range(1):
                eval('self.getfps.Start()')  # start collect fps

                eval(func_name)

                results = eval('self.getfps.SampleResults()')
                fps.append(results[1].value)
                jank_count.append(results[2].value)
                max_frame_delay.append(results[3].value)

                eval('self.getfps.Stop()')
        eval('self.getframe.dumpsysFramestats(caseid)')  # start collect framestats

        try:
            print 'fps: ' + str(fps)
            print fps
            print 'jank count: ' + str(max(jank_count))
            print jank_count
            print 'max frame delay: ' + str(max(max_frame_delay))
            print max_frame_delay

            eval('self.getframe.beginProcessResult(' + caseid + ')')
        except:
            print u'数据收集有误'
    except Exception:
        eval('self.getframe.dumpsysFramestats(' + caseid + ')')
        error_info()
        pass
