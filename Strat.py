import time
import traceback
from filecmp import cmp

import aircv as ac
import cv2 as cv

import buttonFunder
import PictureManage
#from UI import MyThread
from UI import MyThread
from Window import Window


# 计算中心点
def centrePoint(window, rectangle: tuple):
    x = (rectangle[3][0] - rectangle[0][0]) / 2 + rectangle[0][0] + window.left
    y = (rectangle[1][1] - rectangle[0][1]) / 2 + rectangle[0][1] + window.top
    return int(x), int(y)


def sleep():
    time.sleep(1.5)


# 回主菜单
def goMu(window):
    rectangle = buttonFunder.fund(window, PictureManage.mu)  # 判断是否是主菜单
    if rectangle is None:
        rectangle_home= buttonFunder.fund(window, PictureManage.home)  # 判断是否有home键
        if rectangle_home is not None:
            sleep()
            clickPos(window, rectangle_home)  # 点击home
            click(window, PictureManage.home_page)  # 点击主页
            return True
        else:
            return False
    else:
        return True


# 点击
def click(window, button):
    sleep()
    rectangle = buttonFunder.fund(window, button)
    if rectangle is None:  # 如果没找到可能是程序没相应完成 再次等待重试
        sleep()
        sleep()
        rectangle = buttonFunder.fund(window, button)
        x, y = centrePoint(window, rectangle)
        window.mouse_click(x, y)
    x, y = centrePoint(window, rectangle)
    window.mouse_click(x, y)


# 点击某一位置
def clickPos(window, rectangle):
    sleep()
    x, y = centrePoint(window, rectangle)
    window.mouse_click(x, y)


def get_x (elem):
    return elem[0][0]

# 点击最后关卡
def click_last(window, button):
    sleep()
    list = buttonFunder.fund_all(window, button, confidencevalue=0.8)
    list.sort(key=get_x,reverse= True )
    for rectangle in list:
        clickPos(window,rectangle)
        sleep()
        three_xing_rectangle =  buttonFunder.fund(window, PictureManage.three_xing, confidencevalue=0.9)
        if three_xing_rectangle is not None:
            break
        else:
            click(window, PictureManage.back)  # 点击返回键


# 开始战斗
def fight(window, p, times=1):
    click(window, p.start)  # 点击开始行动
    sleep()
    rectangle = buttonFunder.fund(window, p.agency, confidencevalue=0.5)
    if rectangle == None:
        click(window, p.back)  # 点击返回键
        click(window, p.agencycommand)
        click(window, p.start)  # 点击开始行动

    lastTime = 10  # 记录上次战斗时间
    for num in range(0, times):  # 循环刷图
        if num != 0:
            try:
                click(window, p.start)  # 点击开始行动
            except TypeError:
                print('结算未结束，等待5s')
                time.sleep(5)
                click(window, p.start)  # 点击开始行动
        click(window, p.fight)  # 开始战斗
        lastTime = wait_fight(window, p, lastTime)
        time.sleep(5)



# t上次战斗的时间
def wait_fight(window, p, t=0):
    start = time.time()
    time.sleep(t)
    a = 0
    while True:
        time.sleep(5)
        rectangle = buttonFunder.fund(window, p.lv_up)  # 升级
        if rectangle is not None:
            clickPos(window, rectangle)

        rectangle = buttonFunder.fund(window, p.complete)  # 战斗结束
        if rectangle is not None:
            if a != 0:
                end = time.time()
                clickPos(window, rectangle)
                return end - start
            a += 1


def show(reslut):
    img = ac.imread(PictureManage.screenshot)
    for r in reslut:
        cv.rectangle(img, r[0], r[3], (0, 255, 0))
    cv.namedWindow("img", 0)
    cv.imshow('img', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    pass


# 主菜单->龙鸣币
def job_long_ming_bi(window, times=1):
    wuzhi_job(window,PictureManage.longmingbi,PictureManage.money,times,'货物运送')

# 主菜单->粉碎防御
def job_caogou(window, times=1):
    wuzhi_job(window, PictureManage.fenshuifangyv, PictureManage.caigou, times, '粉碎防御')

# 主菜单->资源保障
def job_zhiyuan(window, times=1):
    wuzhi_job(window,PictureManage.ziyuan,PictureManage.SK,times,'资源保障')


def job_zhanshu(window, times=1):
    wuzhi_job(window, PictureManage.zhanshu, PictureManage.LS, times, '战术演习')


def wuzhi_job(window,fuben_p,guanka_p, times=1,name=''):
    click(window, PictureManage.zuozhan)
    click(window, PictureManage.wuzhi)
    try:
        click(window, fuben_p)
    except TypeError:
        print('没找到资源本'+name)
    click_last(window, guanka_p)
    fight(window, PictureManage, times)

def cklx(window, times=1):
    xinpian_job(window,PictureManage.cklx,PictureManage.PR_B,times,name='摧枯拉朽')


def grjt(window, times=1):
    xinpian_job(window,PictureManage.grjt,PictureManage.PR_A,times,name='固若金汤')

def xinpian_job(window,fuben_p,guanka_p, times=1,name=''):
    click(window, PictureManage.zuozhan)
    click(window, PictureManage.xinpian)
    try:
        click(window, fuben_p)
    except TypeError:
        print('没找到资源本'+name)
        return
    click_last(window, guanka_p)
    fight(window, PictureManage, times)


def main(myThread : MyThread):
    dict = {'物资筹备-货物运送':job_long_ming_bi,
            '物资筹备-战术演习': job_zhanshu,
            '物资筹备-空中威胁': job_long_ming_bi,
            '物资筹备-粉碎防御': job_caogou,
            '物资筹备-资源保障': job_zhiyuan,
            '芯片搜索-摧枯拉朽': cklx,
            '芯片搜索-固若金汤': grjt}


    try:
        w = Window(myThread.data['titlename'], screenshotPath=PictureManage.screenshot)
        # 进入主菜单
        if goMu(w) == False:
            print('请回到主菜单')
        else:
            print('开始任务')
            for job in myThread.data['jobs']:
                fun = dict[job[0]]
                fun.__call__(w,job[1])
                goMu(w)
            pass
    except BaseException as ex:
        msg = traceback.format_exc()  # 方式1
        print(msg)
    time.sleep(100)

# def test():
#     w = Window('明日方舟 - MuMu模拟器', screenshotPath=PictureManage.screenshot)
#     # three_xing_rectangle = buttonFunder.fund(w, PictureManage.three_xing, confidencevalue=0.8)  # 查看是否三星
#     # show([three_xing_rectangle])
#
#     try:
#         job_zhanshu(w,1)
#     except BaseException as ex:
#                  msg = traceback.format_exc()  # 方式1
#                  print(msg)
# if __name__ == '__main__':
#     test()
# 打包 √
# 基建
# 客户端 √
# 服务端
# 缓存
