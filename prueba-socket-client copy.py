import conexion,pygame

conn = conexion.ConectionClient()
pygame.init()
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((1024,720), flags)
pygame.display.set_caption("contador")
font1 = pygame.font.SysFont("Arial", 100)

class Button:
    def __init__(self, text, action, bg="yellow"):
        self.font = font1
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.action = action
        self.pressed = False
        self.bg = bg

    def show(self,  x,y):
        self.rect = pygame.Rect(x, y, screen.get_size()[0]/4-10,self.text.get_size()[1]+10)
        if self.pressed:
            pygame.draw.rect(screen, self.bg, self.rect, border_radius=5)
        else:
            pygame.draw.rect(screen, "blue", self.rect, border_radius=5)
        screen.blit(self.text, (x+screen.get_size()[0]/8-self.text.get_size()[0]/2, y))

    def clickdown(self):
        posX,posY = pygame.mouse.get_pos()
        if self.rect.collidepoint(posX,posY) and self.pressed != True:
            self.pressed = True
            self.action()

    def clickup(self):
        self.pressed = False

buttons = [Button("Mandar mensaje", conn.send, bg="blue")]

def draw():
    buttons[0].show(screen.get_size()[0]/2, screen.get_size()[1]/2)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                for button in buttons:
                    button.clickdown()
        if event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                button.clickup()
    draw()
    pygame.display.flip()
