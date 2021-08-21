import pygame,sys
screen = pygame.display.set_mode((500,500))
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
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        if self.pressed:
            self.change(self.bg)
        else:
            self.change()
        screen.blit(self.surface, (self.x, self.y))

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

def show():
    # print(cola)
    render = font1.render(str(cola[0]), 1, colorF)
    screen.blit(render, (20,20))
    i = 0
    for n in cola:
        if n == cola[0]:
            continue
        render = font2.render(str(n), 1, colorF)
        screen.blit(render, (20,120+i*50))
        i += 1

posButtons = 450
buttonAdd = Button("addTicket",(100,posButtons))
buttonDel = Button("delTurn",(200,posButtons))
buttonRes = Button("resetTicket",(300,posButtons))
while True:
    posX = -1
    posY = -1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                posX,posY = pygame.mouse.get_pos()
        # if event.type == pygame.MOUSEBUTTONUP:
        #     posX = -1
        #     posY = -1
    screen.fill((0,0,0))
    show()
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