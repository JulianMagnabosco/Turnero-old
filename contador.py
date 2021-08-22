import pygame,sys

from pygame import surface
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((500,500), flags)
pygame.font.init()
font1 = pygame.font.SysFont("Arial", 100)
font2 = pygame.font.SysFont("Arial", 50)
colorF = 255,255,255

cola = list((1,2,3))

#clases
class Button :
    def __init__(self, text,  pos, bg="yellow"):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", 20)
        self.textRaw = text
        self.bg = bg
        self.pressed = False
        self.change(bg)

    def change(self, bg="black"):
        """Change the text when you click"""
        self.text = self.font.render(self.textRaw, 1, pygame.Color("White"))
        self.size = (self.text.get_size()[0]+10,self.text.get_size()[1]+10)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, pygame.Rect(5,5,5,5))
        self.rect = pygame.Rect(self.x/100*screen.get_size()[0], self.y/100*screen.get_size()[1], self.size[0], self.size[1])

    def show(self):
        if self.pressed:
            self.change(self.bg)
        else:
            self.change()
        screen.blit(self.surface, (self.rect[0], self.rect[1]))

    def click(self, posX,posY):
        self.pressed = False
        if self.rect.collidepoint(posX,posY):
            self.pressed = True
        self.show()
        return self.pressed

#metodos
def addTicket ():
    cola.append(cola[-1]+1)

def delTicket ():
    if len(cola) > 1:
        cola.pop(0)

def resetTicket ():
    cola.clear()
    cola.append(1)

def draw():
    render = font1.render(str(cola[0]), 1, colorF)
    rectFont = (screen.get_size()[0]/4,35,render.get_size()[0],render.get_size()[1]-30)
    pygame.draw.rect(screen, (0,255,0), rectFont, border_radius=5)
    screen.blit(render, (screen.get_size()[0]/4,20))
    i = 0
    for n in cola:
        if n == cola[0]:
            continue
        render = font2.render(str(n), 1, colorF)
        rectFont = (screen.get_size()[0]/4+15,125+i*50,render.get_size()[0],render.get_size()[1]-10)
        pygame.draw.rect(screen, (0,255,0), rectFont, border_radius=5)
        screen.blit(render, (screen.get_size()[0]/4+15,120+i*50))
        i += 1

posButtons = 90
buttonAdd = Button("addTicket",(20,posButtons))
buttonDel = Button("delTurn",(40,posButtons))
buttonRes = Button("resetTicket",(60,posButtons))
while True:
    posX = -1
    posY = -1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                posX,posY = pygame.mouse.get_pos()
    screen.fill((255,255,255))
    draw()
    pressedAdd = buttonAdd.click(posX,posY)
    pressedDel = buttonDel.click(posX,posY)
    pressedRes = buttonRes.click(posX,posY)
    if pressedAdd:
        addTicket()
    if pressedDel:
        delTicket()
    if pressedRes:
        resetTicket()
    pygame.display.flip()