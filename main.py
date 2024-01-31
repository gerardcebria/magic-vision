import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np

image_path = '/Users/gerardcebria/Desktop/MagicVision/ImageFolder/ltc/1c7ac04c-8510-468b-aa6f-f249bde9ff87.jpg'

img = cv2.imread(image_path)

# instance text detector
reader = easyocr.Reader(['en'], gpu=False)

# detect text on image
text_ = reader.readtext(img)

threshold = 0.7
# draw bbox and text
for t_, t in enumerate(text_):
    print(t)

    bbox, text, score = t

    if score > threshold:
        rect1=(int(bbox[0][0]), int(bbox[0][1]))
        rect2=(int(bbox[2][0]), int(bbox[2][1]))
        cv2.rectangle(img, rect1, rect2, (0, 255, 0), 5)
        cv2.putText(img, text, rect1, cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.imshow(img)
plt.show()