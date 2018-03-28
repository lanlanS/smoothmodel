# -*- coding: utf-8 -*-

"""
A TestRunner for use with the Python unit testing framework. It
generates a HTML report to show the result at a glance.

The simplest way to use this is to invoke its main method. E.g.

    import unittest
    import HTMLTestRunner

    ... define your tests ...

    if __name__ == '__main__':
        HTMLTestRunner.main()


For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.

    # output to a file
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='My unit test',
                description='This demonstrates the report output by HTMLTestRunner.'
                )

    # Use an external stylesheet.
    # See the Template_mixin class for more customizable options
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'

    # run the test
    runner.run(my_test_suite)


------------------------------------------------------------------------
Copyright (c) 2004-2007, Wai Yip Tung
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name Wai Yip Tung nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# URL: http://tungwaiyip.info/software/HTMLTestRunner.html

__author__ = "Wai Yip Tung"
__version__ = "0.9.1"

"""
Version 0.8.2
* Show output inline instead of popup window (Viorel Lupu).

Version in 0.8.1
* Validated XHTML (Wolfgang Borgert).
* Added description of test classes and test cases.

Version in 0.8.0
* Define Template_mixin class for customization.
* Workaround a IE 6 bug that it does not treat <script> block as CDATA.

Version in 0.7.1
* Back port to Python 2.3 (Frank Horowitz).
* Fix missing scroll bars in detail log (Podi).
"""

import StringIO
import datetime
import sys
import unittest
from xml.sax import saxutils

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')


# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
#   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>

class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


# ----------------------------------------------------------------------
# Template


class Template_mixin(object):
    """
    Define a HTML template for report customerization and generation.

    Overall structure of an HTML report

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ComparePart          |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
        0: u'通过',
        1: u'失败',
        2: u'错误',
    }

    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = ''

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    %(stylesheet)s
    <link href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css" rel="stylesheet">
    <script type="text/javascript" src="https://cdn.bootcss.com/echarts/4.0.2/echarts-en.common.min.js"></script>
</head>
<body>
    <script language="javascript" type="text/javascript"><!--
    output_list = Array();

    /* level - 0:Summary; 1:Failed; 2:All */
    function showCase(level) {
        trs = document.getElementsByTagName("tr");
        for (var i = 0; i < trs.length; i++) {
            tr = trs[i];
            id = tr.id;
            if (id.substr(0,2) == 'ft') {
                if (level < 1) {
                    tr.className = 'hiddenRow';
                }
                else {
                    tr.className = '';
                }
            }
            if (id.substr(0,2) == 'pt') {
                if (level > 1) {
                    tr.className = '';
                }
                else {
                    tr.className = 'hiddenRow';
                }
            }
        }
    }


    function showClassDetail(cid, count) {
        var id_list = Array(count);
        var toHide = 1;
        for (var i = 0; i < count; i++) {
            tid0 = 't' + cid.substr(1) + '.' + (i+1);
            tid = 'f' + tid0;
            tr = document.getElementById(tid);
            if (!tr) {
                tid = 'p' + tid0;
                tr = document.getElementById(tid);
            }
            id_list[i] = tid;
            if (tr.className) {
                toHide = 0;
            }
        }
        for (var i = 0; i < count; i++) {
            tid = id_list[i];
            if (toHide) {
                document.getElementById('div_'+tid).style.display = 'none'
                document.getElementById(tid).className = 'hiddenRow';
            }
            else {
                document.getElementById(tid).className = '';
            }
        }
    }

    function showEchatDetial(div_id,option){
        var details_div = document.getElementById(div_id)
        var displayState = details_div.style.display

        if (displayState != 'block' ) {
            displayState = 'block'
            details_div.style.display = 'block'
        }
        else {
            details_div.style.display = 'none'
        }
        debugger
        getechart(div_id,option)

    }

    function getechart(div_id,option){
        // 基于准备好的dom，初始化echarts实例
        var myFrameChart = echarts.init(document.getElementById(div_id));
        // 指定图表的配置项和数据
        myFrameChart.setOption(option);
        console.log(option.series[0].data)
    }


    function showTestDetail(div_id){
        var details_div = document.getElementById(div_id)
        var displayState = details_div.style.display
        // alert(displayState)
        if (displayState != 'block' ) {
            displayState = 'block'
            details_div.style.display = 'block'
        }
        else {
            details_div.style.display = 'none'
        }
    }


    function html_escape(s) {
        s = s.replace(/&/g,'&amp;');
        s = s.replace(/</g,'&lt;');
        s = s.replace(/>/g,'&gt;');
        return s;
    }

    function compare_file(files) {   /* ----新增对比功能----- */
        if (files.length) {
            var file = files[0];
            var reader = new FileReader();

            reader.onload = function (e) {
                var resulttable_1 = document.getElementById("result_table");  // 原始结果
                console.log(resulttable_1)

                var temp = this.result.split("<p></p>")[2];
                var a = temp.replace(/result_table/, "compare_result_table");
                var compare_table = a.replace(/option/g,"result_option")
                console.log(compare_table)
                document.getElementById("filecontent").innerHTML = compare_table;

                debugger;
                var resulttable_2 = document.getElementById("compare_result_table"); // 对比结果

                var Rows_1 = resulttable_1.rows.length;   // 原始表的行数
                var Cells_1 = resulttable_1.rows[1].cells.length;  // 原始表的最大列数
                var Rows_2 = resulttable_2.rows.length; // 对比表的行数
                var Cells_2 = resulttable_2.rows[1].cells.length;  // 对比表的最大列数

                for (var i = 1; i < Rows_1; i++) {    //遍历Table的所有Row

                    if (resulttable_1.rows[i].cells.length > 2) {
                        console.log(resulttable_1.rows[i].cells.length)
                        for (var j = 1; j < Rows_2; j++) {    //遍历对比表格的的所有测试项
                            debugger

                            var testcase_1 = resulttable_1.rows[i].cells[1].innerText;
                            var testcase_2 = resulttable_2.rows[j].cells[1].innerText;
                            console.log('resulttable_1[i][1]:'+resulttable_1.rows[i].cells[1].innerText)
                            console.log('resulttable_2[j][1]:'+resulttable_2.rows[j].cells[1].innerText)
                            console.log(resulttable_1.rows[i].cells[2].innerText!='')
                            console.log(testcase_1.trim() == testcase_2.trim())
                            debugger
                            if ((resulttable_1.rows[i].cells[2].innerText!='') && (testcase_1.trim() == testcase_2.trim())) {
                                newtr = resulttable_1.insertRow(i+1);
                                newtr.className= resulttable_1.rows[i].className;  // 写入 （对比数据）行的class 值 <tr class=>
                                newtr.id = resulttable_1.rows[i].id;    // 写入 （对比数据）行的id 值 <tr id=>
                                Rows_1 = Rows_1+1;  // 新增的行数先初始化完成
                                for (tdnum=0;tdnum<=8;tdnum++){   // 仅需要补充 8个 单元格
                                    temtd = newtr.insertCell(tdnum)
                                    temtd.innerHTML = '　';
                                    temtd.style.color='blue';
                                    temtd.align='center';
                                }
                                resulttable_1.rows[i].cells[0].rowSpan = '2';
                                resulttable_1.rows[i].cells[1].rowSpan = '2';
                                resulttable_1.rows[i].cells[11].rowSpan = '2';
                                resulttable_1.rows[i].cells[12].rowSpan = '2';

                                // debugger
                                for(ii=2;ii<11;ii++){
                                    if (ii == 11){
                                        ii = 2;
                                    };

                                    var value = resulttable_2.rows[j].cells[ii].innerText;
                                    console.log('写入值:'+resulttable_2.rows[j].cells[ii].innerText)
                                    resulttable_1.rows[i+1].cells[ii-2].innerText= value;
                                }

                                // debugger;
                                tempdata = resulttable_2.rows[j].cells[11].innerHTML;
                                console.log(tempdata)
                                var re = new RegExp(/data:\[(\d+.*)\d]/)
                                // debugger;
                                temp_comparedata = tempdata.match(re)[1].split(',');  // 获取到 frame count data，填充到原始表格中
                                console.log(temp_comparedata)
                                // debugger;
                                var frame_comparedata=[];
                                for(i1=0;i1<temp_comparedata.length;i1++){
                                    frame_comparedata.push(Number(temp_comparedata[i1].trim()));
                                }
                                // console.log(frame_comparedata)

                                debugger
                                optionid = "option_" + resulttable_1.rows[i].id.replace('.','_');
                                console.log(optionid)
                                eval(optionid).legend.data.push('compare_version');
                                eval(optionid).series.push({name:'compare_version',type:'bar',data:frame_comparedata});
                                console.log(eval(optionid).series)
                                console.log(eval(optionid).series[1])

                            }
                        }
                    }
                }
            }
            reader.readAsText(file);
        }
    }

    /* obsoleted by detail in <div>
    function showOutput(id, name) {
        var w = window.open("", //url
                        name,
                        "resizable,scrollbars,status,width=800,height=450");
        d = w.document;
        d.write("<pre>");
        d.write(html_escape(output_list[id]));
        d.write("\n");
        d.write("<a href='javascript:window.close()'>close</a>\n");
        d.write("</pre>\n");
        d.close();
    }
    */
    --></script>

    <div id="div_base">
        %(heading)s
        %(report)s
        %(ending)s
        %(chart_script)s
    </div>
</body>
</html>
"""  # variables: (title, generator, stylesheet, heading, report, ending, chart_script)

    ECHARTS_SCRIPT = """
        <script type="text/javascript">
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('chart'));

            // 指定图表的配置项和数据
            var option_result = {
                title : {
                    text: '测试执行情况',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%%)"
                },
                legend: {
                    orient: 'vertical',
                    left: 'left',
                    data: ['通过','失败','错误']
                },
                series : [
                    {
                        name: '测试执行情况',
                        type: 'pie',
                        radius : '60%%',
                        center: ['50%%', '60%%'],
                        data:[
                            {value:%(Pass)s, name:'通过'},
                            {value:%(fail)s, name:'失败'},
                            {value:%(error)s, name:'错误'}
                        ],
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option_result);
        </script>
        """  # variables: (Pass, fail, error)

    Frame_Chart = """
        <div id="%(chart_id)s" style="width:600px;height:500px;float:left;" class="popup_window">
            <script  type="text/javascript">
                // 指定图表的配置项和数据
                var %(option_id)s = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross',
                            crossStyle: {
                                color: '#999'
                            }
                        }
                    },
                    toolbox: {
                        feature: {
                            dataView: {show: true, readOnly: false},
                            magicType: {show: true, type: ['line', 'bar']},
                            restore: {show: true},
                            saveAsImage: {show: true}
                        }
                    },
                    legend: {
                        data:['current']
                    },
                    xAxis: [
                        {
                            name: 'ms',
                            type: 'category',
                            data: %(frametime)s,
                            axisPointer: {
                                type: 'shadow'
                            },
                            axisLabel: {
                                formatter: '{value}ms '
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '百分比',
                            interval: 10,
                            axisLabel: {
                                formatter: '{value}%% '
                            }
                        },

                    ],
                    series: [
                        {
                            name:'current',
                            type:'bar',
                            data:%(framecount)s
                        },

                    ]
                };
            </script>
        </div>
        """  # variables: (frametime, framecount)
    Filereader = '''
    <script type="text/javascript">
        window.onload = function() {
            /**
             * 上传函数
             * @param fileInput DOM对象
             * @param callback 回调函数
             */
            var getFileContent = function (fileInput, callback) {
                if (fileInput.files && fileInput.files.length > 0 && fileInput.files[0].size > 0) {
                    //下面这一句相当于JQuery的：var file =$("#upload").prop('files')[0];
                    var file = fileInput.files[0];
                    if (window.FileReader) {
                        var reader = new FileReader();
                        reader.onloadend = function (evt) {
                            if (evt.target.readyState == FileReader.DONE) {
                                callback(evt.target.result);
                            }
                        };
                        // 包含中文内容用gbk编码
                        reader.readAsText(file, 'utf-8');
                    }
                }
            };

        /**
         * upload内容变化时载入内容
         */

    };
    </script>
    '''

    GetComparedata = '''
    <script>
        document.getElementById('xFile').onchange = function () {
            getFileContent(this, function (str) {
                var data =  = str;

            });
        };
    </script>
    '''

    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = u"""
<style type="text/css" media="screen">
    body        { font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }
    table       { font-size: 100%; }
    pre         { white-space: pre-wrap;word-wrap: break-word; }

    /* -- heading ---------------------------------------------------------------------- */
    h1 {
        font-size: 16pt;
        color: gray;
    }
    .heading {
        margin-top: 0ex;
        margin-bottom: 1ex;
    }

    .heading .attribute {
        margin-top: 1ex;
        margin-bottom: 0;
    }

    .heading .description {
        margin-top: 2ex;
        margin-bottom: 3ex;
    }

    /* -- css div popup ------------------------------------------------------------------------ */
    a.popup_link {
    }

    a.popup_link:hover {
        color: red;
    }

    .popup_window {
        display: none;
        position: relative;
        left: 0px;
        top: 0px;
        /*border: solid #627173 1px; */
        padding: 10px;
        /*background-color: #E6E6D6; */
        font-family: "Lucida Console", "Courier New", Courier, monospace;
        text-align: left;
        font-size: 8pt;
        /* width: 500px;*/
    }

    }
    /* -- report ------------------------------------------------------------------------ */
    #show_detail_line {
        margin-top: 3ex;
        margin-bottom: 1ex;
    }
    #result_table {
        width: 99%;
    }
    #header_row {
        font-weight: bold;
        color: #303641;
        background-color: #ebebeb;
    }
    #total_row  { font-weight: bold; }
    .passClass  { background-color: #bdedbc; }
    .failClass  { background-color: #ffefa4; }
    .errorClass { background-color: #ffc9c9; }
    .passCase   { color: #6c6; }
    .failCase   { color: #FF6600; font-weight: bold; }
    .errorCase  { color: #c00; font-weight: bold; }
    .hiddenRow  { display: none; }
    .testcase   { margin-left: 2em; }


    /* -- ending ---------------------------------------------------------------------- */
    #ending {
    }

    #div_base {
                position:absolute;
                top:0%;
                left:5%;
                right:5%;
                width: auto;
                height: auto;
                margin: -15px 0 0 0;
    }
</style>
"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """
    <div class='page-header'>
        <h1>%(title)s</h1>
    %(parameters)s
    </div>
    <div style="float: left;width:50%%;"><p class='description'>%(description)s</p></div>
    <div id="chart" style="width:50%%;height:250px;float:left;"></div>
    """  # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>
    """  # variables: (name, value)

    # ------------------------------------------------------------------------
    # Report
    #
    REPORT_TMPL = u"""
    <div class="btn-group btn-group-sm" style="float:left;width:50%%;">
        <button class="btn btn-default" onclick='javascript:showCase(0)'>总结</button>
        <button class="btn btn-default" onclick='javascript:showCase(1)'>失败</button>
        <button class="btn btn-default" onclick='javascript:showCase(2)'>全部</button>
        <!-- 新增对比功能： 增加对比功能按钮 -->
        <label class="btn btn-default" for="xFile">对比历史数据</label>
        <form><input type="file" id="xFile" accept="excel/xls,excel/xlsx" style="position:absolute;clip:rect(0 0 0 0);"onchange="compare_file(this.files)"></form>
    </div>

    <p></p>
    <table id='result_table' class="table table-bordered">
        <colgroup>
            <col align='left' />
            <col align='right' />
            <col align='right' />
            <col align='right' />
            <col align='right' />
            <col align='right' />
        </colgroup>
        <tr id='header_row'>
            <td colspan='2'>测试套件/测试用例</td>
            <td> 整体平均每帧耗时 </td>
            <td> 修正平均每帧耗时 </td>
            <td> 优秀率（5-8ms帧数占比）</td>
            <td> 掉帧率（Miss Vsync） </td>
            <td> 劣帧率 （Janky Frame）</td>
            <td> High input latency </td>
            <td> Slow UI thread </td>
            <td> Slow bitmap uploads </td>
            <td> Slow issue draw commands </td>
            <td> 帧耗时分布图 </td>
            <td> 查看 </td>
        </tr>
        %(test_list)s
    <p></p>
        <tr id='total_row'>
            <td colspan='2'>总分</td>
            <td align="center"> %(sscore)s</td>
            <td align="center"> %(mscore)s</td>
            <td align="center"> %(escore)s</td>
            <td colspan='3'>Pass: %(Pass)s</td>
            <td colspan='3'>Failed: %(fail)s</td>
            <td colspan='2'>Error: %(error)s</td>
        </tr>
    </table>


"""  # variables: (test_list, sscore, mscore, escore, Pass, fail, error)

    REPORT_CLASS_TMPL = u"""
    <tr class='%(style)s'>
        <td>Case ID</td>
        <td>%(desc)s</td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td align="center"><a href="javascript:showClassDetail('%(cid)s',%(count)s)">详情</a></td>
    </tr>
"""  # variables: (style, desc, avgFps, avgJank, fail, error, cid)    删除一行 <td>%(error)s</td>

    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td align='center'>%(case_id)s</td>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>

    <td align="center"><b> %(avgeScore)s </b></td>
    <td align="center"> %(mavgeScore)s </td>
    <td align="center"> %(excellent_rate)s </td>
    <td align="center"> %(missvsync)s </td>
    <td align="center"> %(janky)s </td>
    <td align="center"> %(inputlatency)s </td>
    <td align="center"> %(slow_ui)s </td>
    <td align="center"> %(slow_bitmap)s </td>
    <td align="center"> %(slow_draw)s </td>
    <td align="center">
        <a class="popup_link" onfocus='this.blur();' href="javascript:showEchatDetial('%(chart_id)s',%(option_id)s)" >
        帧分布直方图</a>
            %(FrameChart)s
    </td>
    <td colspan='5' align='center'>

    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')" >
        %(status)s</a>

    <div id='div_%(tid)s' class="popup_window">
        <pre>
        %(script)s
        </pre>
    </div>
    <!--css div popup end-->

    </td>
</tr>
"""  # variables: (tid, caseid, Class, style, desc, FrameChart, fps, jank, max_drop status)
    # 新增 FrameChart caseid fps jank max_drop

    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>%(status)s</td>
</tr>
"""  # variables: (tid, Class, style, desc, status)

    REPORT_TEST_OUTPUT_TMPL = r"""%(id)s: %(output)s"""  # variables: (id, output)
    REPORT_TEST_OUTPUT_CASEID = r"""%(case_id)s"""  # variables: (case id)
    REPORT_TEST_OUTPUT_SUMS = r"""%(avgeScore)s"""  # variables: (avgeScore)
    REPORT_TEST_OUTPUT_MSCORE = r"""%(mavgeScore)s"""  # variables: (modifySocre)
    REPORT_TEST_OUTPUT_ERATE = r"""%(excellent_rate)s"""  # variables: (excellent_rate)
    # REPORT_TEST_OUTPUT_FRAME = r"""%(frameinfo_add)s"""  # variables: (frameinfo file address)

    REPORT_TEST_OUTPUT_MissVsync = r"""%(missvsync)s"""  # variables: (Number Missed Vsync)
    REPORT_TEST_OUTPUT_JankyFrame = r"""%(janky)s"""  # variables: (Janky frames)
    REPORT_TEST_OUTPUT_INPUT = r"""%(inputlatency)s"""  # variables: (Number High input latency)
    REPORT_TEST_OUTPUT_UI = r"""%(slow_ui)s"""  # variables: (Number Slow UI thread)
    REPORT_TEST_OUTPUT_BITMAP = r"""%(slow_bitmap)s"""  # variables: (Number Slow bitmap uploads)
    REPORT_TEST_OUTPUT_DRAW = r"""%(slow_draw)s"""  # variables: (Number Slow issue draw commands)

    # ------------------------------------------------------------------------
    # ENDING
    #

    ENDING_TMPL = """
    <div id='ending'>&nbsp;</div>
    <div id="filecontent"> </div>
    """


# -------------------- The end of the Template class -------------------


TestResult = unittest.TestResult


class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []
        self.subtestlist = []

    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = StringIO.StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()

    def addSuccess(self, test):
        if test not in self.subtestlist:
            self.success_count += 1
            TestResult.addSuccess(self, test)
            output = self.complete_output()
            self.result.append((0, test, output, ''))
            if self.verbosity > 1:
                sys.stderr.write('ok ')
                sys.stderr.write(str(test))
                sys.stderr.write('\n')
            else:
                sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')

    def addSubTest(self, test, subtest, err):
        if err is not None:
            if getattr(self, 'failfast', False):
                self.stop()
            if issubclass(err[0], test.failureException):
                self.failure_count += 1
                errors = self.failures
                errors.append((subtest, self._exc_info_to_string(err, subtest)))
                output = self.complete_output()
                self.result.append((1, test, output + '\nSubTestCase Failed:\n' + str(subtest),
                                    self._exc_info_to_string(err, subtest)))
                if self.verbosity > 1:
                    sys.stderr.write('F  ')
                    sys.stderr.write(str(subtest))
                    sys.stderr.write('\n')
                else:
                    sys.stderr.write('F')
            else:
                self.error_count += 1
                errors = self.errors
                errors.append((subtest, self._exc_info_to_string(err, subtest)))
                output = self.complete_output()
                self.result.append(
                        (2, test, output + '\nSubTestCase Error:\n' + str(subtest),
                         self._exc_info_to_string(err, subtest)))
                if self.verbosity > 1:
                    sys.stderr.write('E  ')
                    sys.stderr.write(str(subtest))
                    sys.stderr.write('\n')
                else:
                    sys.stderr.write('E')
            self._mirrorOutput = True
        else:
            self.subtestlist.append(subtest)
            self.subtestlist.append(test)
            self.success_count += 1
            output = self.complete_output()
            self.result.append((0, test, output + '\nSubTestCase Pass:\n' + str(subtest), ''))
            if self.verbosity > 1:
                sys.stderr.write('ok ')
                sys.stderr.write(str(subtest))
                sys.stderr.write('\n')
            else:
                sys.stderr.write('.')


class HTMLTestRunner(Template_mixin):
    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):
        self.stream = stream
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description

        self.startTime = datetime.datetime.now()

        self.sscore = []
        self.mscore = []
        self.escore = []

    def run(self, test):
        """Run the given test case or test suite."""
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.generateReport(test, result)
        print('\nTime Elapsed: %s' % (self.stopTime - self.startTime))  # ,file= sys.stderr)
        return result

    def sortResult(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n, t, o, e in result_list:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        if result.success_count: status.append(u'通过 %s' % result.success_count)
        if result.failure_count: status.append(u'失败 %s' % result.failure_count)
        if result.error_count:   status.append(u'错误 %s' % result.error_count)
        if status:
            status = ' '.join(status)
        else:
            status = 'none'
        return [
            (u'开始时间', startTime),
            (u'运行时长', duration),
            (u'状态', status),
        ]

    def generateReport(self, test, result):
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        chart = self._generate_chart(result)
        output = self.HTML_TMPL % dict(
                title=saxutils.escape(self.title),
                generator=generator,
                stylesheet=stylesheet,
                heading=heading,
                report=report,
                ending=ending,
                chart_script=chart.decode('utf-8')  # 需要修改编码格式
        )
        self.stream.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                    name=saxutils.escape(name),
                    value=saxutils.escape(value),
            )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
                title=saxutils.escape(self.title),
                parameters=''.join(a_lines),
                description=saxutils.escape(self.description),
        )
        return heading

    def _generate_report(self, result):
        rows = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            # subtotal for a class
            np = nf = ne = 0
            for n, t, o, e in cls_results:
                if n == 0:
                    np += 1
                elif n == 1:
                    nf += 1
                else:
                    ne += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            row = self.REPORT_CLASS_TMPL % dict(
                    style=ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                    desc=desc,
                    count=np + nf + ne,
                    avgFps=np,  # TODO:   总case的平均fps
                    avgJank=nf,  # TODO：  总case的累计jank次数
                    max_drop=ne,  # TODO：  总case的累计掉帧时长
                    cid='c%s' % (cid + 1),
            )
            rows.append(row)

            for tid, (n, t, o, e) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e)

        report = self.REPORT_TMPL % dict(
                test_list=''.join(rows),
                sscore=str('%.2f' % (sum(self.sscore) / len(self.sscore))),
                mscore=str('%.2f' % (sum(self.mscore) / len(self.mscore))),
                escore=str('%.2f' % (sum(self.escore) / len(self.escore))),
                Pass=str(result.success_count),
                fail=str(result.failure_count),
                error=str(result.error_count),
        )
        return report

    def _generate_chart(self, result):
        chart = self.ECHARTS_SCRIPT % dict(
                Pass=str(result.success_count),
                fail=str(result.failure_count),
                error=str(result.error_count),
        )
        return chart

    def _generate_framechart(self, chart_id, option_id, time, count):
        frame_chart = self.Frame_Chart % dict(  # Frame_Chart : javascript
                chart_id=str(chart_id),
                option_id=str(option_id),
                frametime=str(time),
                framecount=str(count),
        )
        return frame_chart

    def _generate_report_test(self, rows, cid, tid, n, t, o, e):  # 单条用例的测试结果报告
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid + 1, tid + 1)

        for tem in o.split('\n'):
            if tem.startswith('case Name:'):
                name = tem.split(':')[-1]  # 修改测试用例名字
                break
            else:
                name = 'UNKNOW'

        doc = t.shortDescription() or ""
        if name:
            desc = doc and ('%s: %s' % (name, doc)) or name
        else:
            desc = doc and ('%s: %s' % ('UNKNOW', doc)) or 'UNKNOW'
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL

        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
                id=tid,
                output=saxutils.escape(o + e),
        )

        case_id = self.REPORT_TEST_OUTPUT_CASEID % dict(  # new added
                case_id=saxutils.escape(o + e)
        )

        avgeScore = self.REPORT_TEST_OUTPUT_SUMS % dict(  # new added
                avgeScore=saxutils.escape(o + e)
        )

        mavgeScore = self.REPORT_TEST_OUTPUT_MSCORE % dict(  # new added
                mavgeScore=saxutils.escape(o + e)
        )
        excellent_rate = self.REPORT_TEST_OUTPUT_ERATE % dict(  # new added
                excellent_rate=saxutils.escape(o + e)
        )

        # frameinfo_add = self.REPORT_TEST_OUTPUT_FRAME % dict(  # new added # DELETE THIS CROW
        #         frameinfo_add=saxutils.escape(o + e)
        # )

        missvsyncdata = self.REPORT_TEST_OUTPUT_MissVsync % dict(
                missvsync=script
        )

        jankydata = self.REPORT_TEST_OUTPUT_JankyFrame % dict(
                janky=script
        )
        inputlatencydata = self.REPORT_TEST_OUTPUT_INPUT % dict(
                inputlatency=script
        )
        slow_ui = self.REPORT_TEST_OUTPUT_UI % dict(
                slow_ui=script
        )
        slow_bitmap = self.REPORT_TEST_OUTPUT_BITMAP % dict(
                slow_bitmap=script
        )
        slow_drawdata = self.REPORT_TEST_OUTPUT_DRAW % dict(
                slow_draw=script
        )

        # 初始化数据
        v_case_id = '0'
        v_inputlatency = '0'
        v_jank = v_max_drop = '0'
        v_janky = v_missvsync = v_slow_bitmap = v_slow_draw = v_slow_ui = '0'

        time = count = '0'
        fpslist = '0'

        # 匹配数据
        for tmp in script.split('\n'):
            if tmp.startswith('case id:'):
                v_case_id = tmp.split(':')[-1]
                continue

            if tmp.startswith('jank rate:'):
                v_janky = tmp.split(':')[1]
                continue
            if tmp.startswith('real jank rate:'):
                v_missvsync = tmp.split(':')[1]
                # jankscore = (100-float(v_missvsync.split('%')[0])) * 0.3
                # self.jscore.append(jankscore)
                continue
            if tmp.startswith('High input latency:'):
                v_inputlatency = tmp.split(':')[1]
                continue
            if tmp.startswith('Slow UI thread:'):
                v_slow_ui = tmp.split(':')[1]
                continue
            if tmp.startswith('Slow bitmap uploads:'):
                v_slow_bitmap = tmp.split(':')[1]
                continue
            if tmp.startswith('Slow issue draw commands rate:'):
                v_slow_draw = tmp.split(':')[1]
                continue

            if tmp.startswith('Frame Latency:'):  # time = script.split('\n')[13].split(":")[-1]
                time = tmp.split(":")[-1]
                continue
            if tmp.startswith('Frame Count:'):  # count = script.split('\n')[14].split(":")[-1]
                count = tmp.split(":")[-1]
                continue

                # if tmp.startswith('fps:'):  # fpslist = fps.split('\n')[16].split(':')[1].split(',')
                #     fpslist = tmp.split(':')[1].split(',')
                #     continue
                # if tmp.startswith('jank count:'):
                #     v_jank = tmp.split(':')[1]
                #     continue
                # if tmp.startswith('max frame delay:'):
                #     v_max_drop = tmp.split(':')[1]
                #     continue

        # totalfps = 0
        # fpslist_len = 0
        # if fpslist:
        #     for i in fpslist:
        #         if i.strip(' [').strip(']') != 'None':
        #             totalfps += int(i.strip(' [').strip(']'))
        #             fpslist_len += 1
        #     if fpslist_len != 0:
        #         avgfps = int(totalfps / fpslist_len)
        #     else:
        #         avgfps = '0'
        # else:
        #     avgfps = '0'

        chart_id_data = 'framechart_' + tid
        option_id = 'option_' + tid.replace('.', '_')
        if time and count:
            frame_chart = self._generate_framechart(chart_id_data, option_id, time, count)

            count_int = [float(i.strip('[').strip(']')) for i in count.split(',')]
            time_int = [int(i.strip('[').strip(']')) for i in time.split(',')]
            scorelist = []
            avgelist = []

            avgelist = [x * y for x, y in zip(time_int, count_int)]
            avgeScore = sum(avgelist) / 100
            excellent_rate = sum(count_int[:4])

            for t in time_int:
                if t < 100:
                    scorelist.append(t * count_int[time_int.index(t)])
            if scorelist and sum(count_int[0:47]):
                mavgeScore = sum(scorelist) / sum(count_int[0:47])
            else:
                mavgeScore = 0
        else:
            time = count = '0'
            frame_chart = self._generate_framechart(chart_id_data, option_id, time, count)
            avgeScore = mavgeScore = excellent_rate = 0

        self.sscore.append(avgeScore)
        self.mscore.append(mavgeScore)
        self.escore.append(excellent_rate)

        if v_case_id and v_inputlatency and avgeScore and mavgeScore and excellent_rate and v_janky and v_missvsync and v_slow_bitmap and \
                v_slow_draw and v_slow_ui:
            row = tmpl % dict(
                    tid=tid,
                    Class=(n == 0 and 'hiddenRow' or 'none'),
                    style=(n == 2 and 'errorCase' or (n == 1 and 'failCase' or 'none')),
                    desc=desc,
                    FrameChart=frame_chart.decode("utf-8"),
                    script=script,
                    case_id=v_case_id,
                    status=self.STATUS[n],
                    avgeScore=str('%.2f' % avgeScore),
                    mavgeScore=str('%.2f' % mavgeScore),
                    excellent_rate=str(excellent_rate),
                    # frameinfo_add=frameinfo_add.split('\n')[12].split("output\\")[1],
                    missvsync=v_missvsync,
                    janky=v_janky,
                    inputlatency=v_inputlatency,
                    slow_ui=v_slow_ui,
                    slow_bitmap=v_slow_bitmap,
                    slow_draw=v_slow_draw,
                    chart_id=chart_id_data.decode("utf-8"),
                    option_id=option_id.decode("utf_8")
            )
            rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL

    def _getframescore(self, count, time):
        count_int = [float(i.strip('[').strip(']')) for i in count.split(',')]
        time_int = [int(i.strip('[').strip(']')) for i in time.split(',')]
        scorelist = []

        avgescore = sum(count_int) / 100
        good_percent = sum(count[:3])

        for t in time_int:
            if t < 100:
                scorelist.append(t * count_int[time_int.index(t)])

        b_avgescore = sum(scorelist)

        '''
        第一版打分方案：
        if len(count_int) > 5:
            level1 = sum(count_int[:5])
        else:
            level1 = 0
        if len(count_int) > 10:
            level2 = sum(count_int[6:10])
        else:
            level2 = 0
        if len(count_int) > 36:
            level3 = sum(count_int[11:36])
        else:
            level3 = 0
        if len(count_int) > 37:
            level4 = sum(count_int[37:])
        else:
            level4 = 0
        framescore = level1 * 0.35 + level2 * 0.2 - level3*0.15 - level4*0.3
        return framescore
        '''


##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note: Reuse unittest.TestProgram to launch test. In the future we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.
class TestProgram(unittest.TestProgram):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """

    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate HTMLTestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)


main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)
