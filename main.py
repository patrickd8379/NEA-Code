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

TRACKMENU = "trackMenu.py"
SETUPMENU = "setupMenu.py"
PAUSEMENU = "pauseMenu.py"
DRIVE = "drive.py"
LEADERBOARDSCREEN = "leaderboardScreen.py"

DEFAULTSETUP = [3, 3, 3, 3, 3, 3]

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
                exec(open(TRACKMENU).read()) #Go to the track menu
        else:
            pygame.draw.rect(screen, yellow, startButton)

        drawText("Start", font, black, screen, (screenWidth/2)-25, 365)

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
                exec(open(LEADERBOARDSCREEN).read()) #Show the leaderboard with the lap the user set
                saving = False
        else:
            pygame.draw.rect(screen, yellow, submitButton)

        screen.blit(submitText, (submitButton.center[0]-30, submitButton.center[1]-10))
        screen.blit(userNameText, ((screenWidth/2-userNameBox.width/2), (screenHeight/2-userNameBox.height/2)))
        pygame.display.flip()
        clock.tick(60)

mainMenu()
