import cv2
import easyocr
import requests
import matplotlib.pyplot as plt
import numpy as np

image_path = '/Users/gerardcebria/Desktop/MagicVision/ImageFolder/ltc/00f40514-d37d-423f-aa0c-1875300f43a8.jpg'

img = cv2.imread(image_path)

# instance text detector
reader = easyocr.Reader(['en'], gpu=False)

# detect text on image
text_ = reader.readtext(img)

threshold = 0.2
# draw bbox and text

print(text_[0])
text_ = [text_[0]]
for t_, t in enumerate(text_):
    # print(t)

    bbox, text, score = t

    if score > threshold:
        rect1=(int(bbox[0][0]), int(bbox[0][1]))
        rect2=(int(bbox[2][0]), int(bbox[2][1]))
        cv2.rectangle(img, rect1, rect2, (255, 0, 0), 5)
        cv2.putText(img, text, rect1, cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

        card_name = text
        # card_name = text.replace(' ','+').replace(',','').replace('.','')
        api_url = f"""https://api.scryfall.com/cards/named?exact={card_name}"""
        print(api_url)
        response = requests.get(api_url)
        if response.status_code == 200:
            cv2.rectangle(img, rect1, rect2, (0, 255, 0), 5)
        print(response.json())

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.imshow(img)
plt.show()