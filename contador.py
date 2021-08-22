import pygame,sys

from pygame import surface
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((500,500), flags)
pygame.font.init()
font1 = pygame.font.SysFont("Arial", 100)
font2 = pygame.font.SysFont("Arial", 50)
colorBF = 0,200,255

cola = list((1,2,3))

#clases
class Button :
    def __init__(self, text,  pos, action, bg="yellow"):
        self.font = pygame.font.SysFont("Arial", 20)
        self.textRaw = text
        self.text = self.font.render(self.textRaw, 1, pygame.Color("White"))
        self.size = (self.text.get_size()[0]+10,self.text.get_size()[1]+10)
        self.surface = pygame.Surface(self.size)
        # self.x = float(pos[0]-self.size[0]/screen.get_size()[0]*50)
        # self.y = float(pos[1]-self.size[1]/screen.get_size()[1]*50)
        self.x = pos[0]
        self.y = pos[1]
        self.action = action
        self.pressed = False
        self.bg = bg
        self.change(bg)

    def change(self, bg="black"):
        """Change the text when you click"""
        self.surface.fill(bg)
        self.surface.blit(self.text, pygame.Rect(5,5,5,5))
        self.rect = pygame.Rect(self.x/100.0*screen.get_size()[0], self.y/100.0*screen.get_size()[1], self.size[0], self.size[1])

    def show(self):
        if self.pressed:
            self.change(self.bg)
            self.pressed = False
        else:
            self.change()
        screen.blit(self.surface, (self.rect[0] - self.rect[2]/2, self.rect[1] - self.rect[3]/2))

    def click(self):
        self.pressed = False
        posX,posY = pygame.mouse.get_pos()

        if self.rect.collidepoint(posX,posY):
            self.pressed = True
            self.action()

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
    screen.fill((255,255,255))

    pygame.draw.rect(screen, "green", (0,0,screen.get_size()[0],50), border_radius=5)
    render = font1.render(str(len(cola)), 1, "white")
    screen.blit(render, (0,0))

    buttonAdd.show()
    buttonDel.show()
    buttonRes.show()

    render = font1.render(str(cola[0]), 1, "white")
    rectFont = (screen.get_size()[0]/4,35,render.get_size()[0],render.get_size()[1]-30)
    pygame.draw.rect(screen, colorBF, rectFont, border_radius=5)
    screen.blit(render, (screen.get_size()[0]/4,20))
    i = 0
    for n in cola:
        if n == cola[0]:
            continue
        render = font2.render(str(n), 1, "white")
        rectFont = (screen.get_size()[0]/4+15,125+i*50,render.get_size()[0],render.get_size()[1]-10)
        pygame.draw.rect(screen, colorBF, rectFont, border_radius=5)
        screen.blit(render, (screen.get_size()[0]/4+15,120+i*50))
        i += 1

posButtons = 75
buttonAdd = Button("addTicket",(posButtons,10),addTicket)
buttonDel = Button("delTurn",(posButtons,20),delTicket)
buttonRes = Button("resetTicket",(posButtons,30),resetTicket)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                buttonAdd.click()
                buttonDel.click()
                buttonRes.click()
        # if event.type == pygame.MOUSEBUTTONUP:
        #     posX = -1
        #     posY = -1
    draw()
    pygame.display.flip()