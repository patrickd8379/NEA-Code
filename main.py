import pygame, sys, math, os, tracks
pygame.init()
clock = pygame.time.Clock()

class Track():
    def __init__(self, trackName, trackLeaderboard, trackImage, trackTerrain):
        self.trackName = trackName
        self.trackLeaderboard = trackLeaderboard
        self.trackImage = trackImage
        self.trackTerrain = trackTerrain

    def getTrackLeaderboard():
        return self.trackLeaderboard

class Setup():
    def __init__(self, frontWing, rearWing, camber, toe, gear, brake):
        self.frontWing = frontWing #1-5
        self.rearWing = rearWing #1-5
        self.camber = camber #1-5
        self.toe = toe #1-5
        self.gear = gear #1-5
        self.brakeBias = brake #1-5

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

racecarImage = pygame.image.load(os.path.join('images', 'racecar.png'))

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

        if startButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, startButton)
            if click == True:
                trackMenu()
        else:
            pygame.draw.rect(screen, yellow, startButton)

        drawText("Start", font, black, screen, (screenWidth/2)-25, 365)

        pygame.display.update()
        clock.tick(60)

def trackMenu():
    inTrackMenu = True

    track1Button = pygame.Rect(25, 100, 185, 219)
    track1Preview = pygame.image.load(os.path.join('images', 'track1preview.png'))

    track2Button = pygame.Rect(283, 100, 185, 219)
    track2Preview = pygame.image.load(os.path.join('images', 'track2preview.png'))

    track3Button = pygame.Rect(540, 100, 185, 219)
    track3Preview = pygame.image.load(os.path.join('images', 'track3preview.png'))

    while inTrackMenu:
        screen.fill(blue)
        drawText("Track Menu", font, black, screen, 20, 20)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inTrackMenu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()

        if track1Button.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, track1Button)
            screen.blit(track1Preview, (30,105))
            if click == True:
                trackName = "track1"
                trackLeaderboard = open("track1leaderboard.txt", "w+")
                trackImage = pygame.image.load(os.path.join('images', 'track1.png'))
                trackTerrain = pygame.image.load(os.path.join('images', 'track1terrain.png'))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain)
                setupMenu()
        else:
            pygame.draw.rect(screen, yellow, track1Button)
            screen.blit(track1Preview, (30,105))
        if track2Button.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, track2Button)
            screen.blit(track2Preview, (288,105))
            if click == True:
                trackName = "track2"
                trackLeaderboard = open("track2leaderboard.txt", "w+")
                trackImage = pygame.image.load(os.path.join('images', 'track2.png'))
                trackTerrain = pygame.image.load(os.path.join('images', 'track2terrain.png'))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain)
                setupMenu()
        else:
            pygame.draw.rect(screen, yellow, track2Button)
            screen.blit(track2Preview, (288,105))
        if track3Button.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, track3Button)
            screen.blit(track3Preview, (545,105))
            if click == True:
                trackName = "track3"
                trackLeaderboard = open("track3leaderboard.txt", "w+")
                trackImage = pygame.image.load(os.path.join('images', 'track3.png'))
                trackTerrain = pygame.image.load(os.path.join('images', 'track3terrain.png'))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain)
                setupMenu()
        else:
            pygame.draw.rect(screen, yellow, track3Button)
            screen.blit(track3Preview, (545,105))

        pygame.display.update()
        clock.tick(60)

def setupMenu():
    inSetupMenu = True

    fwImage = pygame.image.load(os.path.join('images', 'frontWingSetup.png'))
    fwSelectorImage = pygame.image.load(os.path.join('images', 'selector.png'))
    fwSelector = fwSelectorImage.get_rect()
    fwSelector.center = (102, 188)

    rwImage = pygame.image.load(os.path.join('images', 'rearWingSetup.png'))
    rwSelectorImage = pygame.image.load(os.path.join('images', 'selector.png'))
    rwSelector = rwSelectorImage.get_rect()
    rwSelector.center = (303, 193)

    gbSelectorImage = pygame.image.load(os.path.join('images', 'selector.png'))
    gbSelector = gbSelectorImage.get_rect()
    gbSelector.center = (498, 193)

    camberSelectorImage = pygame.image.load(os.path.join('images', 'selector.png'))
    camberSelector = camberSelectorImage.get_rect()
    camberSelector.center = (107, 400)

    toeSelectorImage = pygame.image.load(os.path.join('images', 'selector.png'))
    toeSelector = toeSelectorImage.get_rect()
    toeSelector.center = (302, 400)

    bbSelectorImage = pygame.image.load(os.path.join('images', 'selector.png'))
    bbSelector = bbSelectorImage.get_rect()
    bbSelector.center = (497, 400)

    while inSetupMenu:
        screen.fill(blue)
        drawText("Setup Menu", font, black, screen, 20, 20)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inSetupMenu = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

        mx, my = pygame.mouse.get_pos()

        #MAKE IT DETECT WHEN HOVERING OVER A SELECTOR AND CHANGE THE CURSOR TO THE HAND
        #LET THE USER MOVE THE SELECTOR TO SPECIFIC POINTS ON THE LINE

        screen.blit(fwImage, (20,50))
        screen.blit(fwSelectorImage, fwSelector.center)

        screen.blit(rwImage, (215,50))
        screen.blit(rwSelectorImage, rwSelector)

        screen.blit(fwImage, (410,50))
        screen.blit(gbSelectorImage, gbSelector)

        screen.blit(fwImage, (20,257))
        screen.blit(camberSelectorImage, camberSelector)

        screen.blit(fwImage, (215,257))
        screen.blit(toeSelectorImage, toeSelector)

        screen.blit(fwImage, (410,257))
        screen.blit(bbSelectorImage, bbSelector)

        pygame.display.update()
        clock.tick(60)

mainMenu()
