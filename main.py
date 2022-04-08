import pygame, sys, math, os, tracks, mainMenu
pygame.init()
clock = pygame.time.Clock()

screenWidth = 750
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))

font = pygame.font.SysFont("C:\Windows\Fonts\Daytona.ttf", 30)

yellow = (255,240,107)
yellowDark = (201,200,89)
red = (255,0,0)
blue = (66,170,245)
black = (0,0,0)
white = (255,255,255)
buttonColour = (255, 255, 0)
buttonColourDark = (230, 230, 0)
green = (67, 240, 36)
greenDark = (53, 189, 28)
purple = (174, 87, 250)

racecarImage = pygame.image.load(os.path.join('images', 'racecar.png')).convert_alpha()

DEFAULTSETUP = [3, 3, 3, 3, 3, 3]

def drawText(text, font, color, surface, x, y): #Function to draw text
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)
