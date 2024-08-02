import sys
from conection_client import ConectionClient
from display import *



address = "localhost"
port = 8000
lines = []
with open('./config.txt') as f:
    lines = f.readlines()
for l in lines:
    startVar = l.find(" = ")
    if startVar >= 1:
        if l[:startVar] == "ADDRESS":
            address = l[startVar+2:].strip()
        if l[:startVar] == "PORT":
            port = int(l[startVar+2:] )

conn = ConectionClient(address,port)
dataRaw = list()

for data in conn.data[1:-1].split(']['):
    value = data.strip('][').split(', ')
    try:
        dataRaw.append([int(x) for x in value])
    except:
        dataRaw.append([])

colaDataC = list(dataRaw[0])
colaDataP = list(dataRaw[1])
colaDataOB = list(dataRaw[2])
tasks = list()

#metodos

buttons = list()
colas = (Cola("C", 0, (0,155,200),colaDataC),
Cola("P", 1, (0,155,0),colaDataP),
Cola("OB", 2, (155,0,0),colaDataOB))

def draw():
    screen.fill((255,255,255))

    pygame.draw.rect(screen, (200,200,200), (0,0,screen.get_size()[0],100))
    
    for c in colas:
        c.show()

while True:
    dataRaw.clear()
    info = conn.send(str(tasks))
    for data in info[1:-1].split(']['):
        value = data.split(', ')
        try:
            dataRaw.append([int(x) for x in value])
        except:
            dataRaw.append([])
    print(dataRaw)
    colaC = list(dataRaw[0])
    colaP = list(dataRaw[1])
    colaOB = list(dataRaw[2])
    tasks.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                for button in buttons:
                    button.clickdown()
        if event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                button.clickup()
    draw()
    pygame.display.flip()