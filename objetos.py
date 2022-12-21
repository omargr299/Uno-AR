from pygame.sprite import Sprite 
from pygame.image import load
from random import choice
from time import sleep

posesion = False

def deseleccion():
    global posesion 

    posesion=False
    
class Carta(Sprite):
    w = 50
    h = 70

    def __init__(self,c,n,x,y) -> None:
        super().__init__()
        self.color = c
        self.numero = n
        self.x = x
        self.y = y
        self.image = load(f".\\img_cartas\\carta_{self.numero}{self.color}.gif")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

    def Mover(self,x,y):
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
        if(x>=self.rect.left and x<=self.rect.right and y>=self.rect.top and y<=self.rect.bottom):
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
    cartas = []
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

    def Agarrar(self):
        carta = choice(self.cartas)
        self.cartas.remove(carta)
        return carta


class Jugador():
    def __init__(self,mazo,x,y) -> None:
        self.mazo = mazo
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

    def Tiene(self,centro):
        for carta in self.mazo:
            if carta.color == centro.color or carta.numero == centro.numero:
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
        self.centro = self.mazo.Agarrar()
        self.centro.Colocar(w//2-25,h//2-35)
        self.turno = self.J1

    def deseleccionar(self):
        margen = 10
        for carta in self.J1.mazo:

            if carta.select:
                if carta.rect.x>=self.centro.rect.left+margen and carta.rect.x<=self.centro.rect.right-margen and carta.rect.y>=self.centro.rect.top-margen and carta.rect.y<=self.centro.rect.bottom+margen:
                    res = self.CambiarCentro(carta,self.J1)
                    if res!=None: return res
                carta.Regresar()
            carta.select = False

    def CambiarCentro(self,carta,jugador):
        if carta==None: return

        carta.Colocar(self.centro.x,self.centro.y)
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
            print("Maquina")
        elif self.turno is self.J2:
            self.turno = self.J1
            print("Humano")
        self.turno.Tiene(self.centro)
        

    def IA(self):
        seleccion = self.J2.IA(self.centro)

        if seleccion==None: 
            seleccion = self.mazo.Agarrar()
            seleccion.Ocultar()
            self.J2.Agregar(seleccion)
            self.J2.Ordenar()
            return [seleccion,False]

        return [self.CambiarCentro(seleccion,self.J2),True]




