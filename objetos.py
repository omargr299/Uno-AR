from pygame.sprite import Sprite
from pygame import Surface,Rect
from pygame.image import load
from random import choice
from time import sleep

posesion = False

MARGIN = 10

def deseleccion():
    global posesion 

    posesion=False
    
class Carta(Sprite):
    w = 50
    h = 70

    def __init__(self,c,n,x,y) -> None:
        super().__init__()
        self.color:str = c
        self.numero:int = n
        self.x:int = x
        self.y:int = y
        self.image:Surface = load(f".\\img_cartas\\carta_{self.numero}{self.color}.gif")
        self.rect:Rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

    def Mover(self,x,y):
        x1 = self.x - x
        y1 = self.y - y
        x1/=100
        y1/=100
        for _ in range(100):
            self.rect.x += x1
            self.rect.y += y1
        self.rect.x = x
        self.rect.y = y

    def Regresar(self):
        self.Mover(self.x,self.y)

    def Colocar(self,x,y):
        self.x = x
        self.y = y
        self.Mover(x,y)

    def Mostrar(self):
        self.image = load(f".\\img_cartas\\carta_{self.numero}{self.color}.gif")

    def Ocultar(self):
        self.image = load(".\\img_cartas\\carta_rv.gif")

    def Intr(self):
        nueva = CartaIntr(self)
        return nueva

    
    
class CartaIntr(Carta):
    def __init__(self, carta) -> None:
        super().__init__(carta.color, carta.numero, carta.rect.x, carta.rect.y)
        self.select = False

    def update(self,x,y,click=False,punto=(0,0)) -> None:
        global posesion
        if(x>=self.rect.left and x<=self.rect.right and y>=self.rect.top-MARGIN and y<=self.rect.bottom+MARGIN):
            if (click and not posesion) or self.select:
                posesion = True
                self.select = True
                self.Mover(
                             punto[0] - (self.w//2),
                             punto[1] - (self.h//2)
                            )
    def NoIntr(self):
        nueva = Carta(self.color, self.numero, self.rect.x, self.rect.y)
        return nueva

            
class Mazo(Sprite):
    cartas:list[Carta] = []
    permitir = False

    def __init__(self,x,y) -> None:
        super().__init__()
        self.image = load(".\\img_cartas\\carta_rv.gif")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    """ def update(self,x,y,click=False,punto=(0,0)) -> None:
        if(x>=self.rect.left and x<=self.rect.right and y>=self.rect.top and y<=self.rect.bottom):
            if click:
                #if(not self.permitir): return
                self.cartas.pop()
                print(len(self.cartas)) """

    def Llenar(self):
        for color in ['r','b','g','y']:
            for num in range(1,10):
                self.cartas.append( Carta(color,num,0,0) )

    def Repartir(self):
        seleccion = []
        for i in range(7):
            seleccion.append(self.Agarrar())
        return seleccion

    def Agarrar(self) -> Carta:
        carta = choice(self.cartas)
        self.cartas.remove(carta)
        return carta


class Jugador():
    def __init__(self,mazo,x,y) -> None:
        self.mazo:list[Carta] = mazo
        self.x = x
        self.y = y
        self.Ordenar()
        self.agarrar = False

    def Ordenar(self):
        x = self.x - (50*len(self.mazo))//2
        for carta in self.mazo:
            carta.Colocar(x, self.y)
            x+=50

    def Agregar(self,carta):
        self.mazo.append(carta)
        self.Ordenar()

    def Tiene(self,centro:Carta):
        for carta in self.mazo:
            if carta.color == centro.color or carta.numero == centro.numero:
                print(carta.color, carta.numero, centro.color, centro.numero)
                self.agarrar = True
                return
        
        self.agarrar = False

class Humano(Jugador):
    def __init__(self, mazo,x,y) -> None:
        self.mazo = []

        for carta in mazo:
            self.mazo.append( CartaIntr(carta) )

        super().__init__(self.mazo,x,y)

    def Agregar(self, carta: Carta):
        carta = carta.Intr()
        super().Agregar(carta)
        print(f"Humano cartas: {len(self.mazo)}")
        return carta


class Maquina(Jugador):
    def __init__(self, mazo,x,y) -> None:
        super().__init__(mazo,x,y)
        
        for carta in self.mazo:
            carta.image = load(".\\img_cartas\\carta_rv.gif")
    
    def IA(self, centro):
        for carta in self.mazo:
            if carta.color == centro.color or carta.color == centro.color:
                return carta

class Mesa():
    def __init__(self,mazo: Mazo,w: int,h: int) -> None:
        self.mazo = mazo
        self.mazo.Llenar()
        self.J1 = Humano(self.mazo.Repartir(), w//2, h-100)
        self.J2 = Maquina(self.mazo.Repartir(), w//2, 50)
        self.centro:Carta = self.mazo.Agarrar()
        self.centro.Colocar(w//2-25,h//2-35)
        self.turno = self.J1
        self.turno_text = "Tu turno"
        self.tunro_color = (0,255,0)

    def deseleccionar(self):
        
        for carta in self.J1.mazo:

            if carta.select:
                if carta.rect.x>=self.centro.rect.left-MARGIN and carta.rect.x<=self.centro.rect.right+MARGIN and carta.rect.y>=self.centro.rect.top-MARGIN and carta.rect.y<=self.centro.rect.bottom+MARGIN:
                    if carta.color==self.centro.color or carta.numero==self.centro.numero: 
                        res = self.CambiarCentro(carta,self.J1)
                        if res!=None: return res
                carta.Regresar()
            carta.select = False

    def CambiarCentro(self,carta:Carta,jugador:Jugador):
        if carta==None: return

        carta.Colocar(self.centro.x,self.centro.y)
        print(carta.x,carta.y)
        ant = self.centro
        self.centro = carta.NoIntr() if type(carta) == CartaIntr else carta
        self.centro.Mostrar()
        jugador.mazo.remove(carta)
        
        jugador.Ordenar()
        self.CambiarTurno()

        return [ant,carta,self.centro]

    def CambiarTurno(self):
        if self.turno is self.J1:
            self.turno = self.J2
            self.turno_text = "Turno de la maquina"
            self.tunro_color = (255,0,0)
            print("Maquina")
        elif self.turno is self.J2:
            self.turno = self.J1
            self.turno_text = "Tu turno"
            self.tunro_color = (0,255,0)
            print("Humano")
        self.turno.Tiene(self.centro)
        

    def IA(self):
        seleccion = self.J2.IA(self.centro)
        sleep(2)
        if seleccion==None: 
            self.CambiarTurno()
            print("IA agarro")
            seleccion = self.mazo.Agarrar()
            seleccion.Ocultar()
            self.J2.Agregar(seleccion)
            self.J2.Ordenar()
            return [seleccion,False]

        print("IA puso una carta")
        return [self.CambiarCentro(seleccion,self.J2),True]




