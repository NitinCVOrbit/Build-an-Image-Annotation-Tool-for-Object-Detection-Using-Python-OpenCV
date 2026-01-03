import cv2

IMAGE_PATH = "images/01.jpg"
LABEL_PATH = "labels/01.jpglabel.txt"

img = cv2.imread(IMAGE_PATH)
img = cv2.resize(img, (720,480))

with open(LABEL_PATH,'r') as file:
    for line in file:
        box = line.strip().split()
        cls_id, x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.putText(img, f'{cls_id}', (x1,y1-5), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,0,255), 2)

cv2.imshow('Labelled_image',img)
cv2.imwrite('output_02.png',img)
cv2.waitKey(0)