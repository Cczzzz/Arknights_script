import win32api
import win32gui

import win32con
from PIL import ImageGrab
import aircv as ac
import cv2 as cv


class Window(object):
    # screenshotPath 截图存放目录
    def __init__(self, titlename, classname=None, screenshotPath='C://Users/cc/Desktop/game/mu.PNG',
                 template_width=1600,
                 template_height=989):
        self.titlename = titlename
        self.classname = classname
        self.screenshotPath = screenshotPath
        hwnd = win32gui.FindWindow(classname, titlename)  # window句柄
        self.hwnd = hwnd
        win32gui.SetForegroundWindow(self.hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.width = right - left  # 窗口宽
        self.height = bottom - top  # 窗口高
        self.template_width = template_width
        self.template_height = template_height

    def screenshot(self, left_percent=0, top_percent=0, right_percent=0, bottom_percent=0):
        self.foregroundWindow()

        img = ImageGrab.grab(bbox=(
            self.left + self.width * left_percent,
            self.top + self.height * top_percent,
            self.right + self.width * right_percent,
            self.bottom + self.height * bottom_percent))
        img.save(self.screenshotPath)
        img.close()
        return self.screenshotPath

    # 置顶窗口
    def foregroundWindow(self):
        win32gui.SetForegroundWindow(self.hwnd)

    # 模拟鼠标点击
    def mouse_click(self, x, y):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def show(self, rectangle):
        img2 = ac.imread(self.screenshotPath)
        cv.rectangle(img2, rectangle[0], rectangle[3], (0, 255, 0))
        cv.namedWindow("img", 0)
        cv.imshow('img', img2)
        cv.waitKey(0)
        cv.destroyAllWindows()
