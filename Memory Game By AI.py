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

AI = True
AIpairs = 0  
pointsAI = 0

gameFinished = False

# -------------- screen setting --------------

white = (255, 255, 255)
grey = (45, 45, 50)

screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Memory Game By AI')
screen.fill(grey)

# ---------- Loading images ---------------

h = pygame.image.load('images_AI/h.png')
i = pygame.image.load('images_AI/i.png')
j = pygame.image.load('images_AI/j.png')
k = pygame.image.load('images_AI/k.png')
l = pygame.image.load('images_AI/l.png')
m = pygame.image.load('images_AI/m.png')
n = pygame.image.load('images_AI/n.png')
c = pygame.image.load('images_AI/c.png')

Back = pygame.image.load('images_AI/Back.png')
Won = pygame.image.load('images_AI/Won.png')

imageAI = pygame.image.load('images_AI/AI.png')
happy = pygame.image.load('images_AI/happy.png')

# ---------------- Arrays an Dictionaries ---------------------

# Array: All images
images_array = [ h, i, j, k, l, m, n, c , h, i, j, k, l, m, n, c]

# Array: All locations
cardsLocs_array = [(0, 0), (100, 0), (200, 0), (300, 0),
                  (0, 120), (100, 120), (200, 120), (300, 120),
                  (0, 240), (100, 240), (200, 240), (300, 240),
                  (0, 360), (100, 360), (200, 360), (300, 360),
                ]

# Stores images as values, and its locations as keys
cardsToPlay = {}

AImemory = {}

# Shuffles arrays of images and locations
random.shuffle(images_array)
random.shuffle(cardsLocs_array)

# Store shuffled images and its shuffled locations in dictionary cardsToPlay.
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
    scoreAI(pointsAI)

    while not gameFinished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        noMoreCardsToPlay()
        AIchoosing()

# AI choosing its two cards, an checking if they are a pair.
def AIchoosing():
    global AIpairs
    global cardsToPlay

    screen.blit(imageAI, (450, 100))
    pygame.display.update()

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

def selectCardBasedOnHeuristics(cardsToPlay):
    for loc, img in cardsToPlay.items():
        # Check if the card is adjacent to a known pair
        if isAdjacentToKnownPair(loc, cardsToPlay):
            return loc, img

        # Check if the card matches a partially revealed pair
        if matchesPartialPair(img, cardsToPlay):
            return loc, img

    # If no heuristic applies, randomly select a card
    return random.choice(list(cardsToPlay.items()))

def isAdjacentToKnownPair(loc, cardsToPlay):
    x, y = loc
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    
    for neighbor_loc in neighbors:
        if neighbor_loc in cardsToPlay:
            if cardsToPlay[neighbor_loc] not in AImemory.values():
                return True
    return False

def matchesPartialPair(img, cardsToPlay):
    for loc, revealed_img in AImemory.items():
        if revealed_img == img and loc in cardsToPlay:
            return True
    return False

# Checks if there are no more available cards to flip
def noMoreCardsToPlay():
    if len(cardsToPlay) == 0:
        time.sleep(.75)

        screen.blit(Won, (0, 0))
        screen.blit(happy, (650, 200))
        pygame.display.update()
        
        time.sleep(2)
        pygame.quit()

# Displays the score of the AI
def scoreAI(scoreAI):
    pygame.draw.rect(screen, grey, (450, 300, 230, 100))
    font = pygame.font.SysFont(None, 40)
    text = font.render("AI Pairs: " + str(scoreAI), True, white)
    screen.blit(text, (450, 300))

# Calling game_logic to begin the game
gameLogic()