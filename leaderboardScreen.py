import pygame, sys, math, os, tracks
from main import *
from trackMenu import track

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
                    currentSetup = copySetup
                    exec(open(SETUPMENU).read())
            else:
                pygame.draw.rect(screen, green, button[0])
        else: #Display the rest with a yellow background
            if button[0].collidepoint((mx, my)):
                pygame.draw.rect(screen, yellowDark, button[0])
                if click == True:
                    copySetup = button[1][-6:]
                    copySetup = [int(setting) for setting in copySetup]
                    currentSetup = copySetup
                    exec(open(SETUPMENU).read())
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
            exec(open(SETUPMENU).read())  #Return to the setup menu
    elif trackButton.collidepoint((mx, my)):
        pygame.draw.rect(screen, yellow, setupButton)
        pygame.draw.rect(screen, yellowDark, trackButton)
        if click == True:
            onLeaderboard = False
            exec(open(TRACKMENU).read()) #Return to the track menu
    else:
        pygame.draw.rect(screen, yellow, setupButton)
        pygame.draw.rect(screen, yellow, trackButton)

    screen.blit(setupText, (setupButton.center[0]-setupTextRect.width/2, setupButton.center[1]-setupTextRect.height/2))
    screen.blit(trackText, (trackButton.center[0]-trackTextRect.width/2, trackButton.center[1]-trackTextRect.height/2))

    pygame.display.flip()
    clock.tick(60)
