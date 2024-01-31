import cv2
import easyocr
import requests
import tkinter as tk
from PIL import Image, ImageTk

# Instancia el lector de texto
reader = easyocr.Reader(['en'], gpu=True)

# Accede a la cámara web (en este caso, la cámara principal, 0)
cap = cv2.VideoCapture(0)

window_width = 400
window_height = 300
total = 0.00

# TODO: Implement cards already read
cards_read = []

# Función para actualizar la interfaz gráfica con el nuevo frame
def update_gui():
    global total
    ret, frame = cap.read()
    frame = cv2.resize(frame, (window_width, window_height))
    text_ = reader.readtext(frame)
    
    threshold = 0.7
    
    for t_, t in enumerate(text_):
        bbox, text, score = t

        if score > threshold:
            rect1=(int(bbox[0][0]), int(bbox[0][1]))
            rect2=(int(bbox[2][0]), int(bbox[2][1]))
            cv2.rectangle(frame, rect1, rect2, (0, 0, 255), 5)
            cv2.putText(frame, text, rect1, cv2.FONT_HERSHEY_COMPLEX, 0.65, (0, 0, 255), 1)
            cv2.putText(frame, 'NOT FOUND', rect2, cv2.FONT_HERSHEY_COMPLEX, 0.65, (0, 0, 255), 1)

            # if text.replace(' ','+').replace(',','').replace('.','') == card_name:
            #     break
            # card_name = text.replace(' ','+').replace(',','').replace('.','')
            card_name = text
            api_url = f"""https://api.scryfall.com/cards/named?exact={card_name}"""
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                price = float(data['prices']['eur'])
                total = total+price
                cv2.rectangle(frame, rect1, rect2, (0, 255, 0), 5)
                cv2.putText(frame, 'FOUND', rect2, cv2.FONT_HERSHEY_COMPLEX, 0.65, (0, 255, 0), 1)

    # Convierte el frame a un formato compatible con Tkinter
    img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    panel.config(image=img)
    panel.image = img
    
    # Actualiza el texto en el área de texto
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"Total Precio: {total}")

    # Programa una llamada recursiva después de 10 ms
    root.after(10, update_gui)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Interfaz de Webcam")

# Panel para mostrar la ventana de la cámara
panel = tk.Label(root)
panel.pack(side="left", padx=10, pady=10)

# Área de texto para mostrar información
text_area = tk.Text(root, height=10, width=30)
text_area.pack(side="right", padx=10, pady=10)

# Inicia la actualización de la interfaz gráfica
update_gui()

# Función para detener la captura y cerrar la interfaz gráfica al presionar 'q'
def quit_app(event):
    if event.char == 'q':
        cap.release()
        cv2.destroyAllWindows()
        root.destroy()

# Enlace la función quit_app al evento de tecla 'q'
root.bind('<Key>', quit_app)

# Inicia el bucle principal de la interfaz gráfica
root.mainloop()
