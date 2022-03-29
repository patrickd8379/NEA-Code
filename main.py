import pygame, sys, math, os, tracks, trackMenu
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

currentFastest = [math.inf, ""] #Reset currentFastest
holdLaps = None
holdSectors = None

def drawText(text, font, color, surface, x, y): #Function to draw text
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)

click = False

def mainMenu():
    while True: #While on main menu
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #If the user quits the game
                pygame.quit() #End the program
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit() #End program if esc pressed
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True #Left click on mouse is considered a click

        screen.fill(blue)
        drawText("Main Menu", font, black, screen, 20, 20)

        startButton = pygame.Rect((screenWidth/2)-50, 350, 100, 50)

        mx, my = pygame.mouse.get_pos()

        if startButton.collidepoint((mx, my)): #If the mouse is in contact with the button
            pygame.draw.rect(screen, yellowDark, startButton) #Change the colour of the button
            if click == True:
                trackMenu.runTrackMenu() #Go to the track menu
        else:
            pygame.draw.rect(screen, yellow, startButton)

        drawText("Start", font, black, screen, (screenWidth/2)-25, 365)

        pygame.display.update()
        clock.tick(60)

mainMenu()
