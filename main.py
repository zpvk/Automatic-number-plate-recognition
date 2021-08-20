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
    import numpy as np
    import pytesseract as tess

    tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    img = cv.imread('02.jpeg', cv.IMREAD_COLOR)
    img = cv.resize(img, (400, 200))

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.bilateralFilter(gray, 13, 15, 15)

    edged = cv.Canny(gray, 30, 200)

    contours = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv.contourArea, reverse=True)[:10]
    screenCnt = []
    screenCnt1 = None

    for c in contours:
        # approximate the contour
        peri = cv.arcLength(c, True)  # The function computes a curve length or a closed contour perimeter
        approx = cv.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            screenCnt1 = approx
            screenCnt.append(approx)
    text = []
    if len(screenCnt) != 0:
        print(len(screenCnt))
        for sc in screenCnt:
            xd = cv.drawContours(img, [sc], -1, (0, 0, 255), 3)
            # text.append(tess.image_to_string(xd))
            # cv.imshow('Cropped', xd)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
        print(text)
    else:
        final = tess.image_to_string(gray)
        print(final)
 


    mask = np.zeros(gray.shape, np.uint8)
    for s in screenCnt:
        new_image = cv.drawContours(mask, [s], 0, 255, -1, )
        new_image = cv.bitwise_and(img, img, mask=mask)
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

        text.append(tess.image_to_string(Cropped))
        cv.imshow('Cropped', Cropped)
        cv.waitKey(0)
        cv.destroyAllWindows()
    print(text)
    # text = pytesseract.image_to_string(Cropped, config='--psm 11')
    # print("programming_fever's License Plate Recognition\n")
    # print("Detected license plate Number is:", text)
    # img = cv.resize(img, (500, 300))
    # Cropped = cv.resize(Cropped, (400, 200))
    # cv.imshow('car', img)
    # cv.imshow('Cropped', Cropped)
    #
    # cv.waitKey(0)
    # cv.destroyAllWindows()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
