import cv2
import numpy as np
import tkinter as tk
import threading

ventana = "Paint xD"
lienzo = 255 * np.ones((500, 500, 3), dtype="uint8")
trazos = []
rectangle_color = (0, 0, 0)
flag = False
forma = 'rectangulo'
puntos = []
tamano_borrador = 20  # Tamaño del borrador
grosor = 2  # Grosor del lápiz

def event_handler(event, x, y, flags, param):
    global x1, y1, x2, y2, lienzo, flag, forma, puntos
    if event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y
        flag = True
        if forma == 'lapiz' or forma == 'borrador':
            puntos.append((x, y))

    if event == cv2.EVENT_MOUSEMOVE:
        if flag:
            x2, y2 = x, y
            lienzo = 255 * np.ones((500, 500, 3), dtype="uint8")
            for rect in trazos:  # Dibuja todas las formas guardadas
                if rect[2] == 'rectangulo':
                    cv2.rectangle(lienzo, rect[0], rect[1], rectangle_color, thickness=grosor)
                elif rect[2] == 'circulo':
                    cv2.circle(lienzo, rect[0], int(((rect[0][0]-rect[1][0])**2 + (rect[0][1]-rect[1][1])**2)**0.5), rectangle_color, thickness=grosor)
                elif rect[2] == 'linea':
                    cv2.line(lienzo, rect[0], rect[1], rectangle_color, thickness=grosor)
                elif rect[2] == 'borrador' or rect[2] == 'lapiz':
                    for i in range(len(rect[0])-1):
                        color = rectangle_color if rect[2] == 'lapiz' else (255, 255, 255)
                        grosor_actual = grosor if rect[2] == 'lapiz' else tamano_borrador
                        cv2.line(lienzo, rect[0][i], rect[0][i+1], color, grosor_actual)
            if forma == 'rectangulo':
                cv2.rectangle(lienzo, (x1, y1), (x2, y2), rectangle_color, thickness=grosor)  # Dibuja la forma actual
            elif forma == 'circulo':
                cv2.circle(lienzo, (x1, y1), int(((x1-x2)**2 + (y1-y2)**2)**0.5), rectangle_color, thickness=grosor)
            elif forma == 'linea':
                cv2.line(lienzo, (x1, y1), (x2, y2), rectangle_color, thickness=grosor)
            elif forma == 'borrador' or forma == 'lapiz':
                puntos.append((x, y))
                for i in range(len(puntos) - 1):
                    color = rectangle_color if forma == 'lapiz' else (255, 255, 255)
                    grosor_actual = grosor if forma == 'lapiz' else tamano_borrador
                    cv2.line(lienzo, puntos[i], puntos[i + 1], color, grosor_actual)

    if event == cv2.EVENT_LBUTTONUP:
        x2, y2 = x, y
        if forma != 'lapiz' and forma != 'borrador':
            trazos.append(((x1, y1), (x2, y2), forma))  # Guarda la forma
        elif forma == 'lapiz' or forma == 'borrador':
            trazos.append((puntos.copy(), None, forma))
            puntos = []
        flag = False

def seleccionar_forma(forma_seleccionada):
    global forma, puntos
    forma = forma_seleccionada
    if forma == 'lapiz' or forma == 'borrador':
        puntos = []

def abrir_ventana():
    cv2.namedWindow(ventana)
    cv2.setMouseCallback(ventana, event_handler)

    bandera = True

    while bandera:
        cv2.imshow(ventana, lienzo)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cv2.destroyAllWindows()

root = tk.Tk()
boton_rectangulo = tk.Button(root, text="Rectangulo", command=lambda: seleccionar_forma('rectangulo'))
boton_circulo = tk.Button(root, text="Circulo", command=lambda: seleccionar_forma('circulo'))
boton_linea = tk.Button(root, text="Linea", command=lambda: seleccionar_forma('linea'))
boton_lapiz = tk.Button(root, text="Lapiz", command=lambda: seleccionar_forma('lapiz'))
boton_borrador = tk.Button(root, text="Borrador", command=lambda: seleccionar_forma('borrador'))
boton_abrir = tk.Button(root, text="Abrir Paint", command=lambda: threading.Thread(target=abrir_ventana).start())
boton_rectangulo.pack()
boton_circulo.pack()
boton_linea.pack()
boton_lapiz.pack()
boton_borrador.pack()
boton_abrir.pack()
root.mainloop()





