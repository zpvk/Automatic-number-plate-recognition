# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import cv2 as cv
    import imutils

    img = cv.imread('4.jpeg', cv.IMREAD_COLOR)
    img = cv.resize(img, (400, 200))

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.bilateralFilter(gray, 13, 15, 15)

    edged = cv.Canny(gray, 30, 200)

    contours = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv.contourArea, reverse=True)[:10]
    screenCnt = []

    for c in contours:
        # approximate the contour
        peri = cv.arcLength(c, True)  # The function computes a curve length or a closed contour perimeter
        approx = cv.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            screenCnt.append(approx)
    if len(screenCnt) != 0:
        print(len(screenCnt))
        for sc in screenCnt:
            xd = cv.drawContours(img, [sc], -1, (0, 0, 255), 3)
            cv.imshow('np', xd)
            cv.waitKey(0)
            cv.destroyAllWindows()
    else:
        print("no result")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
