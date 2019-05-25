
import aircv as ac
import cv2 as cv


# 图像匹配
def matchImg(w, imgsrc, imgobj, confidencevalue=0.75):  # imgsrc=原始图像，imgobj=待查找的图片
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)
    if imsrc.shape[0] != w.template_height and imsrc.shape[1] != w.template_width:
        size = (int(imobj.shape[1] * imsrc.shape[1] / w.template_width),
                int(imobj.shape[0] * imsrc.shape[0] / w.template_height))
        imobj = cv.resize(imobj, size, interpolation=cv.INTER_AREA)
    match_result = ac.find_template(imsrc, imobj, confidencevalue)
    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽    return match_result
    return match_result


# 图像匹配
def matchImg_all(w, imgsrc, imgobj, confidencevalue=0.75):  # imgsrc=原始图像，imgobj=待查找的图片
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)
    if imsrc.shape[0] != w.template_height and imsrc.shape[1] != w.template_width:
        size = (int(imobj.shape[1] * imsrc.shape[1] / w.template_width),
                int(imobj.shape[0] * imsrc.shape[0] / w.template_height))
        imobj = cv.resize(imobj, size, interpolation=cv.INTER_AREA)
    match_result = ac.find_all_template(imsrc, imobj, confidencevalue)
    return match_result


def fund(w, button, left_percent=0, top_percent=0, right_percent=0, bottom_percent=0, confidencevalue=0.5):
    reslut = matchImg(w, w.screenshot(left_percent, top_percent, right_percent, bottom_percent), button,
                      confidencevalue)
    if reslut == None:
        return None
    return reslut['rectangle']


def fund_all(w, button, left_percent=0, top_percent=0, right_percent=0, bottom_percent=0, confidencevalue=0.5):
    reslut = matchImg_all(w, w.screenshot(left_percent, top_percent, right_percent, bottom_percent), button,
                          confidencevalue)
    if reslut == None:
        return None, 0
    list = []
    for r in reslut:
        list.append(r['rectangle'])
    return list
