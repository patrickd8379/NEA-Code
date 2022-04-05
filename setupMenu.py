import pygame, sys, math, os, main, drive, trackMenu, leaderboardScreen

def runSetupMenu(track, currentSetup):
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

    main.screen.fill(main.blue)
    main.drawText("Track Menu", main.font, main.black, main.screen, 20, 20)

    while inSetupMenu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inSetupMenu = False
                    trackMenu.runTrackMenu()
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

        if fwPickUp == True or rwPickUp == True or gbPickUp == True or camberPickUp == True or toePickUp == True or bbPickUp == True:
            holding = True

        if driveButtonRect.collidepoint((mx, my)) and holding == False:
            main.screen.blit(driveButtonSelected, (600, 259))
            main.screen.blit(leaderButton, (600, 52))
            if click == True:
                currentSetup = [fwSetup, rwSetup, gbSetup, camberSetup, toeSetup, bbSetup] #Create a setup from inputs
                currentFastest = [math.inf, ""] #Reset currentFastest
                holdLaps = None
                holdSectors = None
                drive.playGame(currentSetup, track, currentFastest, holdLaps, holdSectors) #Drive on track
                inSetupMenu = False
        elif leaderButtonRect.collidepoint((mx, my)) and holding == False:
            main.screen.blit(driveButton, (600, 259))
            main.screen.blit(leaderButtonSelected, (600, 52))
            if click == True:
                leaderboard = open(track.leaderboard, "r+") #Open the leaderboard
                currentSetup = [fwSetup, rwSetup, gbSetup, camberSetup, toeSetup, bbSetup]
                sessionFastest = None
                leaderboardScreen.runLeaderboard(track, None, currentSetup) #Go to the leaderboard
                inSetupMenu = False
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            main.screen.blit(driveButton, (600, 259))
            main.screen.blit(leaderButton, (600, 52))

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

        main.screen.blit(fwImage, (20,50))
        main.screen.blit(fwSelectorImage, fwSelector.center)

        main.screen.blit(rwImage, (215,50))
        main.screen.blit(rwSelectorImage, rwSelector.center)

        main.screen.blit(gbImage, (410,50))
        main.screen.blit(gbSelectorImage, gbSelector.center)

        main.screen.blit(camberImage, (20,257))
        main.screen.blit(camberSelectorImage, camberSelector.center)

        main.screen.blit(toeImage, (215,257))
        main.screen.blit(toeSelectorImage, toeSelector.center)

        main.screen.blit(bbImage, (410,257))
        main.screen.blit(bbSelectorImage, bbSelector.center)

        pygame.display.update()
        main.clock.tick(60)
