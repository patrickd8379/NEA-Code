import pygame, sys, math, os, tracks
from main import *
from setupMenu import *

#Creating the car
setup = currentSetup
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
                print(fastestSectors)
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
        exec(open(PAUSEMENU).read()) #Go to the pause menu
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

    turnAngleString = font.render(str(round(racecar.turnAngle, 2)), True, black)
    screen.blit(turnAngleString, (400, 20))

    accelerationString = font.render(str(round(racecar.acceleration,2)), True, black)
    screen.blit(accelerationString, (500, 20))

    decelerationString = font.render(str(round(racecar.deceleration,2)), True, black)
    screen.blit(decelerationString, (600, 20))
    screen.blit(speedometer, (speedometerBox.center[0]-40, speedometerBox.center[1]-10))
    screen.blit(racecar.image, (screenWidth/2,screenHeight/2))

    clock.tick(60)
