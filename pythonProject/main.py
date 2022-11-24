import numpy as np
import cv2, sys
from matplotlib import pyplot as plt
from PIL import ImageGrab
import pyautogui as pag


def colorClick(event, x, y, flags, param):
      global last, img_color

      if event == cv2.EVENT_LBUTTONDOWN:
          print(img_color[y, x])
          color = img_color[y, x]

          one_pixel = np.uint8(color)
          last = one_pixel


# 마우스 이벤트 처리 함수
def onMouse(event, x, y, flags, param):
    global mask, img
    if event == cv2.EVENT_LBUTTONDOWN:
        seed = (x,y)
        # 색 채우기 적용 ---④
        retval = cv2.floodFill(img, mask, seed, newVal, loDiff, upDiff)
        # 채우기 변경 결과 표시 ---⑤
        cv2.imshow('img', img)
# def endClick(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()


def chooseColor(pal):
    global last, img_color

    cv2.namedWindow('img_color')
    cv2.setMouseCallback('img_color', colorClick)

    img_color = cv2.imread(pal)
    cv2.imshow('img_color', img_color)
    key = cv2.waitKey(0)&0xFF # 이거 안 하면 에러뜸

    cv2.destroyWindow('img_color')
    a = []
    for i in range(0, 3):
        a.append(last[i].item())
    return tuple(a)


img = cv2.imread('Sketch/dori.jpg')
image_gray = cv2.imread('Sketch/dori.jpg', cv2.IMREAD_GRAYSCALE)

b, g, r = cv2.split(img)
image2 = cv2.merge([r, g, b])

blur = cv2.GaussianBlur(image_gray, ksize=(5, 5), sigmaX=0)
ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

edged = cv2.Canny(blur, 10, 250)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, ))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

contours, hierarchy = cv2.findContours(closed.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
total = 0
contours_image = cv2.drawContours(img, contours, -1, (0, 255, 0), 7)

rows, cols = img.shape[:2]
# 마스크 생성, 원래 이미지 보다 2픽셀 크게 ---①
mask = np.zeros((rows+2, cols+2), np.uint8)
# 채우기에 사용할 색 ---②
# a = []
# for i in range (0,3):
#     a.append(last[i].item())

# newVal = chooseColor()

# 최소 최대 차이 값 ---③
loDiff, upDiff = (10, 10, 10), (10, 10, 10)


# 화면 출력
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img', img)
cv2.setMouseCallback('img', onMouse)

while True:
    key = cv2.waitKey(0)

    if key == ord('s'):
        newVal = chooseColor('pallette/spring.jpg')
    elif key == ord('e'):
        newVal = chooseColor('pallette/summer.jpg')
    elif key == ord('f'):
        newVal = chooseColor('pallette/fall.jpg')
    elif key == ord('w'):
        newVal = chooseColor('pallette/winter.jpg')
    elif key == ord('v'):
        cv2.imwrite("result/colored.png", img)
        cv2.destroyAllWindows()
        break
