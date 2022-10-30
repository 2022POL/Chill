import shutil, os
import cv2

path_dir = "images"
file_list = os.listdir(path_dir)  # images 폴더 내 파일 이름 읽어오기
print(file_list)
cnt = 1

for file in file_list:
    extns = file[-4:]  # 이미지 파일 확장자 자르기

    src = cv2.imread("images/"+str(file), cv2.IMREAD_COLOR)  # 원본 데이터
    height, width = src.shape[:2]
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    canny = cv2.Canny(src, 100, 255)

    out = canny.copy()
    out = 255 - out  # canny 알고리즘 돌린 이미지 흑백반전
    # cv2.imshow("flip", cv2.resize(out,None, None, 2, 2, interpolation=cv2.INTER_AREA))

    cv2.imwrite("Edge/" + str(cnt) + extns, out)

    shutil.copyfile("images/yumi.jpg", "Original/" + str(cnt) + extns)
    cnt += 1