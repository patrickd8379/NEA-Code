import pygame, sys, math, os, tracks
from main import *
from trackMenu import track
from drive import *

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
            currentFastest = [math.inf, ""] #Reset currentFastest
            holdLaps = None
            holdSectors = None
            currentSetup = setup
            exec(open(SETUPMENU).read()) #Return to the setup menu
    elif leaderboardButton.collidepoint((mx, my)):
        pygame.draw.rect(screen, yellowDark, leaderboardButton)
        pygame.draw.rect(screen, yellow, setupButton)
        pygame.draw.rect(screen, yellow, resumeButton)
        pygame.draw.rect(screen, yellow, trackButton)
        if click == True:
            paused = False
            holdLaps = None
            holdSectors = None
            saveToLeaderboard(track, fastestLapString, setup) #Save the session
    elif resumeButton.collidepoint((mx, my)):
        pygame.draw.rect(screen, yellowDark, resumeButton)
        pygame.draw.rect(screen, yellow, setupButton)
        pygame.draw.rect(screen, yellow, leaderboardButton)
        pygame.draw.rect(screen, yellow, trackButton)
        if click == True:
            paused = False
            exec(open(DRIVE).read()) #Go back on track with the laps that were set before pausing
    elif trackButton.collidepoint((mx, my)):
        pygame.draw.rect(screen, yellowDark, trackButton)
        pygame.draw.rect(screen, yellow, setupButton)
        pygame.draw.rect(screen, yellow, leaderboardButton)
        pygame.draw.rect(screen, yellow, resumeButton)
        if click == True:
            paused = False
            holdLaps = None
            holdSectors = None
            exec(open(TRACKMENU).read()) #Return to the track menu
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
