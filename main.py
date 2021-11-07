import pygame, sys, math, os, tracks
pygame.init()
clock = pygame.time.Clock()

class Track(): #Properties of the track
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

class LapTimer(): #The timer which is displayed during gameplay
    def __init__(self):
        self.milliseconds = 0
        self.millisecondsAsString = "000"
        self.seconds = 0
        self.secondsAsString = "00"
        self.minutes = 0
        self.currentLapTime = str(self.minutes)+":"+self.secondsAsString+"."+self.millisecondsAsString #The laptime that will be displayed in gameplay
        self.totalLap = str(self.minutes)+self.secondsAsString+self.millisecondsAsString #A numerical value for the laptime
    def updateTimer(self): #Increment the timer and update the totalLap
        self.milliseconds += int((1/60)*1000)
        if self.milliseconds > 999:
            self.milliseconds -= 999
            self.seconds += 1
        if self.seconds > 59:
            self.seconds = 0
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
    def resetTimer(self): #Reset the timer and return the lap
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        return self.currentLapTime, int(self.totalLap)
    def getCurrentTime(self): #Show the current time
        return self.currentLapTime

class Racecar(pygame.sprite.Sprite): #The properties and functions of the car
    def __init__(self, x, y, frontWing, rearWing, gear, camber, toe, brakeBias, rotations=360):
        pygame.sprite.Sprite.__init__(self)
        self.rotImg   = []
        self.minAngle = (360/rotations) #The smallest angle and the amount of degrees the car image can be turned by at a time
        for i in range(rotations):
            rotatedImage = pygame.transform.rotozoom(racecarImage, 360-90-(i*self.minAngle), 1) #Creates a rotated image
            self.rotImg.append(rotatedImage) #Adds the image to the list of rotated images
        self.minAngle = math.radians(self.minAngle) #Converts minAngle to radians for car movement
        self.image = self.rotImg[0]
        self.rect = self.image.get_rect()
        self.heading = 0
        self.speed = 0
        self.x = x
        self.y = y
        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(x, y)
        self.fr = pygame.math.Vector2(int(x+self.rect.width/2), int(y+self.rect.height/2)) #Corners of the car
        self.fl = pygame.math.Vector2(int(x+self.rect.width/2), int(y-self.rect.height/2))
        self.rr = pygame.math.Vector2(int(x-self.rect.width/2), int(y+self.rect.height/2))
        self.rl = pygame.math.Vector2(int(x-self.rect.width/2), int(y-self.rect.height/2))
        self.rect.center = self.position
        self.frontWing = frontWing
        self.rearWing = rearWing
        self.camber = camber
        self.toe = toe
        self.gear = gear
        self.brakeBias = brakeBias
        self.turnAngle = 0
        self.topSpeed = (8.5-(self.rearWing*0.2)-(self.frontWing*0.02)+(self.gear*0.2)-(self.camber*0.01)-(self.toe*0.01)) #Top speed affected by setup choices
        self.acceleration = (0.1-(self.gear*0.01)) #Acceleration affected by gearing choice
        self.deceleration = (0.3-(self.brakeBias*0.05)) #Deceleration affected by brake bias
    def accelerate(self, modifier): #Increase the speed of the car
        if self.speed < self.topSpeed*modifier: #Check if the car can go any faster on this terrain
            self.speed += (self.acceleration*modifier)
        else:
            self.speed = self.topSpeed*modifier
    def brake(self, modifier): #Decrease the speed of the car
        if modifier == 0:
            self.speed = 0
        elif self.speed-self.deceleration > 0:
            self.speed -= self.deceleration
        elif self.speed-self.deceleration < 0 :
            self.speed = 0
    def coast(self, modifier): #Slowly decrease the speed of the car
        if modifier == 0:
            self.speed = 0
        if self.speed > 0.1:
            self.speed -= 0.01
        if self.speed == 0.1:
            self.speed = 0
    def getTurnAngle(self, modifier): #How quickly the car turns
        if abs(self.speed) <= self.topSpeed/2: #If below or at half of top speed
            self.turnAngle = (2+(self.toe*0.1)+(self.camber*0.1)+(self.frontWing*0.1)+(self.rearWing*0.05))*modifier
        else: #If above half of top speed
            self.turnAngle = (2+(self.rearWing*0.2)+(self.frontWing*0.1)+(self.toe*0.05)+(self.camber*0.05))*modifier
        return self.turnAngle
    def turn(self, angle_degrees): #Change the way the car is pointing
        if abs(self.speed) > 0:
            self.heading += math.radians(angle_degrees) #Change the direction the car is facing
            imageIndex = int(self.heading/self.minAngle) % len(self.rotImg) #Get the rotated image corresponding to the heading
            if (self.image != self.rotImg[imageIndex]):
                x,y = self.rect.center
                self.image = self.rotImg[imageIndex] #Change the image to the one facing the correct way
                self.rect  = self.image.get_rect() #Reset the rect of the car
                self.rect.center = (x,y) #Position the car is the place it was before
    def reverse(self, modifier): #Move backwards
        if abs(self.speed) < 3*modifier: #Maximum reverse speed is 3 times the modifier for the terrain
            self.speed -= (self.acceleration*modifier)
        else:
            self.speed = -3*modifier
    def update(self): #Move the car based on its speed and heading
        self.velocity.from_polar((self.speed, math.degrees(self.heading))) #Get the change in position based on the speed and direction
        self.position += self.velocity
        self.fr += self.velocity
        self.fl += self.velocity
        self.rr += self.velocity
        self.rl += self.velocity
        self.rect.center = (round(self.position[0]), round(self.position[1]))

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

defaultSetup = [3, 3, 3, 3, 3, 3]

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
                trackMenu() #Go to the track menu
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
            if click == True: #Track 1 is selected and loaded
                trackName = "track1"
                trackLeaderboard = "track1leaderboard.txt"
                trackImage = pygame.image.load(os.path.join('images', 'track1.png')).convert_alpha()
                trackImage = pygame.transform.scale(trackImage, (3656, 2704))
                trackTerrain = pygame.image.load(os.path.join('images', 'track1terrain.png')).convert_alpha()
                trackTerrain = pygame.transform.scale(trackTerrain, (3656, 2704))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 1000, 1000, tracks.track1, tracks.track1Sectors)
                inTrackMenu = False
                setupMenu(track, defaultSetup) #Go to the setup menu with the track that has been opened
        else:
            pygame.draw.rect(screen, yellow, track1Button)
            screen.blit(track1Preview, (30,105))
        if track2Button.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, track2Button)
            screen.blit(track2Preview, (288,105))
            if click == True: #Track 2 is selected and loaded
                trackName = "track2"
                trackLeaderboard = "track2leaderboard.txt"
                trackImage = pygame.image.load(os.path.join('images', 'track2.png')).convert_alpha()
                trackImage = pygame.transform.scale(trackImage, (4570, 3380))
                trackTerrain = pygame.image.load(os.path.join('images', 'track2terrain.png')).convert_alpha()
                trackTerrain = pygame.transform.scale(trackTerrain, (4570, 3380))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 1000, 200, tracks.track2, tracks.track2Sectors)
                inTrackMenu = False
                setupMenu(track, defaultSetup)
        else:
            pygame.draw.rect(screen, yellow, track2Button)
            screen.blit(track2Preview, (288,105))
        if track3Button.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, track3Button)
            screen.blit(track3Preview, (545,105))
            if click == True: #Track 3 is selected and loaded
                trackName = "track3"
                trackLeaderboard = "track3leaderboard.txt"
                trackImage = pygame.image.load(os.path.join('images', 'track3.png')).convert_alpha()
                trackImage = pygame.transform.scale(trackImage, (3656, 2704))
                trackTerrain = pygame.image.load(os.path.join('images', 'track3terrain.png')).convert_alpha()
                trackTerrain = pygame.transform.scale(trackTerrain, (3656, 2704))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 600, 170, tracks.track3, tracks.track3Sectors)
                inTrackMenu = False
                setupMenu(track, defaultSetup)
        else:
            pygame.draw.rect(screen, yellow, track3Button)
            screen.blit(track3Preview, (545,105))

        pygame.display.update()
        clock.tick(60)

def setupMenu(track, currentSetup):
    inSetupMenu = True

    leaderButtonRect = pygame.Rect(600, 52, 100, 207)
    leaderButton = pygame.image.load(os.path.join('images', 'leaderButton.png')).convert_alpha()
    leaderButtonSelected = pygame.image.load(os.path.join('images', 'leaderButtonSelected.png')).convert_alpha()

    driveButtonRect = pygame.Rect(600, 259, 100, 207)
    driveButton = pygame.image.load(os.path.join('images', 'driveButton.png')).convert_alpha()
    driveButtonSelected = pygame.image.load(os.path.join('images', 'driveButtonSelected.png')).convert_alpha()

    fwImage = pygame.image.load(os.path.join('images', 'frontWingSetup.png')).convert_alpha()
    fwSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    fwSelector = fwSelectorImage.get_rect()

    rwImage = pygame.image.load(os.path.join('images', 'rearWingSetup.png')).convert_alpha()
    rwSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    rwSelector = rwSelectorImage.get_rect()

    gbImage = pygame.image.load(os.path.join('images', 'gearRatioSetup.png')).convert_alpha()
    gbSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    gbSelector = gbSelectorImage.get_rect()

    camberImage = pygame.image.load(os.path.join('images', 'camberSetup.png')).convert_alpha()
    camberSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    camberSelector = camberSelectorImage.get_rect()

    toeImage = pygame.image.load(os.path.join('images', 'toeSetup.png')).convert_alpha()
    toeSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    toeSelector = toeSelectorImage.get_rect()

    bbImage = pygame.image.load(os.path.join('images', 'brakeSetup.png')).convert_alpha()
    bbSelectorImage = pygame.image.load(os.path.join('images', 'selector.png')).convert_alpha()
    bbSelector = bbSelectorImage.get_rect()

    click = False
    fwPickUp = False
    rwPickUp = False
    gbPickUp = False
    camberPickUp = False
    toePickUp = False
    bbPickUp = False
    holding = False

    fwSetup = currentSetup[0]
    rwSetup = currentSetup[1]
    gbSetup = currentSetup[2]
    camberSetup = currentSetup[3]
    toeSetup = currentSetup[4]
    bbSetup = currentSetup[5]

    fwSelectorPositions = {1:28, 2:65, 3:102, 4:139, 5:177}
    fwSelector.center = (fwSelectorPositions[fwSetup], 188)

    rwSelectorPositions = {1:224, 2:263, 3:300, 4:337, 5:372}
    rwSelector.center = (rwSelectorPositions[rwSetup], 188)

    gbSelectorPositions = {1:419, 2:458, 3:495, 4:532, 5:567}
    gbSelector.center = (gbSelectorPositions[gbSetup], 188)

    camberSelectorPositions = {1:28, 2:65, 3:102, 4:139, 5:177}
    camberSelector.center = (camberSelectorPositions[camberSetup], 395)

    toeSelectorPositions = {1:224, 2:263, 3:300, 4:337, 5:372}
    toeSelector.center = (toeSelectorPositions[toeSetup], 395)

    bbSelectorPositions = {1:419, 2:458, 3:495, 4:532, 5:567}
    bbSelector.center = (bbSelectorPositions[bbSetup], 395)

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
                    fwPickUp = False #Drop any dragable objects
                    rwPickUp = False
                    gbPickUp = False
                    camberPickUp = False
                    toePickUp = False
                    bbPickUp = False
                    holding = False
        mx, my = pygame.mouse.get_pos()

        if fwPickUp == True or rwPickUp == True or gbPickUp == True or camberPickUp == True or toePickUp == True or bbPickUp == True:
            holding = True

        if fwSelector.collidepoint((mx, my)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND) #Show the cursor as a hand
            if click == True: #Pick up that selector
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

        if driveButtonRect.collidepoint((mx, my)) and holding == False:
            screen.blit(driveButtonSelected, (600, 259))
            screen.blit(leaderButton, (600, 52))
            if click == True:
                currentSetup = [fwSetup, rwSetup, gbSetup, camberSetup, toeSetup, bbSetup] #Create a setup from inputs
                currentFastest = [math.inf, ""] #Reset currentFastest
                drive(track, currentSetup, None, currentFastest, None) #Drive on track
                inSetupMenu = False
        elif leaderButtonRect.collidepoint((mx, my)) and holding == False:
            screen.blit(driveButton, (600, 259))
            screen.blit(leaderButtonSelected, (600, 52))
            if click == True:
                leaderboard = open(track.leaderboard, "r+") #Open the leaderboard
                currentSetup = [fwSetup, rwSetup, gbSetup, camberSetup, toeSetup, bbSetup]
                displayLeaderboard(track, leaderboard, None, currentSetup) #Go to the leaderboard
                inSetupMenu = False
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            screen.blit(driveButton, (600, 259))
            screen.blit(leaderButton, (600, 52))

        if fwPickUp == True:
            if mx < 28: #Positions that the selector can be dragged to to change that component
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

def getTrackSection(racecar, track): #Find the section of the track the car is on
    colourAtRL = (track.terrain.get_at((int(racecar.rl[0]+390), int(racecar.rl[1]+265))))[:3] #Find the colour on the terrain map that each corner of the car is on
    colourAtRR = (track.terrain.get_at((int(racecar.rr[0]+390), int(racecar.rr[1]+265))))[:3]
    colourAtFL = (track.terrain.get_at((int(racecar.fl[0]+390), int(racecar.fl[1]+265))))[:3]
    colourAtFR = (track.terrain.get_at((int(racecar.fr[0]+390), int(racecar.fr[1]+265))))[:3]
    frDone = False
    flDone = False
    rrDone = False
    rlDone = False
    sectionsIn = [] #Sections that the car is in
    wheelsOff = 0 #The amount of corners of the car that are off the track
    for section in track.sections:
        if flDone == False and colourAtFL == section[1]: #If that corner of the car has not been found in a section yet
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

    for section in sectionsIn: #Decide which section will be used to effect the car performance
        if section[2][1] == "Wall": #Wall has highest priority and will be applied immediately if touched
            return section
        if section[3] == False: #If one corner of the car is in a section out of track limits, it is recorded as a wheel off
            wheelsOff += 1
    if wheelsOff > 2: #If more than 2 wheels are off the track, the car is considered off the track and effects of the off-track sections are applied
        for section in sectionsIn: #Applies the effects of either gravel, grass or track
            if section[2][1] == "Gravel":
                return section
            elif section[2][1] == "Grass":
                return section
            else:
                return section #The section has track terrain
    else: #The car is in track limits
        for section in sectionsIn:
            if section[2][1] != "Track": #Sections that aren't track are ignored
                sectionsIn.remove(section)
        trackSectionsIn = []
        [trackSectionsIn.append(section) for section in sectionsIn if section not in trackSectionsIn]
        if len(trackSectionsIn) > 1:
            if trackSectionsIn[1][0] > trackSectionsIn[0][0]:
                return trackSectionsIn[1]
        return trackSectionsIn[0]

def getFastestLap(lapToAdd, fastestLap, fastestLapString): #Find the fastesst lap
    print(lapToAdd, fastestLap)
    if lapToAdd[2] == True:
        if lapToAdd[3] < fastestLap:
            fastestLap = lapToAdd[3]
            fastestLapString = lapToAdd[1]
    return fastestLap, fastestLapString

def getValidLap(section, validLap): #Check if the lap is valid
    if validLap == False: #Stays false if its false
        return False
    elif section[3] == False: #If the current section is out of track limits, the lap is invalidated
        validLap = False
    return validLap

def resetToStart(racecar, track): #Stop the car and return it to the start
    racecar.speed = 0
    racecar.heading = 0
    racecar.fr = pygame.math.Vector2(int(racecar.x+racecar.rect.width/2), int(racecar.y+racecar.rect.height/2))
    racecar.fl = pygame.math.Vector2(int(racecar.x+racecar.rect.width/2), int(racecar.y-racecar.rect.height/2))
    racecar.rr = pygame.math.Vector2(int(racecar.x-racecar.rect.width/2), int(racecar.y+racecar.rect.height/2))
    racecar.rl = pygame.math.Vector2(int(racecar.x-racecar.rect.width/2), int(racecar.y-racecar.rect.height/2))
    racecar.image = racecar.rotImg[0]
    racecar.position = track.spawnPoint

def getTheoBest(sectors):
    totalTheo = str(sum(sectors))
    print(totalTheo)
    while len(totalTheo) < 6:
        totalTheo = "0" + totalTheo
    theoBest = str(totalTheo[:-5]+":"+totalTheo[-5:-3]+"."+totalTheo[-3:])
    return theoBest

def drive(track, setup, holdLaps, currentFastest, holdSectors):

    #Creating the car
    racecar = Racecar(track.spawnPoint[0], track.spawnPoint[1], setup[0], setup[1], setup[2], setup[3], setup[4], setup[5])
    racecarGroup = pygame.sprite.Group()
    racecarGroup.add(racecar)

    lapTimer = LapTimer()
    sectorTimer = LapTimer()
    fastestLap = currentFastest[0] #Defaults to infinity. If continuing after a pause, previous fastest lap is stored
    fastestLapString = currentFastest[1] #Defaults to "". If continuing after a pause, string of the previous fastest lap is stored
    currentSector = 3
    validLap = False

    if holdLaps != None: #Add laps from paused session if there are any available
        laps = holdLaps
        currentLap = len(holdLaps)
    else:
        laps = []
        currentLap = 0
    if holdSectors != None: #Gets the fastest sectors if there are any
        fastestSectors = holdSectors
    else:
        fastestSectors = [math.inf, math.inf, math.inf]

    sectorTimes = [0, 0, 0]

    lapDisplay = pygame.Rect(140, 20, 100, 50)

    if fastestLapString == "":
        fLapDisplay = font.render("No Laps", True, white)
    else:
        fLapDisplay = font.render(fastestLapString, True, white)
    fLapDisplayBox = pygame.Rect(20, 20, 100, 50)

    speedometerBox = pygame.Rect(260, 20, 100, 50)

    driving = True

    while driving == True:

        lapTimer.updateTimer()
        sectorTimer.updateTimer()
        currentSection = getTrackSection(racecar, track) #Get the track section the car is in
        if currentSector == 3 and currentSection[0] == track.sectors[0]: #If crossing from sector 3 to 1 (Starting a new lap)
            currentSector = 1
            lapTime, lapTotal = lapTimer.resetTimer()
            sectorTimes[2] = sectorTimer.resetTimer()
            if validLap == True:
                for sectorNum in range(len(sectorTimes)):
                    if sectorTimes[sectorNum][1] < fastestSectors[sectorNum]:
                        fastestSectors[sectorNum] = sectorTimes[sectorNum][1]
            lapToAdd = [currentLap, lapTime, validLap, lapTotal]
            laps.append(lapToAdd)
            fastestLap, fastestLapString = getFastestLap(lapToAdd, fastestLap, fastestLapString) #Compare the new lap to the fastest lap of the session
            if fastestLapString == "":
                fLapDisplay = font.render("No Laps", True, white)
            else:
                fLapDisplay = font.render(fastestLapString, True, white)
            validLap = True
            currentLap += 1
        elif currentSector == 1 and currentSection[0] == track.sectors[1]: #If crossing from sector 1 to 2
            currentSector = 2
            sectorTimes[0] = sectorTimer.resetTimer()
        elif currentSector == 2 and currentSection[0] == track.sectors[2]: #If crossing from sector 2 to 3
            currentSector = 3
            sectorTimes[1] = sectorTimer.resetTimer()
        validLap = getValidLap(currentSection, validLap) #Check if the lap is still valid

        modifier = currentSection[2][0] #Get the terrain effect of the current section the car is in

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if keys[pygame.K_ESCAPE] == True: #If the player pauses the game
            driving = False
            currentFastest = [fastestLap, fastestLapString] #Update the current fastest lap of the session
            pause(track, fastestLapString, setup, laps, currentFastest, fastestSectors) #Go to the pause menu
        if keys[pygame.K_w] or keys[pygame.K_UP] == True: #Accelerator
            racecar.accelerate(modifier)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN] == True:
            if racecar.speed > 0:
                racecar.brake(modifier) #Brake if moving forward
            else:
                racecar.reverse(modifier) #Reverse if stopped or reversing already
        else:
            racecar.coast(modifier)
        if keys[pygame.K_a] or keys[pygame.K_LEFT] == True: #Turn left
            racecar.getTurnAngle(modifier)
            racecar.turn(-racecar.turnAngle)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT] == True: #Turn right
            racecar.getTurnAngle(modifier)
            racecar.turn(racecar.turnAngle)
        if keys[pygame.K_r] == True: #Reset key
            currentSector = 3
            validLap = False
            resetToStart(racecar, track) #Put the car back to the start of the track

        racecar.update()
        pygame.display.flip()
        screen.blit(track.image, (-racecar.rect.center[0], -racecar.rect.center[1])) #Move the background so it looks like the car is moving
        if validLap == True: #Change the colour of the timer based on if the lap is valid or not
            pygame.draw.rect(screen, black, lapDisplay)
        else:
            pygame.draw.rect(screen, red, lapDisplay)
        timer = font.render(lapTimer.currentLapTime, True, white)
        screen.blit(timer, (lapDisplay.center[0]-40, lapDisplay.center[1]-10))

        pygame.draw.rect(screen, purple, fLapDisplayBox)
        screen.blit(fLapDisplay, (fLapDisplayBox.center[0]-40, fLapDisplayBox.center[1]-10))

        speedometer = font.render(str(abs(int(racecar.speed*25)))+" mph", True, white)
        pygame.draw.rect(screen, green, speedometerBox)

        #turnAngleString = font.render(str(racecar.turnAngle), True, black)
        #screen.blit(turnAngleString, (400, 20))
        screen.blit(speedometer, (speedometerBox.center[0]-40, speedometerBox.center[1]-10))
        screen.blit(racecar.image, (screenWidth/2,screenHeight/2))

        clock.tick(60)

def pause(track, fastestLapString, setup, holdLaps, currentFastest, fastestSectors):
    paused = True

    theoreticalBest = getTheoBest(fastestSectors) #Get the sum of best sectors

    while paused:

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        screen.fill(blue)
        drawText("Pause", font, black, screen, 20, 20)
        if theoreticalBest == "0:00.inf": #If there is no theoretical best
            drawText(str("Theoretical Best Lap: No Laps Set"), font, black, screen, screenWidth-400, 20)
        else:
            drawText(str("Theoretical Best Lap: "+theoreticalBest), font, black, screen, screenWidth-400, 20)

        mx, my = pygame.mouse.get_pos()

        resumeButton = pygame.Rect(screenWidth/2-150, 100, 300, 50)
        leaderboardButton = pygame.Rect(screenWidth/2-150, 200, 300, 50)
        setupButton = pygame.Rect(screenWidth/2-150, 300, 300, 50)
        trackButton = pygame.Rect(screenWidth/2-150, 400, 300, 50)

        if setupButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, setupButton)
            pygame.draw.rect(screen, yellow, leaderboardButton)
            pygame.draw.rect(screen, yellow, resumeButton)
            pygame.draw.rect(screen, yellow, trackButton)
            if click == True:
                paused = False
                holdLaps = []
                setupMenu(track, setup) #Return to the setup menu
        elif leaderboardButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, leaderboardButton)
            pygame.draw.rect(screen, yellow, setupButton)
            pygame.draw.rect(screen, yellow, resumeButton)
            pygame.draw.rect(screen, yellow, trackButton)
            if click == True:
                paused = False
                holdLaps = []
                saveToLeaderboard(track, fastestLapString, setup) #Save the session
        elif resumeButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, resumeButton)
            pygame.draw.rect(screen, yellow, setupButton)
            pygame.draw.rect(screen, yellow, leaderboardButton)
            pygame.draw.rect(screen, yellow, trackButton)
            if click == True:
                paused = False
                drive(track, setup, holdLaps, currentFastest, fastestSectors) #Go back on track with the laps that were set before pausing
        elif trackButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, trackButton)
            pygame.draw.rect(screen, yellow, setupButton)
            pygame.draw.rect(screen, yellow, leaderboardButton)
            pygame.draw.rect(screen, yellow, resumeButton)
            if click == True:
                paused = False
                holdLaps = []
                trackMenu() #Return to the track menu
        else:
            pygame.draw.rect(screen, yellow, setupButton)
            pygame.draw.rect(screen, yellow, leaderboardButton)
            pygame.draw.rect(screen, yellow, resumeButton)
            pygame.draw.rect(screen, yellow, trackButton)

        leaderText = font.render("Save this session", True, (0, 0, 0))
        setupText = font.render("Change setup", True, (0, 0, 0))
        resumeText = font.render("Continue driving", True, (0, 0, 0))
        trackText = font.render("Change track", True, (0, 0, 0))
        screen.blit(leaderText, (leaderboardButton.center[0]-80, leaderboardButton.center[1]-10))
        screen.blit(setupText, (setupButton.center[0]-70, setupButton.center[1]-10))
        screen.blit(resumeText, (resumeButton.center[0]-80, resumeButton.center[1]-10))
        screen.blit(trackText, (trackButton.center[0]-70, trackButton.center[1]-10))

        pygame.display.flip()
        clock.tick(60)

def getTotalLap(lap): #Turn the lap string into a number
    lap = "".join(lap.split(":"))
    lap = "".join(lap.split("."))
    return int(lap)

def saveToLeaderboard(track, fastestLapString, setup):
    saving = True
    notSaving = False
    userName = ""
    leaderboard = open(track.leaderboard, "r+")

    if fastestLapString == "": #If no time was set
        notSaving = True

    while notSaving:
        screen.fill(blue)
        drawText("No valid laps were set in that session", font, black, screen, 200, 250)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()

        endText = font.render("End Session", True, (0, 0, 0))
        endButton = pygame.Rect(screenWidth/2-100, 300, 200, 50)

        if endButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, endButton)
            if click == True:
                notSaving = False
                displayLeaderboard(track, leaderboard, None, setup) #Go to the leaderboard with no new laps set
        else:
            pygame.draw.rect(screen, yellow, endButton)

        screen.blit(endText, (endButton.center[0]-60, endButton.center[1]-10))
        pygame.display.flip()
        clock.tick(60)

    while saving:
        screen.fill(blue)
        drawText("Save session to leaderboard", font, black, screen, 20, 20)
        drawText("Enter a user name", font, black, screen, screenWidth/2-100, 100)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(userName) > 0:
                    userName = userName [:-1]
                else:
                    userName += event.unicode

        userName = userName[:15]

        submitButton = pygame.Rect(screenWidth/2-100, 300, 200, 50)
        submitText = font.render("Submit", True, (0, 0, 0))

        userNameText = font.render(userName, True, (0, 0, 0))
        userNameBox = userNameText.get_rect()

        mx, my = pygame.mouse.get_pos()

        if submitButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, submitButton)
            if click == True:
                if len(userName) < 1:
                    userName = "Unnamed"
                leaderLaps = leaderboard.readlines() #Get all the laps
                leaderLaps = [lap.rstrip("\n") for lap in leaderLaps] #Remove \ns from each line
                leaderLaps = [lap[5:] for lap in leaderLaps] #Start each line from the start of the lap time
                leaderboard.seek(0)
                leaderboard.truncate() #Empty the leaderboard
                positionFound = False
                position = 0
                totalLap = getTotalLap(fastestLapString) #The integer value of the lap set in the session
                if len(leaderLaps) < 1: #If there are no previous times to compare to
                    positionFound = True
                else:
                    while positionFound == False and position < len(leaderLaps):
                        currentLap = leaderLaps[position].split(" | ") #The lap at that point in the leaderboard
                        currentLap = getTotalLap(currentLap[0]) #Find the integer value of the lap time
                        if totalLap < currentLap and positionFound == False: #If the lap that has just been set is faster than the current lap on the leaderboard
                            positionFound = True
                        else:
                            position += 1
                #Insert the new lap at its position in the leaderboard
                leaderLaps.insert(position, str(fastestLapString + " | " + userName+ " | " + str(setup[0]) + str(setup[1]) + str(setup[2]) + str(setup[3]) + str(setup[4]) + str(setup[5])))
                leaderBoardPos = 1
                while len(leaderLaps) > 0: #While there are laps to add to the leaderboard
                    if leaderBoardPos < 10: #For single digit numbers
                        print(leaderLaps[0])
                        leaderboard.write(str(leaderBoardPos) + "  | " + leaderLaps[0] + "\n") #Put the lap into the leaderboard
                    else:
                        leaderboard.write(str(leaderBoardPos) + " | " + leaderLaps[0] + "\n")
                    leaderLaps.remove(leaderLaps[0])
                    leaderBoardPos += 1
                leaderboard.close()
                #Create a sting for the fastest lap in the session to show when viewing the leaderboard
                if position < 9:
                    sessionFastest = str(str(position+1) + "  | " + fastestLapString + " | " + userName+ " | " + str(setup[0]) + str(setup[1]) + str(setup[2]) + str(setup[3]) + str(setup[4]) + str(setup[5]))
                else:
                    sessionFastest = str(str(position+1) + " | " + fastestLapString + " | " + userName+ " | " + str(setup[0]) + str(setup[1]) + str(setup[2]) + str(setup[3]) + str(setup[4]) + str(setup[5]))
                leaderboard = open(track.leaderboard, "r+")
                displayLeaderboard(track, leaderboard, sessionFastest, setup) #Show the leaderboard with the lap the user set
                saving = False
        else:
            pygame.draw.rect(screen, yellow, submitButton)

        screen.blit(submitText, (submitButton.center[0]-30, submitButton.center[1]-10))
        screen.blit(userNameText, ((screenWidth/2-userNameBox.width/2), (screenHeight/2-userNameBox.height/2)))
        pygame.display.flip()
        clock.tick(60)

def displayLeaderboard(track, leaderboard, sessionFastest, currentSetup):
    onLeaderboard = True
    if sessionFastest == None: #If there is a newly saved lap to be displayed
        sessionLapPresent = False
    else:
        sessionLapPresent = True

    leaderLaps = []
    leaderLaps = leaderboard.readlines()
    leaderLaps = [lap.rstrip("\n") for lap in leaderLaps]
    leaderButtons = []
    if sessionLapPresent == True:
        if int(sessionFastest[:2]) > 9: #If the new lap is worse than the 9th best, add the top 9 then that lap
            leaderLaps = leaderLaps[:9]
            leaderLaps.append(sessionFastest)
        else:
            leaderLaps = leaderLaps[:10]
    else:
        leaderLaps = leaderLaps[:10] #Otherwise add the top 10 laps

    if len(leaderLaps) > 0:
        for lap in leaderLaps:
            currentLap = lap.split(" | ")
            leaderPos = int(currentLap[0])
            if leaderPos < 10:
                leaderButton = pygame.Rect(screenWidth/2-300, leaderPos*40, 600, 30)
            else:
                leaderButton = pygame.Rect(screenWidth/2-300, 400, 600, 30)
            if sessionLapPresent and sessionFastest == lap: #If the new lap is present and is the same as the lap in the leaderboard
                leaderButtons.append([leaderButton, lap, True])
            else:
                leaderButtons.append([leaderButton, lap, False])

    setupButton = pygame.Rect(screenWidth/2-300, screenHeight-50, 300, 30)
    setupText = font.render("Setup Menu", True, (0, 0, 0))
    setupTextRect = setupText.get_rect()

    trackButton = pygame.Rect(screenWidth/2, screenHeight-50, 300, 30)
    trackText = font.render("Track Menu", True, (0, 0, 0))
    trackTextRect = trackText.get_rect()

    while onLeaderboard:
        screen.fill(blue)
        drawText("Leaderboard", font, black, screen, 20, 20)

        click = False

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        for button in leaderButtons:
            if button[2] == True: #Display the newly saved lap with a green background
                if button[0].collidepoint((mx, my)):
                    pygame.draw.rect(screen, greenDark, button[0])
                    if click == True:
                        copySetup = button[1][-6:]
                        copySetup = [int(setting) for setting in copySetup]
                        setupMenu(track, copySetup)
                else:
                    pygame.draw.rect(screen, green, button[0])
            else: #Display the rest with a yellow background
                if button[0].collidepoint((mx, my)):
                    pygame.draw.rect(screen, yellowDark, button[0])
                    if click == True:
                        copySetup = button[1][-6:]
                        copySetup = [int(setting) for setting in copySetup]
                        setupMenu(track, copySetup)
                else:
                    pygame.draw.rect(screen, yellow, button[0])
            buttonText = font.render(button[1], True, (0, 0, 0))
            buttonTextBox = buttonText.get_rect()
            screen.blit(buttonText, ((screenWidth/2-buttonTextBox.width/2), (button[0].y+5)))

        if setupButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellowDark, setupButton)
            pygame.draw.rect(screen, yellow, trackButton)
            if click == True:
                onLeaderboard = False
                setupMenu(track, currentSetup)  #Return to the setup menu
        elif trackButton.collidepoint((mx, my)):
            pygame.draw.rect(screen, yellow, setupButton)
            pygame.draw.rect(screen, yellowDark, trackButton)
            if click == True:
                onLeaderboard = False
                trackMenu() #Return to the track menu
        else:
            pygame.draw.rect(screen, yellow, setupButton)
            pygame.draw.rect(screen, yellow, trackButton)

        screen.blit(setupText, (setupButton.center[0]-setupTextRect.width/2, setupButton.center[1]-setupTextRect.height/2))
        screen.blit(trackText, (trackButton.center[0]-trackTextRect.width/2, trackButton.center[1]-trackTextRect.height/2))

        pygame.display.flip()
        clock.tick(60)

mainMenu()
