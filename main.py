from wonderwords import RandomSentence
import pygame
import ctypes
import time
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
height = screensize[1]-60
width = screensize[0]
# font = pygame.font.SysFont("Consolas", 150)
pygame.init()
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
clock = pygame.time.Clock()
BLACK = (0,0,0)



# Show estimated time during test 
# Show words per minute at the end
# Add an end Screen
# add a test history



def sentences(sentencesNo):
    r = RandomSentence()
    sentenceList = []
    sentence = ''
    for i in range(0,sentencesNo):
        sentenceList.append(r.sentence())
        sentenceList.append(" ")
    for i in sentenceList:
        sentence += i
    return sentence


def drawText(text,x,y,size,r,g,b):
    font = pygame.font.SysFont("Consolas", int(size))
    textToDisplay = font.render(str(text), True, [r, g, b])
    screen.blit(textToDisplay, [x,y])

class Letter():
    def __init__(self,No,letter):
        self.No = No
        self.offset = 0
        self.letter = letter
        self.width = screensize[0]/40
        self.y = screensize[1]/2
        self.x = (screensize[0]/40*5)+((self.No*screensize[0]/40)/2)
        self.r = 255
        self.g = 255
        self.b = 255
        self.correctletters = 0
    def create(self):
        drawText(self.letter,self.x,self.y,self.width,self.r,self.g,self.b)
    def colourchange(self):
        if len(typed) > self.No:
            self.r = 100
            self.g = 100
            self.b = 100
        if self.No < len(wronglist):    
            if wronglist[self.No] == "wrong":
                self.r = 150
                self.g = 0
                self.b = 0 

        if len(typed)-1< self.No:
            self.r = 255
            self.g = 255
            self.b = 255

class Game():
    def __init__(self):
        self.starttime = 0
        self.correctletters = 0
        self.end = False
        self.endwpm = 0
        self.endacc = 0
game = Game()


# Letter(1,"L"),Letter(2,"s"),Letter(3,'S')
llist =  []
checklist = [] 
wronglist = []
# to do. add a new letter class to this list for every letter in a generated sentence

def makeList(sentenceNo):
    paragraph = sentences(sentenceNo)

    game.correctletters = 0
    
    for i in range(0,len(paragraph)):        
        llist.append(Letter(i,paragraph[i]))
        checklist.append(paragraph[i])
    checklist.pop()

def endscreen():
    game.end = True
    game.endwpm = ((game.correctletters/len(checklist)*15)/(time.time() - game.starttime))*60
    game.endacc = (game.correctletters/len(wronglist)*100)

caps = False
typed = []

def startTest(sentencesNumber):
    llist.clear()
    checklist.clear()
    typed.clear()
    wronglist.clear()
    
    game.starttime = time.time()
    makeList(sentencesNumber)
    game.end = False

startTest(3)

def MoveLetters(direction):
    for i in llist:
        if direction == 'left':
            i.offset -= 1
        if direction == 'right':
            i.offset += 1
        if direction == 'update':
            i.x = (screensize[0]/40*5)+((i.No*screensize[0]/40)/2)+(i.offset*screensize[0]/80)
            i.y = screensize[1]/2
            i.width = screensize[0]/40


def wordCheck():
    print("worcheck run")
 
    
    game.correctletters = 0

    wronglist.clear()
    for i in range(len(typed)): 
        if (i) <= (len(checklist)):
  
            if typed[i] == checklist[i]:
                wronglist.append("correct")
                game.correctletters += 1
            else:
                wronglist.append("wrong")




def typedletters(letter):
    if letter == "backspace" and len(typed)>0:
        typed.pop()
        MoveLetters('right')
    elif caps == True and len(letter) == 1:
        typed.append(letter.upper())
        MoveLetters('left')
        # letter.x -= 1
    elif len(letter) == 1:
        typed.append(letter)
        MoveLetters('left')
        # letter.x -= 1
    elif letter == "space":
        typed.append(' ')   
        MoveLetters('left')

def letterIdicator():
    drawText("_",screensize[0]/8,screensize[1]/2,screensize[0]/40,255,255,255)

def wordsPerMinute():
    if len(wronglist) < 1:
        game.starttime = time.time()
     
    testTime = (time.time()+0.00001) - game.starttime
    if len(checklist) > 0:
        wpm = ((game.correctletters/len(checklist)*15)/testTime)*60
        drawText(f"WPM{round(wpm,2)}",screensize[1]/2,screensize[0]/40,screensize[0]/40,255,255,255)
    else :
        drawText(f"WPM 0",screensize[1]/2,screensize[0]/40,screensize[0]/40,255,255,255)
    if len(wronglist) > 0:
        accuracy = (game.correctletters/len(wronglist)*100)
        drawText(f"ACC {round(accuracy,2)}",screensize[1]/4,screensize[0]/40,screensize[0]/40,255,255,255)
    else:
        drawText(f"ACC 0",screensize[1]/4,screensize[0]/40,screensize[0]/40,255,255,255)
running = True
while running:
    screensize = pygame.display.get_surface().get_size()
    w, h = pygame.display.get_surface().get_size()
    print(w)
    MoveLetters('update')

    
    if game.end == False:
        if len(wronglist) == len(checklist):
            print('game over')
            endscreen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                print(wronglist)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_TAB:

                    startTest(3)

                if event.key == pygame.K_LSHIFT:
                    caps = True
                key = pygame.key.name(event.key) #.lower()
                typedletters(key)
           
                if (len(wronglist))<=len(checklist):
                    wordCheck()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    caps = False
        screen.fill(BLACK)
        for i in llist:
            i.colourchange()
            i.create()
        letterIdicator() 
        wordsPerMinute()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_TAB:
                    game.end = False                    
                    startTest(3)

        screen.fill(BLACK)
        drawText(f"press [TAB] to try again",screensize[1]/2,screensize[0]/8,screensize[0]/40,255,255,255)
        drawText(f"WPM : {round(game.endwpm,3)}",screensize[1]/2,screensize[0]/4,screensize[0]/40,255,255,255)
        drawText(f"ACC : {round(game.endacc,3)}",screensize[1]/2,screensize[0]/(8/3),screensize[0]/40,255,255,255)
    
    pygame.display.update()
quit()