import cv2
import easyocr

# instancia el lector de texto
reader = easyocr.Reader(['en'], gpu=True)

# accede a la cámara web (en este caso, la cámara principal, 0)
cap = cv2.VideoCapture(0)

window_width = 300
window_height = 300

while True:
    # captura el frame de la cámara
    ret, frame = cap.read()

    # cambia el tamaño del frame
    frame = cv2.resize(frame, (window_width, window_height))

    # detecta el texto en el frame
    text_ = reader.readtext(frame)

    threshold = 0.7
    # dibuja los cuadros delimitadores y el texto
    for t_, t in enumerate(text_):
        bbox, text, score = t

        if score > threshold:
            rect1=(int(bbox[0][0]), int(bbox[0][1]))
            rect2=(int(bbox[2][0]), int(bbox[2][1]))
            cv2.rectangle(frame, rect1, rect2, (0, 255, 0), 5)
            cv2.putText(frame, text, rect1, cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

    # muestra el frame con texto detectado
    cv2.imshow('Text Detection', frame)

    # sale del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# libera los recursos
cap.release()
cv2.destroyAllWindows()
