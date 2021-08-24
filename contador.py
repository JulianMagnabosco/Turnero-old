import pygame,sys

from pygame import surface
import pygame.freetype
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((1024,720), flags)
pygame.font.init()
pygame.freetype.init()
font1 = pygame.font.SysFont("Arial", 100)
font2 = pygame.freetype.SysFont("Segoe UI Emoji", 50)
colorBF = 0,200,255

cola = list((1,2,3))

#clases
class Button:
    def __init__(self, text, action, bg="yellow"):
        self.font = font2
        self.textRaw = text
        self.text = self.font.render(self.textRaw, 1, pygame.Color("White"))
        self.size = (self.text.get_sized_glyph_height()+10,self.text.get_sized_height()+10)
        self.surface = pygame.Surface(self.size)
        self.action = action
        self.pressed = False
        self.bg = bg
        self.change(bg)

    def change(self, bg="black"):
        """Change the text when you click"""
        self.surface.fill(bg)
        self.surface.blit(self.text, pygame.Rect(5,5,5,5))

    def show(self,  x,y):
        self.rect = pygame.Rect(x-  self.size[0]/2, y-  self.size[1]/2, self.size[0], self.size[1])
        if self.pressed:
            self.change(self.bg)
            self.pressed = False
        else:
            self.change()
        screen.blit(self.surface, (x - self.rect[2]/2, y - self.rect[3]/2))

    def click(self):
        self.pressed = False
        posX,posY = pygame.mouse.get_pos()

        if self.rect.collidepoint(posX,posY):
            self.pressed = True
            self.action()

#metodos
def addTicket ():
    cola.append(cola[-1]+1)

def nextTicket ():
    if len(cola) > 1:
        cola.pop(0)
    

def resetTicket ():
    cola.clear()
    cola.append(1)

def draw():
    screen.fill((255,255,255))

    posTop = 120
    pygame.draw.rect(screen, "green", (0,0,screen.get_size()[0],posTop))
    render = font1.render(str(len(cola)), 1, "white")
    screen.blit(render, (screen.get_size()[0] / 2 - render.get_size()[0] / 2,0))

    posButton = posTop
    for button in buttons:
        button.show(screen.get_size()[0] * 0.75, button.size[1]/2 + posButton+5)
        posButton += button.size[1] + 5
    
    render = font1.render(str(cola[0]), 1, "white")
    rectFont = (5, posTop + 5, screen.get_size()[0] / 2 - 5, render.get_size()[1])
    pygame.draw.rect(screen, colorBF, rectFont, border_radius=5)
    screen.blit(render, (screen.get_size()[0] / 4 - render.get_size()[0] / 2, posTop + 5))
    posRender = posTop + render.get_size()[1]+5
    
    for n in cola:
        if n == cola[0]:
            continue
        render = font2.render(str(n), 1, "white")
        rectFont = (5, posRender+5, screen.get_size()[0]/2-5, render.get_size()[1])
        pygame.draw.rect(screen, colorBF, rectFont, border_radius=5)
        screen.blit(render, (screen.get_size()[0] / 4 - render.get_size()[0] / 2,posRender+5))
        posRender = posRender + render.get_size()[1]+5

buttons = {
    Button("asdasd",addTicket),
    Button("Llamar y quitar",nextTicket),
    Button("Resetear todo",resetTicket)
}
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                buttonAdd.click()
                buttonNext.click()
                buttonRes.click()
    draw()
    pygame.display.flip()