import cv2
import numpy as np
import pygame as pg
import pygame.camera as camera
from keyboard import is_pressed

def pg2cv():
    pass

def cv2pg(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = np.rot90(img)
    return pg.surfarray.make_surface(img)

pg.init
camera.init()

w,h = 500,500
win = pg.display.set_mode((w,h))
webcam = camera.list_cameras()[0]
camara =camera.Camera(webcam)
camara.start()

#cap = cv2.VideoCapture(0)
loop = True
while loop:
    #ret,frame = cap.read()
    #win.blit(cv2pg(frame),(0,0))
    win.blit(camara.get_image(),(0,0))
    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            loop = False
            break
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                loop = False
                break
            
pg.display.quit()
camara.stop()