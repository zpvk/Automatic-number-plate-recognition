def npr(image_path):
    import cv2 as cv
    import imutils
    import numpy as np
    import pytesseract as tess

    tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # image read and resize
    img = cv.imread(image_path, cv.IMREAD_COLOR) 
    img = cv.resize(img, (400, 200))

    # 
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
        for sc in screenCnt:
            xd = cv.drawContours(img, [sc], -1, (0, 0, 255), 3)
    else:
        print("No Results")
 


    mask = np.zeros(gray.shape, np.uint8)
    for s in screenCnt:
        new_image = cv.drawContours(mask, [s], 0, 255, -1, )
        new_image = cv.bitwise_and(img, img, mask=mask)
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

        fine = tess.image_to_string(Cropped)
        text.append(fine.replace('\x0c','')) # clean output
        cv.imshow('Cropped', Cropped)
        cv.waitKey(0)
        cv.destroyAllWindows()
    if len(text) == 0 or text == '' or text[0]=='':
        print("Sory Can't Identify number plate!!!")
    else:
        print("Number plate should be >>",text)


if __name__ == '__main__':
    image_path = str(input("Enter image parth : "))
    npr(image_path)
