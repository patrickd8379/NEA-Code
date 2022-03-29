import pygame, sys, math, os, main, setupMenu, trackMenu

def runLeaderboard(track, sessionFastest):
    onLeaderboard = True
    if sessionFastest == None: #If there is a newly saved lap to be displayed
        sessionLapPresent = False
    else:
        sessionLapPresent = True

    leaderboard = open(track.leaderboard, "r+")
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
                leaderButton = pygame.Rect(main.screenWidth/2-300, leaderPos*40, 600, 30)
            else:
                leaderButton = pygame.Rect(main.screenWidth/2-300, 400, 600, 30)
            if sessionLapPresent and sessionFastest == lap: #If the new lap is present and is the same as the lap in the leaderboard
                leaderButtons.append([leaderButton, lap, True])
            else:
                leaderButtons.append([leaderButton, lap, False])

    setupButton = pygame.Rect(main.screenWidth/2-300, main.screenHeight-50, 300, 30)
    setupText = main.font.render("Setup Menu", True, (0, 0, 0))
    setupTextRect = setupText.get_rect()

    trackButton = pygame.Rect(main.screenWidth/2, main.screenHeight-50, 300, 30)
    trackText = main.font.render("Track Menu", True, (0, 0, 0))
    trackTextRect = trackText.get_rect()

    while onLeaderboard:
        main.screen.fill(main.blue)
        main.drawText("Leaderboard", main.font, main.black, main.screen, 20, 20)

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
                    pygame.draw.rect(main.screen, main.greenDark, button[0])
                    if click == True:
                        copySetup = button[1][-6:]
                        copySetup = [int(setting) for setting in copySetup]
                        currentSetup = copySetup
                        setupMenu.runSetupMenu(track, currentSetup)
                else:
                    pygame.draw.rect(main.screen, main.green, button[0])
            else: #Display the rest with a yellow background
                if button[0].collidepoint((mx, my)):
                    pygame.draw.rect(main.screen, main.yellowDark, button[0])
                    if click == True:
                        copySetup = button[1][-6:]
                        copySetup = [int(setting) for setting in copySetup]
                        currentSetup = copySetup
                        setupMenu.runSetupMenu(track, currentSetup)
                else:
                    pygame.draw.rect(main.screen, main.yellow, button[0])
            buttonText = main.font.render(button[1], True, (0, 0, 0))
            buttonTextBox = buttonText.get_rect()
            main.screen.blit(buttonText, ((main.screenWidth/2-buttonTextBox.width/2), (button[0].y+5)))

        if setupButton.collidepoint((mx, my)):
            pygame.draw.rect(main.screen, main.yellowDark, setupButton)
            pygame.draw.rect(main.screen, main.yellow, trackButton)
            if click == True:
                onLeaderboard = False
                setupMenu.runSetupMenu(track, currentSetup)  #Return to the setup menu
        elif trackButton.collidepoint((mx, my)):
            pygame.draw.rect(main.screen, main.yellow, setupButton)
            pygame.draw.rect(main.screen, main.yellowDark, trackButton)
            if click == True:
                onLeaderboard = False
                trackMenu.runTrackMenu() #Return to the track menu
        else:
            pygame.draw.rect(main.screen, main.yellow, setupButton)
            pygame.draw.rect(main.screen, main.yellow, trackButton)

        main.screen.blit(setupText, (setupButton.center[0]-setupTextRect.width/2, setupButton.center[1]-setupTextRect.height/2))
        main.screen.blit(trackText, (trackButton.center[0]-trackTextRect.width/2, trackButton.center[1]-trackTextRect.height/2))

        pygame.display.flip()
        main.clock.tick(60)
