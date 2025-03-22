import engine, connection

def addTicket (self,nomCola):
    if len(self.line) > 0:
        self.line.append(self.line[-1]+1)
        self.tasks.append("0"+nomCola)
def delTicket (self,nomCola):
    if len(self.line) > 0:
        self.line.pop(len(self.line)-1)
        self.tasks.append("1"+nomCola)
def _callTicket (self):
    self.line.pop(0)
    self.called -= 1

def callTicket (self,nomCola):
    if len(self.line) > 0:
        self.called += 1
        timer = self.threading.Timer(5,self._callTicket)
        timer.start()
        self.tasks.append("2"+nomCola)
        pygame.mixer.stop()
        pygame.mixer.Sound.play(self.sound)


if __name__ == '__main__':
    screen = engine.Screen()
    screen.lines.append(engine.Line("C", 0, (0,155,200)))
    screen.lines.append(engine.Line("P", 1, (0,155,0)))
    screen.lines.append(engine.Line("OB", 2, (155,0,0)))
    screen.addLine(addticker)
    screen.start()