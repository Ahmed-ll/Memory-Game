import pygame
import time
import random

class Node:
    def __init__(self, loc, img):
        self.loc = loc
        self.img = img

# initialize pygame
pygame.init()

# --------------- All Global variables ---------------

tableWidth = 600  
tableHeight = 600 

cardsWidth = 100  
cardsHeight = 120 

userPairs = 0  
AIpairs = 0    

pointsUser = 0
pointsAI = 0

turnUser = True
turnAI = False

gameFinished = False

# -------------- screen setting --------------

white = (255, 255, 255)
grey = (47, 45, 50)

screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Memory Game')
clock = pygame.time.Clock()
screen.fill(grey)

# ---------- Loading images ---------------

a = pygame.image.load('images/a.png')
b = pygame.image.load('images/b.png')
c = pygame.image.load('images/c.png')
d = pygame.image.load('images/d.png')
e = pygame.image.load('images/e.png')
f = pygame.image.load('images/f.png')
g = pygame.image.load('images/g.png')
h = pygame.image.load('images/h.png')

Back = pygame.image.load('images/Back.png')
youWon = pygame.image.load('images/Won.png')
youLost = pygame.image.load('images/Lost.png')

happy = pygame.image.load('images/happy.png')
sad = pygame.image.load('images/sad.png')

turnAIImage = pygame.image.load('images/turnAIImage.png')
turnUserImage = pygame.image.load('images/turnUserImage.png')
screen.blit(turnUserImage, (450, 100))

# ---------------- Arrays an Dictionaries ---------------------

# Array: All images
images_array = [a, b, c, d, e, f, g, h, 
                
                a, b, c, d, e, f, g, h]

# Array: All locations
cardsLocs_array = [(0, 0), (100, 0), (200, 0), (300, 0),
                  (0, 120), (100, 120), (200, 120), (300, 120),
                  (0, 240), (100, 240), (200, 240), (300, 240),
                  (0, 360), (100, 360), (200, 360), (300, 360),
                  ]

# Stores shuffled images as values, and its locations as keys
cardsToPlay = {}

# Memory of AI
AImemory = {}

# Will store the cards selected by the user for each turn
temp2UserCards = {}

# Shuffles arrays of card images and card locations
random.shuffle(images_array)
random.shuffle(cardsLocs_array)

# Store shuffled card images and shuffled card locations in dictionary cardsToPlay.
z = 0
while z < len(cardsLocs_array):
    cardsToPlay.update({cardsLocs_array[z]: images_array[z]})
    z += 1

# Cover all locations with Back image
p = 0
while p < len(images_array):
    screen.blit(Back, cardsLocs_array[p])
    p += 1

# ------------ game Logic ----------------

# All Steps in the Program
def gameLogic():
    global turnAI
    global turnUser
    global gameFinished

    scoreAI(pointsAI)
    scoreUser(pointsUser)

    gameFinished = False

    while not gameFinished:
        noMoreCardsToPlay()
        if turnUser == False and turnAI == False:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] > 0 and mouse[0] < tableWidth and mouse[1] > 0 and mouse[1] < tableHeight:
                    if turnUser == True:
                        pygame.display.update()
                        xyCoorForAll(mouse[0], mouse[1])

            if turnAI == True:
                turnAImethod()
                AIchoosing()

        pygame.display.update()
        clock.tick(60)

# Get mouse pressed position, and set the top left corner cordinates position of the coordinates 
def xyCoorForAll(x2, y2):
    global AImemory

    if x2 > 0 and x2 < tableWidth and y2 > 0 and y2 < tableHeight:
        x = x2
        i = tableWidth

        y = y2
        j = tableHeight

        bo = True
        bo2 = True
        while bo:
            if x < i:
                global xCoordinate
                xCoordinate = i - cardsWidth
            if i <= 0:
                bo = False  
            i -= cardsWidth

        while bo2:
            if y < j:
                global yCoordinate
                yCoordinate = j - cardsHeight
            if j <= 0:
                bo2 = False
            j -= cardsHeight

        flippingCards(xCoordinate, yCoordinate)

# Flip user selected cards, and store that information on AImemory.
def flippingCards(xCoor, yCoor):
    global cardsToPlay
    global AImemory
    
    c = (xCoor, yCoor)
    for pic_location, picture in cardsToPlay.items():
        if c == pic_location:
            screen.blit(picture, c)
            AImemory.update({c: picture})
            temp2UserCards.update({c: picture})

    compareImagesUser(xCoor, yCoor)

# Check if user cards are equal (a pair).
def compareImagesUser(xCoor, yCoor):
    global cardsToPlay
    global pointsUser
    global temp2UserCards
    global userPairs

    pygame.display.update()
    if len(temp2UserCards) == 2:
        if list(temp2UserCards.values())[0] == list(temp2UserCards.values())[1]:

            # add flipped cards to temp dict
            xc = list(temp2UserCards.keys())[0]
            yc = list(temp2UserCards.keys())[1]

            pointsUser += 1

            del cardsToPlay[xc]
            del cardsToPlay[yc]

            pygame.display.update()
            time.sleep(1)

            pygame.draw.rect(screen, grey, (xc[0], xc[1], cardsWidth, cardsHeight))
            pygame.draw.rect(screen, grey, (yc[0], yc[1], cardsWidth, cardsHeight))
            userPairs += 1
            scoreUser(userPairs)

            temp2UserCards = {}

            pygame.display.update()
            time.sleep(1)

            noMoreCardsToPlay()
            turnAImethod()
            AIchoosing()

        else:
            pygame.display.update()
            time.sleep(1)
            screen.blit(Back, list(temp2UserCards.keys())[0])
            screen.blit(Back, list(temp2UserCards.keys())[1])
            temp2UserCards = {}
            pygame.display.update()
            time.sleep(1)
            turnAImethod()
            AIchoosing()

# AI choosing its two cards, an checking if they are a pair.
def AIchoosing():
    global AIpairs
    global cardsToPlay

    if len(cardsToPlay) == 0:
        noMoreCardsToPlay()

    else:

        card1_loc, card1_img = selectCardBasedOnHeuristics(cardsToPlay)

        for card2_loc, card2_img in cardsToPlay.items():
            if card2_img == card1_img and card2_loc != card1_loc:
                screen.blit(card1_img, card1_loc)
                screen.blit(card2_img, card2_loc)
                pygame.display.update()
                pygame.time.wait(1000)
             
                pygame.draw.rect(screen, grey, (card1_loc[0], card1_loc[1], cardsWidth, cardsHeight))
                pygame.draw.rect(screen, grey, (card2_loc[0], card2_loc[1], cardsWidth, cardsHeight))
                AIpairs += 1
                scoreAI(AIpairs)

                del cardsToPlay[card1_loc]
                del cardsToPlay[card2_loc]
                break

        turnUsermethod()

def selectCardBasedOnHeuristics(cardsToPlay):
    for loc, img in cardsToPlay.items():
        if matchesPartialPair(img, cardsToPlay):
            return loc, img

    return random.choice(list(cardsToPlay.items()))

def matchesPartialPair(img, cardsToPlay):
    for loc, revealed_img in AImemory.items():
        if revealed_img == img and loc in cardsToPlay:
            return True
    return False

# Gives the turn to flip two cards to the user
def turnUsermethod():
    screen.blit(turnUserImage, (450, 100))
    pygame.display.update()
    global turnAI
    global turnUser
    turnUser = True
    turnAI = False
    noMoreCardsToPlay()

# Gives the turn to flip two cards to the AI
def turnAImethod():
    screen.blit(turnAIImage, (450, 100))
    pygame.display.update()
    global turnAI
    global turnUser
    turnUser = False
    turnAI = True
    noMoreCardsToPlay()

# Checks if there are no more available cards to flip
def noMoreCardsToPlay():
    if len(cardsToPlay) == 0:

        screen.fill(grey) 
        time.sleep(.5)
        if (userPairs > AIpairs):
            screen.blit(youWon, (0, 0))
            screen.blit(happy, (650, 200))
        else:
            screen.blit(youLost, (0, 0))
            screen.blit(sad, (650, 200))

        pygame.display.update()
        time.sleep(2)
        pygame.quit()

# Displays the score of the User
def scoreUser(scoreUser):
    pygame.draw.rect(screen, grey, (450, 300, 230, 100))
    font = pygame.font.SysFont(None, 40)
    text = font.render("My Pairs: " + str(scoreUser), True, white)
    screen.blit(text, (450, 300))

# Displays the score of the AI
def scoreAI(scoreAI):
    pygame.draw.rect(screen, grey, (450, 400, 200, 100))
    font = pygame.font.SysFont(None, 40)
    text = font.render("AI Pairs: " + str(scoreAI), True, white)
    screen.blit(text, (450, 400))
    
# Calling game_logic to begin the game
gameLogic()