import cv2
import numpy as np
import SeguimientoManos as sm  
import pygame as pg
from sys import exit
from os import remove
from keyboard import is_pressed
import objetos as obj
from time import sleep

def ActuCentro(cartas):
    global sprites

    sprites.remove(cartas[0])
    sprites.remove(cartas[1])
    sprites.add(cartas[2])

def Cambio(m):
    global turno, mover

    turno = mesa.turno
    mover = m

def Ganador():
    if len(mesa.J1.mazo) == 0:
        return 'J1'
    elif len(mesa.J2.mazo) == 0:
        return 'J2'

    return 'nadie'

def rellenar():
    global sprites,mesa,mazo,click,mover,pubix,pubiy,cubix,cubiy,ganador

    for i in range(3):
        mazo = obj.Mazo(100+(25*i),(h//2)-35)
        sprites.add(mazo)

    mesa = obj.Mesa(mazo,w,h)

    for carta in mesa.J1.mazo:
        sprites.add(carta)

    for carta in mesa.J2.mazo:
        sprites.add(carta)

    sprites.add(mesa.centro)

    pubix, pubiy = 0,0
    cubix, cubiy = 0,0

    click = False
    mover = True
    turno = mesa.turno
    turno.Tiene(mesa.centro)
    ganador = 'nadie'


def vaciar():
    global sprites,vtn
    print("reinicado..")
    sprites.empty()
    rellenar()
    print("juego reiniciado")

def cv2pg(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = np.rot90(img)
    img = cv2.flip(img,0)
    return pg.surfarray.make_surface(img)

w,h = 800,500

pg.init()

vtn = pg.display.set_mode((w,h))
pg.display.set_caption("UNO")

fuente = pg.font.Font(None,50)

cap = cv2.VideoCapture(0)

cuadro = 100
sua = 5
pubix, pubiy = 0,0
cubix, cubiy = 0,0

sprites = pg.sprite.Group()

mesa = None
mazo = None
rellenar()

detector = sm.detectormanos(maxManos=1) 
click = False
mover = True
turno = mesa.turno
turno.Tiene(mesa.centro)
ganador = 'nadie'

print("ya va empezar")
while True:
    ganador = Ganador()
    if ganador != 'nadie':
        break

    rect,frame = cap.read()
    frame = cv2.resize(frame,(w,h))
    frame = cv2.flip(frame,1)

    frame = detector.encontrarmanos(frame) 
    lista, bbox = detector.encontrarposicion(frame) 

    if not mover:
        cartas,centro = mesa.IA()
        if centro: ActuCentro(cartas)
        else: sprites.add(cartas)
        Cambio(True)
        continue
    if len(lista) != 0:
        x1, y1 = lista[8][1:]                  
        x2, y2 = lista[12][1:]   

        dedos = detector.dedosarriba() 
        cv2.rectangle(frame, (0,0), (w, h), (0, 0, 0), 2)  

        if dedos[1]== 1 and dedos[2] == 0:
            if click:
                obj.deseleccion()
                cartas = mesa.deseleccionar()

                if cartas != None: 
                    ActuCentro(cartas)
                    Cambio(False)

                carta=None
                click=False

            x3 = np.interp(x1, (cuadro,w-cuadro), (0,w))
            y3 = np.interp(y1, (cuadro, h-cuadro), (0, h)) 

            cubix = pubix + (x3 - pubix) / sua 
            cubiy = pubiy + (y3 - pubiy) / sua 

            sprites.update(x1,y1)

            cv2.circle(frame, (x1,y1), 10, (0,0,0), cv2.FILLED)
            pubix, pubiy = cubix, cubiy

        if dedos[1] == 1 and dedos[2] == 1:
            longitud, frame, linea = detector.distancia(8,12,frame) 
            #print(longitud)
            if longitud < 50:
                click=True
                if not turno.agarrar:

                    if x1>=mazo.rect.left and x1<=mazo.rect.right and y1>=mazo.rect.top and y1<=mazo.rect.bottom: 
                        print("agarro")
                        carta = mazo.Agarrar()
                        carta = mesa.J1.Agregar(carta)
                        sprites.add(carta)
                        mesa.J1.Ordenar()
                        mesa.CambiarTurno()
                        Cambio(False)
                        continue

                sprites.update(x1,y1,click,(linea[4],linea[5]))
                cv2.circle(frame, (linea[4],linea[5]), 10, (0,255,0), cv2.FILLED)
            pubix, pubiy = cubix, cubiy
            
    fondo = cv2pg(frame)
    vtn.blit(fondo,(0,0))

    sprites.draw(vtn)
    pg.display.update()

    if is_pressed("q"):
        break
    elif is_pressed("r"):
        vaciar()

print(f"Ganador: {ganador}")
sprites.remove(mesa.centro)
sprites.draw(vtn)
pg.display.update()
texto = fuente.render("Ganador: "+ganador,1,(150,150,150))
vtn.blit(texto,(w//2-texto.get_width()//2,h//2-texto.get_height()//2))
pg.display.update()
sleep(2)
remove(r".\fondo.png")
pg.quit()
exit()
