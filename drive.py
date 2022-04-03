import pygame, sys, math, os, main, pauseMenu

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
            rotatedImage = pygame.transform.rotozoom(main.racecarImage, 360-90-(i*self.minAngle), 1) #Creates a rotated image
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

def playGame(setup, track, currentFastest, holdLaps, holdSectors):
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
        fLapDisplay = main.font.render("No Laps", True, main.white)
    else:
        fLapDisplay = main.font.render(fastestLapString, True, main.white)
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
                fLapDisplay = main.font.render("No Laps", True, main.white)
            else:
                fLapDisplay = main.font.render(fastestLapString, True, main.white)
            validLap = True
            currentLap += 1
        elif currentSector == 1 and currentSection[0] == track.sectors[1]: #If crossing from sector 1 to 2
            currentSector = 2
            sectorTimes[0] = sectorTimer.resetTimer()
        elif currentSector == 2 and currentSection[0] == track.sectors[2]: #If crossing from sector 2 to 3
            currentSector = 3
            sectorTimes[1] = sectorTimer.resetTimer()
        elif currentSector == 1 and currentSection[0] == track.sectors[2]: #If crossing from sector 1 to 3 (You are going backwards)
            validLap = False
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
            holdLaps = laps
            holdSectors = fastestSectors
            pauseMenu.runPauseMenu(setup, track, holdLaps, holdSectors, fastestLap, fastestLapString, fastestSectors) #Go to the pause menu
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
        main.screen.fill(main.black)
        main.screen.blit(track.image, (-racecar.rect.center[0], -racecar.rect.center[1])) #Move the background so it looks like the car is moving
        if validLap == True: #Change the colour of the timer based on if the lap is valid or not
            pygame.draw.rect(main.screen, main.black, lapDisplay)
        else:
            pygame.draw.rect(main.screen, main.red, lapDisplay)
        timer = main.font.render(lapTimer.currentLapTime, True, main.white)
        main.screen.blit(timer, (lapDisplay.center[0]-40, lapDisplay.center[1]-10))

        pygame.draw.rect(main.screen, main.purple, fLapDisplayBox)
        main.screen.blit(fLapDisplay, (fLapDisplayBox.center[0]-40, fLapDisplayBox.center[1]-10))

        speedometer = main.font.render(str(abs(int(racecar.speed*25)))+" mph", True, main.white)
        pygame.draw.rect(main.screen, main.green, speedometerBox)

        turnAngleString = main.font.render(str(round(racecar.turnAngle, 2)), True, main.black)
        main.screen.blit(turnAngleString, (400, 20))

        accelerationString = main.font.render(str(round(racecar.acceleration,2)), True, main.black)
        main.screen.blit(accelerationString, (500, 20))

        decelerationString = main.font.render(str(round(racecar.deceleration,2)), True, main.black)
        main.screen.blit(decelerationString, (600, 20))
        main.screen.blit(speedometer, (speedometerBox.center[0]-40, speedometerBox.center[1]-10))
        main.screen.blit(racecar.image, (main.screenWidth/2,main.screenHeight/2))

        main.clock.tick(60)

def getTrackSection(racecar, track): #Find the section of the track the car is on
    colourAtRL = (track.terrain.get_at((int(racecar.rl[0]+390), int(racecar.rl[1]+265))))[:3] #Find the colour on the terrain map that each corner of the car is on
    colourAtRR = (track.terrain.get_at((int(racecar.rr[0]+390), int(racecar.rr[1]+265))))[:3]
    colourAtFL = (track.terrain.get_at((int(racecar.fl[0]+390), int(racecar.fl[1]+265))))[:3]
    colourAtFR = (track.terrain.get_at((int(racecar.fr[0]+390), int(racecar.fr[1]+265))))[:3]
    sectionsIn = [] #Sections that the car is in
    wheelsOff = 0 #The amount of corners of the car that are off the track
    for section in track.sections:
        if colourAtFL == section[1]: #If that corner of the car has not been found in a section yet
            sectionsIn.append(section)
        if colourAtFR == section[1]:
            sectionsIn.append(section)
        if colourAtRL == section[1]:
            sectionsIn.append(section)
        if colourAtRR == section[1]:
            sectionsIn.append(section)
    for section in sectionsIn: #Decide which section will be used to effect the car performance
        if section[2][1] == "Wall": #Wall has highest priority and will be applied immediately if touched
            return section
        if section[3] == False: #If one corner of the car is in a section out of track limits, it is recorded as a wheel off
            wheelsOff += 1
    if wheelsOff > 2: #If more than 2 wheels are off the track, the car is considered off the track and effects of the off-track sections are applied
        offTrackSections = []
        [offTrackSections.append(section) for section in sectionsIn if section[3] == False]
        if len(offTrackSections) > 1:
            if offTrackSections[0] < offTrackSections[1]:
                if len(offTrackSections) == 3 and offTrackSections[0] > offTrackSections[2]:
                    return offTrackSections[2]
                return offTrackSections[0]
            else:
                if len(offTrackSections) == 3 and offTrackSections[1] > offTrackSections[2]:
                    return offTrackSections[2]
                return offTrackSections[1]
        else:
            return offTrackSections[0]
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
