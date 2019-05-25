#!/usr/bin/python
# -*- coding: utf-8 -*-

# newclass.py
import _thread
import threading

import wx
import wx.grid

import Strat

class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,
                                          size=(600, 800))
        self.job = []
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)
        self.panel = panel
        sizer = wx.GridBagSizer(5, 5)

        sizer.Add( wx.StaticText(panel, label='任务排序：'), pos=(0, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT|wx.BOTTOM, border=3)

        grid = wx.grid.Grid(panel)
        grid.CreateGrid(10, 3)
        grid.SetColSize(0,150)
        grid.SetColSize(1, 50)
        grid.SetColSize(2, 50)

        grid.SetColLabelValue(0, "任务名称")
        grid.SetColLabelValue(1, "次数")
        grid.SetColLabelValue(2, "")
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.gridOnCellLeftClick)

        sizer.Add(grid , pos=(1, 0),span=(1, 5),flag=wx.TOP| wx.BOTTOM, border=5)
        self.grid = grid

        task_text =  wx.StaticText(panel, label='任务选择:')
        sizer.Add(task_text, pos=(4, 0), flag=wx.TOP | wx.LEFT, border=8 )

        distros = ['物资筹备-货物运送', '物资筹备-战术演习', '物资筹备-空中威胁', '物资筹备-粉碎防御', '物资筹备-资源保障','芯片搜索-摧枯拉朽','芯片搜索-固若金汤']
        cb = wx.ComboBox(panel,  choices=distros,
                         style=wx.CB_READONLY)
        sizer.Add(cb,pos=(4, 1), span=(1, 1) ,flag=wx.TOP , border=3)
        self.cb = cb

        count_text = wx.StaticText(panel, label='次数:')
        sizer.Add(count_text, pos=(4, 2), flag=wx.TOP | wx.LEFT, border=8)

        sp = wx.SpinCtrl(panel,value ='1',size = (50,20))
        sizer.Add(sp, pos=(4, 3), flag=wx.TOP, border=5)
        self.sp = sp


        b = wx.Button(panel, label="添加任务")
        b.Bind(wx.EVT_BUTTON,self.add)
        sizer.Add(b, pos=(4, 4), flag= wx.RIGHT, border=8)

        line3 = wx.StaticLine(panel)
        sizer.Add(line3, pos=(5, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.BOTTOM, border=10)

        textCtrl_text = wx.StaticText(panel, label='模拟器名称:')
        sizer.Add(textCtrl_text, pos=(6, 0), flag=wx.TOP | wx.LEFT, border=8)

        textCtrl = wx.TextCtrl(panel, size=(200,30))
        sizer.Add(textCtrl, pos=(6, 1),span=(1, 2), flag=wx.TOP , border=3)
        self.textCtrl = textCtrl

        button2 = wx.Button(panel, label="开始")
        sizer.Add(button2, pos=(6, 3), flag=wx.TOP | wx.RIGHT, border=3)
        button2.Bind(wx.EVT_BUTTON, self.start)

        button3 = wx.Button(panel, label="结束")
        sizer.Add(button3, pos=(6, 4), flag=wx.TOP | wx.RIGHT, border=3)
        button3.Bind(wx.EVT_BUTTON, self.end)

        sb = wx.StaticBox(panel, label="选项")

        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        boxsizer.Add(wx.CheckBox(panel, label="循环任务列表"),
                     flag=wx.LEFT | wx.TOP, border=5)
        boxsizer.Add(wx.CheckBox(panel, label="失智休息"),
                     flag=wx.LEFT, border=5)
        boxsizer.Add(wx.CheckBox(panel, label="基建收取"),
                     flag=wx.LEFT | wx.BOTTOM, border=5)
        sizer.Add(boxsizer, pos=(8, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=3)

        text2 = wx.StaticText(panel, label="注意：模拟器名称是指鼠标放到任务栏图标中展示的名称，如：明日方舟 - MuMu模拟器")
        sizer.Add(text2, pos=(9, 0),span=(1, 5), flag=wx.LEFT, border=10)
        sizer.AddGrowableRow(9)
        sizer.AddGrowableCol(4)
        panel.SetSizer(sizer)


    def add(self,e):
        print('aa')
        job =  self.cb.GetValue()
        times = self.sp.GetValue()
        n = len(self.job)
        self.addToGrid(n,job,times)
        self.job.append((job, times))

        e.Skip()
    def gridOnCellLeftClick(self,e):
        print('aa')
        r =e.GetRow()
        c =e.GetCol()
        job = self.job
        n = len(job)
        self.addToGrid(n -1,'', '')
        self.grid.SetCellValue(n -1, 2, '')
        del job[r]
        if c == 2:
            for index in range(len(job)):
                self.addToGrid(index,job[index][0],job[index][1])
                pass
        e.Skip()
        pass

    def addToGrid(self,n,job,times):
        self.grid.SetCellValue(n, 0, job)
        self.grid.SetCellValue(n, 1, str(times))
        self.grid.SetCellValue(n, 2, '删除')
        self.grid.SetCellTextColour(n, 2, wx.RED)
        self.grid.SetReadOnly(n, 0, True)
        self.grid.SetReadOnly(n, 1, True)
        self.grid.SetReadOnly(n, 2, True)

    def start(self,e):
        job = self.job
        #明日方舟 - MuMu模拟器
        thread = MyThread(1, "Thread-1", 1,{'titlename':self.textCtrl.GetValue(),'jobs':job})
        self.thread = thread
        thread.start()

        pass
    def test(self,e):
        pass

    def end(self,e):
        self.thread.event.set()
        print('工作停止')
        pass
class MyThread (threading.Thread):
    def __init__(self, threadID, name, counter,data):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.event  = threading.Event()
        self.data = data
    def run(self):
        print ("开始线程：" + self.name)
        Strat.main(self)
        print ("退出线程：" + self.name)


if __name__ == '__main__':
    app = wx.App()
    Example(None, title="枫叶辅助")
    app.MainLoop()