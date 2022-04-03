import pygame, sys, math, os, main, drive, trackMenu, setupMenu, saveSession

def runPauseMenu(setup, track, holdLaps, holdSectors, fastestLap, fastestLapString, fastestSectors):
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

        main.screen.fill(main.blue)
        main.drawText("Pause", main.font, main.black, main.screen, 20, 20)
        if theoreticalBest == "0:00.inf": #If there is no theoretical best
            main.drawText(str("Theoretical Best Lap: No Laps Set"), main.font, main.black, main.screen, main.screenWidth-400, 20)
        else:
            main.drawText(str("Theoretical Best Lap: "+theoreticalBest), main.font, main.black, main.screen, main.screenWidth-400, 20)

        mx, my = pygame.mouse.get_pos()

        resumeButton = pygame.Rect(main.screenWidth/2-150, 100, 300, 50)
        leaderboardButton = pygame.Rect(main.screenWidth/2-150, 200, 300, 50)
        setupButton = pygame.Rect(main.screenWidth/2-150, 300, 300, 50)
        trackButton = pygame.Rect(main.screenWidth/2-150, 400, 300, 50)

        if setupButton.collidepoint((mx, my)):
            pygame.draw.rect(main.screen, main.yellowDark, setupButton)
            pygame.draw.rect(main.screen, main.yellow, leaderboardButton)
            pygame.draw.rect(main.screen, main.yellow, resumeButton)
            pygame.draw.rect(main.screen, main.yellow, trackButton)
            if click == True:
                paused = False
                currentFastest = [math.inf, ""] #Reset currentFastest
                holdLaps = None
                holdSectors = None
                setupMenu.runSetupMenu(track, setup) #Return to the setup menu
        elif leaderboardButton.collidepoint((mx, my)):
            pygame.draw.rect(main.screen, main.yellowDark, leaderboardButton)
            pygame.draw.rect(main.screen, main.yellow, setupButton)
            pygame.draw.rect(main.screen, main.yellow, resumeButton)
            pygame.draw.rect(main.screen, main.yellow, trackButton)
            if click == True:
                paused = False
                holdLaps = None
                holdSectors = None
                saveSession.saveToLeaderboard(track, fastestLapString, setup) #Save the session
        elif resumeButton.collidepoint((mx, my)):
            pygame.draw.rect(main.screen, main.yellowDark, resumeButton)
            pygame.draw.rect(main.screen, main.yellow, setupButton)
            pygame.draw.rect(main.screen, main.yellow, leaderboardButton)
            pygame.draw.rect(main.screen, main.yellow, trackButton)
            if click == True:
                paused = False
                currentFastest = [fastestLap, fastestLapString]
                drive.playGame(setup, track, currentFastest, holdLaps, holdSectors) #Go back on track with the laps that were set before pausing
        elif trackButton.collidepoint((mx, my)):
            pygame.draw.rect(main.screen, main.yellowDark, trackButton)
            pygame.draw.rect(main.screen, main.yellow, setupButton)
            pygame.draw.rect(main.screen, main.yellow, leaderboardButton)
            pygame.draw.rect(main.screen, main.yellow, resumeButton)
            if click == True:
                paused = False
                holdLaps = None
                holdSectors = None
                trackMenu.runTrackMenu() #Return to the track menu
        else:
            pygame.draw.rect(main.screen, main.yellow, setupButton)
            pygame.draw.rect(main.screen, main.yellow, leaderboardButton)
            pygame.draw.rect(main.screen, main.yellow, resumeButton)
            pygame.draw.rect(main.screen, main.yellow, trackButton)

        leaderText = main.font.render("Save this session", True, (0, 0, 0))
        setupText = main.font.render("Change setup", True, (0, 0, 0))
        resumeText = main.font.render("Continue driving", True, (0, 0, 0))
        trackText = main.font.render("Change track", True, (0, 0, 0))
        main.screen.blit(leaderText, (leaderboardButton.center[0]-80, leaderboardButton.center[1]-10))
        main.screen.blit(setupText, (setupButton.center[0]-70, setupButton.center[1]-10))
        main.screen.blit(resumeText, (resumeButton.center[0]-80, resumeButton.center[1]-10))
        main.screen.blit(trackText, (trackButton.center[0]-70, trackButton.center[1]-10))

        pygame.display.flip()
        main.clock.tick(60)

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
