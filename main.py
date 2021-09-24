import pygame, sys, math, os, tracks
pygame.init()
clock = pygame.time.Clock()

class Track():
    def __init__(self, trackName, trackLeaderboard, trackImage, trackTerrain, x, y, trackSections, trackSectors):
        self.name = trackName
        self.leaderboard = trackLeaderboard
        self.image = trackImage
        self.terrain = trackTerrain
        self.spawnPoint = (x, y)
        self.sections = trackSections
        self.sectors = trackSectors

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

class LapTimer():
    def __init__(self):
        self.milliseconds = 0
        self.millisecondsAsString = "000"
        self.seconds = 0
        self.secondsAsString = "00"
        self.minutes = 0
        self.currentLapTime = str(self.minutes)+":"+self.secondsAsString+"."+self.millisecondsAsString
        self.totalLap = str(self.minutes)+self.secondsAsString+self.millisecondsAsString
    def updateTimer(self):
        self.milliseconds += int((1/60)*1000)
        if self.milliseconds > 999:
            self.milliseconds -= 999
            self.seconds += 1
        if self.seconds > 60:
            self.seconds -= 60
            self.minutes += 1
        self.millisecondsAsString = ""
        self.secondsAsString = ""
        numOfZeros = 0
        while len(str(self.milliseconds)) + numOfZeros < 3:
            self.millisecondsAsString = self.millisecondsAsString + "0"
            numOfZeros += 1
        self.millisecondsAsString += str(self.milliseconds)
        if self.seconds < 10:
            self.secondsAsString = self.secondsAsString + "0"
        self.secondsAsString += str(self.seconds)
        self.currentLapTime = str(self.minutes)+":"+self.secondsAsString+"."+self.millisecondsAsString
        self.totalLap = str(self.minutes)+self.secondsAsString+self.millisecondsAsString
    def resetTimer(self):
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        return self.currentLapTime, int(self.totalLap)
    def getCurrentTime(self):
        return self.currentLapTime

class Racecar(pygame.sprite.Sprite):
    def __init__(self, x, y, frontWing, rearWing, camber, toe, gear, brakeBias, rotations=360):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.rotImg   = []
        self.minAngle = (360/rotations)
        for i in range(rotations):
            rotatedImage = pygame.transform.rotozoom(racecarImage, 360-90-(i*self.minAngle), 1)
            self.rotImg.append(rotatedImage)
        self.minAngle = math.radians(self.minAngle)
        self.image = self.rotImg[0]
        self.rect = self.image.get_rect()
        self.heading = 0
        self.speed = 0
        self.x = x
        self.y = y
        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(x, y)
        self.fr = pygame.math.Vector2(x+int(self.rect.width/2), y+int(self.rect.height/2))
        self.fl = pygame.math.Vector2(x+int(self.rect.width/2), y-int(self.rect.height/2))
        self.rr = pygame.math.Vector2(x-int(self.rect.width/2), y+int(self.rect.height/2))
        self.rl = pygame.math.Vector2(x-int(self.rect.width/2), y-int(self.rect.height/2))
        self.rect.center = self.position
        self.frontWing = frontWing
        self.rearWing = rearWing
        self.camber = camber
        self.toe = toe
        self.gear = gear
        self.brakeBias = brakeBias
        self.turnAngle = 0
        self.topSpeed = (8-(self.rearWing*0.1)-(self.frontWing*0.02)+(self.gear*0.1)-(self.camber*0.01)-(self.toe*0.01))
        self.acceleration = (0.1-(self.gear*0.01))
        self.deceleration = (0.3-(self.brakeBias*0.04))
    def turn(self, angle_degrees):
        if self.speed > 0:
            self.heading += math.radians(angle_degrees)
            imageIndex = int(self.heading/self.minAngle) % len(self.rotImg)
            if (self.image != self.rotImg[imageIndex]):
                x,y = self.rect.center
                self.image = self.rotImg[imageIndex]
                self.rect  = self.image.get_rect()
                self.rect.center = (x,y)
    def accelerate(self, modifier):
        if self.speed < self.topSpeed*modifier:
            self.speed += (self.acceleration*modifier)
        else:
            self.speed = self.topSpeed*modifier
    def brake(self, modifier):
        if modifier == 0:
            self.speed = 0
        elif self.speed-self.deceleration > 0:
            self.speed -= self.deceleration
        elif self.speed-self.deceleration < 0 :
            self.speed = 0
    def coast(self, modifier):
        if modifier == 0:
            self.speed = 0
        if self.speed > 0.1:
            self.speed -= 0.01
        if self.speed == 0.1:
            self.speed = 0
    def update(self):
        self.velocity.from_polar((self.speed, math.degrees(self.heading)))
        self.position += self.velocity
        self.fr += self.velocity
        self.fl += self.velocity
        self.rr += self.velocity
        self.rl += self.velocity
        self.rect.center = (round(self.position[0]), round(self.position[1]))
    def getTurnAngle(self, modifier):
        if self.speed <= self.topSpeed/2:
            self.turnAngle = (2+(self.toe*0.1)+(self.camber*0.1)+(self.frontWing*0.1))*modifier
        else:
            self.turnAngle = (2+(self.rearWing*0.2)+(self.frontWing*0.1))*modifier
        return self.turnAngle

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

racecarImage = pygame.image.load(os.path.join('images', 'racecar.png')).convert_alpha()

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
    track1Preview = pygame.image.load(os.path.join('images', 'track1preview.png')).convert_alpha()

    track2Button = pygame.Rect(283, 100, 185, 219)
    track2Preview = pygame.image.load(os.path.join('images', 'track2preview.png')).convert_alpha()

    track3Button = pygame.Rect(540, 100, 185, 219)
    track3Preview = pygame.image.load(os.path.join('images', 'track3preview.png')).convert_alpha()

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
                    mainMenu()
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
                trackImage = pygame.image.load(os.path.join('images', 'track1.png')).convert_alpha()
                trackImage = pygame.transform.scale(trackImage, (3656, 2704))
                trackTerrain = pygame.image.load(os.path.join('images', 'track1terrain.png')).convert_alpha()
                trackTerrain = pygame.transform.scale(trackTerrain, (3656, 2704))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 700, 500, tracks.track1, tracks.track1Sectors)
                inTrackMenu = False
                setupMenu(track)
        else:
            pygame.draw.rect(screen, yellow, track1Button)
            screen.blit(track1Preview, (30,105))
        if track2Button.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, track2Button)
            screen.blit(track2Preview, (288,105))
            if click == True:
                trackName = "track2"
                trackLeaderboard = open("track2leaderboard.txt", "w+")
                trackImage = pygame.image.load(os.path.join('images', 'track2.png')).convert_alpha()
                trackImage = pygame.transform.scale(trackImage, (3656, 2704))
                trackTerrain = pygame.image.load(os.path.join('images', 'track2terrain.png')).convert_alpha()
                trackTerrain = pygame.transform.scale(trackTerrain, (3656, 2704))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 1000, 1000, tracks.track2, tracks.track2Sectors)
                inTrackMenu = False
                setupMenu(track)
        else:
            pygame.draw.rect(screen, yellow, track2Button)
            screen.blit(track2Preview, (288,105))
        if track3Button.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, track3Button)
            screen.blit(track3Preview, (545,105))
            if click == True:
                trackName = "track3"
                trackLeaderboard = open("track3leaderboard.txt", "w+")
                trackImage = pygame.image.load(os.path.join('images', 'track3.png')).convert_alpha()
                trackImage = pygame.transform.scale(trackImage, (3656, 2704))
                trackTerrain = pygame.image.load(os.path.join('images', 'track3terrain.png')).convert_alpha()
                trackTerrain = pygame.transform.scale(trackTerrain, (3656, 2704))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 600, 170, tracks.track3, tracks.track3Sectors)
                inTrackMenu = False
                setupMenu(track)
        else:
            pygame.draw.rect(screen, yellow, track3Button)
            screen.blit(track3Preview, (545,105))

        pygame.display.update()
        clock.tick(60)

def setupMenu(track):
    inSetupMenu = True

    driveButtonRect = pygame.Rect(600, 259, 100, 207)
    driveButton = pygame.image.load(os.path.join('images', 'driveButton.png')).convert_alpha()
    driveButtonSelected = pygame.image.load(os.path.join('images', 'driveButtonSelected.png')).convert_alpha()

    fwImage = pygame.image.load(os.path.join('images', 'frontWingSetup.png')).convert_alpha()
    fwSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    fwSelector = fwSelectorImage.get_rect()
    fwSelector.center = (102, 188)

    rwImage = pygame.image.load(os.path.join('images', 'rearWingSetup.png')).convert_alpha()
    rwSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    rwSelector = rwSelectorImage.get_rect()
    rwSelector.center = (300, 188)

    gbImage = pygame.image.load(os.path.join('images', 'gearRatioSetup.png')).convert_alpha()
    gbSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    gbSelector = gbSelectorImage.get_rect()
    gbSelector.center = (495, 188)

    camberImage = pygame.image.load(os.path.join('images', 'camberSetup.png')).convert_alpha()
    camberSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    camberSelector = camberSelectorImage.get_rect()
    camberSelector.center = (105, 395)

    toeImage = pygame.image.load(os.path.join('images', 'toeSetup.png')).convert_alpha()
    toeSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    toeSelector = toeSelectorImage.get_rect()
    toeSelector.center = (300, 395)

    bbImage = pygame.image.load(os.path.join('images', 'brakeSetup.png')).convert_alpha()
    bbSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    bbSelector = bbSelectorImage.get_rect()
    bbSelector.center = (495, 395)

    click = False
    fwPickUp = False
    rwPickUp = False
    gbPickUp = False
    camberPickUp = False
    toePickUp = False
    bbPickUp = False

    fwSetup = 3
    rwSetup = 3
    gbSetup = 3
    camberSetup = 3
    toeSetup = 3
    bbSetup = 3

    while inSetupMenu:

        screen.fill(blue)
        drawText("Setup Menu", font, black, screen, 20, 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inSetupMenu = False
                    trackMenu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
                    fwPickUp = False
                    rwPickUp = False
                    gbPickUp = False
                    camberPickUp = False
                    toePickUp = False
                    bbPickUp = False
        mx, my = pygame.mouse.get_pos()

        if fwSelector.collidepoint((mx, my)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if click == True:
                fwPickUp = True
        elif rwSelector.collidepoint((mx, my)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if click == True:
                rwPickUp = True
        elif gbSelector.collidepoint((mx, my)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if click == True:
                gbPickUp = True
        elif camberSelector.collidepoint((mx, my)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if click == True:
                camberPickUp = True
        elif toeSelector.collidepoint((mx, my)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if click == True:
                toePickUp = True
        elif bbSelector.collidepoint((mx, my)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if click == True:
                bbPickUp = True
        elif driveButtonRect.collidepoint((mx, my)):
            screen.blit(driveButtonSelected, (600, 259))
            if click == True:
                currentSetup = Setup(fwSetup, rwSetup, gbSetup, camberSetup, toeSetup, bbSetup)
                drive(track, currentSetup)
                inSetupMenu = False
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            screen.blit(driveButton, (600, 259))

        if fwPickUp == True:
            if mx < 28:
                fwSelector.center = (28, 188)
            elif 28 <= mx <= 36:
                fwSetup = 1
                fwSelector.center = (28, 188)
            elif 36 < mx <= 78:
                fwSetup = 2
                fwSelector.center = (65, 188)
            elif 78 < mx <= 121:
                fwSetup = 3
                fwSelector.center = (102, 188)
            elif 121 < mx <= 158:
                fwSetup = 4
                fwSelector.center = (139, 188)
            elif 158 < mx <= 177:
                fwSetup = 5
                fwSelector.center = (177, 188)
            elif mx > 177:
                fwSelector.center = (177, 188)
        elif rwPickUp == True:
            if mx < 224:
                rwSelector.center = (224, 188)
            elif 224 <= mx <= 245:
                rwSetup = 1
                rwSelector.center = (224, 188)
            elif 245 < mx <= 282:
                rwSetup = 2
                rwSelector.center = (263, 188)
            elif 282 < mx <= 319:
                rwSetup = 3
                rwSelector.center = (300, 188)
            elif 319 < mx <= 356:
                rwSetup = 4
                rwSelector.center = (337, 188)
            elif 356 < mx <= 372:
                rwSetup = 5
                rwSelector.center = (372, 188)
            elif mx > 372:
                rwSelector.center = (372, 188)
        elif gbPickUp == True:
            if mx < 419:
                gbSelector.center = (419, 188)
            elif 419 <= mx <= 438:
                gbSetup = 1
                gbSelector.center = (419, 188)
            elif 438 < mx <= 477:
                gbSetup = 2
                gbSelector.center = (458, 188)
            elif 477 < mx <= 514:
                gbSetup = 3
                gbSelector.center = (495, 188)
            elif 514 < mx <= 551:
                gbSetup = 4
                gbSelector.center = (532, 188)
            elif 551 < mx <= 567:
                gbSetup = 5
                gbSelector.center = (567, 188)
            elif mx > 567:
                gbSelector.center = (567, 188)
        if camberPickUp == True:
            if mx < 28:
                camberSelector.center = (28, 395)
            elif 28 <= mx <= 36:
                camberSetup = 1
                camberSelector.center = (28, 395)
            elif 36 < mx <= 78:
                camberSetup = 2
                camberSelector.center = (65, 395)
            elif 78 < mx <= 121:
                camberSetup = 3
                camberSelector.center = (102, 395)
            elif 121 < mx <= 158:
                camberSetup = 4
                camberSelector.center = (139, 395)
            elif 158 < mx <= 177:
                camberSetup = 5
                camberSelector.center = (177, 395)
            elif mx > 177:
                camberSelector.center = (177, 395)
        elif toePickUp == True:
            if mx < 224:
                toeSelector.center = (224, 395)
            elif 224 <= mx <= 245:
                toeSetup = 1
                toeSelector.center = (224, 395)
            elif 245 < mx <= 282:
                toeSetup = 2
                toeSelector.center = (263, 395)
            elif 282 < mx <= 319:
                toeSetup = 3
                toeSelector.center = (300, 395)
            elif 319 < mx <= 356:
                toeSetup = 4
                toeSelector.center = (337, 395)
            elif 356 < mx <= 372:
                toeSetup = 5
                toeSelector.center = (372, 395)
            elif mx > 372:
                toeSelector.center = (372, 395)
        elif bbPickUp == True:
            if mx < 419:
                bbSelector.center = (419, 395)
            elif 419 <= mx <= 438:
                bbSetup = 1
                bbSelector.center = (419, 395)
            elif 438 < mx <= 477:
                bbSetup = 2
                bbSelector.center = (458, 395)
            elif 477 < mx <= 514:
                bbSetup = 3
                bbSelector.center = (495, 395)
            elif 514 < mx <= 551:
                bbSetup = 4
                bbSelector.center = (532, 395)
            elif 551 < mx <= 567:
                bbSetup = 5
                bbSelector.center = (567, 395)
            elif mx > 567:
                bbSelector.center = (567, 395)

        screen.blit(fwImage, (20,50))
        screen.blit(fwSelectorImage, fwSelector.center)

        screen.blit(rwImage, (215,50))
        screen.blit(rwSelectorImage, rwSelector.center)

        screen.blit(gbImage, (410,50))
        screen.blit(gbSelectorImage, gbSelector.center)

        screen.blit(camberImage, (20,257))
        screen.blit(camberSelectorImage, camberSelector.center)

        screen.blit(toeImage, (215,257))
        screen.blit(toeSelectorImage, toeSelector.center)

        screen.blit(bbImage, (410,257))
        screen.blit(bbSelectorImage, bbSelector.center)

        pygame.display.update()
        clock.tick(60)

def getTrackSection(racecar, track):
    colourAtRL = (track.terrain.get_at(((racecar.rect.center[0]+375), (racecar.rect.center[1]+251))))[:3]
    colourAtRR = (track.terrain.get_at(((racecar.rect.center[0]+375), (racecar.rect.center[1]+269))))[:3]
    colourAtFL = (track.terrain.get_at(((racecar.rect.center[0]+405), (racecar.rect.center[1]+251))))[:3]
    colourAtFR = (track.terrain.get_at(((racecar.rect.center[0]+405), (racecar.rect.center[1]+269))))[:3]
    frDone = False
    flDone = False
    rrDone = False
    rlDone = False
    sectionsIn = []
    wheelsOff = 0
    for section in track.sections:
        if flDone == False and colourAtFL == section[1]:
            sectionsIn.append(section)
            flDone = True
        if frDone == False and colourAtFR == section[1]:
            sectionsIn.append(section)
            frDone = True
        if rlDone == False and colourAtRL == section[1]:
            sectionsIn.append(section)
            rlDone = True
        if rrDone == False and colourAtRR == section[1]:
            sectionsIn.append(section)
            rrDone = True

    for section in sectionsIn:
        if section[2][1] == "Wall":
            return section
        if section[3] == False:
            wheelsOff += 1
    if wheelsOff > 2:
        for section in sectionsIn:
            if section[2][1] == "Gravel":
                return section
            elif section[2][1] == "Track":
                return section
            else:
                return section
    else:
        for section in sectionsIn:
            if section[2][1] != "Track":
                sectionsIn.remove(section)
        if sectionsIn[0][0] > sectionsIn[1][0]:
            return sectionsIn[0]
        else:
            return sectionsIn[1]

def getFastestLap(lapToAdd, fastestLap, fastestLapString):
    print(lapToAdd, fastestLap)
    if lapToAdd[2] == True:
        if lapToAdd[3] < fastestLap:
            fastestLap = lapToAdd[3]
            fastestLapString = lapToAdd[1]
    return fastestLap, fastestLapString

#def getTrackSector(currentSector, section, track, lapTimer, currentLap, validLap, laps, fastestLap, fastestLapString):
    #if currentSector == 3 and section[0] == track.sectors[0]:
        #currentSector = 1
        #lapTime, lapTotal = lapTimer.resetTimer()
        #lapToAdd = [currentLap, lapTime, validLap, lapTotal]
        #laps.append(lapToAdd)
        #fastestLap, fastestLapString = getFastestLap(lapToAdd, fastestLap, fastestLapString)
        #validLap = True
        #currentLap += 1
    #elif currentSector == 1 and section[0] == track.sectors[1]:
        #currentSector = 2
    #elif currentSector == 2 and section[0] == track.sectors[2]:
        #currentSector = 3
    #return validLap, currentLap, currentSector

def getValidLap(section, validLap):
    if validLap == False:
        return False
    elif section[3] == False:
        validLap = False
    return validLap

def resetToStart(racecar, track):
    validLap = False
    currentSector = 3
    racecar.speed = 0
    racecar.heading = 0
    racecar.image = racecar.rotImg[0]
    racecar.position = track.spawnPoint

def drive(track, setup):

    racecar = Racecar(track.spawnPoint[0], track.spawnPoint[1], setup.frontWing, setup.rearWing, setup.camber, setup.toe, setup.gear, setup.brakeBias)
    racecarGroup = pygame.sprite.Group()
    racecarGroup.add(racecar)

    lapTimer = LapTimer()
    fastestLap = math.inf
    fastestLapString = ""
    currentLap = 0
    currentSector = 3
    validLap = False
    laps = []

    lapDisplay = pygame.Rect(screenWidth/2-50, 20, 100, 50)

    driving = True

    while driving == True:

        lapTimer.updateTimer()
        currentSection = getTrackSection(racecar, track)
        if currentSector == 3 and currentSection[0] == track.sectors[0]:
            currentSector = 1
            lapTime, lapTotal = lapTimer.resetTimer()
            lapToAdd = [currentLap, lapTime, validLap, lapTotal]
            laps.append(lapToAdd)
            fastestLap, fastestLapString = getFastestLap(lapToAdd, fastestLap, fastestLapString)
            validLap = True
            currentLap += 1
        elif currentSector == 1 and currentSection[0] == track.sectors[1]:
            currentSector = 2
        elif currentSector == 2 and currentSection[0] == track.sectors[2]:
            currentSector = 3
        validLap = getValidLap(currentSection, validLap)

        modifier = currentSection[2][0]

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if keys[pygame.K_ESCAPE] == True:
            driving = False
            saveSession(track, lapTimer)
        if keys[pygame.K_w] == True:
            racecar.accelerate(modifier)
        elif keys[pygame.K_s] == True:
            racecar.brake(modifier)
        else:
            racecar.coast(modifier)
        if keys[pygame.K_a] == True:
            racecar.getTurnAngle(modifier)
            racecar.turn(-racecar.turnAngle)
        elif keys[pygame.K_d] == True:
            racecar.getTurnAngle(modifier)
            racecar.turn(racecar.turnAngle)
        if keys[pygame.K_r] == True:
            currentSector = 3
            resetToStart(racecar, track)

        racecar.update()
        pygame.display.flip()
        screen.blit(track.image, (-racecar.rect.center[0], -racecar.rect.center[1]))
        if validLap == True:
            pygame.draw.rect(screen, black, lapDisplay)
        else:
            pygame.draw.rect(screen, red, lapDisplay)
        timer = font.render(lapTimer.currentLapTime, True, white)
        screen.blit(timer, (lapDisplay.center[0]-40, lapDisplay.center[1]-10))
        screen.blit(racecar.image, (screenWidth/2,screenHeight/2))

        clock.tick(60)

def saveSession(track, lapTimer):

    click = False

    inSaveSession = True

    while inSaveSession:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.fill(blue)
        drawText("Save session or change setup", font, black, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        leaderboardButton = pygame.Rect(screenWidth/2-150, 200, 300, 50)
        setupButton = pygame.Rect(screenWidth/2-150, 300, 300, 50)

        if setupButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, setupButton)
            pygame.draw.rect(screen, yellow, leaderboardButton)
        elif leaderboardButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, leaderboardButton)
            pygame.draw.rect(screen, yellow, setupButton)
        else:
            pygame.draw.rect(screen, yellow, setupButton)
            pygame.draw.rect(screen, yellow, leaderboardButton)

        leaderText = font.render("Save this session", True, (0, 0, 0))
        setupText = font.render("Change setup", True, (0, 0, 0))
        screen.blit(leaderText, (leaderboardButton.center[0]-80, leaderboardButton.center[1]-10))
        screen.blit(setupText, (setupButton.center[0]-70, setupButton.center[1]-10))

        pygame.display.flip()
        clock.tick(60)

mainMenu()
