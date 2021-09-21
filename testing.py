import pygame, sys, math, tracks
from PIL import Image

class Setup():
    def __init__(self, frontWing, rearWing, camber, toe, gear, brake):
        self.frontWing = frontWing #1-5
        self.rearWing = rearWing #1-5
        self.camber = camber #1-5
        self.toe = toe #1-5
        self.gear = gear #1-5
        self.brakeBias = brake #1-5

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
pygame.init()
clock = pygame.time.Clock()

topSpeedSetup = Setup(1,1,1,1,5,1)
maxGripSetup = Setup(5,5,5,5,1,5)
midSetup = Setup(3,3,3,3,3,3)
currentSetup = midSetup

screenWidth = 750
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
background1 = pygame.image.load(r'C:\Users\Patrick Debattista\Documents\School\CS NEA\NEA Code\images\track1.png')
background1 = pygame.transform.scale(background1, (3656,2704))
terrainMap1 = pygame.image.load(r'C:\Users\Patrick Debattista\Documents\School\CS NEA\NEA Code\images\track1terrain.png')
terrainMap1 = pygame.transform.scale(terrainMap1, (3656,2704))
track1SpawnPoint = (700,500)

background2 = pygame.image.load(r'C:\Users\Patrick Debattista\Documents\School\CS NEA\NEA Code\images\track2.png')
background2 = pygame.transform.scale(background2, (3656,2704))
terrainMap2 = pygame.image.load(r'C:\Users\Patrick Debattista\Documents\School\CS NEA\NEA Code\images\track2terrain.png')
terrainMap2 = pygame.transform.scale(terrainMap2, (3656,2704))
track2SpawnPoint = (1000,1000)

background3 = pygame.image.load(r'C:\Users\Patrick Debattista\Documents\School\CS NEA\NEA Code\images\track3.png')
background3 = pygame.transform.scale(background3, (3656,2704))
terrainMap3 = pygame.image.load(r'C:\Users\Patrick Debattista\Documents\School\CS NEA\NEA Code\images\track3terrain.png')
terrainMap3 = pygame.transform.scale(terrainMap3, (3656,2704))
track3SpawnPoint = (600,170)

currentTrack = background1
terrainMap = terrainMap1

tMapRect = terrainMap.get_rect()
#innerWall = pygame.Surface((4570, 3380))
racecarImage = pygame.image.load(r'C:\Users\Patrick Debattista\Documents\School\CS NEA\NEA Code\images\racecar.png')

#iWallShape = pygame.draw.polygon(innerWall, (122,122,122), ((577,2113),(538, 2150),(2311,1867),(2156,1600),(2415,1304),(2910,1356),(3325,781),(3255,806),(2904,1314),(2398,1268),(2118,890),(2529,290),(2506,209),(2200,507),(2122,537),(1193,1476),(1214,1615),(1221,1963),(1190,2006)))

if currentTrack == background1:
    racecar = Racecar(700,500, currentSetup.frontWing, currentSetup.rearWing, currentSetup.camber, currentSetup.toe, currentSetup.gear, currentSetup.brakeBias)
elif currentTrack == background2:
    racecar = Racecar(1000,1000, currentSetup.frontWing, currentSetup.rearWing, currentSetup.camber, currentSetup.toe, currentSetup.gear, currentSetup.brakeBias)
else:
    racecar = Racecar(600,170, currentSetup.frontWing, currentSetup.rearWing, currentSetup.camber, currentSetup.toe, currentSetup.gear, currentSetup.brakeBias)
font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 20)
speedometer = font.render(str(racecar.speed), True, (0,0,0))
speedoRect = speedometer.get_rect()
speedoRect.center = [screenWidth-100, screenHeight-50]

compass = font.render(str(racecar.position), True, (0,0,0))
compassRect = compass.get_rect()
compassRect.center = [screenWidth-100, screenHeight-100]

racecarGroup = pygame.sprite.Group()
racecarGroup.add(racecar)

LapTimer = LapTimer()
fastestLap = math.inf
fastestLapString = ""
currentLap = 0
currentSector = 3
validLap = False
laps = []

def getTrackSection(racecar):
    #print(int(racecar.fr[0]+390), int(racecar.fr[1]+260))
    #print((racecar.rect.center[0]+390), (racecar.rect.center[1]+260))
    #print(int(racecar.rr[0]-racecar.rect.center[0]), int(racecar.rr[1]-racecar.rect.center[1]))
    colourAtRL = (terrainMap.get_at(((racecar.rect.center[0]+375), (racecar.rect.center[1]+251))))[:3]
    colourAtRR = (terrainMap.get_at(((racecar.rect.center[0]+375), (racecar.rect.center[1]+269))))[:3]
    colourAtFL = (terrainMap.get_at(((racecar.rect.center[0]+405), (racecar.rect.center[1]+251))))[:3]
    colourAtFR = (terrainMap.get_at(((racecar.rect.center[0]+405), (racecar.rect.center[1]+269))))[:3]
    colourAtPosition = (terrainMap.get_at(((racecar.rect.center[0]+390), (racecar.rect.center[1]+260))))[:3]
    frDone = False
    flDone = False
    rrDone = False
    rlDone = False
    sectionsIn = []
    wheelsOff = 0
    if currentTrack == background1:
        for section in tracks.track1:
            if frDone == False:
                if colourAtFR == section[1]:
                    frDone = True
                    sectionsIn.append(section)
            if flDone == False:
                if colourAtFL == section[1]:
                    flDone = True
                    sectionsIn.append(section)
            if rrDone == False:
                if colourAtRR == section[1]:
                    rrDone = True
                    sectionsIn.append(section)
            if rlDone == False:
                if colourAtRL == section[1]:
                    rlDone = True
                    sectionsIn.append(section)
        for section in sectionsIn:
            if section[2][1] == "Wall":
                return section, wheelsOff
            if section[3] == False:
                wheelsOff += 1
        if wheelsOff > 2:
            for section in sectionsIn:
                if section[2][1] == "Gravel":
                    return section, wheelsOff
                elif section[2][1] == "Track":
                    return section, wheelsOff
                else:
                    return section, wheelsOff
        else:
            for section in sectionsIn:
                if section[2][1] != "Track":
                    sectionsIn.remove(section)
            if sectionsIn[0][0] > sectionsIn[1][0]:
                return sectionsIn[0], wheelsOff
            else:
                return sectionsIn[1], wheelsOff

    elif currentTrack == background2:
        for section in tracks.track2:
            if frDone == False:
                if colourAtFR == section[1]:
                    frDone = True
                    sectionsIn.append(section)
            if flDone == False:
                if colourAtFL == section[1]:
                    flDone = True
                    sectionsIn.append(section)
            if rrDone == False:
                if colourAtRR == section[1]:
                    rrDone = True
                    sectionsIn.append(section)
            if rlDone == False:
                if colourAtRL == section[1]:
                    rlDone = True
                    sectionsIn.append(section)
        for section in sectionsIn:
            if section[2][1] == "Wall":
                return section, wheelsOff
            if section[3] == False:
                wheelsOff += 1
        if wheelsOff > 2:
            for section in sectionsIn:
                if section[2][1] == "Gravel":
                    return section, wheelsOff
                elif section[2][1] == "Track":
                    return section, wheelsOff
                else:
                    return section, wheelsOff
        else:
            for section in sectionsIn:
                if section[2][1] != "Track":
                    sectionsIn.remove(section)
            if sectionsIn[0][0] > sectionsIn[1][0]:
                return sectionsIn[0], wheelsOff
            else:
                return sectionsIn[1], wheelsOff

    elif currentTrack == background3:
        for section in tracks.track3:
            if frDone == False:
                if colourAtFR == section[1]:
                    frDone = True
                    sectionsIn.append(section)
            if flDone == False:
                if colourAtFL == section[1]:
                    flDone = True
                    sectionsIn.append(section)
            if rrDone == False:
                if colourAtRR == section[1]:
                    rrDone = True
                    sectionsIn.append(section)
            if rlDone == False:
                if colourAtRL == section[1]:
                    rlDone = True
                    sectionsIn.append(section)
        for section in sectionsIn:
            if section[2][1] == "Wall":
                return section, wheelsOff
            if section[3] == False:
                wheelsOff += 1
        #print(wheelsOff)
        if wheelsOff > 2:
            for section in sectionsIn:
                if section[2][1] == "Gravel":
                    return section, wheelsOff
                elif section[2][1] == "Track":
                    return section, wheelsOff
                else:
                    return section, wheelsOff
        else:
            for section in sectionsIn:
                if section[2][1] != "Track":
                    sectionsIn.remove(section)
            if sectionsIn[0][0] > sectionsIn[1][0]:
                return sectionsIn[0], wheelsOff
            else:
                return sectionsIn[1], wheelsOff

def resetToStart(racecar):
    validLap = False
    racecar.speed = 0
    racecar.heading = 0
    racecar.image = racecar.rotImg[0]
    if currentTrack == background1:
        racecar.position = track1SpawnPoint
    elif currentTrack == background2:
        racecar.position = track2SpawnPoint
    else:
        racecar.position = track3SpawnPoint

def getFastestLap(lapToAdd, fastestLap, fastestLapString):
    print(lapToAdd, fastestLap)
    if lapToAdd[2] == True:
        if lapToAdd[3] < fastestLap:
            fastestLap = lapToAdd[3]
            fastestLapString = lapToAdd[1]
    return fastestLap, fastestLapString

while True:
    #print(racecar.image.get_width(), racecar.image.get_height())
    LapTimer.updateTimer()
    currentSection, wheelsOff = getTrackSection(racecar)
    #print(currentSection[0], currentSector)
    if wheelsOff > 2:
        validLap = False
    #print(currentSection)
    #print(validLap)
    modifier = currentSection[2][0]
    #print(currentSection[2][1])
    if currentTrack == background1:
        if currentSector == 3:
            if currentSection[0] == 5:
                lapTime, lapTotal = LapTimer.resetTimer()
                lapToAdd = [currentLap, lapTime, validLap, lapTotal]
                laps.append(lapToAdd)
                fastestLap, fastestLapString = getFastestLap(lapToAdd, fastestLap, fastestLapString)
                print(fastestLapString)
                validLap = True
                currentSector = 1
                currentLap += 1
        elif currentSector == 1:
            if currentSection[0] == 6:
                currentSector = 2
        elif currentSector == 2:
            if currentSection[0] == 7:
                currentSector = 3
    elif currentTrack == background2:
        if currentSector == 3:
            if currentSection[0] == 4:
                lapTime, lapTotal = LapTimer.resetTimer()
                lapToAdd = [currentLap, lapTime, validLap, lapTotal]
                laps.append(lapToAdd)
                fastestLap, fastestLapString = getFastestLap(lapToAdd, fastestLap, fastestLapString)
                print(fastestLapString)
                validLap = True
                currentSector = 1
                currentLap += 1
        elif currentSector == 1:
            if currentSection[0] == 5:
                currentSector = 2
        elif currentSector == 2:
            if currentSection[0] == 6:
                currentSector = 3
    elif currentTrack == background3:
        if currentSector == 3:
            if currentSection[0] == 5:
                lapTime, lapTotal = LapTimer.resetTimer()
                lapToAdd = [currentLap, lapTime, validLap, lapTotal]
                laps.append(lapToAdd)
                fastestLap, fastestLapString = getFastestLap(lapToAdd, fastestLap, fastestLapString)
                print(fastestLapString)
                validLap = True
                currentSector = 1
                currentLap += 1
        elif currentSector == 1:
            if currentSection[0] == 6:
                currentSector = 2
        elif currentSector == 2:
            if currentSection[0] == 7:
                currentSector = 3
    #print(currentSector)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
        resetToStart(racecar)
    racecar.update()
    pygame.display.flip()
    screen.fill((255,255,255))
    #screen.blit(terrainMap, (-racecar.rect.center[0], -racecar.rect.center[1]))
    screen.blit(currentTrack, (-racecar.rect.center[0], -racecar.rect.center[1]))
    screen.blit(racecar.image, (screenWidth/2,screenHeight/2))
    timer = font.render(LapTimer.currentLapTime, True, (0,0,0))
    screen.blit(timer, ((screenWidth/2)-50, 100))
    #pygame.draw.rect(currentTrack, (255,0,0), racecar.rect)
    #speedometer = font.render(str(round(racecar.speed*25)), True, (0,0,0))
    #compass = font.render(str((-racecar.rect.center[0], -racecar.rect.center[1])), True, (122,122,122))
    #screen.blit(speedometer, speedoRect)
    #screen.blit(compass, compassRect)
    clock.tick(60)
